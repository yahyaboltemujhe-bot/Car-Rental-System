# Deploying Car Rental System to Render.com

## 🚀 Complete Deployment Guide

This guide walks you through deploying your Flask Car Rental System to **Render.com** for free hosting.

---

## 📋 Prerequisites

- GitHub account (to host your code)
- Render.com account (free tier available)
- Project ready with all dependencies

---

## 🛠️ Tech Stack

- **Backend**: Python Flask 3.0.0
- **Frontend**: HTML, CSS, JavaScript (Jinja2 templates)
- **Database**: SQLite (development) → PostgreSQL (production)
- **Architecture**: Layered + 6 GOF Design Patterns
- **Hosting**: Render.com (Free Tier)

---

## 📝 Step 1: Prepare Your Project

### 1.1 Create Production Requirements File

Create/update `requirements.txt`:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-CORS==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

**New additions for production:**
- `gunicorn`: Production WSGI server
- `psycopg2-binary`: PostgreSQL adapter
- `python-dotenv`: Environment variable management

### 1.2 Create `render.yaml` (Optional but Recommended)

Create a file named `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: car-rental-system
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: car-rental-db
          property: connectionString

databases:
  - name: car-rental-db
    databaseName: car_rental
    user: car_rental_user
```

### 1.3 Update `config.py` for Production

Update your `config.py` to support both SQLite (dev) and PostgreSQL (production):

```python
import os
from datetime import timedelta

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # Use PostgreSQL on Render, SQLite locally
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        # Render provides postgres:// but SQLAlchemy needs postgresql://
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///database/car_rental.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Flask configuration
    DEBUG = os.environ.get('FLASK_ENV') != 'production'
```

### 1.4 Update `run.py` for Production

Update your `run.py`:

```python
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Development server (local testing)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
```

For production, Render will use: `gunicorn run:app`

### 1.5 Create `.gitignore`

Ensure you have a `.gitignore` file:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

## 📤 Step 2: Push to GitHub

### 2.1 Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit - Car Rental System with GOF patterns"
```

### 2.2 Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click "New Repository"
3. Name: `car-rental-system`
4. Description: "Car Rental & Fleet Management System with 6 GOF Design Patterns"
5. Make it **Public** (for free Render deployment)
6. Click "Create Repository"

### 2.3 Push Code to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/car-rental-system.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 3: Deploy to Render.com

### 3.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended for easy integration)

### 3.2 Create PostgreSQL Database

1. In Render Dashboard, click "New +"
2. Select "PostgreSQL"
3. Fill in details:
   - **Name**: `car-rental-db`
   - **Database**: `car_rental`
   - **User**: `car_rental_user`
   - **Region**: Choose closest to you
   - **Plan**: Free (or paid for better performance)
4. Click "Create Database"
5. **Important**: Copy the **Internal Database URL** (will be used in web service)

### 3.3 Create Web Service

1. In Render Dashboard, click "New +"
2. Select "Web Service"
3. Click "Connect a repository" → Select your GitHub repo
4. Fill in details:

   **Basic Settings:**
   - **Name**: `car-rental-system`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`

   **Build & Deploy:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`

   **Plan:**
   - Select "Free" (or paid for better performance)

5. Click "Advanced" to add environment variables

### 3.4 Add Environment Variables

Add these environment variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | (Generate random: `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL` | (Paste Internal Database URL from Step 3.2) |

**To generate a secure SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste as SECRET_KEY value.

6. Click "Create Web Service"

### 3.5 Wait for Deployment

- Render will now:
  1. Clone your repository
  2. Install dependencies from `requirements.txt`
  3. Start your app with `gunicorn`
  4. Assign a public URL

- Initial deployment takes 2-5 minutes
- Watch the build logs in real-time

---

## ✅ Step 4: Initialize Production Database

### 4.1 Access Render Shell

1. In your web service dashboard, click "Shell" tab
2. A terminal will open in your deployed app

### 4.2 Initialize Database Schema

Run these commands in the Render shell:

```bash
# Start Python shell
python

# Run database initialization
from app import create_app, db
from app.domain.car import Car
from app.domain.booking import Booking

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created!")
```

Or create a script `init_db.py`:

```python
from app import create_app, db

def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_database()
```

Then run in Render shell:

```bash
python init_db.py
```

### 4.3 Create Admin User

Create `create_admin.py`:

```python
from app import create_app, db
from app.domain.admin import Admin  # Adjust import based on your structure

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Check if admin exists
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin', email='admin@carrental.com')
            admin.set_password('admin123')  # Change this password!
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: admin / admin123")
        else:
            print("ℹ️ Admin user already exists")

if __name__ == "__main__":
    create_admin_user()
