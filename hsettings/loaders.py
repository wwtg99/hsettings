import os
import shlex
import re
from hsettings.hsettings import Settings, nestted_dict


class DictLoader:

    @classmethod
    def load(cls, d, casts=None, key_mappings=None, includes=None, excludes=None, only_key_mappings_includes=False):
        """
        Load dict from dict-like object.

        casts should be a mapping of callable for type transform.

        For example,

        {
            'key1': int,  # transform to int
            'key2': float  # transform to float
        }

        includes should be a list of keys remains.

        excludes should be a list of keys that not remains.

        key_mappings is a dict that map flatten dict to nested dict.

        key_mappings:
        {
            'key': 'config_key'
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

        only_key_mappings_includes indicates only includes keys in key_mappings if key_mappings is set.

        :param dict d:
        :param dict casts: value type casts
        :param dict key_mappings: key mappings
        :param list includes: keys included
        :param list excludes: keys excluded
        :param bool only_key_mappings_includes: only include keys in key_mappings
        :rtype: Settings
        """
        if not isinstance(d, dict):
            raise ValueError('invalid dict')
        ret = dict(d)
        if casts:
            for k, func in casts.items():
                if k in d:
                    ret[k] = func(ret[k])
        if includes:
            ret = dict([(k, ret[k]) for k in ret if k in includes])
        if excludes:
            ret = dict([(k, ret[k]) for k in ret if k not in excludes])
        if key_mappings:
            if only_key_mappings_includes:
                ret = dict([(k, ret[k]) for k in ret if k in key_mappings])
            for k, mk in key_mappings.items():
                if k in ret and mk != k:
                    ret[mk] = ret[k]
                    del ret[k]
            ret = nestted_dict(ret)
        return Settings(ret)


class EnvLoader:

    @classmethod
    def load(cls, filepath=None, casts=None, env_to_key_mapping=None, includes=None, exclueds=None, only_key_mappings_includes=False):
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
        :param list includes: keys included
        :param list excludes: keys excluded
        :param bool only_key_mappings_includes: only include keys in key_mappings
        :rtype: Settings
        """
        envs = {}
        for key in os.environ:
            envs[key] = os.environ[key]
        if filepath:
            envs.update(cls.load_env_file(filepath))
        return DictLoader.load(envs, casts=casts, key_mappings=env_to_key_mapping, includes=includes, excludes=exclueds, only_key_mappings_includes=only_key_mappings_includes)

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
