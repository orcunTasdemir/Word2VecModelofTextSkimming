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
    #str = text_process(text_string)
    #The text process function also puts a $ at the beginnings of paragraphs which will be helpful
    #because I want to positively discriminate paragraph beginnings
    
    """tokenizing all the words and punctuation in the text document"""
    #tokens = nltk.word_tokenize(str) 
    
    
    """sentence ending punctuations are important for us"""
    #sentence_ending_punc = ['.', '?', '!', '...']
    #where the first sentence ending is
    #first_sent_end = [(tokens.index('.')),
                     # (tokens.index('...')),
                     # (tokens.index('?')),
                     # (tokens.index('!'))]
    #where_first_period = min(first_sent_end) 
    
    
    
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
    #sentence = ""
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
    
    
    read_sentence_no_bin = [0, 1]
    
    """
    ###########################################################################################################"""    


    """
    ##############################################################
    ####      Here we start reading "skimming" the text       ####
    ##############################################################"""
    
    #We will read, at least skim the entire thing so our limit is len(tokens)
    # for tok_count in range(300):# range(len(tokens)):  #curtok will indetify the current token we have on the for loop
    #     curtok = tokens[tok_count]
        
             
    #     if curtok not in sentence_ending_punc:
    #         if tokens[tok_count] == '$':
    #             dist_para = 1
    #         else:
    #             sentence += " " + (tokens[tok_count])
    #             #print(sentence)
                
        
    #     #################################################################
    #     ####      if we see the sentence end we will append it       ####
    #     ####      to sentence1 or sentence 2 according to whether    ####
    #     ####      sentence 1 is full or not                          ####
    #     #################################################################
        
    #     else :
    #         #if it was the first sentence get the avg_sentence_vector
    #         if where_first_period == tok_count and first_sentence != 'c':
    #             first_sentence = sentence
    #             #dist_para +=1
    #             print("\nfirst sentence: ", first_sentence)
    #             print("\ndistance from the beginning of the paragraph: ", dist_para)
                
    #             first_sentence_avg = avg_sentence_vector(sentence, model, pos_freq)
    #             #print("first_sentence_avg: ", first_sentence_avg)
    #             sentence = ""
                                
    #         #if sentence one is not full, add to sentence one
    #         elif sentence1 == "":
    #             sentence1 = sentence
    #             dist_para +=1
    #             print("\nsentence", sentence_counter, ": ", sentence1)
    #             print("\ndistance from the beginning of the paragraph: ", dist_para)
    #             sentence_counter += 1
    #             sentence = ""
      

    string = text_process(text_string)
    read_these_sentences = text_real_sentences(string)
    
    ## sentences ##
    first_sentence = read_these_sentences[0].replace("$", "")
    sentence1 = read_these_sentences[1].replace("$", "")
    
          
    #if we are here, it means that both the sentences were full, implement the cosine similarity function
    #print('false or true', first_sentence != "c")
    if first_sentence != "": #if empty we know we read past it   #as in "completed"
        #print(first_sentence)
        #print(sentence1)
        
        print("\nfirst sentence: ", first_sentence)
        print("\nNth sentence from the start of the paragraph: ", dist_para)
        dist_para += 1
        print("\nsentence1: ", sentence1)
        print("\nNth sentence from the start of the paragraph:: ", dist_para)
        
        sens_sim = sentence_similarity(first_sentence, sentence1, model, pos_freq)
        print("\nSentence_similarity no: ", sens_sim)
        sim_list.append(sens_sim)
        #after it is c, we will never go into this line again
        
        #also calculate the similarity between first and the second sentences
        #sens_sim2 = sentence_similarity(sentence1, sentence2, model, pos_freq)
        #print("second_sim: ", sens_sim2)
        #sim_list.append(sens_sim2)
        
        #memorize the average feature vector for the last sentence so that we can compare it to the next "first" sentence, (sentence1)                    
        last_sentence = sentence1
        
        first_avg_vector = avg_sentence_vector(first_sentence, model, pos_freq)
        last_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)                    
        
        avg_vectors_bin.append(first_avg_vector)
        avg_vectors_bin.append(last_avg_vector)
        
        last_sentence = sentence1
        
        #before emptying our sentences the decisions to whether read the sentence or not will be given
        #these decisions will be depending on the theory of optimal foraging, and I will assume that the
        #chances for our reader to read the next sentence is whether the similarity between the last 2 sentence
        #they read were very low, or whether it was very high, they will either want to keep reading in a situation
        #where they want more information, or they want new information.
        
        read_string += first_sentence
        read_string += sentence1           #since these are the first three sentences I have rather loose decision boundaries
        sent_read_aft_jump = 2             #we are setting this to two so that we know we have read 2 sentences uninterrupted so far
        sent_read_total = 2       #total sentences read so that we know what similarities to average
        #dist_para = sent_read_total
        
            
        
        #empty out the sentence one or two so that we can use them again in the second loop
        first_sentence = ""
        #sentence = ""
        sentence1 = ""
        
        
        #all the other times that we are not in the beginning of the text document
    #calculate the sentence similarity in terms of cosine similarity
        
        
    ##########################################################################################
    ####   This is where the code actually happens after the first two sentences,         ####
    ####   the jump decisions are taken, jumps terminated, similarity list is also        ####
    ####   constructed here. Long_term and short_term mean similarities are also          ####
    ####   calculated here alongsisde the important word counts and dist_para corrections ####
    ##########################################################################################
        
    #return read_these_sentences   
    for sentence in read_these_sentences[2:]: #from the third sentence onwards now
        
       
        
        if "$" in sentence:
            dist_para = 1
            sentence = sentence.replace("$", "")
            
        sentence1 = sentence
        
        print("\nSentence",sentence_counter, ": ", sentence1)
        
        sentence_counter += 1
        
        dist_para += 1
        print("\nNth sentence from the start of the paragraph: ", dist_para)
        
        short_importance = 0
        long_importance = 0

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
        #ONLY FOR THE FIRST TWO SENTENCE WHICH MEANS THAT IT IS GOING TO RUN ONLY ONCE or
        #until at least one sentence is read
        if sent_read_total == 2:
            print("\nSIMILARITIES, CORRECTIONS, AND IMPORTANT WORDS CALCULATIONS, STILL NO SENTENCE READ:")
            count = 1
            #print("SIMILARITY LIST LENGTH IS 1")
            #print("SIM LIST ITSELF: ", sim_list)
            long_term_mean_sim = mean(sim_list[-3:])
            print("long_term_mean_sim no", count, ": ", long_term_mean_sim)
            short_term_mean_sim = mean(sim_list[-1:])
            print("short_term_mean_sim no", count, ": ", short_term_mean_sim)
            count += 1
            
            #generate the first version of the ongoing word frequency vector
            #which is going to assist our decision protocol
            # read_sentences = []
            # for sentence in read_string.split('.'):
            #     read_sentences.append(sentence)
            read_sentences = read_string.split()
            #print(read_string)
            #print(read_sentences)
            #print("vfvfdvfdv")
            all_tfi_weights = get_tfi_weights(read_sentences)
            #return all_tfi_weights
            imp_words = get_words(min(short_term_importance, len(all_tfi_weights)), all_tfi_weights)
            print("\nIMPORTANT WORDS SO FAR: ", imp_words)
            # words= []
            # for sentence in read_sentences:
            #     words.append(sentence.split())
            # print("thse are the worrrrrrrrrrrrrrrrrrrds: ", words)
            for word in read_sentences:
                if word in imp_words:
                    short_importance += 1  
                    long_importance += 1 
            print('\nfirst_short_importance for first: ', short_importance)
            print('first_long_importance for first: ', long_importance)
            print("first_short_term_interest: ", short_term_interest)
            print("first_long_term_interest: ", long_term_interest, "\n")
            
        else:
            print("\nSIMILARITIES, CORRECTIONS, AND IMPORTANT WORDS CALCULATIONS:")
            
            long_term_mean_sim = mean(sim_list[-3:])
            print('long_term_mean_sim: ', long_term_mean_sim)
            short_term_mean_sim = mean(sim_list[-1:])
            print('short_term_mean_sim: ', short_term_mean_sim)
            
            read_sentences = read_string.split('.')
            
            #it counts the number of important words the last sentence we read has.
            print(read_sentences)
            short_tfi_weights = get_tfi_weights(read_sentences[-2:])
            #return short_tfi_weights
            #num = min(short_term_importance, len(short_tfi_weights))
            short_term_imp_words = get_words(min(short_term_importance, len(short_tfi_weights)), short_tfi_weights)
            for word in last_sentence.split():   
                #short_importance = 0
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
            print("short_term_imp_words: ", short_term_imp_words) 
            print("long_term_imp_words: ", long_term_imp_words)   
            print('short_importance: ', short_importance)
            print('long_importance: ', long_importance)
                
            #set the variables for the interest and importance depending on where I am on the paragraph
            multip = dist_para_correction(dist_para)
            print("\nmultip: ", multip)
            
            long_term_interest = set_long_term_interest * multip
            print("\nlong term interest_updated: ", long_term_interest)
            
            short_term_interest = set_short_term_interest * multip
            print("short_term_interest_updated: ", short_term_interest)
            
            long_term_importance = round((math.log(dist_para, 18)) + set_long_term_importance)
            print("long_term_importance_updated: ", long_term_importance)
            
            short_term_importance = round((math.log(dist_para, 18)) + set_short_term_importance)  
            print("short_term_importance_updated: ", short_term_importance, "\n")
        
        
        
        #############################################################
        #############################################################
        ##############     READING BEGINS HERE     ##################
        #############################################################
        #############################################################
        
        
        if last_sentence != "" and not_read_count == 0: #if we were reading already  last_sentence in read_string
            
            
            #print("sim_list_len: ", len(sim_list))
            if  sent_read_aft_jump < longest_read: #if smaller than the limit       


                    
                if  long_term_mean_sim < long_term_interest:
                    
                    
                    print('QQQQQQQQQ long_term_mean_sim < long_term_interest QQQQQQQQQ')
                    read =  0.5 + pow((long_term_interest - long_term_mean_sim), 2)
                    print("ratio: ", read)
                    if random.choices([1, 0], [read, (1-read)]) == [1]:#[(1-long_term_mean_sim), long_term_mean_sim]) == 1:
                        print('CHOICE TO KEEP READING: 1')
                        print("last sentence read: ", last_sentence)
                        #print("sentence1: ", sentence1)
                        sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)
                        sim_list.append(sens_sim)
                        print('sens_sim for sentence 1:', sens_sim)
                        sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                        avg_vectors_bin.append(sentence1_avg_vector)                                    
                        read_string += sentence1
                        sent_read_aft_jump += 1
                        sent_read_total += 1
                        #memorize this for learning
                        # sim_skipped_for_long = long_term_mean_sim
                        # sim_skipped_for_long_bin.append(sim_skipped_for_long)
                        # if sim_skipped_for_long + 0.1 <= long_term_interest:
                        #     long_term_interest = long_term_interest - learning_rate
                        read_sentence_no_bin.append((sentence_counter-1))                        
                        continue    

                if short_term_mean_sim < short_term_interest:
                    
                    print('QQQQQQQQQ Short_term_mean_sim < short_term_interest QQQQQQQQQ')
                    read =  0.5 + pow((short_term_interest - short_term_mean_sim), 2)
                    print("ratio: ", read)
                    if random.choices([1, 0], [read, (1- read)]) == [1]:
                        print('CHOICE TO KEEP READING: 2')
                        #if similarity is smaller than this I might not wanna continue reading
                        sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)
                        #print("long term mean sim: ", long_term_mean_sim)
                        sim_list.append(sens_sim)
                        sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                        avg_vectors_bin.append(sentence1_avg_vector)
                        read_string += sentence1
                        sent_read_aft_jump += 1
                        sent_read_total += 1
                        read_sentence_no_bin.append((sentence_counter-1))
                        
                        #memorize this for learning
                        # sim_skipped_for_short = short_term_mean_sim
                        # sim_skipped_for_short_bin.append(sim_skipped_for_short)
                        # if sim_skipped_for_short + 0.1 <= short_term_interest:
                        #     short_term_interest = short_term_interest - learning_rate
                #this is going to be a special case about whether I just read a word
                #on the last sentence that wants me to keep reading because it has been
                #an important word in the context of this text I am reading so far
                # if 1the last sentence had more than 1 important word in the last 3 sentences' tfi,
                        continue
                if short_importance > short_term_importance:
                    #then there is a fifty fifty chance of reading the next sentence
                    #since if we are at this eilf, it means that the sentence was not
                    #already interesting in terms of the past two conditions anyways.
                    #if greater than 2, we are definitely going to read
                    if short_importance == short_term_importance + 1 or random.choice([0, 1], [0.75, 1-0.75]) == [1]:
                        print('CHOICE TO KEEP READING: 3')
                        print('QQQQQQQQQ Short_importance == 2  and  short_importance > 1 QQQQQQQQQ')
                        sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)  
                        sim_list.append(sens_sim)
                        sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                        avg_vectors_bin.append(sentence1_avg_vector)
                        read_string += sentence1
                        sent_read_aft_jump += 1
                        sent_read_total += 1
                        read_sentence_no_bin.append((sentence_counter-1))
                        continue
                #if there have been more than 3 words of importance in the
                #last three sentences we read out of the entire portion of the text we have
                #been, reading, go into this elif.
                if long_importance > long_term_importance:
                    #if we encountered at least 4 words of importance in the last three sentences or if we
                    #randomly select a 1 out of a fifty fifty probability, we read the next sentence.
                    if long_importance >= long_term_importance + 1 or random.choices([0, 1], [0.75, 0.25]) == [1]:
                        print('CHOICE TO KEEP READING: 4')
                        print('QQQQQQQQQ long_importance >=4 QQQQQQQQQ')
                        sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)  
                        sim_list.append(sens_sim)
                        sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
                        avg_vectors_bin.append(sentence1_avg_vector)
                        read_string += sentence1
                        sent_read_aft_jump += 1
                        sent_read_total += 1
                        read_sentence_no_bin.append((sentence_counter-1))
                        continue    
                    
                #ELSE WE JUMP
                print("\n\nWE ARE JUMPING: ...")
                #if long term similarity is higher than the short term similarity
                #then I am going to jump smaller with the hope that I might still land
                #at a location where it is relevant information wrt the long term.
                if long_term_mean_sim > short_term_mean_sim:
                    print("\n\nWE ARE JUMPING via jump_param = 1- long_term_mean_sim")
                    #if all that and the long_importance words were 0, it means that I am
                    #straying further from a coherent paragraph
                    jump_param = 1- long_term_mean_sim
                    jump = np.random.normal((jump_param*10), 2, 1)
                    not_read_count = int(jump)
                    print("by ", not_read_count)
                    continue
                #if opposite I am going to want to jump depending on the long_term_similarity
                #because the lack of that is what is triggering me to jump.
                if long_term_mean_sim < short_term_mean_sim:
                    print("\n\nWE ARE JUMPING via jump_param = 1- long_term_mean_sim")
                    jump_param = 1- long_term_mean_sim
                    jump = np.random.normal((jump_param*10), 2, 1)
                    not_read_count = int(jump)
                    continue
                #if none of those are satisfied above I want to look at the short importance
                #and jump over 1 sentence if it is zero
                if short_term_mean_sim < 0.5 and (long_importance == 0 or short_importance == 0):
                    print("\n\nWE ARE JUMPING because mean sim is very low and there are no important words around")
                    jump = 1
                    not_read_count = jump
                    continue
                #else I want to jump around 3 sentences this is my default
                else :
                    print("\n\nWE ARE JUMPING because we dont want to keep reading")
                    jump = np.random.normal(4, 2, 1)
                    not_read_count = int(jump)                           
                    if not_read_count > 7:
                        not_read_count = 7 # to normalize for the normal distribution
                        print(not_read_count)
                
                
            #jump because you read seven sentences already                            
            else:
                jump = np.random.normal(3, 2, 1)
                not_read_count = int(jump)
                if not_read_count > 7:
                        not_read_count = 7
                print("\n\nWE ARE JUMPING because the max num of sentences to be read is exceeded")
                
        #we were not reading
                
        elif not_read_count - 1 == 0:
            read_string += sentence1
            sent_read_aft_jump += 1
            sent_read_total += 1
            sens_sim = sentence_similarity(last_sentence, sentence1, model, pos_freq)
            sentence1_avg_vector = avg_sentence_vector(sentence1, model, pos_freq)
            avg_vectors_bin.append(sentence1_avg_vector)
            sim_list.append(sens_sim)
            read_string += sentence1
            sent_read_aft_jump += 1
            sent_read_total += 1                                                                                 
            not_read_count = 0 #get out of not read state
            read_sentence_no_bin.append('$')
            read_sentence_no_bin.append((sentence_counter-1))
        
        else:
            not_read_count -= 1
            print("not_read_count: ", not_read_count)                      
        
        #delete the last last_sentence
        last_sentence = sentence1
        
        #memorize the average feature vector for the last sentence so that we can compare it to the next "first" sentence, (sentence1)                    
        #last_sentence = sentence2
        #last_avg_vector = avg_sentence_vector(last_sentence, model, pos_freq)                   
        
        
        #empty out the sentence one or two so that we can use them again in the second loop
        #sentence = ""
        #sentence1 = ""
    
    print("SIM LIST ITSELF: ", sim_list)
    print(read_string)
    print(read_sentence_no_bin)
    real_sentences_display = text_real_sentences_display("metamor.txt")
    display = ""
    for i in read_sentence_no_bin:
        if i == '$':
            display += "\n\n"
        else:
            display += real_sentences_display[i]
    print("\n\n", display)  
    
    return avg_vectors_bin

vectors = model('metamor.txt',
                  google_vectors,
                  pos_freq = pos_freq_matrix,
                  set_long_term_interest = 0.39, #bişeyler birbirine son 3 pair dır yüzde 39 dan az benzediyse oku
                  set_short_term_interest = 0.39, #bişeyler birbirine son 1 pair dır yüzde 39 dan daha az benzediyse oku
                  set_long_term_importance = 5,
                  set_short_term_importance = 3)


#plot the sentences read
display_pca_scatterplot_vectors(vectors)


