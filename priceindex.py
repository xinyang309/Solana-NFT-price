import requests
from tabulate import tabulate
from time import sleep
from datetime import datetime
import sys

timeout = 6
sleeptime = 12
# import nfts and store in variable
def load_nfts():
    _nfts = []
    with open('nfts.txt','r') as file:
        for line in file:
            _nfts.append(line.rstrip('\n'))
    return _nfts

# import tokens and store in variable
def load_tokens():
    _tokens = {}
    with open('tokens.txt','r') as file:
        for line in file:
            line = line.rstrip('\n').split(",")
            _tokens[line[0].strip()] = line[1].strip()
    return _tokens

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
}

def main():
    while True:
        nft = []
        token = []
        s1 = datetime.now()
        for i in load_nfts():
            try:
                name, floorPrice, listedCount = magiceden_api(i, timeout)
            except TypeError:
                nft.append([i, "n/a", "n/a"])
            else:
                nft.append([name, floorPrice, listedCount])
            
        s2 = datetime.now()
        sys.stdout.write("\rProcessing nfts took time... %s \n " % str(s2-s1).rjust(37))
        for key, value in load_tokens().items():
            name = key
            try:
                price = birdeye_api(value, timeout)
            except TypeError:
                token.append([name,"n/a"])
            else:
                token.append([name, price])
        s3 = datetime.now()
        sys.stdout.write("\rProcessing tokens took time... %s \n " % str(s3-s2).rjust(35))
        now_utc = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        print(now_utc)
        print(tabulate(nft))
        print(tabulate(token, floatfmt=".6f"))
        sleep(sleeptime)


def magiceden_api(symbol, timeout):
    sys.stdout.write("\rProcessing nft... %s " % symbol.rjust(46))
    try:
        response = requests.get("https://api-mainnet.magiceden.dev/v2/collections/" + symbol, headers=headers, timeout=timeout)
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
    except requests.exceptions.HTTPError:
        print(response.status_code)
    except requests.exceptions.Timeout:
        print("Timeout")
    else:
        name = response.json()['name']
        floor_price = response.json()['floorPrice']/10**9 * 1.00
        listed = response.json()['listedCount']
        sys.stdout.flush()
        return name, floor_price, listed

def birdeye_api(params, timeout):
    sys.stdout.write("\rProcessing token... %s " % params.rjust(46))
    try:
        response = requests.get("https://public-api.birdeye.so/public/price?address=" + params, headers=headers, timeout=timeout)
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
    except requests.exceptions.HTTPError:
        print(response.status_code)
    except requests.exceptions.Timeout:
        print("Timeout")
    else:
        return response.json()["data"]["value"]


if __name__ == "__main__":
        main()

