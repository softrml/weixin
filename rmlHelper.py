import json

def loadJson(fn):
    try:
        with open(fn) as json_file:
            data = json.load(json_file)
    except:
        data = {}
    return data

def saveJson(data,fn):
    try:
        with open(fn, 'w') as json_file:
            json.dump(data, json_file)
    except:
        print('Error writing %s'%fn)
    #str = json.dumps('{a:b,c:[d,e]}', indent = 4, sort_keys=True) #dump to string

def listToFile(lst,fn):
    try:
        f = open(fn,'w')
        f.writelines(lst)
        f.close()
    except:
        print('Fail to save:',fn)
    
def fileToList(fn):
    try:
        f = open(fn)
        lst = f.readlines()
        f.close()
    except:
         print('Fail to load:',fn)
         return []
    return lst