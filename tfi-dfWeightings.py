# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:58:34 2019

@author: orcuntasdemir
"""

#A function implementation to create tfi-df weightings
#for the words in the text as we read the text per sentence

def get_tfi_weights(sentences):
    
    # sentences = []
    # with open('metamor.txt') as file:
    #     for line in file:
    #         for l in re.split(r"\.\s|\?\s|\!\s|\n",line):
    #             if l:
    #                 sentences.append(l)

    #The details of converting the text document to a matrix of token counts
    cvec = CountVectorizer(stop_words='english', min_df=0, max_df=10, ngram_range=(1,1))
    #Using the converter, get an array of samples and features, the term-document matrix.
    #It is a sparse matrix
    sf = cvec.fit_transform(sentences)
    
    #Transforms the count matrix into a normalized tf representation in our case
    transformer = TfidfTransformer()
    #this is where we transform the count matrix into the weight pairings for the words
    #where sentences will act like documents and add the inverse-document-aspect to our
    #word frequency query.
    transformed_weights = transformer.fit_transform(sf)
    
    #getting the actual weights for words by taking the mean of every sparse matrix
    #ravel flattens the nparray and tolist puts all the weights generated into a list
    weights = np.asarray(transformed_weights.mean(axis=0)).ravel().tolist()
    #for weight in weights:
    
    tfi_matrix = np.empty((0,2))

    for i in range(len(weights)):
        we = weights[i]
        fe = cvec.get_feature_names()[i]    
        list = [we, fe]
        tfi_matrix = np.append(tfi_matrix, list)
        
    size = int(round(len(tfi_matrix))/2)
    tfi_matrix = np.reshape(tfi_matrix, (size, 2))
    
    tfi_matrix = tfi_matrix[np.lexsort(np.fliplr
                                        (tfi_matrix).T)]
    
    tfi_matrix = np.flip(tfi_matrix, 0)
    
    # for i in range(len(tfi_matrix)):
    #     if len((tfi_matrix[i,1]).split()) > 1:
    #         tfi_matrix = np.delete(tfi_matrix, i, 0)
        
    
    return tfi_matrix



#gets the weight of a specific word from the
#importance weights matrix created
    
# def get_weight(all_the_weights, word):
#     if word in all_the_weights['term']:
#         for word_pair in all_the_weights:
#             if word_pair[0] == word:
#                 return word_pair[1]
#     else:
#         return 0   

tfi = get_tfi_weights(['I mean just what I', ' The only advantage to this method is that the " argument is a list of the fields to order the search by. For example, you can sort by the second column, then the third column, then the first column by supplying'])


def get_words(num, all_weights):
    words = []
    for i in range(num):
        words.append(all_weights[i][1])
        if i == num or i == len(all_weights):
            break
    return words
    






tfi = get_tfi_weights([' $ one morning gregor samsa woke troubled dreams found transformed bed horrible vermin',
                        ' lay armour_like back lifted head little could see brown belly slightly domed divided arches stiff sections', ''])















