# 🗄️ Database Setup Guide - Driftwood Cafe
## How to Connect Python Models to PostgreSQL and View in pgAdmin 4

This guide shows you how to take Python SQLAlchemy models (`.py` files) and create actual database tables in PostgreSQL that you can see in pgAdmin 4.

---

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ Python 3.8+ installed
- ✅ PostgreSQL 12+ installed and running
- ✅ pgAdmin 4 installed
- ✅ Your database credentials ready

---

## 🚀 Step-by-Step Setup Process

### **Step 1: Configure Database Connection**

1. **Navigate to the server directory:**
   ```bash
   cd server
   ```

2. **Update your `.env` file with PostgreSQL credentials:**
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```

   **Example:**
   ```env
   DATABASE_URL=postgresql://postgres:ochiengmose@localhost:5432/driftwood_cafe
   ```

   **Format Breakdown:**
   - `postgresql://` - Database type
   - `username` - Your PostgreSQL username (usually `postgres`)
   - `password` - Your PostgreSQL password
   - `localhost` - Database host (use `localhost` for local development)
   - `5432` - PostgreSQL port (default is 5432)
   - `database_name` - Name of your database

---

### **Step 2: Verify Your Models Are Imported**

Check that all your models are imported in `app.py`:

```python
# In app.py
from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order
from models.order_item import OrderItem
from models.review import Review
from models.payment import Payment
```

**Why?** Flask-Migrate needs to see all models to generate migrations.

---

### **Step 3: Create Database Migrations**

Migrations are like version control for your database schema. They convert your Python models into SQL commands.

1. **Initialize migrations (only needed once):**
   ```bash
   flask db init
   ```
   
   ✅ **Skip this if** you already have a `migrations/` folder.

2. **Generate migration from your models:**
   ```bash
   flask db migrate -m "Initial migration with all models"
   ```
   
   **What this does:**
   - Scans all your Python model files
   - Detects tables, columns, and relationships
   - Creates a migration file in `migrations/versions/`
   
   **Expected output:**
   ```
   INFO  [alembic.autogenerate.compare.tables] Detected added table 'users'
   INFO  [alembic.autogenerate.compare.tables] Detected added table 'categories'
   INFO  [alembic.autogenerate.compare.tables] Detected added table 'products'
   INFO  [alembic.autogenerate.compare.tables] Detected added table 'orders'
   INFO  [alembic.autogenerate.compare.tables] Detected added table 'order_items'
   INFO  [alembic.autogenerate.compare.tables] Detected added table 'payments'
   INFO  [alembic.autogenerate.compare.tables] Detected added table 'reviews'
   ```

---

### **Step 4: Apply Migrations to PostgreSQL**

Now create the actual tables in your database:

```bash
flask db upgrade
```

**What this does:**
- Executes the migration file
- Creates all tables in PostgreSQL
- Sets up foreign keys and constraints
- Creates indexes

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> c7666ddfee21, Initial migration with all models
```

---

### **Step 5: Verify Tables in PostgreSQL (Command Line)**

Check that tables were created:

```bash
PGPASSWORD=your_password psql -U postgres -h localhost -d driftwood_cafe -c "\dt"
```

**Expected output:**
```
              List of relations
 Schema |      Name       | Type  |  Owner   
--------+-----------------+-------+----------
 public | users           | table | postgres
 public | categories      | table | postgres
 public | products        | table | postgres
 public | orders          | table | postgres
 public | order_items     | table | postgres
 public | payments        | table | postgres
 public | reviews         | table | postgres
 public | menu_items      | table | postgres
 public | alembic_version | table | postgres
