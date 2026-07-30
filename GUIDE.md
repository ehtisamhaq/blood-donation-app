````python
# Generate a polished Markdown guide for common Django CLI commands and workflow

md_content = """# Django CLI & Development Workflow Cheat Sheet

A practical quick reference for daily Django development commands, virtual environments, migrations, database management, and troubleshooting.

---

## 🚀 Daily Workflow Sequence

When starting a new development session, follow this standard sequence:

```bash
# 1. Navigate to project root
cd ~/Developer/blood_donation_app

# 2. Activate Virtual Environment
source .venv/bin/activate

# 3. Start Development Server
python manage.py runserver

````

---

## 🛠️ Frequently Used Commands

### 1. Database & Migrations

Migrations synchronize your Python `models.py` schema with your PostgreSQL database.

| Command                                      | Usage / Purpose                                                | When to run                                                    |
| -------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `python manage.py makemigrations`            | Detects changes in `models.py` and creates migration files.    | Every time you create or modify a model field.                 |
| `python manage.py makemigrations <app_name>` | Generates migration files for a specific app (e.g., `donors`). | Useful when working on multi-app projects.                     |
| `python manage.py migrate`                   | Applies pending migrations to the PostgreSQL database.         | After running `makemigrations` or after pulling code from Git. |
| `python manage.py showmigrations`            | Lists all migrations and shows which ones are applied `[X]`.   | Troubleshooting database state or missing migrations.          |

> **Workflow Rule:** Modify `models.py` ➔ Run `makemigrations` ➔ Run `migrate`.

---

### 2. Application & Core Management

| Command                                | Usage / Purpose                                                       |
| -------------------------------------- | --------------------------------------------------------------------- |
| `python manage.py startapp <app_name>` | Creates a new app module folder (e.g., `requests`, `users`).          |
| `python manage.py createsuperuser`     | Creates an admin user to log into `/admin/`.                          |
| `python manage.py check`               | Runs system checks for compile errors without starting the server.    |
| `python manage.py shell`               | Opens an interactive Python shell with Django environment pre-loaded. |

#### Using the Django Shell:

```python
# Test database queries directly inside python manage.py shell
from donors.models import BloodRequest
BloodRequest.objects.all()

```

---

### 3. Package & Environment Management

| Command                           | Usage / Purpose                                               |
| --------------------------------- | ------------------------------------------------------------- |
| `source .venv/bin/activate`       | Activates project virtual environment.                        |
| `deactivate`                      | Exits the virtual environment.                                |
| `pip install <package_name>`      | Installs a Python package inside `.venv`.                     |
| `pip freeze > requirements.txt`   | Updates `requirements.txt` with currently installed packages. |
| `pip install -r requirements.txt` | Installs all dependencies listed in `requirements.txt`.       |

---

### 4. Git & Version Control

```bash
# Check status of modified files
git status

# Stage changes
git add .

# Commit changes
git commit -m "Add blood request models and home view"

# Push to remote repository
git push origin main

```

---

## 🔍 Common Troubleshooting Cheat Sheet

### Issue: `zsh: command not found: python` or missing packages

- **Cause:** Virtual environment is not activated.
- **Fix:** Run `source .venv/bin/activate`.

### Issue: `ProgrammingError: relation "xyz" does not exist`

- **Cause:** Model created in `models.py`, but database migrations have not been applied.
- **Fix:** Run `python manage.py makemigrations` then `python manage.py migrate`.

### Issue: `RuntimeError: Model class ... isn't in an application in INSTALLED_APPS`

- **Cause:** The app is missing from `INSTALLED_APPS` in `core/settings.py`.
- **Fix:** Add `'donors'` to `INSTALLED_APPS` array and save the file.

---

## 📂 Project Directory Quick Reference

```text
blood_donation_app/
├── .venv/              <-- Virtual environment binaries
├── .env                <-- Local secrets (DB password, SECRET_KEY)
├── .gitignore          <-- Git exclusions (.venv, .env, __pycache__)
├── requirements.txt    <-- Project dependencies
├── manage.py           <-- CLI entry point
├── core/               <-- Project configuration (settings.py, urls.py)
└── donors/             <-- App module (models.py, views.py, urls.py)

```

"""

