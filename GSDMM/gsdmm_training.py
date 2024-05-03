import pandas as pd
import numpy as np
import gensim
from  gsdmm_library_by_rwalk.gsdmm.mgp import MovieGroupProcess 
from gensim.utils import simple_preprocess

df = pd.read_pickle('resources/preprocessed_bug_data.pkl')
df['title_description'] = df['title'] + ' ' + df['description']
print(df.head())
docs = df.title_description.to_numpy()

# Extract unique IDs for the selected subset of documents
unique_ids = df.unique_id.tolist()

tokenized_docs = [simple_preprocess(doc) for doc in docs]

# print(tokenized_docs)

dictionary = gensim.corpora.Dictionary(tokenized_docs)

# filter extreme cases out of dictionary
dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

# create variable containing length of dictionary/vocab
vocab_length = len(dictionary)

bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

gsdmm = MovieGroupProcess(K=350, alpha=0.1, beta=0.1, n_iters=70)

# y = gsdmm.fit(tokenized_docs, vocab_length)
cluster_assignments = gsdmm.fit(tokenized_docs, vocab_length)

# Create a new column "cluster" in the dataframe for the selected subset
df['cluster'] = cluster_assignments

# Print and save the results
output_df = pd.DataFrame({'unique_id': unique_ids, 'title': docs, 'cluster': cluster_assignments})
output_df.to_csv('resources/gsdmm_experiment/cluster_results_title_description2.csv', index=False)

# Print cluster assignments for each title
# for unique_id, title, cluster in zip(unique_ids, docs, cluster_assignments):
#     print(f'Unique ID: {unique_id} - Title: "{title}" - Cluster: {cluster} - Choose_best_lebel: {gsdmm.choose_best_label(title)}')

doc_count = np.array(gsdmm.cluster_doc_count)
print('Number of documents per topic:', doc_count)

top_index = doc_count.argsort()[-15:][::-1]
print('Most important clusters (by the number of docs inside):', top_index)


def top_words(cluster_word_distribution, top_cluster, values):
    for cluster in top_cluster:
        sort_dicts = sorted(cluster_word_distribution[cluster].items(), key=lambda k: k[1], reverse=True)[:values]
        print("\nCluster %s : %s"%(cluster, sort_dicts))

top_words(gsdmm.cluster_word_distribution, top_index, 20)