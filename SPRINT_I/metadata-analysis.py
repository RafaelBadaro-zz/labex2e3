import json
import pandas as pd
from tqdm import tqdm
from pathlib import Path

_df = None

PROJECT_FOLDER = Path('/home/lucas.rotsen/Git_Repos/labex2')
METRICS_FOLDER = PROJECT_FOLDER.joinpath('SPRINT_I', 'metrics')
METADATA_FPATH = next(PROJECT_FOLDER.joinpath('SPRINT_I').glob('*.csv'))


def process_metrics():
    global _df

    consolidated_locs = list(
        map(generate_consolidated_loc, tqdm(METRICS_FOLDER.glob('*.json'), "Calculating consolidated loc",
                                            len(list(METRICS_FOLDER.glob('*.json'))))))

    _df = pd.read_csv(METADATA_FPATH, sep=',')
    _df_len = _df.shape[0]
    _df['loc'] = [0] * _df_len

    for i in range(0, _df_len):
        corresponding_loc = [v[1] for v in consolidated_locs if v[0] == _df.loc[i, 'name_with_owner'].split('/')[1]][0]
        _df.at[i, 'loc'] = corresponding_loc


def generate_consolidated_loc(metric_fpath):
    with open(metric_fpath) as file:
        metric = json.load(file)

    repo_name = next(iter(metric)).split('/')[0]
    m_values = metric.values()

    consolidated_loc = sum([item.get('loc', 0) for item in m_values])

    return repo_name, consolidated_loc


def calculate_medians():

    medians = {
        'stars': [_df['forks'].median()],
        'watchers': [_df['stars'].median()],
        'forks': [_df['releases'].median()],
        'releases': [_df['watchers'].median()]
    }

    medians_df = pd.DataFrame(medians)

    medians_df.to_csv(PROJECT_FOLDER.joinpath('SPRINT_I', 'medians.csv'), encoding='utf-8', index=False)
    _df.to_csv(PROJECT_FOLDER.joinpath('SPRINT_I', 'repos.csv'), encoding='utf-8', index=False)


if __name__ == '__main__':
    process_metrics()
    calculate_medians()
