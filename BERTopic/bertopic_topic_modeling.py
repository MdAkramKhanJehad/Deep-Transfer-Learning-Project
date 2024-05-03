from bertopic import BERTopic
import json
import pandas as pd
from umap import UMAP
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN


data_frame = pd.read_pickle("resources/preprocessed_bug_data_for_bertopic_with_only_bug.pkl")
data_frame['title_description'] = data_frame['title'] + ' ' + data_frame['description']
data_frame['title_description_comments'] = data_frame['title'] + ' ' + data_frame['description'] + ' ' + data_frame['comments'].fillna('')
print(data_frame.columns)


umap_model = UMAP(n_neighbors=6, n_components=3, min_dist=0.1)
hdbscan_model = HDBSCAN(min_samples=40, prediction_data=True,gen_min_span_tree=True)

embedding_model=SentenceTransformer('all-MiniLM-L6-v2')
vectorizer_model = CountVectorizer(ngram_range=(1,2))
model = BERTopic(umap_model=umap_model,hdbscan_model=hdbscan_model,embedding_model=embedding_model,vectorizer_model=vectorizer_model,top_n_words=7,language="english",calculate_probabilities=True, verbose=True)

topics, prob = model.fit_transform(data_frame['title_description_comments'])

print(model.get_topic_info())