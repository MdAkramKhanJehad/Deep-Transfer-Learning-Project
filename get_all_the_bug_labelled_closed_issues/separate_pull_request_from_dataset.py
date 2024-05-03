import pandas as pd


file_path = 'get_all_the_bug_labelled_closed_issues/issue_dataset.csv'

df = pd.read_csv(file_path)


pull_requests_df = df[df['issue_html_url'].str.contains('/pull/', case=False, na=False)]
issues_df = df[~df['issue_html_url'].str.contains('/pull/', case=False, na=False)]


pull_requests_df.to_csv('get_all_the_bug_labelled_closed_issues/pull_requests.csv', index=False)
issues_df.to_csv('get_all_the_bug_labelled_closed_issues/issues.csv', index=False)