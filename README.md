# My Command Centre

A lightweight, local-first personal command deck and scratchpad for macOS.

My Command Centre combines structured task prioritisation and freeform note-taking in a single, distraction-free workspace. Designed to run quietly in the background as an independent local application, it stays accessible without requiring a terminal window or VS Code to remain open.

## Features

- **Task Management** — Organise tasks into High, Medium, and Low priority tiers with a structured, colour-coded interface.
- **Rich-Text Scratchpad** — Capture ideas, notes, and working documents in an integrated editor with autosave, multi-level lists, and code blocks.
- **End-of-Day Review** — Clear completed tasks and review upcoming deadlines to keep your workspace focused.
- **Local-First Architecture** — Use SQLite for local data storage, keeping your personal workspace independent of external database services.
- **Native macOS Integration** — Run as a background service managed by `launchd`, with the option to add the web interface to your Dock using Safari.
- **Lightweight & Self-Contained** — A Python backend and browser-based frontend, without the overhead of a larger desktop application framework.

## Tech Stack

| Component | Technologies |
|---|---|
| Backend | Python 3.12+, FastAPI, Uvicorn |
| Database | SQLite, `aiosqlite` |
| Frontend | Vanilla JavaScript, Tailwind CSS |
| Rich-Text Editing | Quill.js |
| Interactive UI | SortableJS |
| Templates | Jinja2 |
| macOS Background Service | `launchd` |

## Installation

### macOS — Recommended

The installer configures the application as a local background service, allowing it to run independently of your terminal.

#### 1. Clone the repository

```bash
git clone https://github.com/GoldStar777/my_command_centre.git
cd my_command_centre
```

#### 2. Run the installer

```bash
./install.sh
```

The installer will prompt you for your preferred application title, create a local Python virtual environment, install the required dependencies, and register the background service.

#### 3. Open the application

Navigate to [http://localhost:8000](http://localhost:8000).

#### 4. Add to your Dock (optional)

For convenient access, open the application in Safari and select:

`File → Add to Dock...`

This provides an app-like entry point to your personal command centre.

## Managing the Background Service

### Stop or Uninstall

To stop the background service and remove its registration, run:

```bash
./uninstall.sh
```

Check the uninstall script before running it if you need to confirm whether it removes only the service or also deletes application files or data.

## Manual Setup

You can also run the application directly without installing the macOS background service. This is useful for development and for environments where the installer is not supported.

### Requirements

- Python 3.12 or later
- `pip`

### Setup

#### 1. Clone the repository

```bash
git clone https://github.com/GoldStar777/my_command_centre.git
cd my_command_centre
```

#### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Start the server

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

#### 5. Open the application

Visit [http://localhost:8000](http://localhost:8000) in your browser.

To stop the server, press `Ctrl+C` in the terminal.

## Data & Privacy

My Command Centre is designed as a local-first application, using SQLite for local data storage.

The application is intended to run locally rather than as a publicly accessible service. By default, the manual setup binds the server to `127.0.0.1`, restricting access to the local machine.

Keep the server bound to `127.0.0.1` unless you have a specific reason to make it accessible from other devices.

## Project Structure

Key components include:

- `app.py` — FastAPI application entry point.
- `requirements.txt` — Python dependencies.
- `install.sh` — macOS installation and background-service setup.
- `uninstall.sh` — Background-service removal.
- `.venv/` — Local Python virtual environment, created during installation.

Additional application components may be present depending on the repository version.
