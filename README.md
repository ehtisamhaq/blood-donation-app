# 🩸 Blood Donation Platform

A web application designed to connect blood donors with individuals and hospitals in need of emergency blood donations.

Built with **Django (Python)** and PostgreSQL, with a focus on providing a simple and reliable platform for managing blood donors and emergency blood requests.

---

## 📌 Features

- **Urgent Request Feed:** View critical blood donation requests by blood group, hospital, and location.
- **Donor Directory:** Manage registered donor profiles and donor information.
- **Request Management:** Submit and manage urgent blood donation requests.
- **Admin Dashboard:** Manage donors, requests, users, and other application data through Django Admin.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.14 / Django 6.x
- **Database:** PostgreSQL
- **Database Hosting:** Neon
- **Database Driver:** psycopg2
- **Environment Configuration:** python-dotenv
- **Styling:** HTML5 / Tailwind CSS
- **Virtual Environment:** Python `venv`

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- Git
- PostgreSQL-compatible database (the project currently uses Neon)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/blood_donation_app.git

cd blood_donation_app
```

---

### 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

---

### 3. Install Dependencies

Install the project's Python dependencies:

```bash
pip install -r requirements.txt
```

The main dependencies currently include:

- Django
- psycopg2-binary
- python-dotenv
- asgiref
- sqlparse

---

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```text
blood_donation_app/
├── .env
├── manage.py
├── requirements.txt
└── ...
```

Add your database configuration:

```env
DEBUG=True

SECRET_KEY=your-django-secret-key

DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=your-database-password
DB_HOST=your-neon-host
DB_PORT=5432
```

> **Never commit `.env` to Git.** Make sure `.env` is included in `.gitignore`.

---

### 5. Apply Database Migrations

Apply the existing Django migrations to your database:

```bash
python manage.py migrate
```

If you make changes to Django models later, create new migrations with:

```bash
python manage.py makemigrations
```

Then apply them:

```bash
python manage.py migrate
```

---

### 6. Create a Superuser

To access the Django Admin dashboard:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

---

### 7. Start the Development Server

Run:

```bash
python manage.py runserver
```

The development server will start at:

```text
http://127.0.0.1:8000/
```

Open the URL in your browser.

The Django Admin dashboard is available at:

```text
http://127.0.0.1:8000/admin/
```

---

## 📁 Project Structure

```text
blood_donation_app/
│
├── .venv/                     # Python virtual environment
├── .env                       # Environment variables (not committed)
├── .gitignore
├── manage.py                  # Django project CLI
├── requirements.txt           # Python dependencies
│
├── core/                      # Project-level configuration
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py                # Root URL configuration
│   ├── asgi.py                # ASGI configuration
│   └── wsgi.py                # WSGI configuration
│
└── donors/                    # Blood donor application
    ├── migrations/             # Database migrations
    ├── templates/              # Django templates
    ├── __init__.py
    ├── admin.py               # Django Admin configuration
    ├── apps.py                # App configuration
    ├── models.py              # Database models
    ├── urls.py                # Donor-related URLs
    └── views.py               # Request handling / views
```

> The project structure may grow as additional Django apps and features are added.

---

## 🔐 Environment Variables

The application uses environment variables for configuration and sensitive credentials.

Example:

```env
DEBUG=True

SECRET_KEY=your-django-secret-key

DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=your-database-password
DB_HOST=your-neon-host
DB_PORT=5432
```

### Environment Variable Reference

| Variable      | Description                        |
| ------------- | ---------------------------------- |
| `DEBUG`       | Enables/disables Django debug mode |
| `SECRET_KEY`  | Django secret key                  |
| `DB_NAME`     | PostgreSQL database name           |
| `DB_USER`     | PostgreSQL username                |
| `DB_PASSWORD` | PostgreSQL password                |
| `DB_HOST`     | PostgreSQL server hostname         |
| `DB_PORT`     | PostgreSQL server port             |

For production, use secure environment variables and set:

```env
DEBUG=False
```

---

## 🗄️ Database

The project uses **PostgreSQL** as its database.

The current development database is hosted on **Neon**.

Django connects to PostgreSQL using the `psycopg2-binary` package.

The database configuration is defined in:

```text
core/settings.py
```

and credentials are loaded from:

```text
.env
```

---

## 🧰 Useful Django Commands

### Start the development server

```bash
python manage.py runserver
```

### Create migrations

Run this after modifying Django models:

```bash
python manage.py makemigrations
```

### Apply migrations

```bash
python manage.py migrate
```

### Create an admin user

```bash
python manage.py createsuperuser
```

### Open the Django shell

```bash
python manage.py shell
```

### Show available commands

```bash
python manage.py help
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/AmazingFeature
```

3. Make your changes.
4. Commit your changes:

```bash
git add .
git commit -m "Add AmazingFeature"
```

5. Push the branch:

```bash
git push origin feature/AmazingFeature
```

6. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