```

Run in Render shell:

```bash
python create_admin.py
```

---

## 🎉 Step 5: Access Your Live App

Your app is now live! Access it at:

```
https://car-rental-system.onrender.com
```

(Replace with your actual Render URL)

### Test the Deployment:

1. **Visit homepage**: Should show login page
2. **Login**: Use credentials created in Step 4.3
3. **Navigate pages**: Dashboard, Add Car, Fleet, Tracking, Claims, Keyless
4. **Test patterns**: All GOF patterns should work
5. **Mobile test**: Open on your phone browser

---

## 🔧 Step 6: Custom Domain (Optional)

### 6.1 Add Custom Domain

1. In Render dashboard → Your web service → Settings
2. Scroll to "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain (e.g., `carrental.yourdomain.com`)
5. Follow DNS instructions to add CNAME record

### 6.2 SSL Certificate

Render provides **free SSL certificates** automatically for custom domains!

---

## 🐛 Troubleshooting

### Issue 1: Build Fails

**Error**: `Could not find a version that satisfies the requirement...`

**Solution**: Check Python version compatibility
- Render uses Python 3.7+ by default
- Specify version in `runtime.txt`:
  ```
  python-3.11.0
  ```

### Issue 2: Database Connection Error

**Error**: `could not connect to server`

**Solution**: 
- Verify `DATABASE_URL` environment variable is set
- Check database is in same region as web service
- Use **Internal Database URL** (not External)

### Issue 3: App Crashes on Start

**Error**: `Application failed to respond`

**Solution**:
- Check build logs for errors
- Verify `gunicorn run:app` is correct
- Ensure `run.py` has `app = create_app()` at module level

### Issue 4: Static Files Not Loading

**Error**: CSS/JS not loading

**Solution**:
- Check `url_for('static', ...)` paths in templates
- Verify static folder structure
- Render serves static files automatically

### Issue 5: Free Tier Spins Down

**Issue**: App becomes slow after inactivity

**Solution**:
- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Upgrade to paid plan for 24/7 uptime

---

## 📊 Monitoring & Logs

### View Logs

1. Render Dashboard → Your web service → Logs
2. Real-time logs of all requests and errors
3. Filter by time period

### Performance Metrics

1. Render Dashboard → Your web service → Metrics
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🔄 Updating Your Deployment

### Auto-Deploy from GitHub

Render automatically deploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Updated feature X"
git push origin main
```

Render will:
1. Detect the push
2. Rebuild your app
3. Deploy new version (zero downtime on paid plans)

### Manual Deploy

1. Render Dashboard → Your web service
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 💰 Pricing

### Free Tier Includes:
- ✅ 750 hours/month web service runtime
- ✅ 1GB RAM
- ✅ Automatic HTTPS
- ✅ Custom domains
- ❌ Spins down after 15 min inactivity
- ❌ Limited database storage (1GB PostgreSQL)

### Paid Plans (Starting $7/month):
- ✅ Always-on (no spin down)
- ✅ More RAM/CPU
- ✅ Zero-downtime deploys
- ✅ Larger database

---

## 🎓 FYP Presentation Tips

### Show Live Demo:

1. **Share Live URL**: 
   ```
   https://car-rental-system.onrender.com
   ```

2. **Highlight Features**:
   - "Hosted on Render.com cloud platform"
   - "Production-ready with PostgreSQL database"
   - "Automatic HTTPS encryption"
   - "Accessible from anywhere in the world"

3. **Show Deployment Process**:
   - GitHub integration
   - Automatic deployments
   - Build logs
   - Environment configuration

4. **Mobile Demo**:
   - Open on phone browser
   - Show responsive design
   - Professional mobile experience

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **PostgreSQL Migration**: https://render.com/docs/databases

---

## ✨ Deployment Checklist

- [ ] Updated `requirements.txt` with production dependencies
- [ ] Added `gunicorn` to requirements
- [ ] Updated `config.py` for PostgreSQL support
- [ ] Created `.gitignore` file
- [ ] Pushed code to GitHub
- [ ] Created Render account
- [ ] Created PostgreSQL database on Render
- [ ] Created web service on Render
- [ ] Added environment variables (FLASK_ENV, SECRET_KEY, DATABASE_URL)
- [ ] Initialized database schema
- [ ] Created admin user
- [ ] Tested live deployment
- [ ] Verified all pages work
- [ ] Tested mobile responsiveness
- [ ] Checked all GOF patterns functionality

---

## 🎉 Congratulations!

Your Car Rental System is now **live and accessible worldwide**! 🌍

Perfect for:
- ✅ FYP demonstrations
- ✅ Portfolio showcase
- ✅ Recruiter reviews
- ✅ Mobile testing
- ✅ Real-world usage

**Live URL**: `https://car-rental-system.onrender.com`

Share it proudly! 🚀✨
