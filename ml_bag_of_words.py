import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression


def read_csv(artist_name):
    '''
    - reads the dataframe
    '''
    return pd.read_csv(f'./data/dataframes/{artist_name}_lyrics.csv', index_col=0)


def drop_duplicates(dataframe):
    '''
    - drops the duplicated rows
    '''
    return dataframe.drop_duplicates(inplace=True)


def make_one_dataframe(df_first, df_second):
    '''
    - concats two dataframes
    '''
    frames = [df_first, df_second]
    return pd.concat(frames)


def select_input_output(lyrics_dataframe):
    '''
    - selects input and output for the machine learning model to be fitted \n
    - set Lyrics Column as index column
    '''
    y = lyrics_dataframe.index
    X = lyrics_dataframe.reset_index()['lyrics']
    return X, y


def pipeline():
    '''
    - creates TfidfVectorizer \n
    - creates a pipeline model with TfidfVectorizer and LogisticRegression
    '''
    preprocessing_tfidf = TfidfVectorizer(stop_words='english')
    model = make_pipeline(preprocessing_tfidf,
                          LogisticRegression(class_weight='balanced'))
    return model


def create_list_of_parameters(param_name):
    '''
    -creates a list that consists of entered hyperparameters
    Note: It's still under development
    '''
    param_list = []
    default = input(
        f"Do you want to use default parameters for {param_name} 'y' or 'n':")
    if default == 'n':
        param_list.append(input(f'Please enter first value for {param_name}:'))
        check = input(
            f"Do you want to put more values for {param_name} 'y' or 'n':")
        while check == 'y':
            param_list.append(
                input(f'Please enter next value for {param_name}:'))
            check = input(
                f"Do you want to put more values for {param_name} 'y' or 'n':")
        return param_list


def get_GridSearch_hyperparameters(ngram_range=[(1.1), (1, 2)], max_df=[1.0], min_df=[1], log_C=[0.1, 1.0, 10, 100]):
    '''
    - creates a dictionary of parameters for GridSearch
    '''
    # ngram_range = '(1.1), (1,2)', max_df = '1.0', min_df = '1'  , log_C = '0.1, 1.0, 10, 100'
    #ngram_range = create_list_of_parameters("ngram_range")
    #max_df = create_list_of_parameters("max_df")
    #min_df = create_list_of_parameters("min_df")
    #log_C = create_list_of_parameters("log_C")

    param_grid = {
        'tfidfvectorizer__ngram_range': ngram_range,
        'tfidfvectorizer__max_df': max_df,
        'tfidfvectorizer__min_df': min_df,
        'logisticregression__C': log_C,
    }
    return param_grid


def grid_initialise_and_fit(model_name, param_grid, n_jobs, input_X, output_y):
    '''
    - initialises GridSearch \n
    - fits GridSearch for selected input and output
    '''
    grid_cv = GridSearchCV(estimator=model_name, param_grid=param_grid,
                           cv=5, return_train_score=True, scoring='accuracy', n_jobs=int(n_jobs))
    print("model is fitting... it may take a while!")
    grid_cv.fit(input_X, output_y)
    print('Model is fitted!')
    return grid_cv


def get_train_test_score(grid_cv):
    '''
    - gets best train_test score \n
    - returns a model with best hyperparameters
    '''
    col = [
        'mean_train_score',
        'mean_test_score',
        'rank_test_score'
    ]
    cv_results = pd.DataFrame(grid_cv.cv_results_)
    cv_score = cv_results[col].sort_values(
        by='rank_test_score', ascending=True)
    print(cv_score.iloc[0])
    return grid_cv.best_estimator_


def make_a_prediction(model):
    '''
    - makes a prediction for input strings.
    '''
    check = True
    while check == True:
        test = []
        word = input('please enter something to be predicted:')
        test.append(word)
        pred = model.predict_proba(test)
        print(pd.DataFrame(pred,
                           columns=model[1].classes_,
                           index=test
                           ))
        a = input('Do you want to make more predictions? "y/n":')
        if a == 'n':
            check = False
    exit()