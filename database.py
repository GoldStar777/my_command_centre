import aiosqlite

DB_FILE = "command_center.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("PRAGMA journal_mode = WAL;")

        # 1. Categories Table (Dynamic with colours)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                color TEXT NOT NULL
            );
        """)

        # 2. Tasks Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                priority TEXT DEFAULT 'amber',
                status TEXT DEFAULT 'pending',
                due_date TEXT,
                details TEXT,
                sort_order INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                completed_at TEXT
            );
        """)

        # Safe Column Migrations for existing databases
        columns_to_ensure = [
            ("completed_at", "TEXT"),
            ("sort_order", "INTEGER DEFAULT 0"),
            ("category", "TEXT DEFAULT 'General'"),
            ("details", "TEXT"),
            ("due_date", "TEXT"),
            ("priority", "TEXT DEFAULT 'amber'"),
            ("status", "TEXT DEFAULT 'pending'")
        ]

        for col_name, col_type in columns_to_ensure:
            try:
                await db.execute(f"ALTER TABLE tasks ADD COLUMN {col_name} {col_type};")
            except Exception:
                # Column already exists in table
                pass

        # 3. Scratchpad Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                content TEXT DEFAULT '',
                updated_at TEXT NOT NULL
            );
        """)

        # Seed initial note if missing
        cursor = await db.execute("SELECT id FROM notes WHERE id = 'default'")
        if not await cursor.fetchone():
            await db.execute(
                "INSERT INTO notes (id, content, updated_at) VALUES ('default', '', datetime('now'))"
            )

        # Seed baseline categories if empty
        cursor = await db.execute("SELECT COUNT(*) FROM categories")
        count = (await cursor.fetchone())[0]
        if count == 0:
            defaults = [
                ("c1", "Deep Work", "#6366f1"),   # Indigo
                ("c2", "Strategy", "#0ea5e9"),    # Sky
                ("c3", "Operations", "#10b981"),  # Emerald
                ("c4", "Personal", "#ec4899"),    # Pink
                ("c5", "Admin", "#8b5cf6")        # Purple
            ]
            await db.executemany("INSERT INTO categories (id, name, color) VALUES (?, ?, ?)", defaults)

        await db.commit()
