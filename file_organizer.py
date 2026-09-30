import os
import shutil

def organize_files(target_directory):
    # Dictionary mapping extensions to folder names
    extensions_map = {
        '.pdf': 'Documents_PDF',
        '.docx': 'Documents_Word',
        '.doc': 'Documents_Word',
        '.png': 'Images',
        '.jpg': 'Images',
        '.jpeg': 'Images',
        '.m': 'MATLAB_Scripts',
        '.py': 'Python_Scripts',
        '.txt': 'Text_Files'
    }
    
    if not os.path.exists(target_directory):
        print(f"Error: Directory {target_directory} does not exist.")
        return

    # Loop through files in the directory
    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)
        
        # Skip directories, only look at files
        if os.path.isdir(file_path):
            continue
            
        _, ext = os.path.splitext(filename)
        
        if ext.lower() in extensions_map:
            folder_name = extensions_map[ext.lower()]
            folder_path = os.path.join(target_directory, folder_name)
            
            # Create folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            # Move file into the folder
            shutil.move(file_path, os.path.join(folder_path, filename))
            print(f"Moved: {filename} -> {folder_name}/")
        else:
            print(f"Skipped (unknown extension): {filename}")

if __name__ == "__main__":
    target = input("Enter the path of the folder to organize: ")
    organize_files(target)
    print("Organization complete!")
