# Hostinger Deployment Guide

## Prerequisites
- SSH access to Hostinger
- Python 3.8+ installed on the server
- Hostinger account with Django support

## Deployment Steps

### 1. Connect via SSH
```bash
ssh your_hostinger_username@your_hostinger_domain.com
```

### 2. Clone/Upload Your Project
```bash
cd public_html  # or your project directory
# Either clone from git or upload files
git clone your-repo-url browcher-backend
cd browcher-backend
```

### 3. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Create Environment File
```bash
cp .env.example .env
# Edit .env with your production settings
nano .env
```

**Important settings to update in .env:**
- `DEBUG=False`
- `SECRET_KEY=generate-a-strong-secret-key`
- `ALLOWED_HOSTS=your-domain.com,www.your-domain.com`

### 6. Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and paste it in your `.env` file as `SECRET_KEY`

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run Database Migrations
```bash
python manage.py migrate
```

### 9. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 10. Configure Web Server
**Option A: Using Gunicorn (Recommended)**

Create a systemd service file `/etc/systemd/system/browcher.service`:
```ini
[Unit]
Description=Browcher Django Application
After=network.target

[Service]
Type=notify
User=your_user
WorkingDirectory=/path/to/browcher-backend
ExecStart=/path/to/browcher-backend/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/path/to/browcher-backend/gunicorn.sock \
    --access-logfile - \
    --error-logfile - \
    backend.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start browcher
sudo systemctl enable browcher
```

**Option B: Using Hostinger's Built-in WSGI**

1. In Hostinger control panel, go to "Python"
2. Create a new Python application
3. Set the entry point to `backend/wsgi.py`

### 11. Configure Nginx/Apache Reverse Proxy

**Nginx configuration example:**
```nginx
server {
    server_name browcherBackend.amplinova.com;
    
    location / {
        proxy_pass http://unix:/path/to/browcher-backend/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/browcher-backend/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/browcher-backend/media/;
    }
}
```

### 12. SSL Certificate (HTTPS)
Use Let's Encrypt (usually available in Hostinger):
```bash
sudo certbot --nginx -d browcherBackend.amplinova.com
```

## Post-Deployment Checklist

- [ ] DEBUG = False in production
- [ ] SECRET_KEY is strong and unique
- [ ] ALLOWED_HOSTS configured correctly
- [ ] HTTPS enabled (SSL certificate installed)
- [ ] Static files collected and served
- [ ] Media files accessible
- [ ] Database migrations applied
- [ ] CORS settings configured for your frontend
- [ ] Error logging enabled
- [ ] Regular backups scheduled

## Troubleshooting

**Check Gunicorn status:**
```bash
sudo systemctl status browcher
sudo journalctl -u browcher -n 50
```

**Check Nginx logs:**
```bash
sudo tail -f /var/log/nginx/error.log
```

**Collect static files again:**
```bash
python manage.py collectstatic --clear --noinput
```

**Test configuration:**
```bash
python manage.py check --deploy
```

## Database Upgrade (Optional)

For production, consider upgrading from SQLite to PostgreSQL:

```bash
pip install psycopg2-binary
```

Update `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=browcher_db
DB_USER=browcher_user
DB_PASSWORD=secure_password
DB_HOST=your_db_host
DB_PORT=5432
```

Update `settings.py` to use environment variables for database config.

## Support

For Hostinger-specific issues, contact their support team.
