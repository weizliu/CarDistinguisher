import os
import csv
import numpy as np
import re
from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib
from sklearn import metrics

'''this function is going to get the contend and label from the indexed documents 
the index should be train_index or test_index'''
def get_corpus_and_label(index, filenames, file_label, file_folder):
    doc_num = len(index)
    partial_file_corpus = []
    partial_file_label = np.zeros((doc_num), dtype = np.int)
    for ind in range(0, doc_num):
        '''get the label'''
        filename = filenames[index[ind]]
        partial_file_label[ind] = file_label[index[ind]]
        '''get the contend'''
        open_file = open(file_folder + filename, 'r')
        open_file_csv = csv.reader(open_file)
        data_per_sample = ''
        for item in open_file_csv:
            data_per_sample = data_per_sample + item[0] + ' '
        partial_file_corpus.append(data_per_sample)
        open_file.close()
    return partial_file_corpus, partial_file_label

'''main function begin here'''
'''define the car brand dictionary'''
car_brands = {'bmw': 0, 'honda': 1, 'jeep': 2, 'audi': 3, 'ford': 4, 'hyundai': 5, 'kia': 6, 'lexus': 7, 'mazda': 8, 'nissan': 9, 'toyota': 10, 'ferrari': 11}

'''define the data path and get the file names of this folder'''
file_folder = "Complte Dataset/"
filenames = os.listdir(file_folder)

'''remove the DS_Store document'''
for filename in filenames:
    if "DS" in filename:
        filenames.remove(filename)

'''get the labels of all documents'''
doc_num = len(filenames)
file_corpus = []
train_corpus = []
file_label = np.zeros((doc_num), dtype = np.int)
for ind in range(0, doc_num):
    filename = filenames[ind]
    file_name_split = re.split('\.', filename)
    #userid = file_name_split[0]
    label = file_name_split[1]
    file_label[ind] = car_brands[label]

'''divide the all documents into 5 folders'''
skf = cross_validation.StratifiedKFold(file_label, n_folds = 5)

'''test one folder, while other 4 folders are training folder'''
iter_num = 1;
for train_index, test_index in skf:
    #print("TRAIN:", train_index, "TEST:", test_index)
    train_corpus, train_label = get_corpus_and_label(train_index, filenames, file_label, file_folder)
    test_corpus, test_label = get_corpus_and_label(test_index, filenames, file_label, file_folder)
    vectorize = TfidfVectorizer(encoding='ISO-8859-1', sublinear_tf = True, max_df = 0.5, stop_words = 'english')
    train_data = vectorize.fit_transform(train_corpus)
    test_data = vectorize.transform(test_corpus)
    
    '''begin to training the data'''
    cPara_range = [1.0]
    cPara_range = list(np.logspace(-2,2,10)) # release this annotation and kill the previous sentence to run grid search
    parameters = {'C':cPara_range}
    clf = svm.SVC(kernel = 'linear')
    model_tunning = GridSearchCV(clf, param_grid = parameters)
    
    '''save the model'''
    model_tunning.fit(train_data, train_label)
    joblib.dump(model_tunning, 'training_model_%d.pkl' %(iter_num))
    
    '''load the model'''
    model_tunning = joblib.load('training_model_%d.pkl' %(iter_num)) 
    predict_labels = model_tunning.predict(test_data)

    print "Classification Report:"
    print metrics.classification_report(test_label, predict_labels)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(test_label, predict_labels)
    
    print 'finish test %d' %(iter_num)
    iter_num += 1

'''just for test, just ignore them'''
'''
index = [0,1,2,3,4,5]
partial_file_corpus, partial_file_label = get_corpus_and_label(index, filenames, file_label, file_folder)
#print filenames
print partial_file_corpus[0]
print partial_file_corpus[1]
print partial_file_corpus[2]
print partial_file_label
print filenames[0:3]
print len(partial_file_corpus)
'''






