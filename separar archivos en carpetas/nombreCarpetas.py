import os
class ver_carpetas:
    
    def list_folders(self,directory):
        if not os.path.exists(directory):
            print("Directory does not exist.")
            return

        folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
        return folders

    # Replace 'path_to_directory' with the path of the directory you want to inspect
    def ver_carpetas(self,directory_path):

        folder_names = self.list_folders(directory_path)
        if folder_names:
            print("Folders inside the directory:")
            for folder in folder_names:
                print(folder)
                return folder
        else:
            print("No folders found.")
            return False