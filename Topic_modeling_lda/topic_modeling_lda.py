import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import CoherenceModel
import gensim
from datetime import datetime
from gensim import corpora
from gensim.models import TfidfModel, LdaModel
from gensim.corpora import Dictionary
from nltk.tokenize import word_tokenize
import pyLDAvis.gensim
import pyLDAvis
import nltk
import IPython


def get_preprocessed_data():
    data_frame = pd.read_pickle("resources/concatenated_preprocessed_issue_data.pkl")
    print(data_frame.head())
    data_frame = data_frame.sample(frac = 1)
    print(data_frame.head())
    return data_frame


def tfidf_vectorization(sentences):
    tokenized_corpus = [word_tokenize(sentence) for sentence in sentences]
    dictionary = Dictionary(tokenized_corpus)
    corpus_bow = [dictionary.doc2bow(tokens) for tokens in tokenized_corpus]

    tfidf_model = TfidfModel(corpus_bow)
    tfidf_vector = tfidf_model[corpus_bow]

    return dictionary, tfidf_vector, tokenized_corpus, corpus_bow


def lda_modeling(id2words, corpus_tfidf, num_of_topic):
    alpha = 50 / num_of_topic
    eta = 0.01
    print("Before: ", datetime.now().strftime("%H:%M:%S"))
    lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, random_state=42, num_topics=num_of_topic,
                               id2word=id2words, passes=40, iterations=200, chunksize=1000, eval_every=1,
                               workers=20, alpha=alpha, eta=eta)

    print("After: ", datetime.now().strftime("%H:%M:%S"))
    print("Total topic: ", num_of_topic)
    print(lda_model_tfidf.print_topics())

    return lda_model_tfidf


def calculate_coherence(lda_tfidf_model, dictionary, text_column):
    coherence_model = CoherenceModel(model=lda_tfidf_model, texts=text_column, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    print("Coherence Score: ", coherence_score)
    print("---" * 20)
    return coherence_score


def get_highest_coherence_value_num_of_topics(id2word, tfidf_vectors, tokenize_corpus):
    num_of_topics_list = []
    coherence_values_list = []
    highest_coherence_score = -1
    best_num_of_topics = 0

    for num_of_topics in range(2, 51):
        print("Topic: ", num_of_topics)
        

        lda_model = lda_modeling(id2word, tfidf_vectors, num_of_topics)
        coherence_value = calculate_coherence(lda_model, id2word, tokenize_corpus)

        num_of_topics_list.append(num_of_topics)
        coherence_values_list.append(coherence_value)

        if coherence_value > highest_coherence_score:
            highest_coherence_score = coherence_value
            best_num_of_topics = num_of_topics

    results_df = pd.DataFrame({'Num_of_Topics': num_of_topics_list, 'Coherence_Value': coherence_values_list})
    results_df.to_csv('resources/experiments_result_bow-tfidf/lda_coherence_results5.csv', index=False)

    print("Best Number of Topics:", best_num_of_topics)
    print("Highest Coherence Score:", highest_coherence_score)

    return best_num_of_topics, highest_coherence_score


def match_topics_with_documents(lda_model, corpus_bow, df):
    # Assign topics to each document
    topic_assignments = lda_model.get_document_topics(corpus_bow)

    # Extract the dominant topic for each document
    dominant_topics = [max(topics, key=lambda x: x[1])[0] for topics in topic_assignments]
    df['Dominant_Topic'] = dominant_topics
    df.to_csv('resources/experiments_result_bow-tfidf/documents_with_topics.csv', index=False)

    # return dominant_topics


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
    df = get_preprocessed_data()
    id2word, tfidf_vectors, tokenize_corpus, corpus_bow = tfidf_vectorization(df["concatenated_column"])

    # -------******* For finding optimal number of topic using coherence *******-------
    # best_num_of_topics, highest_coherence_score = get_highest_coherence_value_num_of_topics(id2word, tfidf_vectors, tokenize_corpus)
    
    lda_model_tfidf = lda_modeling(id2word, tfidf_vectors, 6)
    # coherence_score = calculate_coherence(lda_model_tfidf, id2word, tokenize_corpus)
    # match_topics_with_documents(lda_model_tfidf, corpus_bow, df)
    LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model_tfidf, tfidf_vectors, id2word)
    pyLDAvis.show(LDAvis_prepared,  local=False)
    # merge_csv_files('dataset/issue_dataset.csv', 'resources/experiments_result_bow-tfidf/documents_with_topics.csv', 'resources/experiments_result_bow-tfidf/final_merged_exp.csv' )
    
    