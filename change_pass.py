import os
import shutil
import argparse
import time

def backup_and_update_credentials_in_directory(directory, comment, new_username, new_password):
    # Walk through all directories and subdirectories
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name == 'dbsettings.properties':
                file_path = os.path.join(root, file_name)
                # Add timestamp to the bak file
                t = time.localtime()
                timestamp = time.strftime('%m-%d-%Y_%H%M', t)
                backup_file_path = f'{file_path}-{timestamp}.bak'
                # Create a backup of the original file
                shutil.copyfile(file_path, backup_file_path)
                # Update credentials in the original file
                update_credentials(file_path, comment, new_username, new_password)

def update_credentials(file_path, comment, new_username, new_password):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the username and password if the commented line is found
    updated = False
    should_update = False
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() == f'//{comment}':
                should_update = True
                file.write(line)
            elif should_update and '=' in line:
                key, value = line.strip().split('=')
                if key.strip().endswith('user'):
                    file.write(f'{key}={new_username}\n')
                    updated = True
                elif key.strip().endswith('password'):
                    file.write(f'{key}={new_password}\n')
                    updated = True
                else:
                    file.write(line)
                # Stop updating after the first update
                if updated:
                    should_update = False
            else:
                file.write(line)

    if updated:
        print(f"Updated '{file_path}': Username and/or password updated successfully.")
    else:
        print(f"Skipped '{file_path}': Commented line '//{comment}' not found or no updates needed.")

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Update username and password in all dbsettings.properties files.')
    parser.add_argument('directory', type=str, help='Root directory path where settings.properties files are located.')
    parser.add_argument('comment', type=str, help='Comment to look for in the settings.properties files.')
    parser.add_argument('new_username', type=str, help='New username to update to.')
    parser.add_argument('new_password', type=str, help='New password to update to.')
    args = parser.parse_args()

    # Call function to update credentials
    backup_and_update_credentials_in_directory(args.directory, args.comment, args.new_username, args.new_password)

