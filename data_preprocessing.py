#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import packages
import os
import gzip


# In[ ]:


# function to unzip .txt.gz files
def unzip_gz_files(folder_path):
    # verify folder path exists
    if not os.path.exists(folder_path):
        print(f"ERROR: Folder '{folder_path}' does not exist.")
        return

    # unzip all .txt.gz files in all subdirectories of the specified folder
    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            subdirectory_path = os.path.join(root, directory)

            print(f"UNZIPPING FILES IN SUBDIRECTORY: {subdirectory_path}")

            # loop through all files in the current subdirectory
            for filename in os.listdir(subdirectory_path):
                if filename.endswith(".txt.gz"):
                    file_path = os.path.join(subdirectory_path, filename)
                    output_file_path = os.path.join(subdirectory_path, os.path.splitext(filename)[0])

                    with gzip.open(file_path, 'rt') as gzipped_file, open(output_file_path, 'w') as output_file:
                        output_file.write(gzipped_file.read())

                    print(f"...Unzipped {filename} to {output_file_path}")

    print("All .txt.gz files in all folders unzipped.")


# In[ ]:


data_folder_path = 'C:/Users/emily/BINF_43C9/data/'
unzip_gz_files(data_folder_path)

