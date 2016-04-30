import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn import cross_validation
from sklearn.metrics import classification_report
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

def load_file():   
    my = []
    data = []
    target = []
    with open('reviews_sorted/my.txt') as f:
        for line in f:
            my.append([n for n in line.strip().split('|')])
    for pair in my:
        try:
            data.append(pair[0])
            target.append(pair[1])
        except IndexError:
            print ("A line in the file doesn't have enough entries.")
    return data,target

def preprocess():
    data,target = load_file()
    count_vectorizer = CountVectorizer(binary='true')
    data = count_vectorizer.fit_transform(data)
    tfidf_data = TfidfTransformer(use_idf=False).fit_transform(data)
    return tfidf_data

def learn_model(data,target):
    data_train,data_test,target_train,target_test = cross_validation.train_test_split(data,target,test_size=0.4,random_state=43)
    #classifier = LogisticRegression().fit(data_train,target_train)
    #classifier = BernoulliNB().fit(data_train,target_train)
    classifier = DecisionTreeClassifier().fit(data_train,target_train)
    predicted = classifier.predict(data_test)
    #print(predicted)
    evaluate_model(target_test,predicted)

def evaluate_model(target_true,target_predicted):
    #print (classification_report(target_true,target_predicted))
    print ("Accuracy = {:.2%}".format(accuracy_score(target_true,target_predicted)))

def main():
    data,target = load_file()
    tf_idf = preprocess()
    learn_model(tf_idf,target)

main()
