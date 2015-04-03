import os

def listdirs(folder):  
    return next(os.walk(folder))[1]

def listfiles(folder):
    return next(os.walk(folder))[2]
