import sys,re
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':

    data_dir = sys.argv[0]
    print(data_dir)
    
    # Read the data
    train_labels = []
    test_labels = []
    
    f = open('reviews_sorted/neg_reviews.txt','r',encoding='latin1')    
    f1 = open('reviews_sorted/pos_reviews.txt','r',encoding='latin1')
    
    posSentences = re.split(r'\n', f1.read())
    negSentences = re.split(r'\n', f.read())
    
    trainFeatures = posSentences[:800] + negSentences[:800]
    testFeatures = posSentences[800:1000] + negSentences[800:]
    print("Train data: ",len(trainFeatures))
    print("Test data: ",len(testFeatures))
    print("")

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(trainFeatures)    
    test_vectors = vectorizer.transform(testFeatures)


    class1 = ['pos']
    class2 = ['neg']
    for i in range(0,1600):
        if i<800:
            train_labels.append(class1)
        else:
            train_labels.append(class2)
    
    for i in range(0,326):
        if i<200:
            test_labels.append(class1)
        else:
            test_labels.append(class2)
    
    # Perform classification with SVM, kernel=rbf
    classifier_rbf = svm.SVC()
    t0 = time.time()
    classifier_rbf.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_rbf = classifier_rbf.predict(test_vectors)
    t2 = time.time()
    time_rbf_train = t1-t0
    time_rbf_predict = t2-t1

    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1-t0
    time_linear_predict = t2-t1

    # Perform classification with SVM, kernel=linear
    classifier_liblinear = svm.LinearSVC()
    t0 = time.time()
    classifier_liblinear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_liblinear = classifier_liblinear.predict(test_vectors)
    t2 = time.time()
    time_liblinear_train = t1-t0
    time_liblinear_predict = t2-t1

    # Print results in a nice table
    print("SVC(kernel=rbf):")
    print("Training time: %fs\nPrediction time: %fs" % (time_rbf_train, time_rbf_predict))
    print("Accuracy = ",accuracy_score(test_labels, prediction_rbf)*100,'%')
    print("")
    print("SVC(kernel=linear):")
    print("Training time: %fs\nPrediction time: %fs" % (time_linear_train, time_linear_predict))
    print("Accuracy = ",accuracy_score(test_labels, prediction_linear)*100,'%')
    print("")
    #print("LinearSVC:")
    #print("Training time: %fs\nPrediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
    #print("Accuracy = ",accuracy_score(test_labels, prediction_liblinear)*100,'%')
