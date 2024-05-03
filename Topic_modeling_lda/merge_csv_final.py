import pandas as pd

def merge_csv_files(first_csv_path, second_csv_path, output_csv_path):
    df1 = pd.read_csv(first_csv_path)
    df2 = pd.read_csv(second_csv_path)

    # merged_df = pd.merge(df1, df2[['unique_id', 'Dominant_Topic']], on='unique_id', how='left')
    # merged_df.to_csv(output_csv_path, index=False)
    df3 = pd.merge(df1, df2, on = 'unique_id')
    df3.set_index('unique_id', inplace = True)

    # Write it to a new CSV file
    df3.to_csv(output_csv_path)


if __name__ == "__main__":
    merge_csv_files('dataset/issue_dataset.csv', 'resources/gsdmm_experiment/cluster_results_title_description_comments.csv', 'resources/gsdmm_experiment/final_merged_gsdmm_df.csv' )