import json
import datetime
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from dateutil.relativedelta import relativedelta

_df = None

PROJECT_FOLDER = Path('/home/lucas.rotsen/Git_Repos/labex2')
METRICS_FOLDER = PROJECT_FOLDER.joinpath('SPRINT_II', 'metrics')
METADATA_FPATH = next(PROJECT_FOLDER.joinpath('SPRINT_II', "csv_files").glob('mil_*'))


def process_metrics():
    global _df

    consolidated_locs = [generate_consolidated_loc(m) for m in tqdm(list(METRICS_FOLDER.glob('*.json')))]

    _df = pd.read_csv(METADATA_FPATH, sep=',')
    _df_len = _df.shape[0]
    _df['loc'] = _df['release_frequency'] = _df['age'] = [0] * _df_len

    today = datetime.datetime.today()

    for i in range(0, _df_len):
        try:
            corresponding_loc = [v[1] for v in consolidated_locs if v is not None and
                                 v[0] == _df.loc[i, 'name_with_owner'].split('/')[1]][0]
        except IndexError:
            continue

        _df.at[i, 'loc'] = corresponding_loc
        _df.at[i, 'release_frequency'] = _df.loc[i, 'releases'] - (today - datetime.datetime.strptime(
            _df.loc[i, 'created_at'].split('T')[0], '%Y-%m-%d')).days
        _df.at[i, 'age'] = relativedelta(today, datetime.datetime.strptime(
            _df.loc[i, 'created_at'].split('T')[0], '%Y-%m-%d')).years


def generate_consolidated_loc(metric_fpath):
    try:

        with open(metric_fpath) as file:
            metric = json.load(file)

        repo_name = next(iter(metric)).split('/')[0]
        m_values = metric.values()

        consolidated_loc = sum([item.get('loc', 0) for item in m_values])

    except Exception:
        return

    return repo_name, consolidated_loc


def calculate_medians():
    medians = {
        'stars': [_df['stars'].median()],
        'watchers': [_df['watchers'].median()],
        'forks': [_df['forks'].median()],
        'releases': [_df['releases'].median()],
        'release_frequency': [_df['release_frequency'].median()],
        'locs': [_df['loc'].median()],
        'age': [_df['age'].median()]
    }

    medians_df = pd.DataFrame(medians)

    medians_df.to_csv(PROJECT_FOLDER.joinpath('SPRINT_II', 'medians.csv'), encoding='utf-8', index=False)
    _df.to_csv(PROJECT_FOLDER.joinpath('SPRINT_II', 'repos.csv'), encoding='utf-8', index=False)


if __name__ == '__main__':
    process_metrics()
    calculate_medians()
