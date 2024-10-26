import gradio as gr
import numpy as np
import pandas as pd
import os

def analyze_bibliometric(file):
    # Load the data from the uploaded file
    df_Out = pd.read_excel(file.name, header=None, skiprows=4, sheet_name=1)

    # Get the number of columns
    col_num = df_Out.shape[1]

    # Search for #A-Journal Papers
    header_row = pd.read_excel(file.name, header=None, skiprows=3, nrows=1, sheet_name=1)

    A_Journal = '# A- Journal Papers '

    if A_Journal in header_row.values:
        columns = ['Source', 'Name', 'Inst', 'Department', 'PromoYear', 'Title', 'PhDYear',
           'School', 'Scopus ID', 'H-index', '# Papers', 'FWCI',
           '% Top 10% Journals', '# Top 10% Journals', 'H_FWCI', 'H_Year',
           'H_Type', '75th prctile FWCI', '% Top 10% FWcites', '# Top 10% FWcites', '# A- Journal Papers ',
           '# Papers.1', 'FWCI.1', '% Top 10% Journals.1', '# Top 10% Journals.1',
           '75th prctile FWCI.1', '% Top 10% FWcites.1', '# Top 10% FWcites.1',
           '# Papers.2', 'FWCI.2', '% Top 10% Journals.2', '# Top 10% Journals.2',
           'H_FWCI.1', 'H_Year.1', 'H_Type.1', '75th prctile FWCI.2',
           '% Top 10% FWcites.2', '# Top 10% FWcites.2', '# Papers.3', 'FWCI.3',
           '% Top 10% Journals.3', '# Top 10% Journals.3', '75th prctile FWCI.3',
           '% Top 10% FWcites.3', '# Top 10% FWcites.3', '# Books',
           '# Bk chapters ', '# Journal Articles', '# Conference Papers', 'H-index1',
           'URL', 'URL1', 'Unnamed: 50', 'Unnamed: 50','Unnamed: 50']
    else:
        columns = ['Source', 'Name', 'Inst', 'Department', 'PromoYear', 'Title', 'PhDYear',
           'School', 'Scopus ID', 'H-index', '# Papers', 'FWCI',
           '% Top 10% Journals', '# Top 10% Journals', 'H_FWCI', 'H_Year',
           'H_Type', '75th prctile FWCI', '% Top 10% FWcites', '# Top 10% FWcites',
           '# Papers.1', 'FWCI.1', '% Top 10% Journals.1', '# Top 10% Journals.1',
           '75th prctile FWCI.1', '% Top 10% FWcites.1', '# Top 10% FWcites.1',
           '# Papers.2', 'FWCI.2', '% Top 10% Journals.2', '# Top 10% Journals.2',
           'H_FWCI.1', 'H_Year.1', 'H_Type.1', '75th prctile FWCI.2',
           '% Top 10% FWcites.2', '# Top 10% FWcites.2', '# Papers.3', 'FWCI.3',
           '% Top 10% Journals.3', '# Top 10% Journals.3', '75th prctile FWCI.3',
           '% Top 10% FWcites.3', '# Top 10% FWcites.3', '# Books',
           '# Bk chapters', '# Journal Articles', '# Conference Papers', 'H-index1',
           'URL', 'URL1', 'Unnamed: 50', 'Unnamed: 50','Unnamed: 50']

    # To accommodate the varying column size in the file
    column_names = [columns[i] for i in range(0, col_num)]
    df_Out.columns = column_names

    # Rename H-index and H-index1 to promo and current according to whether H-index for candidate is empty
    if pd.isna(df_Out.at[0, 'H-index']):
        df_Out.loc[0, 'H-index'] = df_Out.loc[0, 'H-index1']
        df_Out = df_Out.rename(columns={'H-index': 'H-index.Promo', 'H-index1': 'H-index.Current'})
    else:
        df_Out = df_Out.rename(columns={'H-index': 'H-index.Current', 'H-index1': 'H-index.Promo'})

    name_df = df_Out[['Source', 'Name', 'Inst', 'Department', 'PromoYear', 'Title', 'PhDYear', 'School',
                      'Scopus ID', 'H-index.Promo', 'H-index.Current', 'URL', 'URL1']]

    # Find the index of the first NaN in the specified column
    def find_first_nan_index(col):
        # Get the index of the first NaN
        first_nan_idx = col[col.isna()].index.min()
        return first_nan_idx

    # Find the index of the first NaN in the name column; to remove the rows that has null in name column
    first_nan_index = find_first_nan_index(name_df['Name'])

    # Filter rows up to and excluding the row with the first NaN
    if pd.notna(first_nan_index):  # Ensure there is at least one NaN in the column if first_nan_index is not null
        df_filtered = name_df.loc[:first_nan_index-1].copy()
    else:
        df_filtered = name_df.copy()  # No NaNs found, keep the original DataFrame

    # Since the format is a string, this is the way to remove the unwanted symbol
    df_filtered.loc[:, 'PromoYear'] = df_filtered['PromoYear'].astype(str).apply(lambda x: x.split('~')[1] if '~' in x else x)

    df_filtered.loc[:, 'Scopus ID_01'] = np.nan

    # Ensure 'Scopus ID' is a string before using .str methods
    df_filtered['Scopus ID'] = df_filtered['Scopus ID'].astype(str)

    if df_filtered['Scopus ID'].str.contains('/').any():
        mask = df_filtered['Scopus ID'].str.contains('/')  # Create mask

        # Perform the split and assign results only to the relevant rows
        split_values = df_filtered.loc[mask, 'Scopus ID'].str.split('/', n=1, expand=True)

        # Assign the split values back to the DataFrame
        df_filtered.loc[mask, 'Scopus ID'] = split_values[0]
        df_filtered.loc[mask, 'Scopus ID_01'] = split_values[1]

    df_filtered = df_filtered[['Source', 'Name', 'Inst', 'Department', 'PromoYear', 'Title', 'PhDYear', 'School', 'Scopus ID',
                             'Scopus ID_01', 'H-index.Promo', 'H-index.Current', 'URL', 'URL1']]

    # Save the filtered DataFrame to an Excel file
    output_file = "filtered_bibliometric_analysis.xlsx"
    df_filtered.to_excel(output_file, index=False)

    return output_file

iface = gr.Interface(
    fn=analyze_bibliometric,
    inputs=gr.File(label="Upload the Bibliometric file:"),
    outputs=gr.File(label="Download Analysis"),
    title="Bibliometric Data Analyzer"
)

iface.launch(share=True)
