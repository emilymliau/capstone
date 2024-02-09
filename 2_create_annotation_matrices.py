#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import packages
import os
import gzip
import pandas as pd
import numpy as np


# In[2]:


# function to read GWAS summary statistics for each ancestry group
def read_gwas_summary_stats(file_path):
    return pd.read_csv(file_path, sep = '\t')


# In[3]:


# function to read individual .bedGraph files
def read_bedgraph(file_path):
    columns = ['CHR', 'START', 'END', 'METRIC']
    bedgraph_file = pd.read_csv(file_path, sep = '\t', header = None, names = columns)
    return bedgraph_file


# In[4]:


# function to parse through .bedGraph files and create annotation matrix
def parse_bedgraph_folder(gwas_df, folder_path, output_path):
    # initialize annotation matrix
    annot_matrix = np.zeros((len(gwas_df), 127))
    
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
        for index in range(128):
            if index not in [60, 64]:
                annot_matrix[index][file_counter] = 1
                file_counter += 1

    # create annotation matrix
    matrix_df = pd.DataFrame(annot_matrix)
    anno_matrix_df = pd.concat([gwas_df['RSID'], matrix_df], axis = 1)
    anno_matrix_df['P-VALUE'] = gwas_df['P']
    
    # save annotation matrix as .csv.gz file
    output_file_path = os.path.join(output_path, 'combined.csv.gz')
    anno_matrix_df.to_csv(output_file_path, index = False, compression = 'gzip')

    print(f"Annotation matrix for {output_path} saved to {output_file_path}")


# In[5]:


# establish file paths for data folders
data_folder_path = 'C:/Users/emily/BINF_43C9/data/'
pheno_categories = ['AgeSmk']
ancestry_folders = ['AFR', 'AMR', 'EAS', 'EUR']


# In[ ]:


# read GWAS summary statistics, parse .bedGraph files, and create annotation matrix for each phenotype and ancestry group
for phenotype in pheno_categories:
    for ancestry in ancestry_folders:
        gwas_file_path = os.path.join(data_folder_path, ancestry + '_stratified', 'GSCAN_' + phenotype + '_2022_GWAS_SUMMARY_STATS_' + ancestry + '.txt')
        bedgraph_folder_path = os.path.join(data_folder_path, 'BedGraph')
        output_folder_path = os.path.join(data_folder_path, ancestry + '_stratified', phenotype)

        gwas_df = read_gwas_summary_stats(gwas_file_path)
        parse_bedgraph_folder(gwas_df, bedgraph_folder_path, output_folder_path)

