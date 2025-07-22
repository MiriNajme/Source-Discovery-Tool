import subprocess
from colorama import Fore, Style

def backup_database(host, user, password, database, output_file):
    # Construct the mysqldump command
    command = [
        r'C:\Moodle5.1\server\mysql\bin\mysqldump',
        f'--host={host}',
        f'--user={user}',
        f'--password={password}',
        f'{database}',
        f'--result-file={output_file}'
    ]
    
    # Run the mysqldump command
    print(f'\nRunning {Fore.YELLOW}{Style.BRIGHT}BACKUP{Style.RESET_ALL} command on {database}')
    subprocess.run(command, shell=True)
    print(f'{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n')


def clear_and_restore_database(host, user, password, database, input_file):
    base_command = [
        r'C:\Moodle5.1\server\mysql\bin\mysql',
        f'--host={host}',
        f'--user={user}',
        f'--password={password}',
    ]
    
    # Construct the mysql clear command
    clear_command = [
        '-e',
        f'DROP DATABASE IF EXISTS {database};'
    ]
    
    # Run the mysql clear command
    print(f'\nStart to {Style.BRIGHT}{Fore.RED}CLEARING{Style.RESET_ALL} backup database ({database}).\nIt will take time, please wait!!')
    subprocess.run( base_command + clear_command, shell=True)
    print(f'{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n')

    
    # Construct the mysql create database command
    create_database_command = [
        '-e',
        f'CREATE DATABASE {database};'
    ]
    
    # Run the mysql create database command
    print(f'\n{Style.BRIGHT}{Fore.BLUE}Creating{Style.RESET_ALL} new backup database ({database})')
    subprocess.run( base_command + create_database_command, shell=True)
    print(f'{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n')

    
    # Construct the mysql restore command
    restore_command = [
      f'{database}',
      f'< {input_file}'
    ]

    # Run the mysql restore command
    print(f'\n{Style.BRIGHT}{Fore.MAGENTA}Restoring{Style.RESET_ALL} backup file.\nIt will take time, please wait!!')
    subprocess.run(' '.join(base_command + restore_command), shell=True)
    print(f'{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n')
    
    
    print(f'\n🎉🎉🎉\tMISSION {Style.BRIGHT}{Fore.CYAN}COMPLETED{Style.RESET_ALL} SUCCESSFULLY.\t🎆🎆🎆\n')
   

if __name__ == "__main__":
    # Replace these values with your database configuration
    host = 'localhost'
    user = 'root'
    password = ''
    backup_from_database = 'moodle'
    restore_to_database = 'moodle_backup'
    
    # Specify the output file for the backup
    backup_file = r'C:\My_Docs\Codes\backup.sql'

    # Perform backup
    backup_database(host, user, password, backup_from_database, backup_file)

    # Perform clear and restore
    clear_and_restore_database(host, user, password, restore_to_database, backup_file)
