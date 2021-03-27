import argparse
import csv
import json

import requests


def auth(username, password, server):
    print(username)
    postdata = {'username': username, 'password': password}
    res = requests.post(server, json=postdata)
    print(res.text)
    return res.json()


def write_fail_csv(entries, path):
    with open(path, 'w') as csv_f:
        csv_w = csv.writer(csv_f, delimiter=',')
        csv_w.writerows(entries)


def parse_csv_to_memory(csv_path):
    """This probably doesn't need to be a function but it's separated for
    testability and to do additional functionality when parsing CSVs.
    """
    with open(csv_path) as csv_f:
        csv_r = csv.reader(csv_f, delimiter=',')
        csv_data = [row for row in csv_r]
    return csv_data


def load_csv_to_db(csv_data, entrymap, server, authkey, dry_run=False):
    failed_entries = []
    for entry in csv_data[1:]:
        # Do a dry run if no server address
        if not server:
            dry_run = True
            server = '0.0.0.0'
        res_code, res_text, postdata = send_entry(
            server, entry, entrymap, dry_run, authkey)
        if res_code not in {200, 201}:  # STATUS CODE not OK
            entry.extend([postdata, res_text, res_code])
            failed_entries.append(entry)
    return failed_entries


def build_entrymap(csv_column_names, column_map):
    """Builds a db column name to csv column index mapping. If no mapping file
    is given, we naively create the mapping using the order of the rows.

    column_map provided should be {csv column name: db column name},
    not including the primary ID.
    """
    # Naive approach, assumes the csv column names matches the db column names
    db_content_names = csv_column_names[1:]
    if column_map is None:
        return {
            column_name: index
            for index, column_name in enumerate(db_content_names, start=1)
        }

    if len(column_map) != len(db_content_names):
        print("WARNING: The db and csv column mapping file provided are "
              "mismatched in length. db column names are: "
              f"\n{db_content_names}\nThe provided column mapping "
              f"generated the following maping: \n{column_map}")

    # Using mapping provided by user to create the mapping
    db_column_to_index_map = {}
    for csv_column_name, db_column_name in column_map.items():
        if csv_column_name not in db_content_names:
            print(f"WARNING: {csv_column_name} not part of the db column "
                  f"names for values {db_content_names}. This may be warning"
                  "may be triggered due to including the primary key in the "
                  "mapping file. To not have this warning printed, remove "
                  "that mapping entry.")
            continue
        db_column_to_index_map[db_column_name] = csv_column_names.index(
            csv_column_name)
    return db_column_to_index_map


def send_entry(server, entry, entrymap, dry_run, authkey):
    postdata = {}
    for column_name, csv_index in entrymap.items():
        postdata[column_name] = entry[csv_index]

    print(postdata)
    if not dry_run:
        auth_headers = {'Authorization': 'JWT ' + authkey['access_token']}
        res = requests.post(server, json=postdata, headers=auth_headers)
        res_code = res.status_code
        print(res_code, res.text)
    else:
        res_code = 200  # STATUS CODE OK
    return res_code, res.text, postdata


def main(argv):
    if argv.dry_run:
        print("\nThis is a dry run. No data will be loaded to server whether "
              "a server_address has been provided or not.\n")
    elif not argv.server_address:
        print("\nWARNING: A server address was not provided in args. "
              "Only printing results locally. Use the -h arg if you don't "
              "know what this means.\n")
    authkey = auth(argv.auth_username, argv.auth_password, argv.auth_api)

    csv_data = parse_csv_to_memory(argv.csv_path)

    if argv.entrymap_path is not None:
        with open(argv.entrymap_path, "r") as fp:
            column_map = json.load(fp)
    entrymap = build_entrymap(
        csv_column_names=csv_data[0],
        column_map=column_map)

    failed_entries = load_csv_to_db(
        csv_data=csv_data,
        entrymap=entrymap,
        server=argv.server_address,
        authkey=authkey,
        dry_run=argv.dry_run)

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
        '--entrymap_path', '-e', dest='entrymap_path', required=False,
        default=None,
        help='the path to the JSON mapping file for db column names to csv'
        ' column names')
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
    parser.add_argument(
        '--user', '-u', dest='auth_username', required=True,
        help='the username to log in to the api with')
    parser.add_argument(
        '--pass', '-p', dest='auth_password', required=True,
        help='the password to log in to the api with')
    parser.add_argument(
        '--auth', '-a', dest='auth_api', required=True,
        help='the auth api')
    args = parser.parse_args()
    main(args)
