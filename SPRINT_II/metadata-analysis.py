import json
import datetime
import pandas as pd
from tqdm import tqdm
from pathlib import Path

_df = None

PROJECT_FOLDER = Path('/home/lucas.rotsen/Git_Repos/labex2')
METRICS_FOLDER = PROJECT_FOLDER.joinpath('SPRINT_II', 'metrics')
METADATA_FPATH = next(PROJECT_FOLDER.joinpath('SPRINT_II', "csv_files").glob('mil_*'))


def process_metrics():
    global _df

    consolidated_locs = list(
        map(generate_consolidated_loc, tqdm(METRICS_FOLDER.glob('*.json'), "Calculating consolidated loc",
                                            len(list(METRICS_FOLDER.glob('*.json'))))))

    _df = pd.read_csv(METADATA_FPATH, sep=',')
    _df_len = _df.shape[0]
    _df['loc'] = [0] * _df_len
    _df['release_frequency'] = [0] * _df_len

    today = datetime.datetime.today()

    for i in range(0, _df_len):
        corresponding_loc = [v[1] for v in consolidated_locs if v[0] == _df.loc[i, 'name_with_owner'].split('/')[1]][0]
        _df.at[i, 'loc'] = corresponding_loc
        _df.at[i, 'release_frequency'] = _df.loc[i, 'releases'] - (today - datetime.datetime.strptime(
            _df.loc[i, 'created_at'].split('T')[0], '%Y-%m-%d')).days


def generate_consolidated_loc(metric_fpath):
    with open(metric_fpath) as file:
        metric = json.load(file)

    repo_name = next(iter(metric)).split('/')[0]
    m_values = metric.values()

    consolidated_loc = sum([item.get('loc', 0) for item in m_values])

    return repo_name, consolidated_loc


def calculate_medians():
    medians = {
        'stars': [_df['stars'].median()],
        'watchers': [_df['watchers'].median()],
        'forks': [_df['forks'].median()],
        'releases': [_df['releases'].median()]
    }

    medians_df = pd.DataFrame(medians)

    medians_df.to_csv(PROJECT_FOLDER.joinpath('SPRINT_II', 'medians.csv'), encoding='utf-8', index=False)
    _df.to_csv(PROJECT_FOLDER.joinpath('SPRINT_II', 'repos.csv'), encoding='utf-8', index=False)


if __name__ == '__main__':
    process_metrics()
    calculate_medians()
