#Utility file to save and read classifier from a location
import pickle

# Save a python object to a file specified by file_path
def saveObjectToPath(obj, file_path) :
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

# Read a file specified by file_path and create a python object
def getObjectFromPath(file_path) :
    with open(file_path, 'rb') as f:
        obj = pickle.load(f)
    return obj