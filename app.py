import os
import uuid
from datetime import date, datetime, timedelta
from typing import List, Optional
from contextlib import asynccontextmanager

import aiosqlite
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from database import DB_FILE, init_db

def get_app_name() -> str:
    """Reads configured app display name from .config.env if present."""
    config_file = os.path.join(os.path.dirname(__file__), ".config.env")
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("APP_DISPLAY_NAME="):
                        return line.strip().split("=", 1)[1].strip('"\'')
        except Exception:
            pass
    return "My Command Centre"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title=get_app_name(), lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

# Schemas
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    category: str = "General"
    priority: str = "amber"
    due_date: Optional[str] = None
    details: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
    details: Optional[str] = None
    sort_order: Optional[int] = None

class TaskReorder(BaseModel):
    task_ids: List[str]

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1)
    color: str = Field(..., min_length=4)

class AppNameUpdate(BaseModel):
    name: str = Field(..., min_length=1)

class NoteUpdate(BaseModel):
    content: str

def calculate_directive_index(target_priority: str, target_due_date: Optional[str], active_tasks: list) -> int:
    """
    Determines slot index based on:
    1. Priority Tier (Red -> Amber -> Green)
    2. Dated tasks come before undated tasks within the same priority tier
    3. Dated tasks are ordered chronologically (earliest date first)
    4. Undated tasks slot immediately after dated tasks of that tier, above older undated tasks
    """
    target_p = target_priority.lower()
    priority_order = {"red": 1, "amber": 2, "green": 3}
    target_rank = priority_order.get(target_p, 2)

    tier_indices = [
        idx for idx, task in enumerate(active_tasks)
        if priority_order.get(task["priority"].lower(), 2) == target_rank
    ]

    if not tier_indices:
        for idx, task in enumerate(active_tasks):
            if priority_order.get(task["priority"].lower(), 2) > target_rank:
                return idx
        return len(active_tasks)

    tier_start = tier_indices[0]
    tier_end = tier_indices[-1] + 1

    if target_due_date:
        for idx in range(tier_start, tier_end):
            curr_due = active_tasks[idx].get("due_date")
            if not curr_due:
                return idx
            if curr_due > target_due_date:
                return idx
        return tier_end

    for idx in range(tier_start, tier_end):
        if not active_tasks[idx].get("due_date"):
            return idx

    return tier_end


@app.post("/api/tasks")
async def add_task(payload: TaskCreate):
    task_id = str(uuid.uuid4())[:8]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    p = (payload.priority or "amber").lower()
    due = payload.due_date if payload.due_date else None
    
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        
        cursor = await db.execute(
            "SELECT id, priority, due_date FROM tasks WHERE status != 'completed' ORDER BY sort_order ASC, rowid ASC"
        )
        active_tasks = [dict(r) for r in await cursor.fetchall()]
        
        target_index = calculate_directive_index(p, due, active_tasks)

        new_active_ids = [t["id"] for t in active_tasks]
        new_active_ids.insert(target_index, task_id)

        await db.execute("""
            INSERT INTO tasks (id, title, category, priority, status, due_date, details, sort_order, created_at)
            VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, ?)
        """, (task_id, payload.title, payload.category, payload.priority, due, payload.details, target_index, now))

        for order_idx, t_id in enumerate(new_active_ids):
            await db.execute("UPDATE tasks SET sort_order = ? WHERE id = ?", (order_idx, t_id))

        await db.commit()
        return {"id": task_id, "status": "created", "sort_order": target_index}


