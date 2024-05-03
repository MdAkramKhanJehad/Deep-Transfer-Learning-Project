import pandas as pd
import re
import contractions
import nltk
import string
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import unidecode
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import numpy as np


def get_dataframe():
    df = pd.read_csv('dataset/issue_dataset.csv')

    # condition = df['labels'].str.contains('bug|false positive|false negative', case=False)
    # df = df[condition][['title', 'description', 'comments', 'unique_id']]

    df = df[['title', 'description', 'comments', 'unique_id']]

    # print("Column:", df.columns)
    print("Row: ", len(df))
    print("---" * 25)
    print(df.head())
    return df


def count_null_values_description_comments(df):
    all_null = 0
    title_null = 0
    desc_null = 0
    comments_null = 0

    for index, row in df.iterrows():
        if pd.isna(row["description"]):
            desc_null = desc_null + 1
        if pd.isna(row["comments"]):
            comments_null = comments_null + 1
        if pd.isna(row["title"]):
            title_null = title_null + 1
        if pd.isna(row["description"]) and pd.isna(row["comments"]):
            all_null = all_null + 1
        # if len(str(row["description"])) < 1:
        #     desc_null = desc_null + 1
        # if len(str(row["comments"])) < 1:
        #     comments_null = comments_null + 1
        # if len(str(row["title"])) < 1:
        #     title_null = title_null + 1
        # if len(str(row["description"])) < 1 and len(str(row["comments"])) < 1 :
        #     all_null = all_null + 1

    print("Both Null: ", all_null, " || Desc Null: ", desc_null, " || Comments Null: ", comments_null,
          " || Title Null: ", title_null)
    print("---" * 25)


def remove_rows_with_null_value(df, column_name):
    drop_count = 0

    for index, row in df.iterrows():
        if pd.isna(row[column_name]):
            df = df.drop(index)
            drop_count = drop_count + 1

    print("Total Row Drop: ", drop_count, " || Total Row Now: ", len(df))
    print("---" * 25)
    # df.to_pickle("resources/issue_data_after_null_removal.pkl")

    return df


def remove_numbers(text):
    text_without_numbers = re.sub(r'\d+', ' ', text)
    return text_without_numbers


def remove_code(text):
    # find and replace code blocks
    code_pattern = re.compile(r'```[\s\S]*?```|`[\s\S]*?`|<code>[\s\S]*?</code>', flags=re.MULTILINE)
    text_no_code = code_pattern.sub('', text)

    return text_no_code


def remove_markdown_links(text):    
    markdown_link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)', flags=re.MULTILINE)
    text_markdown_http_links = markdown_link_pattern.sub('', text)

    return text_markdown_http_links


def remove_links(text):
    http_link_pattern = re.compile(r'https?://\S+|www\.\S+', flags=re.MULTILINE)
    text_no_http_links = http_link_pattern.sub('', text)

    return text_no_http_links


def remove_noise(text):
    text = remove_code(text)
    text = remove_markdown_links(text)
    text = remove_links(text)
    text = re.sub(r'@[\w]+', '', text)  # removed the usernames from the text. e.g., @ajibabraham

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U00002700-\U000027BF"  # dingbats
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    punctuation_pattern = re.compile("[\.\,\!\?\:\;\'\"\(\)\{\}]+")

    # Combine both patterns into a single pattern
    # combined_pattern = re.compile(emoji_pattern.pattern + "|" + punctuation_pattern.pattern, flags=re.UNICODE)
    combined_pattern = re.compile(emoji_pattern.pattern, flags=re.UNICODE)

    clean_text = combined_pattern.sub(r' ', text)
    clean_text = " ".join(clean_text.split())

    return clean_text


def remove_accented_chars(text):
    """remove accented characters from text, e.g. café"""
    text = unidecode.unidecode(text)
    return text


def strip_html_tags(text):
    """remove html tags from text"""
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")
    return stripped_text


def expand_contractions(text):
    """expand shortened words, e.g. don't to do not"""
    text = contractions.fix(text)
    return text


def remove_punctuation(text):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    text_no_punctuation = text.translate(translator)

    return text_no_punctuation


def stem_text(text):
    words = word_tokenize(text)
    porter_stemmer = PorterStemmer()
    
    stemmed_words = [porter_stemmer.stem(word) for word in words]
    stemmed_text = ' '.join(stemmed_words)
    
    return stemmed_text



def perform_lemmatization(text):
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)

    words = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    lemmatized_text = " ".join(lemmatized_words)

    return lemmatized_text


