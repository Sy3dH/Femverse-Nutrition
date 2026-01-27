# Femverse Nutrition

A clinical nutrition application built with Python.  
Runs on **uv** environment and **FastAPI / Uvicorn**.

---

## 🛠 Prerequisites

- Python 3.11+ installed
- [uv](https://pypi.org/project/uv/) (Python package manager)

- The project is tested with Python 3.13
---

## ⚡ Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Sy3dH/Femverse-Nutrition.git
cd Femverse-Nutrition

2. **Install dependencies using uv**

```bash
uv sync
```

> This will create a `.uv` environment and install all packages from your `pyproject.toml`.

3. **Activate the uv environment**

### Linux / macOS

```bash
source .uv/bin/activate
```

### Windows (Command Prompt)

```cmd
.uv\Scripts\activate.bat
```

### Windows (PowerShell)

```powershell
.uv\Scripts\Activate.ps1
```

---

## 🚀 Running the Application

Start the FastAPI server using **Uvicorn**:

```bash
uvicorn app.main:app --port 8000 --reload
```

* `--port 8000` → The port where the app will run (can be changed)
* `--reload` → Auto-reload on code changes (useful for development)

Once running, open your browser at:

```
http://127.0.0.1:8000
```

You can also access the automatic API docs at:

```
http://127.0.0.1:8000/docs
```

---

## ✅ Deactivating the Environment

```bash
deactivate
```
