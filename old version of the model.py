# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:33:47 2019

@author: orcuntasdemir
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:22:02 2019

@author: orcuntasdemir
"""
#Here is the start of our model

sens_sim = sentence_similarity("one morning gregor samsa woke troubled dreams found transformed bed horrible vermin"
                               ,"lay armour_like back lifted head little could see brown belly slightly domed divided arches stiff sections", 
                               google_vectors,
                               pos_freq_matrix)


def model(text_string,
          model,
          pos_freq = pos_freq_matrix,
          set_long_term_interest = 0.59,
          set_short_term_interest = 0.69,
          set_long_term_importance = 5,
          set_short_term_importance = 2):
    
    long_term_interest = set_long_term_interest
    short_term_interest = set_short_term_interest
    long_term_importance = set_long_term_importance
    short_term_importance = set_short_term_importance
    
    
    """Preprocessing the string"""
    str = text_process(text_string)
    #The text process function also puts a $ at the beginnings of paragraphs which will be helpful
    #because I want to positively discriminate paragraph beginnings
    
    """tokenizing all the words and punctuation in the text document"""
    tokens = nltk.word_tokenize(str) 
    
    
    """sentence ending punctuations are important for us"""
    sentence_ending_punc = ['.', '?', '!', '...']
    #where the first sentence ending is
    first_sent_end = [(tokens.index('.')),
                      (tokens.index('...')),
                      (tokens.index('?')),
                      (tokens.index('!'))]
    where_first_period = min(first_sent_end) 
    
    
    
    """
    ###########################################################################################################"""    
    """parameters"""
    longest_read = 7             #longest string of sentences that it is allowed to read
    not_read_count = 0                                      #dont read until this time...
    sent_read_aft_jump = 0
    #interest = eg.0.29    #interest where if the sentence is below this level of similarity I wanna read
                           #because it is probably something different      
    
    #Creation of some empty string variables to hold the several different sentences    
    #the current sentence
    sentence = ""
    #the very first sentence of the text is important to start the satisfaction measurement
    first_sentence = ""
    #The first sentence of the reading loop
    sentence1 = ""
    #the last sentence that we read the last loop is also important to store
    last_sentence = ""
    #The list we store all the similarity values
    sim_list = []
    #Our average vector storage for the sentences read
    avg_vectors_bin = []
    #distance from the paragraph beginning
    dist_para = 1
    #sentence counter to see which sentence on the text that we are at
    sentence_counter = 2
    
    read_string = ""
    """
    ###########################################################################################################"""    


    """
    ##############################################################
    ####      Here we start reading "skimming" the text       ####
    ##############################################################"""
    
    #We will read, at least skim the entire thing so our limit is len(tokens)
    for tok_count in range(300):# range(len(tokens)):  #curtok will indetify the current token we have on the for loop
        curtok = tokens[tok_count]
        
             
        if curtok not in sentence_ending_punc:
            if tokens[tok_count] == '$':
                dist_para = 1
            else:
                sentence += " " + (tokens[tok_count])
                #print(sentence)
                
        
        #################################################################
        ####      if we see the sentence end we will append it       ####
        ####      to sentence1 or sentence 2 according to whether    ####
        ####      sentence 1 is full or not                          ####
        #################################################################
        
        else :
            #if it was the first sentence get the avg_sentence_vector
            if where_first_period == tok_count and first_sentence != 'c':
                first_sentence = sentence
                #dist_para +=1
                print("\nfirst sentence: ", first_sentence)
                print("\ndistance from the beginning of the paragraph: ", dist_para)
                
                first_sentence_avg = avg_sentence_vector(sentence, model, pos_freq)
                #print("first_sentence_avg: ", first_sentence_avg)
                sentence = ""
                                
            #if sentence one is not full, add to sentence one
            elif sentence1 == "":
                sentence1 = sentence
                dist_para +=1
                print("\nsentence", sentence_counter, ": ", sentence1)
                print("\ndistance from the beginning of the paragraph: ", dist_para)
                sentence_counter += 1
                sentence = ""
                
                #if we are here, it means that both the sentences were full, implement the cosine similarity function
                #print('false or true', first_sentence != "c")
                if first_sentence != "c": #as in "completed"
                    #print(first_sentence)
                    #print(sentence1)
                    sens_sim = sentence_similarity(first_sentence, sentence1, model, pos_freq)
                    
                    print("\nSentence_similarity no", (sentence_counter - 2),": ", sens_sim)
                    sim_list.append(sens_sim)
                    #after it is c, we will never go into this line again
                    
                    #also calculate the similarity between first and the second sentences
                    #sens_sim2 = sentence_similarity(sentence1, sentence2, model, pos_freq)
                    #print("second_sim: ", sens_sim2)
                    #sim_list.append(sens_sim2)
                    
                    #memorize the average feature vector for the last sentence so that we can compare it to the next "first" sentence, (sentence1)                    
                    last_sentence = sentence1
                    
                    first_avg_vector = avg_sentence_vector(first_sentence, model, pos_freq)
                    last_avg_vector = avg_sentence_vector(last_sentence, model, pos_freq)
                    
                    
                    avg_vectors_bin.append(first_avg_vector)
                    avg_vectors_bin.append(last_avg_vector)
                    
                    #before emptying our sentences the decisions to whether read the sentence or not will be given
                    #these decisions will be depending on the theory of optimal foraging, and I will assume that the
                    #chances for our reader to read the next sentence is whether the similarity between the last 2 sentence
                    #they read were very low, or whether it was very high, they will either want to keep reading in a situation
                    #where they want more information, or they want new information.
                    
                    read_string += first_sentence + "."
                    read_string += sentence1 + "."     #since these are the first three sentences I have rather loose decision boundaries
                    sent_read_aft_jump = 2             #we are setting this to two so that we know we have read 2 sentences uninterrupted so far
                    sent_read_total = 2       #total sentences read so that we know what similarities to average
                    #dist_para = sent_read_total
                    
                        
                    
                    #empty out the sentence one or two so that we can use them again in the second loop
                    first_sentence = "c"
                    sentence = ""
                    sentence1 = ""
                    
                    
                    #all the other times that we are not in the beginning of the text document
                #calculate the sentence similarity in terms of cosine similarity
                    
                    
                ##########################################################################################
                ####   This is where the code actually happens after the first two sentences,         ####
                ####   the jump decisions are taken, jumps terminated, similarity list is also        ####
                ####   constructed here. Long_term and short_term mean similarities are also          ####
                ####   calculated here alongsisde the important word counts and dist_para corrections ####
                ##########################################################################################
                    
                    
                else:                
                    #print(sentence1)
                    #print(sentence2)
                    
                    #print("sens_sim: ", sens_sim)
                    #also calculate the similarity between first and the second sentences
                    #sens_sim2 = sentence_similarity(sentence1, sentence2, model, pos_freq)
                    
                    #sim_list.append(sens_sim2)
                    #print("second_sim: ", sens_sim2)                    
                    #before emptying our sentences and also before resetting our last_sentence the decisions to whether read the sentence or not will be given
                    #these decisions will be depending on the theory of optimal foraging, and I will assume that the
                    #chances for our reader to read the next sentence is whether the similarity between the last 2 sentence
                    #they read were very low, or whether it was very high, they will either want to keep reading in a situation
                    #where they want more information, or they want new information.
                    
                    #learning_rate = 0.05  # 5% is our correction for the interest parameters
                    print("\nSentence_similarity_list_length: ", len(sim_list))
                    # if len(sim_list) == 10:
                    #     return sim_list
                    #ONLY FOR THE FIRST TWO SENTENCE WHICH MEANS THAT IT IS GOING TO RUN ONLY ONCE
                    if len(sim_list) == 1:
                        count = 1
                        print("SIMILARITY LIST LENGTH IS 1")
                        print("SIM LIST ITSELF: ", sim_list)
                        long_term_mean_sim = mean(sim_list)
                        print("long_term_mean_sim no", count, ": ", long_term_mean_sim)
                        short_term_mean_sim = mean(sim_list)
                        print("long_term_mean_sim no", count, ": ", long_term_mean_sim)
                        count += 1
                        
                        short_importance = 0
                        long_importance = 0
                        
                        #generate the first version of the ongoing word frequency vector
                        #which is going to assist our decision protocol
                        # read_sentences = []
                        # for sentence in read_string.split('.'):
                        #     read_sentences.append(sentence)
                        read_sentences = read_string.split()
                        #print(read_string)
                        print(read_sentences)
                        #print("vfvfdvfdv")
                        all_tfi_weights = get_tfi_weights(read_sentences)
                        #return all_tfi_weights
                        imp_words = get_words(min(short_term_importance, len(all_tfi_weights)), all_tfi_weights)
                        words= []
                        for sentence in read_sentences:
                            words.append(sentence.split())
                        for word in words:
                            if word in imp_words:
                                short_importance = short_importance + 1  
                                long_importance = long_importance + 1 
                        print('first_short_importance for first: ', short_importance)
                        print('first_long_importance for first: ', long_importance)
                        
                    else:
                        long_term_mean_sim = mean(sim_list[-3:])
                        print(sim_list[-3:])
                        print('long_term_mean_sim: ', long_term_mean_sim)
                        short_term_mean_sim = mean(sim_list[-1:])
                        print('short_term_mean_sim: ', short_term_mean_sim)
                        
                        read_sentences = read_string.split('.')
                        
                        #it counts the number of important words the last sentence we read has.
                        #print(read_sentences)
                        short_tfi_weights = get_tfi_weights(read_sentences[-3:])
                        #return short_tfi_weights
                        #num = min(short_term_importance, len(short_tfi_weights))
                        short_term_imp_words = get_words(min(short_term_importance, len(short_tfi_weights)), short_tfi_weights)
                        for word in last_sentence.split():   
                            short_importance = 0
                            if word in short_term_imp_words[0:]:
                                short_importance = short_importance + 1
                                
                        #it counts the number of important word we encountered in the last
                        #three sentences that we read
                        all_tfi_weights = get_tfi_weights(read_sentences)        
                        long_term_imp_words = get_words(min(long_term_importance, len(all_tfi_weights)), all_tfi_weights)
                        last_n_sentences = read_sentences[-(long_term_importance):]
                        words = []
                        for sentence in last_n_sentences:                            
                            words.append(sentence.split())
                        for word in words:   
                            if word in long_term_imp_words[0:]:
                                long_importance = long_importance + 1
                                
                        print('first_short_importance: ', short_importance)
                        print('first_long_importance: ', long_importance)
                            
                    #set the variables for the interest and importance depending on where I am on the paragraph
                    multip = dist_para_correction(dist_para)
                    print("multip: ", multip)
                    
                    long_term_interest = set_long_term_interest * multip
                    print("long term int: ", long_term_interest)
                    
                    short_term_interest = set_short_term_interest * multip
                    print("short_term_interest: ", short_term_interest)
                    
                    long_term_importance = round(-(math.log(dist_para, 50)) + set_long_term_importance)
                    print("long_term_importance: ", long_term_importance)
                    
                    short_term_importance = round(-(math.log(dist_para, 50)) + set_short_term_importance)  
                    print("short_term_importance: ", short_term_importance)
                    
                    
                    if last_sentence != "" and not_read_count == 0: #if we were reading already  last_sentence in read_string
                        print("WE ARE READING")
                        print("sim_list_len: ", len(sim_list))
                        if  sent_read_aft_jump < longest_read: #if smaller than the limit                           
                            print("long term mean sim: ", long_term_mean_sim)
                            print("long_term_interest: ", long_term_interest)
                            if  long_term_mean_sim < long_term_interest:
                                #print('here000000000000000000000000000000000000000000000000000000000000000000000')
                                if random.choices([1, 0], [0.8, 0.2]) == [1]:#[(1-long_term_mean_sim), long_term_mean_sim]) == 1:
                                    print('CHOICE TO KEEP READING')
                                    print("last sentence: ", last_sentence)
                                    sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)
                                    sim_list.append(sens_sim)
                                    print('sens_sim for sentence 1:', sens_sim)
                                    sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                                    avg_vectors_bin.append(sentence1_avg_vector)                                    
                                    read_string += sentence1 + "."
                                    sent_read_aft_jump += 1
                                    sent_read_total += 1
                                    #dist_para += 1
                                    #memorize this for learning
                                    # sim_skipped_for_long = long_term_mean_sim
                                    # sim_skipped_for_long_bin.append(sim_skipped_for_long)
                                    # if sim_skipped_for_long + 0.1 <= long_term_interest:
                                    #     long_term_interest = long_term_interest - learning_rate
                                    
                            elif short_term_mean_sim < short_term_interest:
                                if random.choices([1, 0], [0.8, 0.2]) == [1]:
                                    print('here000000000000000000000000000000000000000000000000000000000000000000000')
                                    #if similarity is smaller than this I might not wanna continue reading
                                    sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)
                                    print("long term mean sim: ", long_term_mean_sim)
                                    sim_list.append(sens_sim)
                                    sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                                    avg_vectors_bin.append(sentence1_avg_vector)
                                    read_string += sentence1 + "."
                                    sent_read_aft_jump += 1
                                    sent_read_total += 1
                                    #dist_para += 1
                                    #memorize this for learning
                                    # sim_skipped_for_short = short_term_mean_sim
                                    # sim_skipped_for_short_bin.append(sim_skipped_for_short)
                                    # if sim_skipped_for_short + 0.1 <= short_term_interest:
                                    #     short_term_interest = short_term_interest - learning_rate
                            #this is going to be a special case about whether I just read a word
                            #on the last sentence that wants me to keep reading because it has been
                            #an important word in the context of this text I am reading so far
                            # if 1the last sentence had more than 1 important word in the last 3 sentences' tfi,
                            elif len(sim_list) > 1:
                                print("sim_list_len: ", len(sim_list))
                                if short_importance > 1:
                                    #then there is a fifty fifty chance of reading the next sentence
                                    #since if we are at this eilf, it means that the sentence was not
                                    #already interesting in terms of the past two conditions anyways.
                                    #if greater than 2, we are definitely going to read
                                    if short_importance == 2 or random.choice([0, 1], [0.5, 0.5]) == [1]:
                                        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                                        sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)  
                                        print("long term mean sim: ", long_term_mean_sim)
                                        sim_list.append(sens_sim)
                                        sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                                        avg_vectors_bin.append(sentence1_avg_vector)
                                        read_string += sentence1 + "."
                                        sent_read_aft_jump += 1
                                        sent_read_total += 1
                                        #dist_para += 1
                                #if there have been more than 3 words of importance in the
                                #last three sentences we read out of the entire portion of the text we have
                                #been, reading, go into this elif.
                                elif long_importance > 3:
                                    #if we encountered at least 4 words of importance in the last three sentences or if we
                                    #randomly select a 1 out of a fifty fifty probability, we read the next sentence.
                                    if long_importance >=4 or random.choices([0, 1], [0.5, 0.5]) == [1]:
                                        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                                        sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)  
                                        print("long term mean sim: ", long_term_mean_sim)
                                        sim_list.append(sens_sim)
                                        sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                                        avg_vectors_bin.append(sentence1_avg_vector)
                                        read_string += sentence1 + "."
                                        sent_read_aft_jump += 1
                                        sent_read_total += 1
                                        #dist_para += 1
                                        
                                
                                else:
                                    print("JUMPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                                    #if long term similarity is higher than the short term similarity
                                    #then I am going to jump smaller with the hope that I might still land
                                    #at a location where it is relevant information wrt the long term.
                                    if long_term_mean_sim > short_term_mean_sim:
                                        #if all that and the long_importance words were 0, it means that I am
                                        #straying further from a coherent paragraph
                                        jump_param = 1- short_term_mean_sim
                                        jump = np.random.normal((jump_param*10), 2, 1)
                                        not_read_count = int(jump)
                                    #if opposite I am going to want to jump depending on the leng_term_similarity
                                    #because the lack of that is what is triggering me to jump.
                                    elif long_term_mean_sim < short_term_mean_sim:
                                        jump_param = 1- long_term_mean_sim
                                        jump = np.random.normal((jump_param*10), 2, 1)
                                        not_read_count = int(jump)
                                    #if none of those are satisfied above I want to look at the short importance
                                    #and jump over 1 sentence if it is zero
                                    elif short_importance == 0:
                                       jump = 1
                                       not_read_count = jump
                                    #else I want to jump around 4 sentences
                                    else :
                                       jump = np.random.normal(4, 2, 1)
                                       not_read_count = int(jump)                           
                                    if not_read_count > 7:
                                        not_read_count = 7 # to normalize for the normal distribution
                                    print(not_read_count)
                                    
                        else:
                            print("JUMPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                            jump = np.random.normal(5, 2, 1)
                            not_read_count = int(jump)
                            if not_read_count > 7:
                                    not_read_count = 7
                            print(not_read_count)
                            
                    elif not_read_count - 1 == 0: #we were not reading
                        read_string += sentence1 + "."
                        sent_read_aft_jump += 1
                        sent_read_total += 1
                        sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)
                        print("long term mean sim: ", long_term_mean_sim)
                        sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                        avg_vectors_bin.append(sentence1_avg_vector)
                        sim_list.append(sens_sim)
                        read_string += sentence1 + "."
                        sent_read_aft_jump += 1
                        sent_read_total += 1
                        #dist_para += 1                                                                                  
                        not_read_count = 0 #get out of not read state
                    
                    else:
                        not_read_count -= 1                        
                    
                    #delete the last last_sentence
                    last_sentence = ""
                    
                    #memorize the average feature vector for the last sentence so that we can compare it to the next "first" sentence, (sentence1)                    
                    #last_sentence = sentence2
                    #last_avg_vector = avg_sentence_vector(last_sentence, model, pos_freq)                   
                    
                    
                    #empty out the sentence one or two so that we can use them again in the second loop
                    sentence = ""
                    sentence1 = ""
            
    print(read_string)  
    return avg_vectors_bin

vectors = model('metamor.txt',
                  google_vectors,
                  pos_freq = pos_freq_matrix,
                  set_long_term_interest = 0.80,
                  set_short_term_interest = 0.89,
                  set_long_term_importance = 5,
                  set_short_term_importance = 3)


#plot the sentences read
#display_pca_scatterplot_vectors(vectors)


