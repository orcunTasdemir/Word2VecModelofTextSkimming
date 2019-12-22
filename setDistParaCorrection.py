# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:49:51 2019

@author: orcuntasdemir
"""
import math

def dist_para_correction(dist_para):
    
    # y = -ln(x) + 1
    #I will use this function to control the correction for our
    #interest variables, our interest will get greater as it is a
    #new beginning for a paragraph, which will make it easier for
    #our mean_sim to be lower than the interest point.
    correction_coef = (-math.log((dist_para/2), 60)) + 1
    return correction_coef


def dist_para_correction_low_log(dist_para):
    correction_coef = (-math.log((dist_para/2), 100)) + 1
    return correction_coef
    
    
    
    

