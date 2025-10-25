
import os, glob

def alls(fileName) :
    
    dirname = "."
    if os.path.dirname(fileName) :
        dirname = os.path.dirname(fileName)
        
    print(dirname)
    #print(glob.glob(os.path.dirname(fileName) + "/*.py"))
    #print(os.path.dirname(fileName) + "/*.py")
    #files = glob.glob(dirname + "/*.py")
    dirs = [os.path.basename(f) + '/__init__.py' for f in glob.glob(dirname + "/*") if os.path.isdir(f) and not ('__' in f) and os.path.exists(f + '/__init__.py')]
    files = [os.path.basename(f)[:-3] for f in glob.glob(dirname + "/*.py")]

    return files + dirs
    