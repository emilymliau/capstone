# import packages
import os
import gzip
import pandas as pd
import numpy as np
import tarfile

# establish gwas and annotation dataframes
gwas_amr = pd.read_csv('C:/Users/emily/BINF_43C9/data/AMR_stratified/GSCAN_AgeSmk_2022_GWAS_SUMMARY_STATS_AMR.txt', sep = '\t')
gwas_amr.head()
annot_amr = np.zeros((len(gwas_amr), 127))

folder_path = 'C:/Users/emily/BINF_43C9/data/BedGraph'
print(folder_path)

# verify folder path exists
if not os.path.exists(folder_path):
    print(f"ERROR: Folder '{folder_path}' does not exist.")
    exit()

# function to read individual .bedGraph files
def read_bedgraph(file_path):
    columns = ['CHR', 'START', 'END', 'METRIC']
    bedgraph_file = pd.read_csv(file_path, sep = '\t', header = None, names = columns)
    return bedgraph_file

# function to parse through .bedGraph files
def parse_bedgraph_folder(folder_path):
    dataframes = []
    files = os.listdir(folder_path)
    bedgraph_files = [file for file in files if file.endswith(".bedGraph")]

    for bedgraph_file in bedgraph_files:
        file_path = os.path.join(folder_path, bedgraph_file)
        df = read_bedgraph(file_path)

        df.columns = ['CHR', 'START', 'END', 'METRIC']
        x = df['METRIC'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        temp = df.loc[df['METRIC'] > x[0.6]]
        merged = pd.merge(gwas_amr, temp, how = 'inner', left_on = ['CHR', 'POS'], right_on = ['CHR', 'START'])
        result_df = merged[(merged['POS'] >= merged['START']) & (merged['POS'] <= merged['END'])]

        file_counter = 0
        for index in range(128):
          if index not in [60, 64]:
            annot_amr[index][file_counter] = 1
            file_counter += 1

# create AMR annotation matrix
parse_bedgraph_folder(folder_path)
matrix_amr = pd.DataFrame(annot_amr)
anno_matrix_amr = pd.concat([gwas_amr['RSID'], matrix_amr], axis = 1)
anno_matrix_amr['P-VALUE'] = gwas_amr['P']
anno_matrix_amr.head()

# export annotation matrix to .csv.gz file
anno_matrix_amr.to_csv('C:/Users/emily/BINF_43C9/data/AMR_stratified/AMR_combined.csv.gz', index = False, compression = 'gzip')