from config import config
from tools.utils import validate_config


def test_config():
    for ad_config in config:
        ad_config = config[ad_config]
        validate_config(ad_config)
    assert 2 + 2 == 4
