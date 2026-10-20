
# Command Centre

A lightweight, local-first personal command deck and scratchpad for macOS and Windows.

Command Centre brings structured task management and freeform note-taking together in one focused workspace. With platform-specific installers, customisable branding, and local data storage, it provides a convenient, native-feeling productivity app without requiring you to keep a terminal window or VS Code open.

## Features

- **Executive Directive Deck** — Organise tasks by High, Medium, and Low priority using colour-coded tiers, chronological due-date ordering, and category tags.
- **Rich-Text Scratchpad** — Capture ideas, notes, and working documents in an integrated editor with autosave, multi-level lists, and code blocks.
- **Personalised Branding** — Choose your name and preferred app title during installation, then rename the application directly from the homepage at any time.
- **End-of-Day Audit** — Generate a summary of the tasks you completed that day, clear those completed tasks from your directive list, and receive a reminder of tasks coming up tomorrow.
- **Local-First Storage** — Store your tasks and notes in a local SQLite database without requiring a cloud database or online account.
- **Cross-Platform Installation** — Automated installation scripts for macOS and Windows make setup straightforward.
- **Background Operation on macOS** — Run as a background service managed by `launchd`, independently of a terminal window.
- **Flexible Uninstallation** — Choose to preserve your existing user data or perform a full, destructive data wipe.

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

Choose the instructions for your operating system.

### macOS

The macOS installer creates a Python virtual environment, installs dependencies, prompts you to personalise the application, and registers Command Centre as a background service.

**1. Clone the repository**

```bash
git clone https://github.com/GoldStar777/my_command_centre.git
cd my_command_centre
```

**2. Run the installer**

```bash
chmod +x install.sh uninstall.sh
./install.sh
```

Follow the prompts to enter your name and preferred application title. The installer configures the local environment and registers the background service.

**3. Open Command Centre**

