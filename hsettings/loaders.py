import os
import shlex
import re
from hsettings.hsettings import Settings, nestted_dict


class EnvLoader:

    @classmethod
    def load(cls, filepath=None, casts=None, env_to_key_mapping=None):
        """
        Load environments from system env and env file.

        casts should be a mapping of callable for type transform.

        For example,

        {
            'key1': int,  # transform to int
            'key2': float  # transform to float
        }

        env_to_key_mapping:
        {
            'env': 'config_key'
        }

        For example,

        {
            'TEMP': 'config.temp'
        }

        This will generate

        {
            'config': {
                'temp': <value to TEMP>
            }
        }

        :param filepath: env file
        :param env_to_key_mapping: map env to a nested config
        :rtype: Settings
        """
        envs = {}
        for key in os.environ:
            envs[key] = os.environ[key]
        if filepath:
            envs.update(cls.load_env_file(filepath))
        if casts:
            for k, func in casts.items():
                if k in envs:
                    envs[k] = func(envs[k])
        if env_to_key_mapping:
            for k, mk in env_to_key_mapping.items():
                if k in envs:
                    val = envs[k]
                    envs[mk] = val
                    del envs[k]
            envs = nestted_dict(envs)
        return Settings(envs)

    @classmethod
    def load_env_file(cls, filepath):
        """
        Load from env file.

        :param filepath:
        :return: dict
        """
        envs = {}
        with open(filepath) as fp:
            for line in fp:
                tokens = list(shlex.shlex(line, posix=True))
                # parses the assignment statement
                if len(tokens) < 3:
                    continue
                name, op = tokens[:2]
                value = ''.join(tokens[2:])
                if op != '=':
                    continue
                if not re.match(r'[A-Za-z_][A-Za-z_0-9]*', name):
                    continue
                value = value.replace(r'\n', '\n').replace(r'\t', '\t')
                envs[name] = value
        return envs


class JsonLoader:

    @classmethod
    def load(cls, filepath):
        """
        Load from json file.

        :param filepath:
        :rtype: Settings
        """
        import json
        with open(filepath) as fp:
            return Settings(json.load(fp))


class YamlLoader:

    @classmethod
    def load(cls, filepath):
        """
        Load from yaml file.

        :param filepath:
        :rtype: Settings
        """
        import yaml
        with open(filepath) as fp:
            return Settings(yaml.load(fp))
