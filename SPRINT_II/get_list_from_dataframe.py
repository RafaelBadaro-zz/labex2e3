import pandas as pd
from pathlib import Path

SPRINT_FOLDER = Path('/home/lucas.rotsen/Git_Repos/labex2/SPRINT_II')
METADATA_FPATH = next(SPRINT_FOLDER.joinpath('csv_files').glob('mil_*'))


def get_url_list_from_dataframe():
    df = pd.read_csv(METADATA_FPATH, sep=',')

    url_list = [url + '.git' for url in df['url'].tolist()]

    with open(SPRINT_FOLDER.joinpath('repository-list.txt'), 'w') as file:
        for item in url_list:
            file.write("%s\n" % item)


if __name__ == '__main__':
    get_url_list_from_dataframe()
