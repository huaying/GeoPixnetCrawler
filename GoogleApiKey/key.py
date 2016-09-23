import os, json

"""
    royal3501@gmail.com: GeoPixnet, PixnetAPI1 - 3
    geopixnetservice@gmail.com: key1-10

"""
keyfile = "api_keys"
keys = []


def readKeyFile():
    keys = []
    with open(os.path.dirname(os.path.abspath(__file__))+'/'+keyfile) as key_file:
        keys = json.load(key_file)
    
    return keys

def getKey():
    return keys[0] if keys else ""
    
def nextKey():

    if not keys: return
    keys.append(keys.pop(0))
    with open(os.path.dirname(os.path.abspath(__file__))+'/'+keyfile, 'w') as key_file:
        key_file.write(json.dumps(keys))
    
    return getKey()


keys = readKeyFile()

if __name__ == "__main__":
    print(getKey())
    for i in range(10):
        print(nextKey())
