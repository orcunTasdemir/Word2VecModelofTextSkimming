# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:37:58 2019

@author: orcuntasdemir
"""

def display_pca_scatterplot(model, words=None, sample=0):
    if words == None:
        words = np.random.choice(list(model.vocab.keys()), sample)
    else:  
        word_vectors = np.array([model[w] for w in words])
        twodim = PCA().fit_transform(word_vectors)[:,:2]
        
        plt.figure(figsize=(12,12))
        plt.scatter(twodim[:,0], twodim[:,1], edgecolors='k', c='r')
        for word, (x,y) in zip(words, twodim):
            plt.text(x+0.05, y+0.05, word)
            
display_pca_scatterplot(glove_vectors, ['coffee', 'tea', 'beer', 'wine', 'brandy', 'rum', 'champagne', 'water',
                         'spaghetti', 'borscht', 'hamburger', 'pizza', 'falafel', 'sushi', 'meatballs',
                         'dog', 'horse', 'cat', 'monkey', 'parrot', 'koala', 'lizard',
                         'frog', 'toad', 'monkey', 'ape', 'kangaroo', 'wombat', 'wolf',
                         'france', 'germany', 'hungary', 'luxembourg', 'australia', 'fiji', 'china',
                         'homework', 'assignment', 'problem', 'exam', 'test', 'class',
                         'school', 'college', 'university', 'institute'])


#display the sentences read on a plot with your choice of the 
def display_pca_scatterplot_vectors(vectors, title):
    twodim = PCA().fit_transform(vectors)[:,:2]    
    plt.figure(figsize=(12,12))
    plt.title(title)
    plt.scatter(twodim[:,0], twodim[:,1], edgecolors='k', c='r')
    plt.xticks(np.arange(0, 1, 0.5))
    plt.yticks(np.arange(0, 1, 0.5))
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    
    
