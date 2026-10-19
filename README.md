cat << 'EOF' > README.md
# Command Centre

A lightweight, local-first personal command deck and scratchpad buffer built for macOS. Runs quietly in the background as an independent native app without keeping terminal windows or VSCode open.

## Features
- **Executive Task Directive Deck:** Structured task prioritization with color-coded tiers (High / Medium / Low).
- **Word-Style Scratchpad Buffer:** Integrated rich text editor with autosave, multi-level lists, and syntax blocks.
- **End-of-Day Audit:** Clear your daily completed tasks and inspect upcoming deadlines in one click.
- **Native Mac Integration:** Installs as a lightweight macOS `launchd` background daemon accessible via Safari's "Add to Dock".

## Tech Stack
- **Backend:** Python 3.12+, FastAPI, Uvicorn, SQLite (`aiosqlite`)
- **Frontend:** Vanilla JS, Tailwind CSS, Quill.js, SortableJS, Jinja2 Templates

## Quickstart (macOS)

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/command-centre.git](https://github.com/YOUR_USERNAME/command-centre.git)
   cd command-centre

2. Run the dynamic installer:
    ```bash
    ./install.sh

The script will ask for your preferred app title, create the local environment, install dependencies, and register the background service.

3. Pin to dock:
- Open Safari and navigate to http://localhost:8000.
- Go to File → Add to Dock....

## Stopping or Uninstalling

To stop the background daemon and remove the service:

    ./uninstall.sh

## Manual Cross-Platform Run (Windows/Linux)

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app:app --port 8000

EOF

--