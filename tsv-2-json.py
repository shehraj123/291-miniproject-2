# References - https://www.geeksforgeeks.org/python-tsv-conversion-to-json/

import json

def tsv2json(name):
    """
    Converts tab-seperated fiels into json with proper conversions.
    Arguments:
        name - name of tsv file
    Returns:
        None
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

            if t in ("primaryProfession", "knownForTitles", "genres", "characters", "numVotes"):
                if t == "characters":
                    if f == '\\N':
                        d[t] = f.strip().split(',')
                    f = f[1:-1]
                    f = f.strip().split(",")
                    f = [f[i][1:-1] for i in range(len(f))]
                    d[t] = f

                elif t == "numVotes":
                    d[t] = int(f.strip())    
                else:
                   f = f.strip().split(',')
                   d[t] = f
            else:
                f = f.strip()
                d[t] = f      
        arr.append(d)
          
    file.close()    
    file = open(name+".json", 'w+', encoding='utf-8')
       
    file.write(json.dumps(arr, indent=4))  
    file.close()

def convert(files):
    """
    Conversion wrapper.
    Arguments:
        files - list of file names
    Returns:
        N/A
    """
    for filename in files:
        tsv2json(filename)

if __name__ == "__main__":
    tsv2json("title.principals")        