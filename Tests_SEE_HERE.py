# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 18:22:53 2019

@author: orcuntasdemir
"""


""" Texts I made the model read """
def skim(text_file):
    
    string = text_process(text_file)
    read_these_sentences = text_real_sentences(string)
    
    distance_para_bin = model(text_file,
                      google_vectors,
                      pos_freq = pos_freq_matrix,
                      set_long_term_interest = 0.69,
                      set_short_term_interest = 0.79,
                      set_long_term_importance = 5,
                      set_short_term_importance = 3,
                      set_long_term_imp_limit = 3, 
                      set_short_term_imp_limit = 1,
                      how_many_sentences_to_read = len(read_these_sentences))
    #plot the sentences read
    #display_pca_scatterplot_vectors(vectors, "Metamorphosis by Franz Kafka")
    return distance_para_bin
    
    
 
bin_accumulate = []    
for i in range(5):
    dist_para_bin = skim("Sayingno.txt")
    bin_accumulate.append(dist_para_bin)
bin_accumulate = list(chain.from_iterable(bin_accumulate))
plt.hist(bin_accumulate, facecolor = 'blue', alpha= None)
plt.xlabel("Order of line within paragraph")
plt.ylabel("Total times that the nth rank sentence was read")
    


# string = text_process("Prince.txt")
# read_these_sentences = text_real_sentences(string)

# vectors = model('Prince.txt',
#                   google_vectors,
#                   pos_freq = pos_freq_matrix,
#                   set_long_term_interest = 0.69,
#                   set_short_term_interest = 0.79,
#                   set_long_term_importance = 7,
#                   set_short_term_importance = 4,
#                   how_many_sentences_to_read = len(read_these_sentences))


# #plot the sentences read
# display_pca_scatterplot_vectors(vectors, "Prince by by Niccolò Machiavelli")













