# 🌿 Organic Farm - Database Configuration Guide

## Professional Database Setup

This guide helps you set up a production-ready PostgreSQL database with secure credentials matching the Organic Farm brand.

### Color Theme Information
The project uses a **Premium Organic Luxury Theme** with the following colors:

```
Primary Colors:
- Deep Forest Green: #123524
- Dark Olive: #2f4f2f
- Olive Green: #4e6b3c

Accent Colors:
- Gold: #c8a96b
- Soft Gold: #d8bf8b

Neutral Colors:
- Beige: #e8dcc3
- Ivory: #f8f5ee
```

---

## Database Setup Instructions

### 1. PostgreSQL Installation

**Windows:**
```powershell
# Download and install PostgreSQL from https://www.postgresql.org/download/windows/
# Or use Chocolatey:
choco install postgresql
```

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

---

### 2. Create Database and User

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE organicfarming_db
    ENCODING 'UTF8'
    OWNER postgres;

-- Create dedicated user (CHANGE PASSWORD!)
CREATE USER organicfarm_user WITH PASSWORD 'OrganicFarm@2024SecurePass!';

-- Grant privileges
ALTER ROLE organicfarm_user SET client_encoding TO 'utf8';
ALTER ROLE organicfarm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE organicfarm_user SET default_transaction_deferrable TO on;
ALTER ROLE organicfarm_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE organicfarming_db TO organicfarm_user;

-- Exit psql
\q
```

---

### 3. Environment Variables Setup

Create a `.env` file in your project root:

```bash
# Database Configuration
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=organicfarming_db
DJANGO_DB_USER=organicfarm_user
DJANGO_DB_PASSWORD=OrganicFarm@2024SecurePass!
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=5432

# Django Security
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

### 4. Windows PowerShell Setup

```powershell
# Set environment variables
$env:DJANGO_DB_ENGINE = "django.db.backends.postgresql"
$env:DJANGO_DB_NAME = "organicfarming_db"
$env:DJANGO_DB_USER = "organicfarm_user"
$env:DJANGO_DB_PASSWORD = "OrganicFarm@2024SecurePass!"
$env:DJANGO_DB_HOST = "localhost"
$env:DJANGO_DB_PORT = "5432"

# Or use .env file with python-dotenv
pip install python-dotenv
```

### 5. Install Required Python Packages

```bash
pip install psycopg2-binary
pip install python-dotenv
pip install django
```

---

### 6. Run Django Migrations

```bash
cd organicfarming

# Create migrations
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

### 7. Verify Database Connection

```bash
# Test connection
python manage.py dbshell

# In psql prompt, verify tables:
\dt
\q
```

---

## Security Best Practices

✅ **DO:**
- Use strong passwords (min 16 characters, mix uppercase, lowercase, numbers, special chars)
- Store `.env` file in `.gitignore`
- Use environment variables for all sensitive data
- Regularly backup your database
- Use SSL/TLS for database connections in production

❌ **DON'T:**
- Hardcode database credentials in settings.py
- Share `.env` files on version control
- Use default PostgreSQL passwords
- Disable SSL in production
- Commit sensitive information to Git

---

## Database Backup

### Backup PostgreSQL Database

```bash
# Backup to file
pg_dump -U organicfarm_user -h localhost organicfarming_db > backup.sql

# Restore from backup
psql -U organicfarm_user -h localhost organicfarming_db < backup.sql
```

---

## Troubleshooting

**Connection Refused:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list              # Mac
```

**Password Authentication Failed:**
- Verify credentials in `.env`
- Check PostgreSQL user exists: `psql -U postgres -c "\du"`

**Role does not exist:**
```sql
CREATE USER organicfarm_user WITH PASSWORD 'your-password';
```

---

## Theme Integration

The database configuration works seamlessly with our premium organic luxury theme:
- Professional green color scheme matches brand identity
- Gold accents for premium feel
- Dark mode support for better accessibility
- Responsive design for all devices

---

## Support & Contact

For database issues or theme customization:
- Email: database@organicfarm.com
- Documentation: See settings.py
- Theme colors: See style.css :root section

Happy farming! 🌿
