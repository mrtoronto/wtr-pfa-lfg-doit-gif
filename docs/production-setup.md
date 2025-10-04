# Production Deployment Guide

## Quick Start Summary

1. **Local Setup**: Generate SSH key and add to DigitalOcean
2. **Create Droplet**: Ubuntu 22.04 with your SSH key selected
3. **Server Setup**: Create non-root user, install dependencies (nginx, PostgreSQL, uv)
4. **Database Setup**: Create PostgreSQL database and user
5. **App Setup**: Clone repo, run migrations, configure systemd and nginx
6. **Fix Permissions**: `chmod 755` your home directory for nginx socket access
7. **GitHub Secrets**: Add 8 secrets for automated deployments
8. **Deploy**: Push to `main` branch - GitHub Actions handles the rest!

## Initial SSH Setup for DigitalOcean

Before setting up your server, you need to create and configure SSH keys.

### 1. Generate SSH Key (on your local machine)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# When prompted:
# - File location: Press Enter (default: ~/.ssh/id_ed25519)
# - Passphrase: Optional - press Enter to skip or add for extra security
```

### 2. Add SSH Key to DigitalOcean

```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
```

- Go to DigitalOcean → **Settings** → **Security** → **SSH Keys**
- Click **Add SSH Key**
- Paste your public key (starts with `ssh-ed25519 ...`)
- Give it a name (e.g., "My MacBook")
- Click **Add SSH Key**

### 3. Create Droplet

- When creating your droplet, **select your SSH key** under "Authentication"
- Choose Ubuntu 22.04 LTS
- Note your server's IP address (e.g., `64.227.105.186`)

### 4. Connect to Server

```bash
# Connect as root (first time)
ssh root@YOUR_SERVER_IP
```

### 5. Create Non-Root User (IMPORTANT - Security Best Practice)

```bash
# Create user (replace 'youruser' with your preferred username)
adduser youruser

# Add user to sudo group
usermod -aG sudo youruser

# Copy SSH keys to new user
rsync --archive --chown=youruser:youruser ~/.ssh /home/youruser

# Test new user (open a NEW terminal window, keep root session open)
ssh youruser@YOUR_SERVER_IP

# If the above works, you can optionally disable root login:
sudo vim /etc/ssh/sshd_config
# Change: PermitRootLogin yes → PermitRootLogin no
sudo systemctl restart ssh
```

**From now on, use your non-root user for all operations!**

## Server Setup (Ubuntu 22.04)

### 1. Update system and install dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip nginx postgresql postgresql-contrib git
```

### 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.bashrc
```

### 3. Setup PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE myapp_db;
CREATE USER myapp_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;
\q
```

### 4. Clone and setup application

```bash
cd ~
git clone https://github.com/mrtoronto/wtr-pfa-lfg-doit-gif.git pfa
cd pfa

# Create local_settings.py
# Note: If using GitHub Actions CI/CD, this will be created automatically on deploy
cat > local_settings.py << 'EOF'
SECRET_KEY = 'your-super-secret-key-here'
DATABASE_URL = 'postgresql://myapp_user:your_secure_password@localhost/myapp_db'
EOF

# Install dependencies
uv sync

# Initialize database
uv run sh migrate_db.sh
```

### 5. Configure systemd service

```bash
# IMPORTANT: Edit the service file to set your username
# Change "User=matt" to "User=youruser" (your actual username)
vim deploy/configs/systemd/myapp.service

# Copy and enable service
sudo cp deploy/configs/systemd/myapp.service /etc/systemd/system/myapp.service
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp
sudo systemctl status myapp
```

### 6. Configure nginx

```bash
# Edit the nginx config with your domain (or leave as-is for IP-based access)
vim deploy/configs/nginx/myapp.conf

# Copy and enable nginx config
sudo cp deploy/configs/nginx/myapp.conf /etc/nginx/sites-available/myapp
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/myapp
sudo rm /etc/nginx/sites-enabled/default  # Remove default site

# Test and reload nginx
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Fix permissions for nginx socket access (IMPORTANT)

```bash
# Allow nginx (www-data user) to access the socket file
# This is required because the socket is in your home directory
chmod 755 /home/youruser

# Verify nginx can access the socket
sudo -u www-data test -r /home/youruser/pfa/myapp.sock && echo "✓ Socket accessible" || echo "✗ Permission issue"
```

### 8. Test your deployment

```bash
# Your app should now be accessible at:
# http://YOUR_SERVER_IP (e.g., http://64.227.105.186)

# Check if the app is responding
curl -I http://YOUR_SERVER_IP
```

## Setup SSL with Let's Encrypt (Optional)

Requires a domain name.

```bash
# First, point your domain's A record to your server's IP
# Then run:
sudo apt install -y certbot python3-certbot-nginx

# Update nginx config with your domain name before running certbot
# Edit /etc/nginx/sites-available/myapp and change server_name from _ to yourdomain.com
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Update config.py to use https:
# Change PREFERRED_URL_SCHEME = 'http' to 'https' in production mode
```

