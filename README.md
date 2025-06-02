# Noir CLI

Noir is a simple command-line interface (CLI) tool to help you jot down and manage your notes effectively. Whether it's for your projects, infrastructure tasks, or personal reminders, Noir aims to keep things organized.

## Features

- **Create Notes**: Quickly add new notes with a title and type.
- **List Notes**: View all your notes or filter them by type or completion status.
- **Note Types**: Categorize your notes (e.g., `project`, `infra`, `personal`).
- **Track Status**: Notes can be marked as pending or completed.
- **Timestamped**: Notes automatically record creation time and completion time.
- **Simple Storage**: Notes are stored locally in a JSON file (`data/notes.json`).

## Getting Started

_(This section can be expanded once you have setup.py or installation instructions)_

Currently, you can run the CLI from the source code:

### Prerequisites

- Python (version used in development, e.g., 3.8+)
- Poetry or `pip` for managing dependencies (Typer, Rich, TinyDB, Pydantic, python-dependency-injector).

### Running

1.  Clone the repository (if applicable).
2.  Navigate to the project directory.
3.  Install dependencies (e.g., `pip install -r requirements.txt` or `poetry install`).
4.  Run the application:
    - Using the main module:
      ```bash
      python -m src.main <command> [options]
      ```
    - Or, if you have a `run.py` script:
      ```bash
      python run.py <command> [options]
      ```

## Usage Examples

_(These commands are based on the current files)_

- **Add a new personal note:**

  ```bash
  python -m src.main add "Remember to buy milk" --note-type personal
  ```

- **Add a new project note (default type is personal if not specified for add):**

  ```bash
  python -m src.main add "Setup a new project environment" --note-type project
  ```

- **List all notes:**

  ```bash
  python -m src.main list
  ```

- **List only project notes:**

  ```bash
  python -m src.main list --note-type project
  ```

- **List only completed notes:**

  ```bash
  python -m src.main list --completed
  ```

- **List only pending notes:**
  ```bash
  python -m src.main list --no-completed # Or --completed false, depending on Typer's bool handling for False
  # (Reviewing list.py, it seems to use --completed / --no-completed or completed=True/False)
  # python -m src.main list --completed false # Assuming this would work, or an explicit pending filter if added
  ```
  Actually, `src/commands/list.py` defines `completed: Optional[bool] = Option(None, ...)`.
  So it would be:
  ```bash
  python -m src.main list --completed # for completed notes
  python -m src.main list --no-completed # for pending notes
  ```

## Future Development

- Implement `complete` and `delete` commands.
- Package the application for easier installation via `pip`.
- Add more filtering options for listing notes.
- Potentially add search functionality.
