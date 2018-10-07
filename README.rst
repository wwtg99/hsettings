Hybrid Settings
---------------

Description
===========

This package can load settings from multiple sources and hybrid them into one dict-like object.

Installation
============

For Python 3.5+

.. code-block:: shell

    pip install hsettings


Usage
=====

Load settings
~~~~~~~~~~~~~

Load settings from dict.

.. code-block:: python

    from hsettings.loaders import DictLoader
    data1 = {
        'k1': 'v1',
        'k2': 'v2',
        'k3': 1,
        'k4': '1'
    }
    settings = DictLoader.load(data1)

    // type casts
    settings = DictLoader.load(data1, casts={
        'k3': str, 'k4': int
    })
    assert settings.get('k3') == '1'
    assert settings.get('k4') == 1
    // keys includes
    settings = DictLoader.load(data1, includes=['k1', 'k2'])
    assert settings.as_dict() == {'k1': 'v1', 'k2': 'v2'}
    // keys excludes
    settings = DictLoader.load(data1, excludes=['k3', 'k4'])
    assert settings.as_dict() == {'k1': 'v1', 'k2': 'v2'}
    // keys includes and excludes
    settings = DictLoader.load(
        data1, 
        includes=['k1', 'k2'], 
        excludes=['k2', 'k3']
    )
    assert settings.as_dict() == {'k1': 'v1'}
    // map keys to inner keys
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
    // map keys to inner keys and only contains these keys
    // this is useful to load use defined envs
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


Load settings from json file.

.. code-block:: python

    from hsettings.loaders import JsonLoader
    settings = JsonLoader.load(json_file)


Load settings from yaml file.

.. code-block:: python

    from hsettings.loaders import YamlLoader
    settings = YamlLoader.load(yaml_file)


Load settings from environment and/or env file.
Support casts, env_to_key_mapping, includes, excludes and only_key_mappings_includes as DictLoader.
Use env_to_key_mapping and only_key_mappings_includes parameters to only get specific env settings.

.. code-block:: python

    // load from environment
    from hsettings.loaders import EnvLoader
    settings = EnvLoader.load()

    // load from environment and env file
    from hsettings.loaders import EnvLoader
    settings = EnvLoader.load(env_file) 


Use settings
~~~~~~~~~~~~

.. code-block:: python

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

    // get settings by get method or []
    print(settings.get('k1'))
    // output v1
    print(settings['k1'])
    // output v1
    // use dot(.) to get inner value
    print(settings.get('k2.k2-1'))
    // output v2-1
    print(settings['k2.k2-1'])
    // output v2-1
    // set default value if not set
    // note None is not equal to not set
    print(settings.get('not_set', 'yes'))
    // output yes
    // get whole settings as dict
    print(settings.as_dict())
    // clone a new settings
    settings2 = settings.clone()
    print(settings2 == settings)
    // output True
    print(settings2 is settings)
    // output False

    // set settings by set method or []
    settings.set('k3', 'v3')
    print(settings['k3])
    // output v3
    settings['k3'] = 'vv3'
    print(settings['k3'])
    // output vv3

    // merge settings, keys conflict will be overrided
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
    print(settings3['k2.k2-1'])
    print(settings3['k2.k2-1'])
    // output kk2-1
    // output v2-1


More examples are in tests.


Test
====

Run unit test

.. code-block:: shell

    pytest

