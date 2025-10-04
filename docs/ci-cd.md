# CI/CD Setup with GitHub Actions

The GitHub Actions workflow automatically deploys your app when you push to `main`. It will:
- Run tests
- Pull latest code on the server
- Install dependencies with `uv`
- Create `local_settings.py` with your secrets
- Copy systemd and nginx config files
- Run database migrations
- Restart the app service
- Remove the default nginx site

## Required GitHub Secrets

Go to your GitHub repository: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 8 secrets:

### 1. SSH_PRIVATE_KEY

Your private SSH key for server access.

```bash
cat ~/.ssh/id_ed25519
```

Copy the **entire output** (including `-----BEGIN` and `-----END` lines)

### 2. SERVER_HOST

Your server's IP address (e.g., `64.227.105.186`) or domain name.

### 3. SERVER_USERNAME

Your non-root username on the server (e.g., `matt`).

### 4. SUDO_PASSWORD

The password for your server user.

### 5. SECRET_KEY

Flask secret key - generate with:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 6. DB_NAME

PostgreSQL database name (e.g., `myapp_db`).

### 7. DB_USER

PostgreSQL username (e.g., `myapp_user`).

### 8. DB_PASSWORD

PostgreSQL password (use the same password from the PostgreSQL setup step).

## How It Works

The deploy workflow will automatically create `local_settings.py` on the server with these credentials.

The CI/CD pipeline will automatically deploy to production when you push to the `main` branch.

## Manual Trigger

You can also manually trigger the deployment workflow from the GitHub Actions tab.

