import os
from typing import Dict, Set
from pathlib import Path
from eips_exposed.common.exceptions import ConfigurationError

CONFIG: Dict = {
    'EIPS_REMOTE_REPO': 'https://github.com/ethereum/EIPs.git',
    'EIPS_LOCAL_REPO': os.environ.get('EIPS_LOCAL_REPO'),
    'EIPS_DIR': None,
    'SERVER_PORT': os.environ.get('EIPS_SERVER_PORT', 5000),
    'EIPS_DB_URL': os.environ.get('EIPS_DB_URL'),
}


def assert_required_config(names: Set[str]) -> None:
    """ Require that a config var is defined or die """
    for name in names:
        if not CONFIG.get(name):
            raise ConfigurationError('Missing configuration for {}'.format(name))


REQUIRED_CONFIG: Set = {'EIPS_REMOTE_REPO', 'EIPS_LOCAL_REPO', 'EIPS_DB_URL'}
assert_required_config(REQUIRED_CONFIG)

# Coerce paths
CONFIG['EIPS_LOCAL_REPO'] = Path(CONFIG['EIPS_LOCAL_REPO'])  # type: ignore
CONFIG['EIPS_DIR'] = CONFIG['EIPS_LOCAL_REPO'].joinpath('EIPS')  # type: ignore