Visit [http://localhost:8000](http://localhost:8000) in Safari.

**4. Add it to your Dock (optional)**

In Safari, select **File → Add to Dock…** to create a convenient, app-like entry point.

### Windows

The Windows installer automates the initial setup, including creating the virtual environment and installing dependencies.

**1. Clone the repository**

Open Command Prompt or PowerShell and run:

```powershell
git clone https://github.com/GoldStar777/my_command_centre.git
cd my_command_centre
```

**2. Run the installer**

Double-click `install.bat` in File Explorer, or run:

```powershell
.\install.bat
```

Follow the prompts to enter your name and preferred application title. The installer configures the environment, installs the dependencies, and launches the server.

**3. Open Command Centre**

Visit [http://localhost:8000](http://localhost:8000) in your browser.

**4. Install it as an app (optional)**

For a more desktop-like experience, use Microsoft Edge or Google Chrome to install the webpage as an app. Open the browser menu and look for the option to install or save the page as an app; the exact wording varies by browser version.

## How to Use Command Centre

Command Centre is designed around two complementary spaces: your directive deck for managing tasks and your scratchpad for capturing thoughts and working notes.

### 1. Manage Your Directives

Use the directive deck as your central task list.

- **Add tasks** as they arise throughout the day.
- **Set priorities** using the High, Medium, and Low tiers to distinguish urgent work from less pressing tasks.
- **Assign categories** to organise tasks by project, context, or type of work.
- **Set due dates** to keep deadlines visible and make it easier to identify what needs attention next.
- **Update and complete tasks** as you work through your daily priorities.

The aim is to keep your immediate commitments visible without losing track of upcoming deadlines.

### 2. Use the Scratchpad

Use the integrated rich-text editor for everything that does not belong in your task list.

- Capture ideas and reminders before you forget them.
- Write longer notes, plans, and working documents.
- Structure information with headings, multi-level lists, and other rich-text formatting.
- Keep code snippets and technical notes in code blocks.

The editor autosaves your work, making it suitable for an ongoing personal workspace rather than a temporary note.

### 3. Personalise Your Workspace

During installation, enter your name and choose a title for your application.

You can change the app title later by clicking the title on the homepage and entering a new one. There is no need to reinstall the application simply to rename your workspace.

### 4. Run Your End-of-Day Audit

The **End-of-Day** button is designed to close out your working day and prepare you for the next one. It does more than simply clear completed tasks.

When you use it, the application:

1. **Summarises your completed work.** It provides a summary of the tasks you completed during the day, giving you a concise record of your progress.
2. **Clears completed tasks from your directive deck.** Tasks marked as completed are removed from the active task list, keeping the workspace uncluttered and focused on outstanding work.
3. **Looks ahead to tomorrow.** It reminds you of upcoming tasks due tomorrow, helping you identify priorities before the next working day begins.

#### A suggested daily workflow

- **Morning:** Review your directives, check deadlines, and identify your highest-priority work.
- **During the day:** Add tasks as needed, update priorities, and mark work as completed. Use the scratchpad to capture ideas and notes.
- **End of day:** Press the End-of-Day button, review your completion summary, and take note of tomorrow's upcoming tasks.
- **Next morning:** Start with a cleaner directive deck and a clearer view of what needs attention.

**Important:** The End-of-Day action is intended to clear completed tasks from your active directives. Use it once you are ready to close out the day, and review the summary and upcoming reminders before moving on.

## Uninstallation

Command Centre includes uninstall scripts for both operating systems. You can choose to preserve your user data or perform a full wipe.

### macOS

From the repository directory, run:

```bash
./uninstall.sh
```

### Windows

From the repository directory, double-click `uninstall.bat`, or run:

```powershell
.\uninstall.bat
```

### Choose What Happens to Your Data

The uninstaller offers two approaches:

- **Retain user data** — Remove the service or stop the application while preserving your existing database and its contents, allowing you to retain your tasks and notes for future use.
- **Nuclear Wipe** — Perform a destructive uninstall that removes local user data and associated application files covered by the uninstall script.

The Nuclear Wipe option is irreversible. Make sure you no longer need your stored information before confirming it, and back up anything important beforehand.

Uninstalling the service does not necessarily remove the repository directory itself. You can delete that directory separately if you no longer need the project files.

## Manual Setup

If you prefer not to use the automated installers, you can set up and launch the application manually.

### Requirements

- Python 3.12 or later
- `pip`

### macOS

```bash
git clone https://github.com/GoldStar777/my_command_centre.git
cd my_command_centre

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app:app --host 127.0.0.1 --port 8000
```

### Windows (PowerShell)

```powershell
git clone https://github.com/GoldStar777/my_command_centre.git
cd my_command_centre

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

uvicorn app:app --host 127.0.0.1 --port 8000
```

If PowerShell prevents activation of the virtual environment, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

Then install the dependencies and run the `uvicorn` command shown above.

Once the server is running, open [http://localhost:8000](http://localhost:8000). To stop a manually started server, press `Ctrl+C` in the terminal.

## Data & Privacy

Command Centre is designed as a local-first application. It uses SQLite for local data storage and does not require a cloud database or online account.

When running locally, the application is intended to be accessed through `http://localhost:8000`. The manual setup binds the server to `127.0.0.1`, restricting access to the local machine.

Keep backups of any important information. If you uninstall the application, choose the data-retention option if you want to preserve your existing tasks and notes. The Nuclear Wipe option is intended for users who explicitly want to remove their local data.

## Project Structure

| File or directory | Purpose |
|---|---|
| `app.py` | FastAPI application and web interface routes |
| `database.py` | SQLite database operations |
| `templates/` | HTML templates for the interface |
| `requirements.txt` | Python dependencies |
| `install.sh` | macOS installer and background-service setup |
| `uninstall.sh` | macOS uninstaller |
| `install.bat` | Windows installer |
| `uninstall.bat` | Windows uninstaller |
