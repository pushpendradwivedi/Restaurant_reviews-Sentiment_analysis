import nltk
import yaml
import csv

class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):
    def __init__(self):
        pass
        
    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

#text = """What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad. Apart from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."""
count = 0
f = open('food.csv','r',encoding='latin1')
csv_f = csv.reader(f)

for row in csv_f:
    count+=1
    if count<11000:
        print(count)
    elif count>=11000:
        text = row[3]
    
        splitter = Splitter()
        postagger = POSTagger()

        splitted_sentences = splitter.split(text)
    
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    
        class DictionaryTagger(object):
            def __init__(self, dictionary_paths):
                files = [open(path, 'r') for path in dictionary_paths]
                dictionaries = [yaml.load(dict_file) for dict_file in files]
                map(lambda x: x.close(), files)
                self.dictionary = {}
                self.max_key_size = 0
                for curr_dict in dictionaries:
                    for key in curr_dict:
                        if key in self.dictionary:
                            self.dictionary[key].extend(curr_dict[key])
                        else:
                            self.dictionary[key] = curr_dict[key]
                            self.max_key_size = max(self.max_key_size, 5000)
    
            def tag(self, postagged_sentences):
                return [self.tag_sentence(sentence) for sentence in postagged_sentences]
    
            def tag_sentence(self, sentence, tag_with_lemmas=False):
                """  the result is only one tagging of all the possible ones. The resulting tagging is determined by these two priority rules: - longest matches have higher priority - search is made from left to right"""
                tag_sentence = []
                N = len(sentence)
                if self.max_key_size == 0:
                    self.max_key_size = N
                i = 0
                while (i < N):
                    j = min(i + self.max_key_size, N) #avoid overflow
                    tagged = False
                    while (j > i):
                        expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                        expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                        if tag_with_lemmas:
                            literal = expression_lemma
                        else:
                            literal = expression_form
                        if literal in self.dictionary:
                            #self.logger.debug("found: %s" % literal)
                            is_single_token = j - i == 1
                            original_position = i
                            i = j
                            taggings = [tag for tag in self.dictionary[literal]]
                            tagged_expression = (expression_form, expression_lemma, taggings)
                            if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                                original_token_tagging = sentence[original_position][2]
                                tagged_expression[2].extend(original_token_tagging)
                            tag_sentence.append(tagged_expression)
                            tagged = True
                        else:
                            j = j - 1
                    if not tagged:
                        tag_sentence.append(sentence[i])
                        i += 1
                return tag_sentence
        
        dicttagger = DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml'])
        
        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        
        def value_of(sentiment):
            if sentiment == 'positive': return 1
            if sentiment == 'negative': return -1
            return 0
        
        def sentiment_score(review):    
            return sum ([value_of(tag) for sentence in dict_tagged_sentences for token in sentence for tag in token[2]])
        
        senti=sentiment_score(dict_tagged_sentences)
        print(count,senti)
        
        if senti<0:
            f=open('reviews_sorted/neg_reviews.txt','a',encoding='latin1')
            f.write(text)
            f.write('\n')
            f.close()
        elif senti>0:
            f=open('reviews_sorted/pos_reviews.txt','a',encoding='latin1')
            f.write(text)
            f.write('\n')
            f.close()
        else:
            f=open('reviews_sorted/ntrl_reviews.txt','a',encoding='latin1')
            f.write(text)
            f.write('\n')
            f.close()
        
