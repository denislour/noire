Search files...
Dựa trên hình ảnh bạn cung cấp và yêu cầu tạo một ứng dụng CLI tương tự cho quản lý notes với các loại khác nhau, tôi sẽ đề xuất các thư viện Python phù hợp:

## **Thư viện Python được đề xuất:**

### **1. CLI Framework - Click hoặc Typer**

```bash
# Click (phổ biến, ổn định)
pip install click

# Typer (hiện đại, type hints tốt)
pip install typer
```

**Ưu điểm:**

- **Click**: Mature, nhiều tính năng, documentation tốt
- **Typer**: Dựa trên Click nhưng có type hints tự động, syntax đẹp hơn

### **2. Hiển thị bảng - Rich**

```bash
pip install rich
```

**Tính năng:**

- Tạo bảng đẹp như trong hình
- Hỗ trợ màu sắc, emoji (✅, ❌)
- Progress bars, syntax highlighting

### **3. Lưu trữ dữ liệu**

```bash
# SQLite (đơn giản)
# Có sẵn trong Python

# Hoặc TinyDB (NoSQL nhẹ)
pip install tinydb

# Hoặc JSON file đơn giản
```

---

## **Cấu trúc ứng dụng đề xuất:**

```
note-cli/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── note.py          # Note model
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py            # Database operations
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── list.py          # List notes
│   │   ├── add.py           # Add note
│   │   ├── toggle.py        # Toggle complete
│   │   └── delete.py        # Delete note
│   └── utils/
│       ├── __init__.py
│       └── display.py       # Rich table formatting
├── requirements.txt
└── setup.py
```

---

## **Ví dụ implementation với Typer + Rich:**

### **1. Model cho Note:**

```python
# src/models/note.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class NoteType(Enum):
    PROJECT_A = "Project A"
    PROJECT_B = "Project B"
    INFRA = "Infrastructure"
    PERSONAL = "Personal"

@dataclass
class Note:
    id: int
    title: str
    note_type: NoteType
    completed: bool = False
    created_at: datetime = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

### **2. Main CLI với Typer:**

```python
# src/main.py
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from models.note import NoteType

app = typer.Typer()
console = Console()

@app.command()
def add(
    title: str,
    note_type: NoteType = typer.Option(NoteType.PERSONAL, help="Type of note")
):
    """Add a new note"""
    # Implementation here
    console.print(f"✅ Added note: {title} ({note_type.value})")

@app.command("list")
def list_notes(
    note_type: Optional[NoteType] = typer.Option(None, help="Filter by type"),
    completed: Optional[bool] = typer.Option(None, help="Filter by completion status")
):
    """List all notes"""
    # Create rich table similar to your image
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=6)
    table.add_column("Title")
    table.add_column("Type", justify="center")
    table.add_column("Completed", justify="center")
    table.add_column("Created At")
    table.add_column("Completed At")

    # Add rows from database
    # table.add_row("0", "Setup infrastructure", "Infrastructure", "✅", "Mon, 27 May 2024", "Mon, 27 May 2024")

    console.print(table)

@app.command()
def toggle(index: int):
    """Toggle note completion status"""
    # Implementation here
    pass

if __name__ == "__main__":
    app()
```

### **3. Database với TinyDB:**

```python
# src/database/db.py
from tinydb import TinyDB, Query
from models.note import Note, NoteType
from typing import List, Optional

class NoteDatabase:
    def __init__(self, db_path: str = "notes.json"):
        self.db = TinyDB(db_path)
        self.notes = self.db.table('notes')

    def add_note(self, note: Note) -> int:
        return self.notes.insert(note.__dict__)

    def get_notes(self, note_type: Optional[NoteType] = None, completed: Optional[bool] = None) -> List[Note]:
        query = Query()
        conditions = []

        if note_type:
            conditions.append(query.note_type == note_type.value)
        if completed is not None:
            conditions.append(query.completed == completed)

        if conditions:
            results = self.notes.search(query.fragment(conditions[0]))
            for condition in conditions[1:]:
                results = [r for r in results if condition.test(r)]
        else:
            results = self.notes.all()

        return [Note(**result) for result in results]
```

---

## **Cài đặt và chạy:**

### **1. Requirements.txt:**

```txt
typer[all]==0.9.0
rich==13.7.0
tinydb==4.8.0
```

### **2. Setup.py:**

```python
from setuptools import setup, find_packages

setup(
    name="note-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "tinydb"
    ],
    entry_points={
        "console_scripts": [
            "note=src.main:app",
        ],
    },
)
```

### **3. Cài đặt:**

```bash
pip install -e .
```

### **4. Sử dụng:**

```bash
# Add note
note add "Setup database" --note-type PROJECT_A

# List all notes
note list

# List by type
note list --note-type PROJECT_A

# Toggle completion
note toggle 0
```

---

## **Tại sao chọn stack này:**

1. **Typer**: Syntax đẹp, type safety, auto-completion
2. **Rich**: Tạo UI đẹp như trong hình, hỗ trợ màu sắc
3. **TinyDB**: Đơn giản, không cần setup database server
4. **Enum cho NoteType**: Type safety cho các loại note

Bạn có muốn tôi triển khai chi tiết hơn phần nào không?
