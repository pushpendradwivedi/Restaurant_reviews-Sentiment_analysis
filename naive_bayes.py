import re, math, collections, itertools
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

def evaluate_features(feature_select):
        
        posSentences = open('reviews_sorted/pos_reviews.txt', 'r',encoding='latin1')
        negSentences = open('reviews_sorted/neg_reviews.txt', 'r',encoding='latin1')
        posSentences = re.split(r'\n', posSentences.read())
        negSentences = re.split(r'\n', negSentences.read())
 
        posFeatures = []
        negFeatures = []

        #breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
        for i in posSentences:
                posWords = re.findall(r"[\w']+|[.,!?;]", i)
                posWords = [feature_select(posWords), 'pos']
                posFeatures.append(posWords)
        for i in negSentences:
                negWords = re.findall(r"[\w']+|[.,!?;]", i)
                negWords = [feature_select(negWords), 'neg']
                negFeatures.append(negWords)

        #selects 3/4 of the features to be used for training and 1/4 to be used for testing
        #posCutoff = int(math.floor(len(posFeatures)*3/4))
        negCutoff = int(math.floor(len(negFeatures)*3/4))
        trainFeatures = posFeatures[:800] + negFeatures[:800]
        testFeatures = posFeatures[800:1000] + negFeatures[800:]

        classifier = NaiveBayesClassifier.train(trainFeatures)

        referenceSets = collections.defaultdict(set)
        testSets = collections.defaultdict(set)
        
        for i, (features, label) in enumerate(testFeatures):
                referenceSets[label].add(i)
                predicted = classifier.classify(features)
                testSets[predicted].add(i)

        print ("Train on %d instances\nTest on %d instances" % (len(trainFeatures), len(testFeatures)))
        print ("Accuracy:", nltk.classify.util.accuracy(classifier, testFeatures)*100,'%')
        classifier.show_most_informative_features(10)

def make_full_dict(words):
    return dict([(word, True) for word in words])

evaluate_features(make_full_dict)
