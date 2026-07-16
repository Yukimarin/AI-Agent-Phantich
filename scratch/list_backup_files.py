import os

backup_dir = r"C:\Users\DELL\Desktop\Backup\PTIT"
if os.path.exists(backup_dir):
    print("Files in Backup/PTIT:")
    for f in os.listdir(backup_dir):
        print(f"  {f}")
else:
    print(f"Directory {backup_dir} does not exist.")

parent_dir = r"C:\Users\DELL\Desktop\Backup"
if os.path.exists(parent_dir):
    print("\nFiles in Backup:")
    for f in os.listdir(parent_dir):
        print(f"  {f}")
