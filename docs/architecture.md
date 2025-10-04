# Architecture Overview

## Tech Stack

- **Backend**: Flask web application with SQLAlchemy ORM
- **Frontend**: HTML templates with Jinja2 templating engine
- **Database**: PostgreSQL (production) / SQLite (development)
- **Package Manager**: uv (modern Python package manager)
- **Web Server**: Gunicorn with gevent workers
- **Reverse Proxy**: nginx
- **Process Manager**: systemd (Linux services)
- **CI/CD**: GitHub Actions
- **Migrations**: Flask-Migrate (Alembic)

## Requirements

- Python 3.9+
- PostgreSQL (for production)
- nginx (for production)
- Linux server with systemd (Ubuntu 22.04 recommended for production)

## Project Structure

```
your-project/
├── app/
│   ├── __init__.py
│   ├── create_app/
│   │   ├── __init__.py
│   │   ├── create_app.py
│   │   ├── extensions.py
│   │   └── create_migration_app.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── db/
│   │       ├── __init__.py
│   │       └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main_routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── login.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
├── deploy/
│   └── configs/
│       ├── nginx/
│       │   └── myapp.conf
│       └── systemd/
│           └── myapp.service
├── migrations/
├── tests/
│   ├── __init__.py
│   └── test_basic.py
├── .github/
│   └── workflows/
│       └── deploy.yml
├── config.py
├── wsgi.py
├── main.py
├── pyproject.toml
├── Makefile
├── migrate_db.sh
├── .flaskenv
├── .gitignore
└── README.md
```

## Security Considerations

1. Never commit `local_settings.py` or `.env` files
2. Use strong SECRET_KEY in production
3. Enable firewall on production server (ports 22, 80, 443)
4. Keep dependencies updated: `uv lock --upgrade`
5. Use HTTPS in production with SSL certificates
6. Regularly backup your database

