import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from sklearn.manifold import TSNE
from tqdm import tqdm


def read_preprocessed_data():
    df = pd.read_pickle("resources/preprocessed_issue_data.pkl")
    print(df.columns)
    return df


def concat_title_description_comments(df):
    result_df = pd.DataFrame({'concatenated_column': df['title'] + " " + df['description'] + " " + df['comments']})
    result_df['word_count'] = result_df["concatenated_column"].apply(lambda x: len(str(x).split()))

    # remove rows with less than 4 word count
    result_df = result_df[result_df['word_count'] >= 4]
    result_df = result_df.drop('word_count', axis=1)
    result_df["unique_id"] = df['unique_id']
    # print(result_df.head())

    return result_df


def plot_frequency_dist_of_number_of_words_for_each_text(dataframe):
    dataframe['word_count'] = dataframe["concatenated_column"].apply(lambda x: len(str(x).split()))
    dataframe = dataframe[dataframe['word_count'] >= 4]

    # Set up Matplotlib and Seaborn settings
    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    sns.set_palette("husl")

    # Plot the word count distribution using Seaborn's distplot
    bins = range(0, dataframe['word_count'].max() + 15, 15)
    sns.histplot(dataframe['word_count'], bins=bins, kde=False, color='green', edgecolor='black')

    plt.title('Word Count Distribution')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')

    plt.xlim(0, 1500)
    plt.ylim(0, 500)
    plt.savefig("resources/word_count_distribution_after_preprocessing.png")
    plt.show()


def create_word_cloud(df):
    cloud = WordCloud(colormap="Set2", width=600, height=400).generate(str(df["concatenated_column"]))
    fig = plt.figure(figsize=(13, 13))
    plt.axis("off")
    plt.imshow(cloud, interpolation='bilinear')
    plt.savefig("resources/word_cloud_after_preprocessing.png")
    plt.show()


def train_word2vec_model(df):
    tokenized_corpus = [word_tokenize(sentence) for sentence in df["concatenated_column"]]
    # print(tokenized_corpus[0])
    word2vec_model = Word2Vec(sentences=tokenized_corpus, vector_size=100, window=5, min_count=1, workers=4)
    word2vec_model.save("resources/word2vec_model.model")

    # v1 = word2vec_model.wv['model']
    sim_words = word2vec_model.wv.most_similar('rescan')
    print(sim_words)
    sim_words2 = word2vec_model.wv.most_similar('false')
    print(sim_words2)
    sim_words3 = word2vec_model.wv.most_similar('analysis')
    print(sim_words3)


if __name__ == "__main__":
    df = read_preprocessed_data()
    df = concat_title_description_comments(df)
    print(df.columns)
    df.to_pickle("resources/concatenated_preprocessed_issue_data.pkl")
    df = pd.read_pickle("resources/concatenated_preprocessed_issue_data.pkl")

    # plot_frequency_dist_of_number_of_words_for_each_text(df)
    # print(df.head())
    # print("--*--*--*--*--*--*--*--*--*--*--*--*--*--*-- Column:", df.columns)
    # create_word_cloud(df)
    train_word2vec_model(df)

