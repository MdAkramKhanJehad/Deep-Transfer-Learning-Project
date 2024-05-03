# pip install ktrain

# Import necessary libraries
import pandas as pd
import ktrain
from ktrain import text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load your dataset
# Assuming you have a DataFrame 'df' with columns 'concatenated_column' and 'Dominant_Topic'
# Replace it with your actual data loading logic
# df = load_your_dataset()

df = pd.read_csv("resources/experiments_result_bow-tfidf/final_merged_result_for_analysis/final_merged_exp.csv")

# Split the dataset into training and testing sets
# train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Function to evaluate a model
def evaluate_model(model_name, df):
    print(f"Evaluating Model: {model_name}")
    
    target = ['Dominant_Topic']
    data = ['concatenated_column']

    X = df[data]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.1, random_state=42)
    X_train = X_train.dropna()
    y_train = y_train.dropna()


    max_len = 500
    batch_size = 6
    learning_rate = 5e-5
    epochs = 1
    model_ = model_name
    t_mod = text.Transformer(model_, maxlen=max_len, classes = [0, 1, 2, 3, 4, 5, 6])


    '''Converting split data to list [so it can processed]'''
    #train
    X_tr = X_train['concatenated_column'].tolist()
    y_tr = y_train['Dominant_Topic'].tolist()

    #test
    X_ts = X_test['concatenated_column'].tolist()
    y_ts = y_test['Dominant_Topic'].tolist()


    # Pre-processing training & test data
    train = t_mod.preprocess_train(X_tr,y_tr)
    test = t_mod.preprocess_train(X_ts,y_ts)

    # Model Classifier
    model = t_mod.get_classifier()

    learner = ktrain.get_learner(model, train_data=train, val_data=test, batch_size=batch_size)
    learner.fit_onecycle(learning_rate, epochs)
    x = learner.validate(class_names=t_mod.get_classes())

    print(x)


# Evaluate each model
evaluate_model('distilbert-base-uncased', df)
evaluate_model('bert-base-uncased', df)
evaluate_model('xlm-roberta-base', df)
evaluate_model('roberta-base', df)
