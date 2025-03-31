# **First Flask app ever**
This repo showed Flask knowledges that I have gathered over time.

## **March 31, 2025**
### **Things have done**
1. Simple Flask project's structure for REST API only. (A Flask project can follow the MVC (Model-View-Controller) architecture, similar to PHP or ASP.NET. "REST API only" means that this project will serve only as the backend, providing REST API endpoints.)
2. Simple Flask project's initialization (following [flask-api-example](https://github.com/apryor6/flask_api_example) on GitHub).

### **Knowledges have gathered**
1. **Project's structure (the explanation has been made by ChatGPT):**

    **📂 Root Directory (`first-flask-app-ever`)**
    These files handle project-wide settings, dependencies, and entry points.

    | File | Purpose |
    |------|---------|
    | **`.gitignore`** | Excludes unnecessary files from Git (e.g., `__pycache__/`, `.env`, `*.pyc`). |
    | **`manage.py`** | Manages the app (e.g., running, migrations, custom commands). |
    | **`README.md`** | Documentation for setup, API usage, and project structure. |
    | **`requirements.txt`** | Lists required Python packages. Install them with `pip install -r requirements.txt`. |
    | **`tree.txt`** | (Probably) stores the directory structure, generated using `tree /f > tree.txt`. |
    | **`wsgi.py`** | Entry point for deploying with a WSGI server (e.g., Gunicorn, uWSGI). |

    ---

    **📂 `app/` (Main API Logic)**
    This folder contains **all backend logic** (config, routes, and different API modules).

    | File | Purpose |
    |------|---------|
    | **`config.py`** | Manages configuration settings (e.g., database URL, API keys). |
    | **`routes.py`** | Registers API routes globally. |
    | **`__init__.py`** | Initializes the Flask app and imports required modules. |

    ---

    **📂 `app/api-collection-X/` (Feature Modules)**
    Each **API collection** is treated as a separate module (e.g., `api-collection-1`, `api-collection-2`, `api-collection-3`).  
    This is a **modular approach** for organizing multiple API functionalities.

    | File | Purpose |
    |------|---------|
    | **`controller.py`** | Defines Flask route handlers (e.g., `GET`, `POST`, `PUT`, `DELETE`). |
    | **`interface.py`** | Defines abstract classes or business rules for services. |
    | **`model.py`** | Defines the data model (e.g., SQLAlchemy ORM or Pydantic model). |
    | **`schema.py`** | Handles request/response validation using libraries like Marshmallow or Pydantic. |
    | **`service.py`** | Contains business logic (e.g., CRUD operations, calling external APIs). |
    | **`__init__.py`** | Makes this folder a Python package. |