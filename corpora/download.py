import gzip
import sys

from urllib.request import urlretrieve

def download():
    print("Downloading preparsed datasets...")
    urlretrieve("http://people.rc.rit.edu/~bsm9339/corpora/stanford_politeness/wikipedia.parsed.json.gz", "wikipedia.parsed.json.gz")
    urlretrieve("http://people.rc.rit.edu/~bsm9339/corpora/stanford_politeness/stack-exchange.parsed.json.gz", "stack-exchange.parsed.json.gz")
    print("Finished!")

def extract():
    try:
        print("Extracting preparsed Wikipedia dataset. This will take a while...")
        with gzip.open("wikipedia.parsed.json.gz", "rb") as infile:
            with open("wikipedia.parsed.json", "wb+") as outfile:
                for line in infile:
                    outfile.write(line.decode("utf-8"))

        print("Extracting preparsed Stack Exchange dataset. This will take a while...")
        with gzip.open("stack-exchange.parsed.json.gz", "rb") as infile:
            with open("stack-exchange.parsed.json", "wb+") as outfile:
                for line in infile:
                    outfile.write(line.decode("utf-8"))

        print("Finished!")
    except FileNotFoundError as e:
        print("Oops! It looks like you are missing some files. Try running "
              "'python download.py download' to grab them!")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        download()
        extract()
    elif args[0] == 'download':
        download()
    elif args[0] == 'extract':
        extract()
    else:
        print("Received invalid command.")
