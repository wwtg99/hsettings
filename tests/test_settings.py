import os
from hsettings.hsettings import flatted_dict, nestted_dict, Settings


class TestSettings:

    def test_flat_nest(self):
        data1 = {
            'k1': 'v1',
            'k2': {
                'k2-1': 'v2-1',
                'k2-2': 'v2-2'
            },
            'k3': ['v3-1', 'v3-2'],
            'k4': 1,
            'k5': [0, 1, 2],
            'k6': {
                'k6-1': '',
                'k6-2': None,
                'k6-3': 1.2
            },
            'k7': {
                '1': '11'
            }
        }
        data2 = {
            'k1': 'v1',
            'k2.k2-1': 'v2-1',
            'k2.k2-2': 'v2-2',
            'k3': ['v3-1', 'v3-2'],
            'k4': 1,
            'k5': [0, 1, 2],
            'k6.k6-1': '',
            'k6.k6-2': None,
            'k6.k6-3': 1.2,
            'k7.1': '11'
        }
        flatted = flatted_dict(data1)
        assert flatted == data2
        assert nestted_dict(flatted) == data1
        nested = nestted_dict(data2)
        assert nested == data1
        assert flatted_dict(nested) == data2
        assert flatted_dict({}) == {}
        assert nestted_dict({}) == {}

    def test_settings(self):
        data1 = {
            'k1': 'v1',
            'k2': {
                'k2-1': 'v2-1',
                'k2-2': 'v2-2'
            },
            'k3': ['v3-1', 'v3-2'],
            'k4': 1,
            'k5': [0, 1, 2],
            'k6': {
                'k6-1': '',
                'k6-2': None,
                'k6-3': 1.2
            },
            'k7': {
                'k7-1': {
                    'k7-1-1': 7
                }
            }
        }
        settings = Settings(data1)
        assert settings.get('k1') == data1['k1']
        assert settings['k1'] == data1['k1']
        assert settings.get('k2.k2-1') == data1['k2']['k2-1']
        assert settings['k2.k2-1'] == data1['k2']['k2-1']
        assert settings.get('k3') == data1['k3']
        assert settings['k3'] == data1['k3']
        assert settings.get('k4') == data1['k4']
        assert settings['k4'] == data1['k4']
        assert settings.get('k7.k7-1.k7-1-1') == data1['k7']['k7-1']['k7-1-1']
        assert settings['k7.k7-1.k7-1-1'] == data1['k7']['k7-1']['k7-1-1']
        assert settings.get('k7.k7-1') == data1['k7']['k7-1']
        assert settings['k7.k7-1'] == data1['k7']['k7-1']
        assert settings.as_dict() == data1
        settings2 = settings.clone()
        assert settings == settings2
        assert settings is not settings2
        assert str(settings) == str(data1)
        settings2.set('k1', 'vv1')
        assert settings2.get('k1') == 'vv1'
        settings2['k1'] = 'vvv1'
        assert settings2.get('k1') == 'vvv1'
        settings2.set('k2.k2-1', 'vv2-1')
        assert settings2.get('k2.k2-1') == 'vv2-1'
        settings2['k2.k2-1'] = 'vvv2-1'
        assert settings2.get('k2.k2-1') == 'vvv2-1'
        settings2.set('k3', 'v3')
        assert settings2['k3'] == 'v3'
        settings2['k3'] = 'vv3'
        assert settings2['k3'] == 'vv3'
        data2 = {
            'k1': 'kk1',
            'k2': {
                'k2-1': 'kk2-1'
            },
            'k5': [3, 4],
            'k6': {
                'k6-2': 'kk6-2',
                'k6-4': 2.4
            }
        }
        settings3 = settings.clone()
        settings3.merge(data2)
        assert settings3['k1'] == 'kk1'
        assert settings3['k2.k2-1'] == 'kk2-1'
        assert settings3['k2.k2-2'] == 'v2-2'
        assert settings3['k3'] == ['v3-1', 'v3-2']
        assert settings3['k4'] == 1
        assert settings3['k5'] == [3, 4]
        assert settings3['k6.k6-1'] == ''
        assert settings3['k6.k6-2'] == 'kk6-2'
        assert settings3['k6.k6-3'] == 1.2
        assert settings3['k6.k6-4'] == 2.4
        settings4 = settings.clone()
        settings4.merge(Settings(data2))
        assert settings3 == settings4

    def test_json_loader(self):
        data1 = {
            'k1': 'v1',
            'k2': {
                'k2-1': 'v2-1',
                'k2-2': 'v2-2'
            },
            'k3': ['v3-1', 'v3-2'],
            'k4': 1,
            'k5': [0, 1, 2],
            'k6': {
                'k6-1': '',
                'k6-2': None,
                'k6-3': 1.2
            }
        }
        tmp_file = 'tmp.json'
        import json
        with open(tmp_file, 'w') as fp:
            json.dump(data1, fp)
        from hsettings.loaders import JsonLoader
        settings = JsonLoader.load(tmp_file)
        assert settings.as_dict() == data1
        os.unlink(tmp_file)

    def test_yaml_loader(self):
        data1 = {
            'k1': 'v1',
            'k2': {
                'k2-1': 'v2-1',
                'k2-2': 'v2-2'
            },
            'k3': ['v3-1', 'v3-2'],
            'k4': 1,
            'k5': [0, 1, 2],
            'k6': {
                'k6-1': '',
                'k6-2': None,
                'k6-3': 1.2
            }
        }
        tmp_file = 'tmp.yml'
        import yaml
        with open(tmp_file, 'w') as fp:
            yaml.dump(data1, fp)
        from hsettings.loaders import YamlLoader
        settings = YamlLoader.load(tmp_file)
        assert settings.as_dict() == data1
        os.unlink(tmp_file)

    def test_dict_loader(self):
        from hsettings.loaders import DictLoader
        data1 = {
            'k1': 'v1',
            'k2': 'v2',
            'k3': 1,
            'k4': '1'
        }
        settings = DictLoader.load(data1)
        assert settings.as_dict() == data1
        settings = DictLoader.load(data1, casts={'k3': str, 'k4': int})
        assert settings.get('k3') == '1'
        assert settings.get('k4') == 1
        settings = DictLoader.load(data1, includes=['k1', 'k2'])
        assert settings.as_dict() == {'k1': 'v1', 'k2': 'v2'}
        settings = DictLoader.load(data1, excludes=['k3', 'k4'])
        assert settings.as_dict() == {'k1': 'v1', 'k2': 'v2'}
        settings = DictLoader.load(data1, includes=['k1', 'k2'], excludes=['k2', 'k3'])
        assert settings.as_dict() == {'k1': 'v1'}
        settings = DictLoader.load(data1, key_mappings={
            'k2': 'k2.k2-1',
            'k3': 'k2.k2-2'
        })
        assert settings.as_dict() == {
            'k1': 'v1',
            'k2': {
                'k2-1': 'v2',
                'k2-2': 1
            },
            'k4': '1'
        }
        settings = DictLoader.load(data1, key_mappings={
            'k2': 'k2.k2-1',
            'k3': 'k2.k2-2'
        }, only_key_mappings_includes=True)
        assert settings.as_dict() == {
            'k2': {
                'k2-1': 'v2',
                'k2-2': 1
            }
        }

    def test_env_loader(self):
        from hsettings.loaders import EnvLoader
        settings = EnvLoader.load()
        data_env = dict(os.environ)
        assert settings.as_dict() == data_env
        data1 = {
            'k1': 'v1',
            'k2': 'v2',
            'k3': 1
        }
        tmp_file = 'tmp.env'
        with open(tmp_file, 'w') as fp:
            for k, v in data1.items():
                fp.write('{}={}\n'.format(k, v))

        settings = EnvLoader.load(tmp_file)
        data2 = {
            'k1': 'v1',
            'k2': 'v2',
            'k3': '1'
        }
        data_env = dict(os.environ)
        data_env.update(data2)
        assert settings.as_dict() == data_env
        settings = EnvLoader.load(tmp_file, casts={'k3': int})
        data3 = {
            'k1': 'v1',
            'k2': 'v2',
            'k3': 1
        }
        data_env = dict(os.environ)
        data_env.update(data3)
        assert settings.as_dict() == data_env
        settings = EnvLoader.load(tmp_file, casts={'k3': int}, env_to_key_mapping={
            'k2': 'k2.k2-1',
            'k3': 'k2.k2-2'
        })
        data4 = {
            'k1': 'v1',
            'k2': {
                'k2-1': 'v2',
                'k2-2': 1
            }
        }
        data_env = dict(os.environ)
        data_env.update(data4)
        assert settings.as_dict() == data_env
        os.unlink(tmp_file)
