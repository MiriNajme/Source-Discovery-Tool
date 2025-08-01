# Source Discovery Tool

This repository provides simple scripts to compare two Moodle databases and identify any structural or data differences.  
It is designed for administrators and developers who want to detect changes made to a Moodle database, such as after upgrades, manual edits, or migrations.

---

## Features

- Compare the structure and data between two Moodle databases.
- Generate detailed reports of changed, inserted, and deleted rows.
- Write all detected differences to a dedicated difference database for review.
- Includes batch and Python scripts for automating both backup/restore and comparison.

---

## Getting Started

You will need:
- Your main Moodle database (original, unchanged)
- The backup/restore script will automatically create a backup database (for comparison)
- **You must manually create an empty database** for differences (default name: `diff_database`)

All database credentials are hardcoded in the Python scripts—**edit the `.py` files to match your server and database details.**

---

### Prerequisites

- Python 3.x
- [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/) (`pip install mysql-connector-python`)
- MySQL/MariaDB server access for all databases
- Permission to create databases and tables
- Access to `mysqldump` and `mysql` command-line tools (for backup/restore)
  > **Tip:** If you get a “command not found” error for `mysqldump` or `mysql`, you may need to add your MySQL `bin` directory to your system `PATH`, or edit the script to include the full path to these tools.


---

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/MiriNajme/Moodle_Database_Comparison.git
    cd Moodle_Database_Comparison
    ```

2. Edit the credentials in `compare_databases.py` and `moodle_backup_restore.py` for your server setup.

---

## Usage

### Step 1: Create the Difference Database

Before starting, **create an empty database** (default: `diff_database`) where the differences will be stored.  
You can do this in MySQL with:
```sql
CREATE DATABASE diff_database;
```

### Step 2: Run the Backup/Restore Script

To create a fresh backup of your main Moodle database using mysqldump and restore this backup automatically as a new backup database for comparison run:

```bash
python moodle_backup_restore.py
```
or the batch file `moodle_backup_restore`.

### Step 3: Make a Change
Make the change you want to track in your main Moodle database.

### Step 4: Run the Comparison Script

To compare your main and backup Moodle databases, run
```bash
python compare_databases.py
```
or the batch file `compare_databases.py`.

## Disclaimer

This tool is provided **as-is**, with no warranty or guarantee of correctness.

**Always back up your data before running any database operation.**


