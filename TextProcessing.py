# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:37:25 2019

@author: orcuntasdemir
"""

def text_process(text_file):

    #What I need to do is to get the text file
    text = open(text_file, encoding="utf8")

    #Read it into a string file, get rid of the '\n' symbols from the beginning
    str = text.read().replace('\n\n',' $ ') #.replace('\n',' ') #

    #Everything to lower-case
    str = str.lower() #Everything is lower case

    #get a contractions dictionary
    contractions = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had", #got rid of he would
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "I had",
    "i'd've": "I would have",
    "i'll": "I will",
    "i'll've": "I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }

    #get rid of contractions

    for word in str.split():
        if word.lower() in contractions:
            str = str.replace(word, contractions[word.lower()])



    #replace '-' that is connecting some of the words with _ so that it is one word we can look
    #up from the vocabulary from word2vec vectors
    str = re.sub(r"-","_", str)
    
    #and also get rid of quotations
    #str = re.sub(r'"'," ", str)    
    
    #and also get rid of semicolons
    str = re.sub(r';'," ", str) 
    
    #and also get rid of colons
    str = re.sub(r':'," ", str) 
    
    #Also get rid of commas, which are not that important in this case anyways
    str = re.sub(r','," ", str)    
    
    #remove numbers
    str = re.sub(r'\d+', '', str)
    
    #Now get rid of all the other 's' knowing that they are possesive
    str = re.sub("s\'", "", str)
    str = re.sub("\'s", "", str)
    
    #get rid of the weird first 3 characters in the text 
    str = str[3:len(str)]
    
    #place specific marking for beginnings of paragraphs if there are any
    
    
    #And finally get rid of the stop words
    stop_words = set(stopwords.words('english'))    
    words = str.split()
    str_list = [word for word in words if word not in stop_words]
    str = " ".join(str_list)
    
    str += "..."
    str += "!"
                       
    return str

"""FOR READING
for reading use text_process function and put the output string into text_real_sentence to get
the sentence that we are going to read through in the model"""

def text_real_sentences(string1):

    #What I need to do is to get the text file
    #text = open(text_file, 'r')

    #Read it into a string file, get rid of the '\n' symbols from the beginning
    #str = text.read().replace('\n\n',' $ ') #.replace('\n',' ') #

    tokens = nltk.word_tokenize(string1) 
    
    quotations = ['"', "'", '``', "''"]
    sentence_ending_punc = ['.', '?', '!', '...']
    
    not_sentence = False
    
    all_sentences_list = []
    sentence = ""
    
    for tok_count in range(len(tokens)):
        curtok = tokens[tok_count]
        if curtok not in sentence_ending_punc:
            if tokens[tok_count] in quotations:
                not_sentence = not not_sentence
                sentence += " " + (tokens[tok_count])
            else:
                sentence += " " + (tokens[tok_count])
        elif not_sentence == True:
            sentence += " " + (tokens[tok_count])
        else:
            all_sentences_list.append(sentence)
            sentence = ""  
    
    all_sentences_list_r = []   

    for sentence in all_sentences_list:
        sentence1 = sentence.replace('"', "")
        sentence1 = sentence1.replace("'", "")
        sentence1 = sentence1.replace("''", "")
        sentence1 = sentence1.replace('``', "")
        all_sentences_list_r.append(sentence1)
    
    return all_sentences_list_r



"""THIS FUNCTION ONLY FOR DISPLAY:
    put the text file into this function to generate the sentences that we are actually
    reading but without missing words. The sentence boundaries will be the same because
    the tokenizer is used the same way, we will refer to this to display the sentences 
    that our model read in full length"""
def text_real_sentences_display(text_file):

    #What I need to do is to get the text file
    text = open(text_file, encoding="utf8")

    #Read it into a string file, get rid of the '\n' symbols from the beginning
    str = text.read().replace('\n\n',' $ ') #.replace('\n',' ') #

    tokens = nltk.word_tokenize(str) 
    
    quotations = ['"', "'", '``', "''"]
    sentence_ending_punc = ['.', '?', '!', '...']
    
    not_sentence = False
    
    all_sentences_list = []
    sentence = ""
    
    for tok_count in range(len(tokens)):
        curtok = tokens[tok_count]
        if curtok not in sentence_ending_punc:
            if tokens[tok_count] in quotations:
                not_sentence = not not_sentence
                sentence += " " + (tokens[tok_count])
            else:
                sentence += " " + (tokens[tok_count])
        elif not_sentence == True and len(sentence.split()) < 20:
            sentence += " " + (tokens[tok_count])
        else:
            sentence += "."
            all_sentences_list.append(sentence)
            sentence = ""  
     
    all_sentences_list_return = []
    for sentence in all_sentences_list:
        #sentence1 = sentence.replace('"', "")
        #sentence1 = sentence1.replace("'", "")
        #this is going to make our sentences look better because the quotations are
        #all going to be the same double quotation character --> "
        #The dollar sign will be converted into an empty line to recreate the paragraph divsions
        sentence1 = sentence.replace("''", '"')
        sentence1 = sentence1.replace('``', '"')
        #sentence1 = sentence1.replace("$", "\n\n")
        all_sentences_list_return.append(sentence1)
    
    return all_sentences_list_return

# string = text_process("metamor.txt")
# read_sentences_example = text_real_sentences(string)

# real_sentences_display_example = text_real_sentences_display("metamor.txt")


# tokens = nltk.word_tokenize(string) 




# #What I need to do is to get the text file
# text = open("metamor.txt", 'r')

# #Read it into a string file, get rid of the '\n' symbols from the beginning
# str = text.read().replace('\n\n',' $ ') #.replace('\n',' ') #

# tokens = nltk.word_tokenize(str) 
