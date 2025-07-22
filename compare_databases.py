import mysql.connector			  
from colorama import Fore, Style


def compare_databases(moodle_config, backup_config, diff_config):
    # Connect to the first database
    conn_main = mysql.connector.connect(**moodle_config)
    cursor_main = conn_main.cursor(dictionary=True)

    # Connect to the second database
    conn_backup = mysql.connector.connect(**backup_config)
    cursor_backup = conn_backup.cursor(dictionary=True)

    # Connect to the third database (diff database)
    conn_diff = mysql.connector.connect(**diff_config)
    cursor_diff = conn_diff.cursor(dictionary=True)

    try:
        # Truncate the diff table before starting the comparison
        truncate_query = "TRUNCATE TABLE diff_table;"
        cursor_diff.execute(truncate_query)
        conn_diff.commit()
        
        # Get list of tables for each database
        tablesMain = get_tables(cursor_main, moodle_config['database'])
        tablesBackup = get_tables(cursor_backup, backup_config['database'])

        # Compare tables
        common_tables = set(tablesMain).intersection(tablesBackup)

        print (f'\nSTART {Fore.LIGHTGREEN_EX}COMPARING{Style.RESET_ALL} DATABASES')
        print ('##############################################\n')
                
        is_found = False
        
        for table in common_tables:
            updated_rows, new_rows, deleted_rows = compare_table_data(cursor_main, cursor_backup, table)
            if updated_rows or new_rows or deleted_rows:
                is_found = True
                
                print(f' TABLE: {Fore.LIGHTMAGENTA_EX}{table}{Style.RESET_ALL}')
                
                if updated_rows:
                    print(f'\n {Fore.LIGHTYELLOW_EX}Updated Rows{Style.RESET_ALL}:')
                    
                    for row in updated_rows:
                        print(f"\tROW_ID = {row['row_id']}")
                        save_difference_to_table(cursor_diff, table, row)

                if new_rows:
                    print(f'\n {Fore.LIGHTGREEN_EX}New Rows{Style.RESET_ALL}:')
                    
                    for row in new_rows:
                        print(f"\tROW_ID = {row['row_id']}")
                        save_difference_to_table(cursor_diff, table, row)

                if deleted_rows:
                    print(f'\n {Fore.LIGHTRED_EX}Deleted Rows{Style.RESET_ALL}:')
                    
                    for row in deleted_rows:
                        print(f"\tROW_ID = {row['row_id']}")
                        save_difference_to_table(cursor_diff, table, row)
                
                print ('\n--------------------------------------------------\n')
                
        if not is_found:
            print(f'\n{Fore.LIGHTGREEN_EX}NO DIFFERENCE{Style.RESET_ALL} WAS FOUND! 🎉🎉🎉')
            
    finally:
        # Close connections
        cursor_main.close()
        conn_main.close()
        cursor_backup.close()
        conn_backup.close()
        conn_diff.commit()  # Commit the transaction if successful
        cursor_diff.close()
        conn_diff.close()

def get_tables(cursor, database_name):
    cursor.execute(f"SHOW TABLES FROM {database_name};")
    return [table[f'Tables_in_{database_name}'] for table in cursor.fetchall()]
    
def compare_table_data(cursor_main, cursor_backup, table):
    cursor_main.execute(f"SELECT * FROM {table};")
    dataMain = cursor_main.fetchall()

    cursor_backup.execute(f"SELECT * FROM {table};")
    dataBackup = cursor_backup.fetchall()

    updated_rows = []
    new_rows = []
    deleted_rows = []

    # Compare rows for differences, new rows, and deleted rows
    for row_main in dataMain:
        row_main_id = row_main.get('id', 0)
        matching_row = next((row_backup for row_backup in dataBackup if row_backup.get('id') == row_main_id), None)

        if not matching_row:
            # Row exists in the first database but not in the second (new row)
            new_rows.append({
                'name': table,
                'row_id': row_main_id,
                'action_type': 'INSERTED'
            })
        elif row_main != matching_row:
            # Rows are different
            updated_rows.append({
                'name': table,
                'row_id': row_main_id,
                'action_type': 'UPDATED'
            })

    for row_backup in dataBackup:
        row_backup_id = row_backup.get('id', 0)
        if not any(row_main.get('id') == row_backup_id for row_main in dataMain):
            # Row exists in the second database but not in the first (deleted row)
            deleted_rows.append({
                'name': table,
                'row_id': row_backup_id,
                'action_type': 'DELETED'
            })

    return updated_rows, new_rows, deleted_rows


def save_difference_to_table(cursor_diff, table, difference):
    insert_query = """
    INSERT INTO diff_table (name, row_id,action_type)
    VALUES (%s, %s, %s)
    """

    values = (
        difference['name'],
        str(difference['row_id']),
        difference['action_type']
    )

    try:
        cursor_diff.execute(insert_query, values)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_diff.rollback()  # Rollback the transaction in case of an error
    #else:
    #    conn_diff.commit()  # Commit the transaction if successful
    
    
if __name__ == "__main__":
    # Replace with your database configurations
    moodle_config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'port':'3306',
        'database': 'moodle'
    }

    backup_config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'port':'3306',
        'database': 'moodle_backup'
    }

    diff_config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'port':'3306',
        'database': 'diff_database'
    }

    compare_databases(moodle_config, backup_config, diff_config)
