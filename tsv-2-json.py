# References - https://www.geeksforgeeks.org/python-tsv-conversion-to-json/

import json

def tsv2json(name):
    """
    """
    filename = name + ".tsv"
    arr = []
    file = open(filename, 'r', encoding='utf-8')
    a = file.readline()
    data = file.read()
    data = data.splitlines()
      
    titles = [t.strip() for t in a.split('\t')]
    for line in data:
        d = {}
        for t, f in zip(titles, line.split('\t')):

            if t in ("primaryProfession", "knownForTitles", "genres", "characters"):
                f = f.strip().split(',')
                d[t] = f
            else:
                d[t] = f.strip()  
        
        arr.append(d)
          
    file.close()    
    file = open(name+".json", 'w+', encoding='utf-8')
       
    file.write(json.dumps(arr, indent=4))  
    file.close()

def convert(files):
    """
    """
    for filename in files:
        tsv2json(filename)