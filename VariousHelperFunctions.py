# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 22:01:10 2019

@author: orcuntasdemir
"""

############################################################
###   Get similar words from the model of your choice   ####
############################################################
def get_similar_words(word, model):
    words=[]
    for word_couple in glove_vectors.most_similar(word):
        words.append(word_couple[0])
    return words

#################################################################
### Function to get an averaged feature vector for a sentence ###
#################################################################
def avg_sentence_vector(sentence, model, pos_freq_matrix):
    index_words_set = set(model.index2word)
    words = sentence.split()
    feature_vector = np.zeros((300,), dtype='float32')
    n_words = 0
    for word_count in range(len(sentence.split())):
        if words[word_count] in index_words_set:
            n_words += 1
            if is_word_in_matrix(words[word_count], pos_freq_matrix):
                rating1 = get_pos_rating(get_pos(words[word_count], pos_freq_matrix))
                rating2 = get_frequency_rating(words[word_count])
                #rating gets multiplied into the sentence
                vec_add = model[words[word_count]] * rating1 * rating2
                feature_vector = np.add(feature_vector, vec_add)
            else:
                feature_vector = np.add(feature_vector, model[words[word_count]])
    if(n_words > 0):
        feature_vector = np.divide(feature_vector, n_words)
    return feature_vector  


######################################################################################## 
############              Gives special ratings for pos types               ############
########################################################################################
def get_pos_rating(pos):
    rating = 1
    if pos[0:2] == 'NN':
        rating = 4
    elif pos[0:2] == 'VB':
        rating = 3
    elif pos in ('RB', 'RBR', 'RBS', 'PRP'):   
        rating = 0.01
    elif pos in ('CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD'):
        rating = 0.5
    elif pos in ('PDT', 'POS', 'PRP', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WRB'):
        rating = 0
    return rating    

###################################################################
####   Takes two average sentence vectors and gives you the    ####
####   sentence similarity score                               ####
###################################################################
def sentence_similarity(sentence1, sentence2, model, pos_freq):
    sen1 = avg_sentence_vector(sentence1, model, pos_freq_matrix)
    sen2 = avg_sentence_vector(sentence2, model, pos_freq_matrix)

    return 1-cosine(sen1, sen2)

""" Eliminates the words that are above or below some frequency level. """
def frequency_filter(sentence, pos_freq_matrix):
    output_sentence = sentence
    for word in sentence.split():
        if is_word_in_matrix(word, pos_freq_matrix):
            frequency = get_freq(word, pos_freq_matrix)
            # print(type(frequency))
            # print(frequency)
            if int(frequency) > 5039:
                output_sentence = re.sub(word,'', output_sentence)
        else:
            continue
    return output_sentence
    

ret = frequency_filter('yeah like would no bus', pos_freq_matrix)

#ratings from the frequency matrix
# def get_frequency_rating(word):
#     if is_word_in_matrix(word, pos_freq_matrix):
#             frequency = get_freq(word, pos_freq_matrix)
#             top_freq = int(pos_freq_matrix[0][2])
#             rating = (top_freq - int(frequency))/top_freq
#             #rating = math.pow((int(frequency)/int(pos_freq_matrix[0][2])), -1)
#     return rating
    
def get_frequency_rating(word):
    if is_word_in_matrix(word, pos_freq_matrix):
            for i in range(len(pos_freq_matrix)):
                if word == pos_freq_matrix[i][0]:
                    rating = i / len(pos_freq_matrix)
    return rating
    
              
    