```

---

### **Step 6: View Tables in pgAdmin 4**

1. **Open pgAdmin 4**

2. **Connect to your PostgreSQL server:**
   - Expand "Servers" in the left sidebar
   - Click on your server (e.g., "PostgreSQL 12")
   - Enter your password if prompted

3. **Navigate to your database:**
   ```
   Servers → PostgreSQL → Databases → driftwood_cafe
   ```

4. **Expand the database structure:**
   ```
   driftwood_cafe → Schemas (1) → public → Tables
   ```

5. **Refresh the Tables folder:**
   - Right-click on "Tables"
   - Select "Refresh"
   - Click the arrow to expand

6. **You should now see all your tables:**
   - alembic_version
   - categories
   - menu_items
   - order_items
   - orders
   - payments
   - products
   - reviews
   - users

7. **Explore a table:**
   - Click on any table (e.g., `users`)
   - Right-click → "View/Edit Data" → "All Rows"
   - You can see columns, data types, and constraints

---

## 🔄 Common Workflows

### **Adding a New Model**

When you create a new model file:

1. **Create the model file** (e.g., `models/new_model.py`)
2. **Import it in `app.py`:**
   ```python
   from models.new_model import NewModel
   ```
3. **Generate migration:**
   ```bash
   flask db migrate -m "Add new_model table"
   ```
4. **Apply migration:**
   ```bash
   flask db upgrade
   ```
5. **Refresh pgAdmin 4** to see the new table

---

### **Modifying an Existing Model**

When you change a model (add/remove columns):

1. **Edit the model file** (e.g., add a new column)
2. **Generate migration:**
   ```bash
   flask db migrate -m "Add new column to users"
   ```
3. **Review the migration file** in `migrations/versions/`
4. **Apply migration:**
   ```bash
   flask db upgrade
   ```
5. **Refresh pgAdmin 4** to see the changes

---

### **Rolling Back a Migration**

If something goes wrong:

```bash
# Go back one migration
flask db downgrade

# Go back to a specific migration
flask db downgrade <revision_id>
```

---

## 🐛 Troubleshooting

### **Problem: "password authentication failed"**

**Solution:** Check your `.env` file credentials:
```env
DATABASE_URL=postgresql://correct_username:correct_password@localhost:5432/driftwood_cafe
```

---

### **Problem: "database does not exist"**

**Solution:** Create the database first:
```bash
PGPASSWORD=your_password psql -U postgres -h localhost -c "CREATE DATABASE driftwood_cafe;"
```

---

### **Problem: Tables don't appear in pgAdmin 4**

**Solution:**
1. Right-click on "Tables" → "Refresh"
2. Right-click on "driftwood_cafe" database → "Refresh"
3. Disconnect and reconnect to the server
4. Verify tables exist via command line:
   ```bash
   PGPASSWORD=your_password psql -U postgres -h localhost -d driftwood_cafe -c "\dt"
   ```

---

### **Problem: "Target database is not up to date"**

**Solution:** Apply pending migrations:
```bash
flask db upgrade
```

---

### **Problem: Migration detects no changes**

**Solution:**
1. Verify model is imported in `app.py`
2. Check that you saved the model file
3. Restart your Flask app
4. Try again:
   ```bash
   flask db migrate -m "Your message"
   ```

---

## 📊 Understanding the Model → Table Flow

```
┌─────────────────────────┐
│  Python Model (.py)     │
│  models/user.py         │
│                         │
│  class User(db.Model):  │
│    id = db.Column(...)  │
│    name = db.Column(...)│
└───────────┬─────────────┘
            │
            │ flask db migrate
            ▼
┌─────────────────────────┐
│  Migration File         │
│  migrations/versions/   │
│  xxx_initial.py         │
│                         │
│  def upgrade():         │
│    op.create_table(...) │
└───────────┬─────────────┘
            │
            │ flask db upgrade
            ▼
┌─────────────────────────┐
│  PostgreSQL Table       │
│  (visible in pgAdmin)   │
│                         │
│  CREATE TABLE users (   │
│    id SERIAL PRIMARY... │
│    name VARCHAR(80)...  │
└─────────────────────────┘
```

---

## ✅ Quick Reference Commands

```bash
# Check database connection
flask db current

# See migration history
flask db history

# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback one migration
flask db downgrade

# Check tables in PostgreSQL
PGPASSWORD=password psql -U postgres -d driftwood_cafe -c "\dt"

# Check table structure
PGPASSWORD=password psql -U postgres -d driftwood_cafe -c "\d users"
```

---

## 🎯 Summary

**The Process:**
1. ✅ Configure `DATABASE_URL` in `.env`
2. ✅ Import all models in `app.py`
3. ✅ Run `flask db migrate` to generate migration
4. ✅ Run `flask db upgrade` to create tables
5. ✅ Refresh pgAdmin 4 to see tables

**Key Files:**
- `.env` - Database credentials
- `app.py` - Model imports
- `models/*.py` - Your table definitions
- `migrations/versions/` - Migration files

**Remember:** Every time you change a model, you need to create and apply a new migration!

---

## 📞 Need Help?

If you encounter issues:
1. Check the error message carefully
2. Verify your database credentials
3. Ensure PostgreSQL is running
4. Check that all models are imported in `app.py`
5. Review the migration file in `migrations/versions/`

Happy coding! 🚀
