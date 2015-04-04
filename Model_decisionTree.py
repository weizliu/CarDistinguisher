#This is model for decision tree, it read samples and output classification report, confusion matrix, accuracy, decision tree and map from number to label name.
'''
If you want to run this file, you need to make some changes in scikit-learn package:
First, you need to modify fit function of pipeline.py as following:
    1)Adding parameter i_fold in the function header;
    2)Adding the following in line150(after calling __pre_tranform__ function):
            Xt = Xt.toarray() #this is to transform sparse matrix to dense one, which is required by decision tree interface;
    3)Then add the following right after Xt = Xt.toarray(), which can output decision tree into pdf format:
            clf = tree.DecisionTreeClassifier()
            clf = clt.fit(Xt, y)
            dot_data = StringIO()
            tree.export_graphviz(clf, out_file = dot_data)
            graph = pydot.graph_from_dot_data(dot_data.getvalue())
            graph.write_pdf(str(i_fold) + '.pdf')
      and in order to make this work, you also need to add the following in the beginning of the pipeline.py:
            from sklearn import tree
            from sklearn.external.six import StringIO
            import pydot
Second, you need to modify __pre_transform__ function of pipeline.py as following:
    1)Adding parameter i_fold in the function header(please do remember add it too when calling this function)
    2)Adding the following right after calling fit_transform(about row 125), which will output map from number to label name:
             map_feature_name = open(str(i_fold)+'_map_feature_name.txt', 'w')
             feature_name = transform.get_feature_names()
             count = 0
             for item in feature_name:
                 item = str(item.encode('utf-8')).rstrip()
                 map_feature_name.write(str(count) + ": " + item + '\n')
                 count += 1 
             map_feature_name.close()
      and in order to make this work, you also need to add the following in the beginning of the pipeline.py:
            import json
Third, you need to modify predict function in BaseDecisionTree class in sklearn/tree/tree.py as following:
    1)Adding X = X.toarray() in the beginning of the function, this is to make X dense.
      


'''
from sklearn import tree
from sklearn.externals.six import StringIO
import pydot 
from sklearn.feature_extraction.text import TfidfTransformer
import IPython
import sklearn as sk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import re
import csv
import os
from sklearn.cross_validation import cross_val_score, KFold
from sklearn import cross_validation
from scipy.stats import sem
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from sklearn import metrics


def read_data(dir, data, label_number, file_name):
    data_file_name = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    count = 0
    for item in data_file_name:
        if 'DS' in item:
            continue
        data_file_name_split = re.split('\.', item)
        userid = data_file_name_split[0]
        label = data_file_name_split[1]
        data_file = open(dir+item, 'r')
        file_name.append(dir+item)
        data_ob = csv.reader(data_file)
        data_per_sample = ''
        for  data_item in data_ob:
            data_per_sample = data_per_sample + data_item[0] + ' '

        data.append(data_per_sample)
        label_number.append(car_brands[label])
        data_file.close()


def train_and_evaluate(clf, X_train, X_test, y_train, y_test, i_fold):
    
    clf.fit(X_train, i_fold, y_train)
    
    print "Accuracy on training set:"
    print clf.score(X_train, y_train)
    print "Accuracy on testing set:"
    print clf.score(X_test, y_test)
    
    y_pred = clf.predict(X_test)
    
    print "Classification Report:"
    print metrics.classification_report(y_test, y_pred)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(y_test, y_pred)


def evaluate_cross_validation(clf, X, y):
    scores = cross_validation.StratifiedKFold(y, n_folds = 5)
    i_fold = 1;
    for tr, te in scores:
        xtr = [X[i] for i in tr]
        ytr = [y[i] for i in tr]
        xte = [X[i] for i in te]
        yte = [y[i] for i in te]
        train_and_evaluate(clf, xtr, xte, ytr, yte, i_fold)
        i_fold += 1
        

data = []
label_number = []
file_name = []
dir = 'samples1/'
car_brands = {'bmw': 0, 'honda': 1, 'jeep': 2, 'audi': 3, 'ford': 4, 'hyundai': 5, 'kia': 6, 'lexus': 7, 'mazda': 8, 'nissan': 9, 'toyota': 10, 'ferrari': 11}


read_data(dir, data, label_number, file_name)


clf_3 = Pipeline([
    ('vect', TfidfVectorizer()),
    ('clf', tree.DecisionTreeClassifier()),
])

evaluate_cross_validation(clf_3, data, label_number)


