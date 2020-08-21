# mano-aloe-csv-script
python script to transfer csv data to a certain website

```
usage: main.py [-h] --csv_path CSV_PATH [--dry_run]
               [--fail_csv_path FAIL_CSV_PATH] [--server SERVER_ADDRESS]

Parse a specifically formatted CSV

optional arguments:
  -h, --help            show this help message and exit
  --csv_path CSV_PATH, -c CSV_PATH
                        the path to the csv file
  --dry_run, -d         performs a dry run locally when provided with a
                        server_address
  --fail_csv_path FAIL_CSV_PATH, -f FAIL_CSV_PATH
                        the path to drop a csv with failed entries
  --server SERVER_ADDRESS, -s SERVER_ADDRESS
                        the server address for the results to be uploaded
```
