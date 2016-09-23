# -- coding: UTF-8 --
import json, collections, re, os
import urllib.request
#import sys
#sys.path.append('../')
import GoogleApiKey.key

class TaiwanAddrParser:

    taiwan = None
    cities = {}
    areas = collections.defaultdict(list)

    def __init__(self):
        self.load()
        self.buildIndex()
    def load(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/TaiwanAddress.json') as json_file:
            self.taiwan = json.load(json_file)

    def buildIndex(self):
        for city in self.taiwan:
            cityname = city['CityName']
            self.cities[cityname.replace(u'臺',u'台')] = city
            self.cities[cityname] = city
            for area in city['AreaList']:
                self.areas[area['AreaName']].append(cityname)

    def parseLine(self,line):
        """
        input: string(oneline)
        output: tuple(address,lat,lng)
        """
        #issue : oneline and multiple address
        line = line.strip()
        n = len(line)
        for i in range(n):
            if line[i:i+3] in self.cities:
                end = re.search(r"\W",line[i:])

                if end: addr = line[i:i+end.start()]
                else: addr = line[i:]

                if len(addr) > 3:
                    xy = self.validateAddr(addr)
                    if xy: return ((addr,xy[0],xy[1]))
        return None

    def parseArticle(self,string):
        """
        input: string(multilines)
        output: [tuple(address,lat,lng)]
        """
        xys = set()
        addrs = []
        for line in string.split('\n'):
            addrdata = self.parseLine(line)
            if addrdata and (addrdata[1],addrdata[2]) not in xys:
                xys.add((addrdata[1],addrdata[2]))
                addrs.append(addrdata)
        return addrs

    def parse(self, source_file, isUrl=False):
        """
        input: filename "/path/to/file"
        output: [tuple(address,lat,lng)]
        """
        xys = set()
        addrs = []

        if isUrl:
            source = urllib.request.urlopen(source_file)
        else:
            source = open(source_file)

        with source as input_file:
            for line in input_file:
                try:
                    line = line.strip().decode('utf-8')
                except: pass

                addrdata = self.parseLine(line)
                if addrdata and (addrdata[1],addrdata[2]) not in xys:
                    xys.add((addrdata[1],addrdata[2]))
                    addrs.append(addrdata)
        return addrs

    def validateAddr(self,addr, retry = 0):
        """
        check this given address on google api to see if it's valid
        """
        if retry > 20: return None

        #api_key = "AIzaSyAAdHJCqwnkCfeU92LerKfPTCNkN0QtxVY"
        api_key = GoogleApiKey.key.getKey()
        googleapi = "https://maps.googleapis.com/maps/api/geocode/json?key="+api_key+"&address="
        #print(googleapi)
        geocode = urllib.request.urlopen(googleapi+urllib.parse.quote(addr))
        res = json.loads(geocode.read().decode('utf-8'))

        if res and res["results"]:
            rlt = res["results"][0]
            if rlt["geometry"]["location_type"] == "ROOFTOP" and "Taiwan" in rlt["formatted_address"]:
                return (rlt["geometry"]["location"]["lat"],rlt["geometry"]["location"]["lng"])
        
        if res and not res["results"] and res["status"] == "OVER_QUERY_LIMIT":
            api_key = GoogleApiKey.key.nextKey()
            res = self.validateAddr(addr, retry = retry+1)        
            if res: return res

        return None



tap = TaiwanAddrParser()
def parseURL(source_file):
    return tap.parse(source_file,True)

def parseArticle(article):
    return tap.parseArticle(article)

def parseFile(source_file):
    return tap.parse(source_file,False)

#test
if __name__ == "__main__":
    print(parseArticle("台北市松山區南京東路3段259號8樓之2\n台北市松山區南京東路三段259號8樓之2\n台北市松山區南京東路三段259號8樓之3\n台北市松山區南京東路三段258號8樓之2\n台北市松山區南京東路二段259號8樓之2\n台北市松山區南京東路三段259號8樓"))
    print(parseFile("test"))
    print(parseURL("https://tw.ysm.emarketing.yahoo.com/soeasy/?fe_type=1"))
