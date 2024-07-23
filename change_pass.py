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
                # Update credentials in original file
                update_credentials(file_path, comment, new_username, new_password)

""" def update_credentials(file_path, comment, new_username, new_password):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the username and password if the commented line is found
    updated = False
    with open(file_path, 'w') as file:
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip() == f'//{comment}':
                # Skip current line
                file.write(line)
                i += 1
                # Update the next two lines assuming they need to be updated
                if i < len(lines):
                    key, value = lines[i].strip().split('=')
                    # If current_username is same as new_username 
                    if value == {new_username}:
                        break
                    # Else update the username
                    else:
                        file.write(f'{key}={new_username}\n')
                        updated = True
                if i + 1 < len(lines):
                    key, value = lines[i + 1].strip().split('=')
                    file.write(f'{key}={new_password}\n')
                    updated = True
                i += 2  # Move to the line after the updated lines
            else:
                file.write(line)
                i += 1

    if updated:
        print(f"Updated '{file_path}': Username and password updated successfully to '{new_username}' and '{new_password}'.")
    else:
        print(f"Skipped '{file_path}': Commented line '//{comment}' not found.")"""

def update_credentials(file_path, comment, new_username, new_password):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the username and password if the commented line is found
    updated = False
    with open(file_path, 'w') as file:
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip() == f'//{comment}':
                # Skip current line
                file.write(line)
                i += 1
                # Update the lines for username and password
                user_updated = False
                password_updated = False
                while i < len(lines):
                    parts = lines[i].strip().split('=')
                    if len(parts) >= 2:
                        key, value = parts[0], '='.join(parts[1:])
                        if key.endswith('.db.user'):
                            if not user_updated:
                                if value.strip() != new_username:
                                    file.write(f'{key}={new_username}\n')
                                    updated = True
                                    user_updated = True
                                else:
                                    file.write(lines[i])
                        elif key.endswith('.db.password'):
                            if not password_updated:
                                file.write(f'{key}={new_password}\n')
                                updated = True
                                password_updated = True
                            else:
                                file.write(lines[i])
                        else:
                            file.write(lines[i])
                    else:
                        file.write(lines[i])
                    i += 1
                break
            else:
                file.write(line)
                i += 1

    if updated:
        print(f"Updated '{file_path}': Username and password updated successfully to '{new_username}' and '{new_password}'.")
    else:
        print(f"Skipped '{file_path}': Commented line '//{comment}' not found.")



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

