# Flask Production Application

A production-ready Flask web application with user authentication, database migrations, and automated deployment.

## Features

- 🚀 Flask web application with SQLAlchemy ORM
- 🎨 HTML/Jinja2 templates with modern CSS
- 🗄️ PostgreSQL (production) / SQLite (development)
- 📦 Modern Python package management with `uv`
- 🔐 User authentication system
- 🔄 Database migrations with Flask-Migrate
- 🚢 Automated CI/CD with GitHub Actions
- 🌐 Production-ready with nginx + Gunicorn + systemd

## Quick Start (Local Development)

### Prerequisites

- Python 3.9+
- `uv` package manager

### Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/mrtoronto/wtr-pfa-lfg-doit-gif.git
cd wtr-pfa-lfg-doit-gif

# Quick setup (recommended)
./setup_dev.sh
```

### Running the App

```bash
# Option 1: Using make (recommended)
make run

# Option 2: Direct command
uv run python wsgi.py

# Option 3: Flask development server
uv run flask run
```

Visit `http://127.0.0.1:4200` in your browser.

### Database Migrations

Whenever you make changes to your models:

```bash
uv run sh migrate_db.sh
```

### Running Tests

```bash
# Run all tests
make test

# With coverage
uv run pytest tests/ -v --cov=app --cov-report=html
```

## Documentation

For detailed documentation on deployment, operations, and troubleshooting, see the [`docs/`](docs/) folder:

- **[Architecture Overview](docs/architecture.md)** - Tech stack, project structure, and security considerations
- **[Production Setup](docs/production-setup.md)** - Complete guide for deploying to DigitalOcean/Ubuntu
- **[CI/CD Setup](docs/ci-cd.md)** - GitHub Actions configuration and secrets
- **[Operations Guide](docs/operations.md)** - Managing services, nginx, and manual deployments
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## Project Structure

```
wtr-pfa-lfg-doit/
├── app/                    # Application code
│   ├── create_app/        # App factory and extensions
│   ├── models/            # Database models
│   ├── routes/            # Route handlers
│   ├── templates/         # Jinja2 templates
│   └── static/            # CSS, JS, images
├── deploy/                # Deployment configs
│   └── configs/
│       ├── nginx/         # nginx configuration
│       └── systemd/       # systemd service files
├── docs/                  # Documentation
├── migrations/            # Database migrations
├── tests/                 # Test suite
├── config.py             # App configuration
├── wsgi.py               # WSGI entry point
└── pyproject.toml        # Dependencies
```

## Contributing

1. Create a new branch for your feature
2. Make your changes and add tests
3. Run tests: `make test`
4. Submit a pull request

## License

Your license here