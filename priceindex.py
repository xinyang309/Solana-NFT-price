import requests
from tabulate import tabulate
import sched, time
from datetime import datetime, timezone, timedelta
import sys


delta = timedelta(hours=8)

# for Magiceden API
symbol = ["crypto_coral_tribe",
    "genesis_genopets_habitats",
    "genopets_habitats",
    "genopets",
    "okay_bears",
    "degods",
    "cets_on_creck",
    "trippin_ape_tribe",
    "bohemia_",
    "cat_cartel",
    "trip_memory",
]

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
}

#for birdeye API
params={
            "sol" : "So11111111111111111111111111111111111111112",
            "KI" : "kiGenopAScF8VF31Zbtx2Hg8qA5ArGqvnVtXb83sotc",
            "Gene" : "GENEtH5amGSi8kHAtQoezp1XEXwZJ8vcuePYnXdKrMYz",
}


def main():
    while True:
        nft = []
        token = []
        # time tick
        s1 = datetime.now()
        for i in symbol:
            try:
                name, floorPrice, listedCount = magiceden_api(i)
            except TypeError:
                nft.append([i, "n/a", "n/a"])
            else:
                nft.append([name, floorPrice, listedCount])
            
        s2 = datetime.now()
        sys.stdout.write("\rProcessing nfts took time... %s \n " % str(s2-s1).rjust(37))
        for key, value in params.items():
            name = key
            try:
                price = birdeye_api(value)
            except TypeError:
                token.append([name,"n/a"])
            else:
                token.append([name, price])
        s3 = datetime.now()
        sys.stdout.write("\rProcessing tokens took time... %s \n " % str(s3-s2).rjust(35))
        now_utc = datetime.now(timezone(delta)).strftime("%Y-%m-%d %H:%M:%S %Z")
        print(now_utc)
        print(tabulate(nft))
        print(tabulate(token, floatfmt=".6f"))
        time.sleep(30)


def magiceden_api(symbol):
    sys.stdout.write("\rProcessing nft... %s " % symbol.rjust(46))
    try:
        response = requests.get("https://api-mainnet.magiceden.dev/v2/collections/" + symbol, headers=headers, timeout=12)
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
        pass
    except requests.exceptions.HTTPError:
        print(response.status_code)
        pass
    except requests.exceptions.Timeout:
        print("Timeout")
        pass
    else:
        name = response.json()['name']
        floor_price = response.json()['floorPrice']/10**9 * 1.00
        listed = response.json()['listedCount']
        sys.stdout.flush()
        return name, floor_price, listed

def birdeye_api(params):
    sys.stdout.write("\rProcessing token... %s " % params.rjust(46))
    try:
        response = requests.get("https://public-api.birdeye.so/public/price?address=" + params, headers=headers, timeout=12)
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
        pass
    except requests.exceptions.HTTPError:
        print(response.status_code)
        pass
    except requests.exceptions.Timeout:
        print("Timeout")
        pass
    else:
        return response.json()["data"]["value"]


if __name__ == "__main__":
        main()

