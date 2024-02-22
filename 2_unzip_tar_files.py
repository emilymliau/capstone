# import packages
import os
import tarfile

# function to unzip .tar.gz files
def unzip_tar_files(folder_path):
    # verify folder path exists
    if not os.path.exists(folder_path):
        print(f"ERROR: Folder '{folder_path}' does not exist.")
        return
    
    # list all files in the specified directory
    files = os.listdir(folder_path)

    # select files with ".tar.gz" extension
    tar_files = [file for file in files if file.endswith(".tar.gz")]

    # unzip all .tar.gz files in the specified folder
    for tar_file in tar_files:
        tar_file_path = os.path.join(folder_path, tar_file)
        output_folder = os.path.join(folder_path, os.path.splitext(tar_file)[0])

        # create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok = True)

        with tarfile.open(tar_file_path, 'r:gz') as tar:
            tar.extractall(output_folder)

        print(f"...Unzipped {tar_file} to {output_folder}")
        
    print("All .tar.gz files in 23andMe data folder unzipped.")

data_folder_path = 'C:/Users/emily/BINF_43C9/data/23andMe/'
unzip_tar_files(data_folder_path)