"""Client program."""

import argparse
import requests

from utils.helpers import process_csv
from tasks.tasks import send


def main():
    """Entry point for the client."""
    parser = argparse.ArgumentParser(description='Client program.')
    parser.add_argument('-f',
                        '--file',
                        action='store',
                        dest='file_loc',
                        default=None, help='Optional data file location',
                        required=False)

    parser.add_argument('-u',
                        '--url',
                        action='store',
                        dest='file_url',
                        default=None, help='Optional data file URL',
                        required=False)
    cmd_args = parser.parse_args()
    file_loc = cmd_args.file_loc
    file_url = cmd_args.file_url
    csv_file_name = None

    if file_loc:
        csv_file_name = file_loc
    elif file_url:
        csv_file_name = 'user_data_file.csv'
        response = requests.get(file_url, verify=False)
        with open(csv_file_name, 'wb') as f:
            f.write(response.content)
    user_data = process_csv(csv_file_name)
    # Place the data into the queue and get the result.
    result = send.delay(user_data).get()
    if result == 'Success':
       print('Operation succeeded')
    else:
       print('Failed')


if __name__ == '__main__':
    main()
