# Static Application Security Testing(SAST) Tools Issue Analysis: A Categorization of Bugs

This is the implementation of our project "Static Application Security Testing(SAST) Tools Issue Analysis: A Categorization of Bugs".

## Abstract
In the rapidly evolving landscape of software development, Security-Focused Static Analysis (SAST) tools holds a critical role in ensuring the security of applications. However, the effectiveness of these tools is hindered by the prevalence of uncharacterized bugs, presenting a formidable challenge without a comprehensive categorization or taxonomy. This paper addresses this issue by presenting an approach to categorize uncharacterized bugs within open-source SAST tools available on platforms like GitHub. Leveraging state-of-the-art clustering techniques, advanced methods are employed to categorize and classify these bugs. The results reveal that no single model emerged as the definitive solution, emphasizing the complexity of the problem. The key takeaway from this study underscores the indispensable role of human intervention in bug categorization for SAST tools, indicating the necessity for continued human effort in refining and enhancing the reliability of these crucial security tools. This study contributes to the ongoing discourse on enhancing SAST tool effectiveness and ensuring a more secure software development environment.

## Installation
You're expected to have python 3.9.6 installed on your system.

With pip:
- pip/pip3 install -r requirements.txt

## Usage

### Data Collection
- **get_all_the_bug_labelled_closed_issues/GetBugLabeledClosedIssue.py -** Run this file getting all the closed issues with specific keywords(available in a list in line 94) from the repositores listed in ***dataset/sast_tools.csv***. 

### Data Preprocessing
- **preprocessing/data_preprocessing.py -** Run this code for preprocessing the data.

### LDA Based Clustering
- **Topic_modeling_lda/topic_modeling_lda.py -** Run this code for clustering using LDA. 

### GSDMM Based Clustering
- **GSDMM/gsdmm_training.py -** Run this code for clustering using the GSDMM.The library is added manually in the *GSDMM/gsdmm_library_by_rwalk/* folder.
 
### BERTopic Based Clustering
- **BERTopic/bertopic.ipynb -** Run this code in Kaggle (https://www.kaggle.com/) for clustering using the BERTopic.
