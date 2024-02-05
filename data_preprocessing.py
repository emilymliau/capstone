from google.colab import drive
import os
import gzip
import pandas as pd
import tarfile

# mount google drive
def mount_google_drive(my_folder):
  root = '/content/drive'
  drive.mount(root, force_remount = True)
  dest_folder = root + '/My Drive' + my_folder
  os.chdir(dest_folder)

  curr_path = os.getcwd()
  if (len(curr_path) > 0):
    print('Current Path: ', os.getcwd())
    return curr_path
  else:
    raise Exception('\n Failed to Mount Google Drive\n')

my_folder = '/Colab Notebooks/BINF 43C9: Capstone/'
curr_path = mount_google_drive(my_folder)

folder_path = curr_path + "data/AMR_stratified/"

# verify folder path exists
if not os.path.exists(folder_path):
    print(f"ERROR: Folder '{folder_path}' does not exist.")
    exit()

# unzip .txt.gz files
for filename in os.listdir(folder_path):
    if filename.endswith(".txt.gz"):
        file_path = os.path.join(folder_path, filename)
        output_file_path = os.path.join(folder_path, os.path.splitext(filename)[0])

        with gzip.open(file_path, 'rt') as gzipped_file, open(output_file_path, 'w') as output_file:
            output_file.write(gzipped_file.read())

        print(f"Unzipped {filename} to {output_file_path}")

print("All files unzipped.")

# list all files in folder
files = os.listdir(folder_path)

# select only .txt files
txt_files = [file for file in files if file.endswith(".txt")]

# add phenotype column to each file and aggregate all files into combined dataframe
dataframes = []

for file in txt_files:
    category = file.split('_')[1]
    file_path = os.path.join(folder_path, file)

    df = pd.read_csv(file_path, sep='\t', header=0)
    df['PHE'] = category
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index = True)
print(combined_df)

# # export combined dataframe to .csv file
# output_file_path = '/content/drive/My Drive/Colab Notebooks/BINF 43C9: Capstone/data/AMR_stratified_all.csv'
# combined_df.to_csv(output_file_path, index = False)

# # unzip functional annotation data
# file_path = '/content/drive/My Drive/Colab Notebooks/BINF 43C9: Capstone/data/GenoSkylinePlus_bed.tar.gz'
# output_folder_path = '/content/drive/My Drive/Colab Notebooks/BINF 43C9: Capstone/data/'
#
# if not os.path.exists(output_folder_path):
#     os.makedirs(output_folder_path)
#
# with tarfile.open(file_path, 'r:gz') as tar:
#     tar.extractall(output_folder_path)
#
# print(f"Unzipped GenoSkylinePlus_bed.tar.gz to {output_folder_path}")
# print("All files unzipped.")