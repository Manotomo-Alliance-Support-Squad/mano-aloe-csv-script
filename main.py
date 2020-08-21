import argparse
import csv
import requests


def write_fail_csv(entries, path):
    with open(path, 'w') as csv_f:
        csv_w = csv.writer(csv_f, delimiter=',')
        csv_w.writerows(entries)


def parse_csv(csv_path, server, dry_run=False):
    i = 0
    entrynames = []
    failed_entries = []
    with open(csv_path) as csv_f:
        csv_r = csv.reader(csv_f, delimiter=',')
        for row in csv_r:
            if i > 0:
                # Print dry run results if no server address
                if not server:
                    dry_run = True
                    server = '0.0.0.0'
                res_code, postdata = send_entry(
                    server, row, entrynames, dry_run)
                if res_code != 200 and res_code != 201:  # STATUS CODE not OK
                    row.extend([postdata, res_code])
                    failed_entries.append(row)
            else:
                entrynames = row
                #row.extend(['postdata', 'response code'])
                #failed_entries.append(row)
                i += 1
    return failed_entries


def send_entry(server, entry, entrynames, dry_run):
    url = server
    postdata = {
        entrynames[0]: str(entry[0]),
        entrynames[1]: str(entry[1]),
        entrynames[2]: str(entry[2]),
        entrynames[3]: str(entry[3])
        #entrynames[4]: str(entry[4])
        #TODO: Add a way to specify the columns we are sending. Sometimes the server will complain if we send an undefined column
    }
    if not dry_run:
        res = requests.post(url, json=postdata)
        res_code = res.status_code
        print(res_code, res)
    else:
        print(postdata)
        res_code = 200  # STATUS CODE OK
    return res_code, postdata


def main(argv):
    if argv.dry_run:
        print("\nThis is a dry run. No data will be loaded to server whether "
              "a server_address has been provided or not.\n")
    elif not argv.server_address:
        print("\nWARNING: A server address was not provided in args. "
              "Only printing results locally. Use the -h arg if you don't "
              "know what this means.\n")
    failed_entries = parse_csv(
        argv.csv_path, argv.server_address, argv.dry_run)

    total_failed_entries = len(failed_entries)
    if total_failed_entries > 1:
        print(
            "\nTHERE WERE {} ENTRIES THAT FAILED TO BE PROCESSED. "
            "PLEASE SEE \"{}\" TO DETERMINE IF THERE'S ANY DATA REMEDIATION "
            "THAT'S NEEDED.\n".format(
                total_failed_entries, argv.fail_csv_path))
        write_fail_csv(failed_entries, argv.fail_csv_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse a specifically formatted CSV')
    parser.add_argument(
        '--csv_path', '-c', dest='csv_path', required=True,
        help='the path to the csv file')
    parser.add_argument(
        '--dry_run', '-d', dest='dry_run', action='store_true',
        help='performs a dry run locally when provided with a '
        'server_address')
    parser.add_argument(
        '--fail_csv_path', '-f', dest='fail_csv_path',
        default='./failed_entires.csv',
        help='the path to drop a csv with failed entries')
    parser.add_argument(
        '--server', '-s', dest='server_address', required=False,
        help='the server address for the results to be uploaded')
    args = parser.parse_args()
    main(args)
