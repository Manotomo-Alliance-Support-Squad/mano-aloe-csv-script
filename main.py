import argparse
import csv
import requests


def parse_csv(csv_path, server, dry_run=False):
    i = 0
    entrynames = []
    with open(csv_path) as csv_f:
        csv_r = csv.reader(csv_f, delimiter=',')
        for row in csv_r:
            if i > 0:
                print(row)
                if server and not dry_run:
                    send_entry(server, row, entrynames)
            else:
                entrynames = row
                i += 1


def send_entry(server, entry, entrynames):
    url = server + "/api/messages"
    postdata = {
        entrynames[0]: str(entry[0]),
        entrynames[1]: str(entry[1]),
        entrynames[2]: str(entry[2]),
        entrynames[3]: str(entry[3]),
        entrynames[4]: str(entry[4])
    }
    res = requests.post(url, json=postdata)
    # Not super actionable if we have failures.
    # Should probably add in retry or mechanism to drop
    # a local file with the failed dataset.
    print(res)
    print(res.status_code)


def main(argv):
    if argv.dry_run:
        print("\nThis is a dry run. No data will be loaded to server whether "
              "a server_address has been provided or not.\n")
    elif not argv.server_address:
        print("\nWARNING: A server address was not provided in args. "
              "Only printing results locally. Use the -h arg if you don't "
              "know what this means.\n")
    parse_csv(argv.csv_path, argv.server_address, argv.dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse a specifically formatted CSV')
    parser.add_argument(
        '--csv_path', '-c', dest='csv_path', required=True,
        help='the path to the csv file')
    parser.add_argument(
        '--dry_run', '-d', dest='dry_run', action='store_true',
        help='performs a dry run locally even when provided '
        'with server_address')
    parser.add_argument(
        '--server', '-s', dest='server_address', required=False,
        help='the server address for the results to be uploaded')
    args = parser.parse_args()
    main(args)
