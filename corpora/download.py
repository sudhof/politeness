import urllib
import gzip
import sys
import traceback

downloader = urllib.URLopener()

def download():
    print("Downloading preparsed datasets..."
    wikipedia = downloader.retrieve("http://people.rc.rit.edu/~bsm9339/corpora/stanford_politeness/wikipedia.parsed.json.gz", "wikipedia.parsed.json.gz")
    stack_exchange = downloader.retrieve("http://people.rc.rit.edu/~bsm9339/corpora/stanford_politeness/stack-exchange.parsed.json.gz", "stack-exchange.parsed.json.gz")
    print("Finished!")
          
def extract():
    try:
        print("Extracting preparsed datasets. This will take a while...")
        open("wikipedia.parsed.json", "w+").write(gzip.open("wikipedia.parsed.json.gz", "rb"))
        open("stack-exchange.parsed.json", "w+").write(gzip.open("stack-exchange.parsed.json.gz", "rb"))
        print("Finished!")
    except Exception as e:
        traceback.print_exception(extype, exvalue, extrace)

if __name__ = "__main__":
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
