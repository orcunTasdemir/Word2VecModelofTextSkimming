# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:34:11 2019

@author: orcuntasdemir
"""
# -*- coding: utf-8 -*-

from itertools import chain
import sys
import math
import random
from statistics import mean
########################################################
import numpy as np
import matplotlib.pyplot as plt
########################################################
import gensim
from gensim.models import KeyedVectors
#from gensim.test.utils import common_texts
########################################################
import nltk
import nltk.data
from nltk.corpus import stopwords
########################################################
from scipy.spatial.distance import cosine
import scipy.sparse as sparse
from scipy import stats
########################################################
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
########################################################
import pandas as pd
########################################################
import re
import string

 ### IMPORTANT ###
# at least include a frequency constant that gets multiplied
#with the words vector before the addition process for the
#sentence vector calculation#


#do a matrix that you add the words that you already saw and
#accumulate the number of times you see it again

#further text processing where if when you get rid of ing or ed
#the word is still in the glove_vectors.vocab, keep it that way

print("#####################################")
print("Welcome to the Skim Reading Model:")
print("#####################################\n")

print("Loading the models...\n")
### LOAD THE MODELS ###
###############################################################
glove_vectors = KeyedVectors.load('glove_vectors', mmap='r')
print("Loaded the word2vec model\n")

google_vectors = KeyedVectors.load('google_vectors', mmap='r')
print("Loaded the google vectors\n")
###############################################################
print("############################")
print("THE FUNCTIONS")
print("############################\n")
##############################################################################################################
print("turn_word_list(word_vecs):\n", "Turning the word_vec query results to a list of the words returned\n " +
                                              "for it to be used by the display_pca_scatterplot function\n " +
                                                "it also can turn the weight_list into just the names of\n " +
                                                              "the words which helps for some for loops.\n")

print("display_pca_scatterplot(model, words=None, sample=0):\n", "Displays a scatterplot, takes a word list\n " +
                                                           "and one of the models and puts them in a graph\n")

print("get_freq_weights(sentences):\n", "Takes sentences from the model at each step and recalculates the\n " +
                                       "importances of the words in the text that is read so far.\n " +
                                 "Returns a new all_weights[] where we can access the weights again.\n")

print("get_weight(all_the_weights, word):\n", "Takes the list of all the weights and a word and returns the\n " +
                                                          "weight if the word is present in the weights yet.\n")

print("text_process(text_file):\n", "Takes a text file and processes it, removing stopwords, turning every\n " +
                                     "word to lower case, getting rid of contractions, and some more tweaks.\n")

print("get_similar_words(word, model):\n", "Takes model and a word and returns the 10 closest words.\n")

print("avg_sentence_vector(sentence, model):\n", "Returns an average word2vec vector for a sentence.\n")

print("sentence_similarity(sentence1, sentence2, model):\n", "Calculates the cosine similarity between the\n " +
                                                                   "averaged vectors of two sentence inputs.\n")

print("create_pos_freq():\n", "Creates a matrix of some 100.000 words with part of speech and frequency score.\n")

print("get_pos(word, pos_freq_matrix):\n", "Gives you the part of speech information for the word,\n " +
                                                   "searching it in the pos_freq_matrix passed down.\n")

    
##############################################################################################################
    

#pos_freq_matrix = create_pos_freq()





















