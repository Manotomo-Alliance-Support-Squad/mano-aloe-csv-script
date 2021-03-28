# mano-aloe-csv-script
python script to transfer csv data to a certain website

```
usage: main.py [-h] --csv_path CSV_PATH [--entrymap_path ENTRYMAP_PATH]
               [--dry_run] [--fail_csv_path FAIL_CSV_PATH]
               [--duplicate_column_name DUPLICATE_COLUMN_NAME]
               [--server SERVER_ADDRESS] --user AUTH_USERNAME --pass
               AUTH_PASSWORD --auth AUTH_API

Parse a specifically formatted CSV

optional arguments:
  -h, --help            show this help message and exit
  --csv_path CSV_PATH, -c CSV_PATH
                        the path to the csv file
  --entrymap_path ENTRYMAP_PATH, -e ENTRYMAP_PATH
                        the path to the JSON mapping file for db column names
                        to csv column names
  --dry_run, -d         performs a dry run locally when provided with a
                        server_address
  --fail_csv_path FAIL_CSV_PATH, -f FAIL_CSV_PATH
                        the path to drop a csv with failed entries
  --duplicate_column_name DUPLICATE_COLUMN_NAME, -dc DUPLICATE_COLUMN_NAME
                        The column name where duplicate is marked and skipped.
                        If there are any values within that column, it will
                        count as a hit.
  --server SERVER_ADDRESS, -s SERVER_ADDRESS
                        the server address for the results to be uploaded
  --user AUTH_USERNAME, -u AUTH_USERNAME
                        the username to log in to the api with
  --pass AUTH_PASSWORD, -p AUTH_PASSWORD
                        the password to log in to the api with
  --auth AUTH_API, -a AUTH_API
                        the auth api

```

## Entry Map JSON File

An entry map should be a json file with the `csv column name` as the key and the `db column name` as the value.

For example:

If you want to insert the below CSV file:

|time|csv_col_a|csv_col_b|
|--|--|--|
|115901|aaaaaa|bbbbbb|

Into the DB table below:

|db_col_1|db_col_2|
|--|--|
|bbbbbb|aaaaaa|

I would need to create a the below JSON mapping file:
```
{
  'csv_col_a': 'db_col_2',
  'csv_col_b': 'db_col_1',
}
```

The time column in the csv will be ignored.

## Duplicate Entries to Ignore

Use the `--duplicate_column_name` argument to add in the name of the CSV column that you want to use to ignore a row completely. Any values within that cell will automatically skip the entire row.
