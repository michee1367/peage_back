import os, glob
from tools.packages import alls

fileName = __file__
listes = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(fileName) + "/*.py")]

dirname = "."
if os.path.dirname(fileName) :
    dirname = os.path.dirname(fileName)
    

#print(glob.glob(os.path.dirname(fileName) + "/*.py"))
#print(os.path.dirname(fileName) + "/*.py")
print(glob.glob(dirname + "/*.py") )
listes = [os.path.basename(f)[:-3] for f in glob.glob(dirname + "/*") if os.path.isdir(f) and not ('__' in f) and os.path.exists(f + '/__init__.py')]

print(alls(fileName))


