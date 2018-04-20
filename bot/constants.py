# coding=utf-8
import logging
import os
from collections import ChainMap
from pathlib import Path

import yaml


log = logging.getLogger(__name__)


def _required_env_var_constructor(loader, node):
    value = loader.construct_scalar(node)
    return os.environ[value]


def _env_var_constructor(loader, node):
    value = loader.construct_scalar(node)
    return os.getenv(value)


yaml.SafeLoader.add_constructor('!REQUIRED_ENV', _required_env_var_constructor)
yaml.SafeLoader.add_constructor('!ENV', _env_var_constructor)


with open('config-example.yml') as f:
    _CONFIG_YAML = ChainMap(yaml.safe_load(f))


if Path('config.yml').exists():
    log.error("Found `config.yml` file, loading constants from it.")
    with open('config.yml') as f:
        _CONFIG_YAML.new_child(yaml.safe_load(f))


class YAMLGetter(type):
    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        if cls.subsection is not None:
            return _CONFIG_YAML[cls.section][cls.subsection][name]
        return _CONFIG_YAML[cls.section][name]

    def __getitem__(cls, name):
        return cls.__getattr__(name)


class Bot(metaclass=YAMLGetter):
    section = 'bot'


class Cooldowns(metaclass=YAMLGetter):
    section = 'bot'
    subsection = 'cooldowns'


class Emojis(metaclass=YAMLGetter):
    section = 'bot'
    subsection = 'emojis'


class Channels(metaclass=YAMLGetter):
    section = 'guild'
    subsection = 'channels'


class Roles(metaclass=YAMLGetter):
    section = 'guild'
    subsection = 'roles'


class Guild(metaclass=YAMLGetter):
    section = 'guild'


class Keys(metaclass=YAMLGetter):
    section = 'keys'


class ClickUp(metaclass=YAMLGetter):
    section = 'clickup'


class Papertrail(metaclass=YAMLGetter):
    section = 'papertrail'


class URLs(metaclass=YAMLGetter):
    section = 'urls'


SITE_URL = URLs.site or "pythondiscord.local:8080"
SITE_PROTOCOL = 'http' if 'local' in SITE_URL else 'https'
SITE_API_USER_URL = f"{SITE_PROTOCOL}://api.{SITE_URL}/user"
SITE_API_TAGS_URL = f"{SITE_PROTOCOL}://api.{SITE_URL}/tags"