def remove_whitespace(text):
    """remove extra whitespaces from text"""
    text = text.strip()
    return " ".join(text.split())


def remove_stopwords(text):
    nltk.download('stopwords', quiet=True)
    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]

    filtered_text = ' '.join(filtered_words)

    return filtered_text



def preprocess_text(text):
    # text = strip_html_tags(text)


    try:
        if len(str(text)) > 5:
            text = text.replace(
                "Issues is only for reporting a bug/feature request. For limited support, questions, and discussions, "
                "please join [MobSF Slack channel]("
                "https://join.slack.com/t/mobsf/shared_invite/zt-153nfus2r-hMCGrwzm8Lyy3OxsihnolQ) Please include all "
                "the requested and relevant information when opening a bug report. Improper reports will be closed "
                "without any response.",
                '')
            text = text.replace(
                "Issues is only for reporting a bug/feature request. For limited support, questions, and discussions, "
                "please join MobSF Slack channel: http://tiny.cc/mobsf Please include all the requested and relevant "
                "information when opening a bug report. Improper reports will be closed without any response.",
                '')
            text = text.replace(
                "Issues is only for reporting a bug/feature request. For limited support, questions, and discussions, "
                "please join [MobSF Slack channel]("
                "https://mobsf.slack.com/join/shared_invite"
                "/enQtNzM2NTAyNzA1MjgxLTdjMzkzNDc3ZjdiMjkwZTZhMmFhNDlkZmMwZDhjNDNmYTAzYWE5NGZlMDIzYzliNTdiMDQ2MTRlYjU1MjkyNGM) Please include all the requested and relevant information when opening a bug report. Improper reports will be closed without any response.",
                '')
            text = text.replace("If you're requesting a new feature/enhancement, explain why you'd like it to be added and it's importance. **Is your feature request related to a problem? Please describe.** A clear and concise description of what the problem is. **Describe the solution you'd like** A clear and concise description of what you want to happen. **Describe alternatives you've considered** A clear and concise description of any alternative solutions or features you've considered. **Additional context** Add any other context or screenshots about the feature request here.", '')
            text = text.replace("Issues is only for reporting a bug/feature request. For limited support, questions, and discussions, please join [MobSF Slack channel](https://join.slack.com/t/mobsf/shared_invite/zt-153nfus2r-hMCGrwzm8Lyy3OxsihnolQ) Please include all the requested and relevant information when opening a bug report. Improper reports will be closed without any response.",'')

            ########### Commented for bertopic preprocessing data ##########
            text = remove_noise(text)
            # text = remove_accented_chars(text)
            # text = text.lower()
            # text = expand_contractions(text)
            text = remove_punctuation(text)

            # # text = stem_text(text)
            text = perform_lemmatization(text)
            # text = remove_numbers(text=text)
            text = remove_whitespace(text)
            text = remove_stopwords(text)
            
        return text

    except Exception as e:
        print(f"An error occurred during preprocessing: {str(e)}")
        return None


def average_word_count(dataframe):
    required_columns = ['title', 'description', 'comments']
    
    # Calculate average word count for each column
    averages = {}
    for column in required_columns:
        word_counts = dataframe[column].apply(lambda x: len(str(x).split()))
        average_word_count = np.mean(word_counts)
        averages[column] = average_word_count
    
    print(averages)




if __name__ == "__main__":
    # ****************--- UNCOMMENT THE BELOW FOR STARTING PRE-PROCESSING FROM SCRATCH  ---****************
    # df = get_dataframe()

    # count_null_values_description_comments(df)
    # df = remove_rows_with_null_value(df, "description")
    
    # print("--*--*--*--*--*--*--*--*--*--*--*--*--*--*-- Column:", df.columns, "\n\n")
    # print(df.head(10), "\n\n")
    # print(df.columns)
    
    # average_word_count(df)
    
    # print("\n\n-------***--------***-------***--------***--------***------- After Preprocessing -------***--------***-------***--------***--------***--------***--------\n\n")

    # df['title'] = df['title'].apply(preprocess_text)
    # df['description'] = df['description'].apply(preprocess_text)
    # df['comments'] = df['comments'].apply(preprocess_text)

    # count_null_values_description_comments(df)
    # average_word_count(df)
    # df = remove_rows_with_null_value(df, "description")
    # df = df[df['title'] != 'feature']
    # print(df[df['title'] != 'feature'])

    # df.to_pickle("resources/preprocessed_bug_data_for_bertopic.pkl")
    
    df = pd.read_pickle("resources/preprocessed_bug_data_for_bertopic.pkl")
    # average_word_count(df)
    print(df.head(15))
