
import os
import hashlib
from collections import defaultdict

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(folder_path):
    files_by_hash = defaultdict(list)

    for root, directories, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            try:
                file_hash = calculate_hash(file_path)
                files_by_hash[file_hash].append(file_path)

            except (PermissionError, OSError) as error:
                print("Skipped:", file_path, "-", error)

    duplicates_found = False

    print("\n===== DUPLICATE FILE REPORT =====")

    for file_hash, file_paths in files_by_hash.items():
        if len(file_paths) > 1:
            duplicates_found = True

            print("\nDuplicate Group:")

            for path in file_paths:
                print(path)

    if not duplicates_found:
        print("No duplicate files found!")


folder = input("Enter folder path to scan: ").strip()

if os.path.isdir(folder):
    find_duplicates(folder)
else:
    print("Invalid folder path!")


