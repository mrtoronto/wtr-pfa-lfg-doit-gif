# Common Operations

## Managing the Production Service

### View logs

```bash
sudo journalctl -u myapp -f
```

### Restart service

```bash
sudo systemctl restart myapp
```

### Stop service

```bash
sudo systemctl stop myapp
```

### Start service

```bash
sudo systemctl start myapp
```

### Check status

```bash
sudo systemctl status myapp
```

## Nginx Operations

### Test configuration

```bash
sudo nginx -t
```

### Reload nginx (no downtime)

```bash
sudo systemctl reload nginx
```

### Restart nginx

```bash
sudo systemctl restart nginx
```

### View logs

```bash
# Error log
sudo tail -f /var/log/nginx/myapp_error.log

# Access log
sudo tail -f /var/log/nginx/myapp_access.log
```

## Manual Deployment

If you need to deploy changes manually without GitHub Actions:

```bash
# SSH to your server (replace with your username and IP)
ssh youruser@YOUR_SERVER_IP

cd pfa
git pull
uv sync
uv run sh migrate_db.sh
sudo systemctl restart myapp
```

## Database Operations

### Run migrations

```bash
cd ~/pfa
uv run sh migrate_db.sh
```

### Connect to PostgreSQL

```bash
psql -U myapp_user -d myapp_db
```

### Backup database

```bash
pg_dump -U myapp_user -d myapp_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore database

```bash
psql -U myapp_user -d myapp_db < backup_20241004_120000.sql
```

