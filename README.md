# Flask Production Application

A production-ready Flask web application with HTML/Jinja templates, nginx reverse proxy, systemd services, CI/CD pipeline, and uv package management.

## Architecture Overview

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

## Local Development

### Initial Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Install dependencies
uv sync --all-groups

# Create .flaskenv from example
cp .flaskenv.example .flaskenv

# Create local_settings.py from example
cp local_settings.example.py local_settings.py
# Edit local_settings.py and set your SECRET_KEY

# Initialize database
uv run flask db init
uv run flask db migrate -m "Initial migration"
uv run flask db upgrade
```

### Running the Application

```bash
# Option 1: Using make (recommended)
make run

# Option 2: Direct command
uv run python wsgi.py

# Option 3: Flask development server
uv run flask run
```

Visit `http://127.0.0.1:5000` in your browser.

### Database Migrations

```bash
# Create a new migration after model changes
uv run flask db migrate -m "Description of changes"

# Apply migrations
uv run flask db upgrade

# Or use the make command
make migrate
```

### Running Tests

```bash
# Run all tests
make test

# Or directly
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=app --cov-report=html
```

## Production Deployment

### Server Setup (Ubuntu 22.04)

1. **Update system and install dependencies:**

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip nginx postgresql postgresql-contrib git
```

2. **Install uv:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.bashrc
```

3. **Setup PostgreSQL:**

```bash
sudo -u postgres psql
CREATE DATABASE myapp_db;
CREATE USER myapp_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;
\q
```

4. **Clone and setup application:**

```bash
cd ~
git clone <your-repo-url> myapp
cd myapp

# Create local_settings.py
cat > local_settings.py << 'EOF'
SECRET_KEY = 'your-super-secret-key-here'
DATABASE_URL = 'postgresql://myapp_user:your_secure_password@localhost/myapp_db'
EOF

# Install dependencies
uv sync

# Initialize database
uv run flask db init
uv run flask db migrate
uv run flask db upgrade
```

5. **Configure systemd service:**

```bash
# Edit the service file with your paths and user
nano deploy/configs/systemd/myapp.service

# Copy and enable service
sudo cp deploy/configs/systemd/myapp.service /etc/systemd/system/myapp.service
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp
sudo systemctl status myapp
```

6. **Configure nginx:**

```bash
# Edit the nginx config with your domain
nano deploy/configs/nginx/myapp.conf

# Copy and enable nginx config
sudo cp deploy/configs/nginx/myapp.conf /etc/nginx/sites-available/myapp
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/myapp
sudo rm /etc/nginx/sites-enabled/default  # Optional

# Test and reload nginx
sudo nginx -t
sudo systemctl reload nginx
```

7. **Setup SSL with Let's Encrypt (recommended):**

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### CI/CD Setup (GitHub Actions)

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

1. **SSH_PRIVATE_KEY**: Your server's SSH private key for GitHub Actions
2. **SERVER_HOST**: Your server's IP address or domain
3. **SERVER_USERNAME**: SSH username on the server
4. **SUDO_PASSWORD**: The sudo password for the server user

The CI/CD pipeline will automatically deploy to production when you push to the `main` branch.

## Common Operations

### Managing the Production Service

```bash
# View logs
sudo journalctl -u myapp -f

# Restart service
sudo systemctl restart myapp

# Stop service
sudo systemctl stop myapp

# Start service
sudo systemctl start myapp

# Check status
sudo systemctl status myapp
```

### Nginx Operations

```bash
# Test configuration
sudo nginx -t

# Reload nginx (no downtime)
sudo systemctl reload nginx

# Restart nginx
sudo systemctl restart nginx

# View logs
sudo tail -f /var/log/nginx/myapp_error.log
sudo tail -f /var/log/nginx/myapp_access.log
```

### Manual Deployment

```bash
ssh user@server
cd myapp
git pull
uv sync
sh migrate_db.sh
sudo systemctl restart myapp
```

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

## Troubleshooting

### Application won't start

```bash
# Check logs
sudo journalctl -u myapp -n 50 --no-pager

# Verify socket file exists
ls -la ~/myapp/*.sock

# Check gunicorn processes
ps aux | grep gunicorn
```

### Database connection errors

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U myapp_user -d myapp_db
```

### Nginx 502 Bad Gateway

```bash
# Check if app socket exists
ls -la /home/youruser/myapp/*.sock

# Check app is running
sudo systemctl status myapp

# Check nginx error logs
sudo tail -f /var/log/nginx/myapp_error.log
```

## License

Your license here

