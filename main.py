import csv
import sys
import getopt
import requests

def help():
    print("[command] \n")

def parse_csv(csv_path, server):
    i=0
    entrynames = []
    with open(csv_path) as csv_f:
        csv_r = csv.reader(csv_f, delimiter=',')
        for row in csv_r:
            if i>0:
                print(row)
                send_entry(server, row, entrynames)
            else:
                entrynames = row
                i+=1

def send_entry(server, entry, entrynames):
    url = server + "/api/messages"
    postdata = {
            entrynames[0] : str(entry[0]),
            entrynames[1] : str(entry[1]),
            entrynames[2] : str(entry[2]),
            entrynames[3] : str(entry[3]),
            entrynames[4] : str(entry[4])}
    res = requests.post(url, json = postdata)
    print(res)
    print(res.status_code)

def main(argv):
    csv_path = ""
    server = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
    except getopt.GetoptError:
        print("Incorrect usage of parameters")
        help()
        sys.exit(1)
    if not opts:
        print("Arguments are required to run")

    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt == '-i':
            csv_path = arg 
        elif opt == '-o':
            server = arg

    if not server or not csv_path:
        print("a server IP and a csv file is required")
        sys.exit(1)
    parse_csv(csv_path, server)
    
if __name__ == "__main__":
    main(sys.argv[1:])
