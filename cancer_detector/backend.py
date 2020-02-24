# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:18:33 2018

@author: HARSHIT
"""

import cv2
import numpy as np
import pickle

image = cv2.imread('D:/College_Stuff/SEM7/PROJECT/Dataset/Papsmear/smear2005/smear2005/New_database_pictures/Colour_Sets/Test/moderate_dysplastic/149316754-149316762-002.bmp')

class features:

    def imageMean(rgbImage):

        mean = rgbImage.mean()

        return mean
    
    def colorRatioMean(rgbImage):
        
        R = cv2.normalize(rgbImage[:,:,0].astype('double'), None, 0, 255, cv2.NORM_MINMAX)
        G = cv2.normalize(rgbImage[:,:,1].astype('double'), None, 0, 255, cv2.NORM_MINMAX)
        B = cv2.normalize(rgbImage[:,:,2].astype('double'), None, 0, 255, cv2.NORM_MINMAX)

        rR = ((100.*R)/(1+B+G))*(256/(1+B+R+G))
        gR = ((100.*G)/(1+R+B))*(256/(1+B+R+G))
        bR = ((100.*B)/(1+R+G))*(256/(1+B+R+G))
        
        redRatio = cv2.normalize(rR.astype('uint8'), None, 0, 255, cv2.NORM_MINMAX)
        greenRatio = cv2.normalize(gR.astype('uint8'), None, 0, 255, cv2.NORM_MINMAX)
        blueRatio = cv2.normalize(bR.astype('uint8'), None, 0, 255, cv2.NORM_MINMAX)
        
        
        RM = redRatio.mean()
        GM = greenRatio.mean()
        BM = blueRatio.mean()
        
        return RM, GM, BM

    def roughnessIndex(rgbImage):

        grayImage = cv2.cvtColor( rgbImage, cv2.COLOR_RGB2GRAY)
        sh = np.shape(grayImage)
        B = np.reshape(grayImage, [sh[0]*sh[1], 1], order='F')
        N = np.array([])
        H = 256
        L = 256
        
        for i in range(len(B)-2):
               N = np.append(N, abs(B[i]-B[i+1]))
               N = np.reshape(N, [i+1, 1], order='F')
               
        LN = np.log(np.sum(N))
        Nmax = 2*H*L*(L-1)
        LNmax = np.log(Nmax)
        RI = LN/LNmax
        
        return RI
    
    def LBPmv(rgbImage):

        from skimage.feature import local_binary_pattern
        grayImage = cv2.cvtColor( rgbImage, cv2.COLOR_RGB2GRAY)
        LBP = local_binary_pattern(grayImage, 8, 16, 'default')
        mean = np.mean(LBP)
        var = np.var(grayImage)
        
        return mean, var
    
    def areas(rgbImage):

        grayImage = cv2.cvtColor( rgbImage, cv2.COLOR_RGB2GRAY)
        ret,thr = cv2.threshold( grayImage, 0, 255, cv2.THRESH_OTSU)
        AreaNuc = 0
        AreaCyt = 0
        sha = np.shape(grayImage)
        for i in range(sha[0]):
            for j in range(sha[1]):
                if thr[i,j] == 255:
                    AreaNuc = AreaNuc+ 1
                else:
                    AreaCyt = AreaCyt + 1
        
        ratio = AreaNuc/(AreaCyt + AreaNuc)
    
        return AreaNuc, AreaCyt, ratio
   
    def variance(rgbImage):
        var = np.var(rgbImage)
        
        return var
    
    def entropy(rgbImage):
        
        unique, counts = np.unique(rgbImage, return_counts=True)
        sh = np.shape(rgbImage)
        histnorm = np.divide(counts, (sh[0]*sh[1]*sh[2]))
                
        E = -np.sum(np.multiply(histnorm, np.log2(histnorm))) # Calculate Entropy
        
        return E

    def perimeter(rgbImage):
        
        grayImage = cv2.cvtColor( rgbImage, cv2.COLOR_RGB2GRAY)
        ret, thr = cv2.threshold( grayImage, 0, 255, cv2.THRESH_OTSU )
        
        edge = cv2.Canny( thr, 0, 255)
        
        peri = np.sum(edge)/255
        
        return peri

r, g, b = features.colorRatioMean(image)
m, v = features.LBPmv(image)
n, c, rat = features.areas(image)

feat = np.array([r, g, b, features.roughnessIndex(image), features.variance(image), features.entropy(image), features.imageMean(image), m, v, n, c, rat, features.perimeter(image)])

feat = np.reshape(feat, [1, 13], 'C')
rFC = pickle.load(open('rFCfinal.sav', 'rb'))

rFC.predict(feat)