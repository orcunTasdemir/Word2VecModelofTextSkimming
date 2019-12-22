# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:52:06 2019

@author: orcuntasdemir
"""

"""YOU NEED TO RUN THIS BEFORE RUNNING THE MODEL"""

"""
Creates the matrix that holds the part of speech and frequency scores for each word so that
I can refer to in in the model to assess the importance of a sentence.
"""
def create_pos_freq():
    text = open('allANC.txt', 'r',
                encoding = 'ascii',
               errors="surrogateescape")
    text
    str = text.read()

    #Loading the word2vec model
    #glove_vectors = KeyedVectors.load('glove_vectors', mmap='r')

    #Loading the google vectors
    #google_vectors = KeyedVectors.load('google_vectors', mmap='r')

    index_words_goog = set(google_vectors.index2word)

    index_words_glov = set(glove_vectors.index2word)

    anc = str.split()
    len(anc)/2

    stop_words = set(stopwords.words('english'))
    matrix = []

    #convert all '-' to '_' because in google vectors new_york not new-york
    str = re.sub(r"-","_", str)
    #all the words in this corpus is lower case anyways so we just split it.
    anc = str.split()

    for i in range(0, 594482, 4):
        print('{0}% Completed\r'.format((i/594482)*100), end='')
        if anc[i] in index_words_goog or anc[i] in index_words_glov:
            if anc[i] not in stop_words and len(anc[i])>2:
                if anc[i].find("'") == -1:
                    matrix.append([anc[i],anc[i+2],anc[i+3]])

    pos_freq = matrix
    return pos_freq


pos_freq_matrix = create_pos_freq()



""" IS THE WORD IN THE MATRIX """     
#gives you whether the word is in the pos_freq_matrix
def is_word_in_matrix(word, pos_freq_matrix):
    for index in pos_freq_matrix:
        if index[0] == word:
            return True
    return False      

#gives index of a word
def get_index(word, pos_freq_matrix):
    indx = 0
    for pair in pos_freq_matrix:
        if pair[0] == word:
            indx = indx + 1
            return indx
        else:
            indx = indx + 1
    return False    
 
""" GET PART OF SPEECH OF THE WORD """     
#gives you the part of speech information for the word
def get_pos(word, pos_freq_matrix):
    for index in pos_freq_matrix:
        if index[0] == word:
            return index[1]
        
"""     GET FREQUENCY OF THE WORD """        
#gives you the frequency information for the word
def get_freq(word, pos_freq_matrix):
    for index in pos_freq_matrix:
        if index[0] == word:
            return index[2]
        
def get_word(freq, pos_freq_matrix):
    for index in pos_freq_matrix:
        if index[2] == freq:
            return index[0]
        
        