@app.patch("/api/tasks/{task_id}")
async def patch_task(task_id: str, payload: TaskUpdate):
    fields, values = [], []
    updates = payload.model_dump(exclude_unset=True)

    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        
        cursor = await db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        current_task = await cursor.fetchone()
        if not current_task:
            raise HTTPException(status_code=404, detail="Task not found")

        current_task = dict(current_task)
        current_priority = current_task["priority"]
        current_due = current_task.get("due_date")
        current_status = current_task["status"]

        new_priority = updates.get("priority", current_priority)
        new_due = updates.get("due_date", current_due)

        priority_changed = "priority" in updates and updates["priority"].lower() != current_priority.lower()
        date_changed = "due_date" in updates and updates["due_date"] != current_due

        if (priority_changed or date_changed) and current_status != "completed":
            cur_active = await db.execute(
                "SELECT id, priority, due_date FROM tasks WHERE status != 'completed' AND id != ? ORDER BY sort_order ASC, rowid ASC",
                (task_id,)
            )
            other_active = [dict(r) for r in await cur_active.fetchall()]
            
            target_index = calculate_directive_index(new_priority, new_due, other_active)
            
            new_active_ids = [t["id"] for t in other_active]
            new_active_ids.insert(target_index, task_id)
            
            for order_idx, t_id in enumerate(new_active_ids):
                await db.execute("UPDATE tasks SET sort_order = ? WHERE id = ?", (order_idx, t_id))

        for key, val in updates.items():
            if key == "status":
                fields.append("status = ?")
                values.append(val)
                if val == "completed":
                    fields.append("completed_at = ?")
                    values.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
                else:
                    fields.append("completed_at = NULL")
            elif key != "sort_order":
                fields.append(f"{key} = ?")
                values.append(val)

        if fields:
            values.append(task_id)
            await db.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", values)

        await db.commit()
        return {"status": "success"}

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    app_title = get_app_name()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": app_title}
    )

# Categories Endpoints
@app.get("/api/categories")
async def get_categories():
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM categories ORDER BY name ASC") as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

@app.post("/api/categories")
async def create_category(payload: CategoryCreate):
    cat_id = str(uuid.uuid4())[:8]
    clean_name = payload.name.strip()
    async with aiosqlite.connect(DB_FILE) as db:
        try:
            await db.execute("INSERT INTO categories (id, name, color) VALUES (?, ?, ?)", (cat_id, clean_name, payload.color))
            await db.commit()
            return {"id": cat_id, "name": clean_name, "color": payload.color}
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="Category name already exists")

@app.delete("/api/categories/{cat_id}")
async def delete_category(cat_id: str):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"status": "success"}

# Tasks Endpoints
@app.get("/api/tasks")
async def get_tasks():
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        query = "SELECT * FROM tasks ORDER BY sort_order ASC, rowid ASC"
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

@app.post("/api/tasks/reorder")
async def reorder_tasks(payload: TaskReorder):
    async with aiosqlite.connect(DB_FILE) as db:
        for index, t_id in enumerate(payload.task_ids):
            await db.execute("UPDATE tasks SET sort_order = ? WHERE id = ?", (index, t_id))
        await db.commit()
    return {"status": "reordered"}

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "deleted"}

# End of Day Workflow Endpoints
@app.get("/api/eod-summary")
async def get_eod_summary():
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute("SELECT * FROM tasks WHERE status = 'completed' ORDER BY sort_order ASC") as cur:
            completed_tasks = [dict(r) for r in await cur.fetchall()]

        tomorrow_str = (date.today() + timedelta(days=1)).isoformat()
        async with db.execute("SELECT * FROM tasks WHERE due_date = ? AND status != 'completed'", (tomorrow_str,)) as cur:
            due_tomorrow = [dict(r) for r in await cur.fetchall()]

        return {
            "completed": completed_tasks,
            "completed_count": len(completed_tasks),
            "due_tomorrow": due_tomorrow,
            "due_tomorrow_count": len(due_tomorrow)
        }

@app.post("/api/purge-completed")
async def purge_completed_tasks():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("DELETE FROM tasks WHERE status = 'completed'")
        deleted_count = cursor.rowcount
        await db.commit()
        return {"status": "purged", "count": deleted_count}

@app.post("/api/settings/name")
async def update_app_name(payload: AppNameUpdate):
    clean_name = payload.name.strip()
    config_file = os.path.join(os.path.dirname(__file__), ".config.env")
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(f'APP_DISPLAY_NAME="{clean_name}"\n')
        return {"status": "success", "app_name": clean_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scratchpad Endpoints
@app.get("/api/notes")
async def get_notes():
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT content, updated_at FROM notes WHERE id = 'default'") as cur:
            row = await cur.fetchone()
            return dict(row) if row else {"content": "", "updated_at": ""}

@app.put("/api/notes")
async def save_notes(payload: NoteUpdate):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("UPDATE notes SET content = ?, updated_at = ? WHERE id = 'default'", (payload.content, now))
        await db.commit()
        return {"status": "saved", "updated_at": now}
