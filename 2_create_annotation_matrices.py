# import packages
import os
import gzip
import pandas as pd
import numpy as np

# function to read GWAS summary statistics for each ancestry group
def read_gwas_summary_stats(file_path):
    return pd.read_csv(file_path, sep = '\t')

# function to read individual .bedGraph files
def read_bedgraph(file_path):
    columns = ['CHR', 'START', 'END', 'METRIC']
    bedgraph_file = pd.read_csv(file_path, sep = '\t', header = None, names = columns)
    return bedgraph_file

# function to parse through .bedGraph files and create annotation matrix
def parse_bedgraph_folder(gwas_df, folder_path, output_path, ancestry, phenotypes):
    # initialize annotation matrix
    annot_matrix = np.zeros((len(gwas_df), 127 + len(phenotypes)))

    # establish path for .bedGraph files
    files = os.listdir(folder_path)
    bedgraph_files = [file for file in files if file.endswith(".bedGraph")]

    # conditions for annotation matrix
    for bedgraph_file in bedgraph_files:
        file_path = os.path.join(folder_path, bedgraph_file)
        bedgraph_df = read_bedgraph(file_path)

        x = bedgraph_df['METRIC'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        temp = bedgraph_df.loc[bedgraph_df['METRIC'] > x[0.6]]

        merged = pd.merge(gwas_df, temp, how = 'inner', left_on = ['CHR', 'POS'], right_on = ['CHR', 'START'])
        result_df = merged[(merged['POS'] >= merged['START']) & (merged['POS'] <= merged['END'])]

        file_counter = 0
        for index, row in result_df.iterrows():
            for col in range(127):
                if col not in [60, 64]:
                    annot_matrix[index, file_counter] = 1
                    file_counter += 1

    # add separate p-value columns for each phenotype
    for i, phenotype in enumerate(phenotypes):
        if phenotype in gwas_df.columns:
            annot_matrix[:, 127 + i] = gwas_df[phenotype].values

    # create annotation matrix
    matrix_df = pd.DataFrame(annot_matrix, columns = [i for i in range(127)] + [f'{phenotype}_pval' for phenotype in phenotypes])

    return matrix_df

# establish file paths for data folders
data_folder_path = '/storage/projects/capstone24/data/'
pheno_categories = ['AgeSmk', 'CigDay', 'DrnkWk', 'SmkCes', 'SmkInit']
ancestry_folders = ['AFR', 'AMR', 'EAS', 'EUR']

# read GWAS summary statistics, parse .bedGraph files, and create annotation matrix for each ancestry group and phenotype
for phenotype in pheno_categories:
    for ancestry in ancestry_folders:
        gwas_file_path = os.path.join(data_folder_path, ancestry + '_stratified', f'GSCAN_{phenotype}_2022_GWAS_SUMMARY_STATS_{ancestry}.txt')
        bedgraph_folder_path = os.path.join(data_folder_path, 'BedGraph')
        output_folder_path = os.path.join(data_folder_path, f'{ancestry}_stratified', f'{ancestry}_stratified_{phenotype}')

        # create the output folder if it doesn't already exist
        os.makedirs(output_folder_path, exist_ok = True)

        gwas_df = read_gwas_summary_stats(gwas_file_path)
        parse_bedgraph_folder(gwas_df, bedgraph_folder_path, output_folder_path, ancestry, pheno_categories)