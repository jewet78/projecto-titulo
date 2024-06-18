import os
import shutil
import random
import glob

# Search for files ending with '.fastq.gz'
fastq_files = glob.glob('*.fastq')  # This pattern assumes the files are in subdirectories, adjust it as needed
print(fastq_files)
file_groups = {}
for file in fastq_files:
    file_name = file.split('/')[-1]  # Extract the file name
    prefix = file_name.split('_')[0]  # Extract the prefix before the first underscore
    if prefix in file_groups:
        file_groups[prefix].append(file)
    else:
        file_groups[prefix] = [file]

print(file_groups)


# Function to copy files to a folder
def copy_files_to_folder(files, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for file in files:
        shutil.copy(file, folder_path)

# Assuming file_groups is the dictionary containing the file groups
# Adjust the paths and numbers as per your requirements
print("b")

total_folders = 300
min_pairs_per_folder = 1
max_pairs_per_folder = 1

min_files_per_folder = min_pairs_per_folder * 2
max_files_per_folder = max_pairs_per_folder * 2

files_to_copy = [file_group for file_group in file_groups.values() if len(file_group) >= 2]
random.shuffle(files_to_copy)

folders_created = 0
print("c")
while folders_created < total_folders:
    selected_files = []
    while len(selected_files) < min_files_per_folder and files_to_copy:
        num_files = min(random.randint(2, len(files_to_copy[0])), max_files_per_folder - len(selected_files))
        selected_files.extend(files_to_copy.pop(0)[:num_files])

    if len(selected_files) < min_files_per_folder:
        files_to_copy = [file_group for file_group in file_groups.values() if len(file_group) >= 2]
        random.shuffle(files_to_copy)
    else:
        folder_name = f"Folder_{folders_created + 1}"
        folder_path = os.path.join("sets3", folder_name)  # Change 'path_to_destination_folder' to your destination folder
        copy_files_to_folder(selected_files, folder_path)
        folders_created += 1
        print(f"new folder created {folder_name}")

print(f"{folders_created} folders created.")