with open("django_cheat_sheet.md", "w") as f:
f.write(md_content)

print("FILE_GENERATED: django_cheat_sheet.md")

````

```text?code_stdout&code_event_index=1
FILE_GENERATED: django_cheat_sheet.md


````

Your Markdown guide has been generated:

---

# Django CLI & Development Workflow Cheat Sheet

A practical quick reference for daily Django development commands, virtual environments, migrations, database management, and troubleshooting.

---

## 🚀 Daily Workflow Sequence

When starting a new development session, follow this standard sequence:

```bash
# 1. Navigate to project root
cd ~/Developer/blood_donation_app

# 2. Activate Virtual Environment
source .venv/bin/activate

# 3. Start Development Server
python manage.py runserver

```

---

## 🛠️ Frequently Used Commands

### 1. Database & Migrations

Migrations synchronize your Python `models.py` schema with your PostgreSQL database.

| Command                                      | Usage / Purpose                                                | When to run                                                    |
| -------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `python manage.py makemigrations`            | Detects changes in `models.py` and creates migration files.    | Every time you create or modify a model field.                 |
| `python manage.py makemigrations <app_name>` | Generates migration files for a specific app (e.g., `donors`). | Useful when working on multi-app projects.                     |
| `python manage.py migrate`                   | Applies pending migrations to the PostgreSQL database.         | After running `makemigrations` or after pulling code from Git. |
| `python manage.py showmigrations`            | Lists all migrations and shows which ones are applied `[X]`.   | Troubleshooting database state or missing migrations.          |

> **Workflow Rule:** Modify `models.py` ➔ Run `makemigrations` ➔ Run `migrate`.

---

### 2. Application & Core Management

| Command                                | Usage / Purpose                                                       |
| -------------------------------------- | --------------------------------------------------------------------- |
| `python manage.py startapp <app_name>` | Creates a new app module folder (e.g., `requests`, `users`).          |
| `python manage.py createsuperuser`     | Creates an admin user to log into `/admin/`.                          |
| `python manage.py check`               | Runs system checks for compile errors without starting the server.    |
| `python manage.py shell`               | Opens an interactive Python shell with Django environment pre-loaded. |

#### Using the Django Shell:

```python
# Test database queries directly inside python manage.py shell
from donors.models import BloodRequest
BloodRequest.objects.all()

```

---

### 3. Package & Environment Management

| Command                           | Usage / Purpose                                               |
| --------------------------------- | ------------------------------------------------------------- |
| `source .venv/bin/activate`       | Activates project virtual environment.                        |
| `deactivate`                      | Exits the virtual environment.                                |
| `pip install <package_name>`      | Installs a Python package inside `.venv`.                     |
| `pip freeze > requirements.txt`   | Updates `requirements.txt` with currently installed packages. |
| `pip install -r requirements.txt` | Installs all dependencies listed in `requirements.txt`.       |

---

### 4. Git & Version Control

```bash
# Check status of modified files
git status

# Stage changes
git add .

# Commit changes
git commit -m "Add blood request models and home view"

# Push to remote repository
git push origin main

```

---

## 🔍 Common Troubleshooting Cheat Sheet

### Issue: `zsh: command not found: python` or missing packages

- **Cause:** Virtual environment is not activated.
- **Fix:** Run `source .venv/bin/activate`.

### Issue: `ProgrammingError: relation "xyz" does not exist`

- **Cause:** Model created in `models.py`, but database migrations have not been applied.
- **Fix:** Run `python manage.py makemigrations` then `python manage.py migrate`.

### Issue: `RuntimeError: Model class ... isn't in an application in INSTALLED_APPS`

- **Cause:** The app is missing from `INSTALLED_APPS` in `core/settings.py`.
- **Fix:** Add `'donors'` to `INSTALLED_APPS` array and save the file.
