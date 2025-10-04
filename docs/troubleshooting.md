# Troubleshooting Guide

## Application Won't Start

### Check logs

```bash
sudo journalctl -u myapp -n 50 --no-pager
```

### Verify socket file exists

```bash
ls -la ~/pfa/*.sock
```

### Check gunicorn processes

```bash
ps aux | grep gunicorn
```

## Database Connection Errors

### Check PostgreSQL is running

```bash
sudo systemctl status postgresql
```

### Test connection

```bash
psql -U myapp_user -d myapp_db
```

### Common issues

- Wrong credentials in `local_settings.py`
- Database doesn't exist
- PostgreSQL service not running
- Firewall blocking connection

## Nginx 502 Bad Gateway

This usually means nginx can't connect to your application.

### Check if app socket exists

```bash
ls -la /home/youruser/pfa/*.sock
```

### Check app is running

```bash
sudo systemctl status myapp
```

### Check nginx error logs

```bash
sudo tail -f /var/log/nginx/myapp_error.log
```

### Common fix: Check socket permissions

```bash
sudo -u www-data test -r /home/youruser/pfa/myapp.sock && echo "✓ OK" || echo "✗ Fix with: chmod 755 /home/youruser"
```

If you see "✗", fix the permissions:

```bash
chmod 755 /home/youruser
sudo systemctl restart myapp
```

## App Crashes on Startup

### View detailed logs

```bash
sudo journalctl -u myapp -n 100 --no-pager
```

### Common issues

1. **Missing DATABASE_URL**: Check `local_settings.py` exists and has `DATABASE_URL`
2. **Wrong user in service file**: Verify `User=` matches your actual username in `/etc/systemd/system/myapp.service`
3. **Database not created**: Make sure PostgreSQL database and user exist
4. **Missing dependencies**: Run `uv sync` in the app directory

## Port Already in Use

If you see an error like "Address already in use":

```bash
# Find what's using the port (e.g., 4200)
sudo lsof -i :4200

# Kill the process
sudo kill <PID>

# Or restart the service
sudo systemctl restart myapp
```

## Migration Errors

### Reset migrations (development only)

**WARNING**: This will delete your database!

```bash
# Delete database
rm dev.db

# Delete migrations
rm -rf migrations/

# Re-initialize
uv run sh migrate_db.sh
```

### Production migration issues

If migrations fail in production:

```bash
# Check migration status
cd ~/pfa
uv run flask db current

# Try running migrations manually
uv run flask db upgrade

# View migration history
uv run flask db history
```

## GitHub Actions Deployment Fails

### Check secrets are set correctly

Go to GitHub → Settings → Secrets and variables → Actions

Verify all 8 secrets are present:
- `SSH_PRIVATE_KEY`
- `SERVER_HOST`
- `SERVER_USERNAME`
- `SUDO_PASSWORD`
- `SECRET_KEY`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

### Check workflow logs

Go to GitHub → Actions tab → Click on the failed workflow run → Review logs

### Common issues

- Wrong server IP or hostname
- SSH key doesn't match
- Server user doesn't have sudo privileges
- Database credentials incorrect

## Still Having Issues?

If you're still stuck:

1. Check all logs: `sudo journalctl -u myapp -f`
2. Verify all configuration files are correct
3. Ensure all dependencies are installed
4. Check file permissions
5. Review the production setup guide step-by-step

