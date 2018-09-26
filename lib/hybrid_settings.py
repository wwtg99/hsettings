import collections


__author__ = 'wuwentao'
__author_email__ = 'wwtg99@126.com'
__prog__ = 'hsettings'
__version__ = '0.1.0'
__descr__ = 'Hybrid settings from multiple sources.'

# Cannot rely on None since it may be desired as a return value.
NOTSET = type(str('NoValue'), (object,), {})


class Settings:

    def __init__(self, setting=None, sep='.'):
        """

        :param setting: default settings
        :param sep: separator char in key, default dot(.)
        """
        super().__init__()
        self._sep = sep
        self._settings = setting if setting and isinstance(setting, dict) else {}
        self._flatted_settings = flatted_dict(self._settings)

    def merge(self, other):
        """
        Merge Settings with another Settings or dict.

        :param other: other Settings or dict
        :return: self
        :rtype: Settings
        """
        if isinstance(other, Settings):
            new_dict = flatted_dict(other.as_dict())
        elif isinstance(other, dict):
            new_dict = flatted_dict(other)
        else:
            raise TypeError('Not supported type')
        self._flatted_settings.update(new_dict)
        self._settings = nestted_dict(self._flatted_settings)
        return self

    def as_dict(self):
        """
        Return dict object.

        :return: dict
        :rtype: dict
        """
        return self._settings

    def clone(self):
        """
        Clone settings.

        :return: new Settings
        :rtype: Settings
        """
        return Settings(dict(self.as_dict()))

    def get(self, item, default=NOTSET):
        """
        Get item.

        :param item: search key, use dot('.) to search in path
        :param default: return value if not found
        :return: value or default if not found
        """
        if self._sep in item:
            if item in self._flatted_settings:
                return self._flatted_settings[item]
            keys = item.split(self._sep)
            func = lambda obj, k: obj[k] if k in obj else NOTSET
            obj = self._settings
            val = default
            for key in keys:
                val = func(obj, key)
                if val is NOTSET:
                    return default
                else:
                    obj = val
            return val
        elif item in self._settings:
            return self._settings[item]
        return default

    def set(self, item, value):
        """
        Set value by key.

        :param item: key, use dot(.) to set in path
        :param value: value to set
        """
        self._flatted_settings[item] = value
        self._settings = nestted_dict(self._flatted_settings)

    def has(self, item):
        """
        Whether contains item key.

        :param item: search key, use dot('.) to search in path
        :return: bool
        :rtype: bool
        """
        if self._sep in item:
            if item in self._flatted_settings:
                return True
        elif item in self._settings:
            return True
        return False

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, item):
        return self.has(item)

    def __eq__(self, o):
        if isinstance(o, Settings):
            return self.as_dict() == o.as_dict()
        return False

    def __str__(self):
        return str(self.as_dict())


def flatted_dict(d, parent_key='', sep='.', quiet=False):
    """
    Flat dict to one level dict.
    Use dot(.) in key to present level.

    :param dict d: target dict
    :param parent_key: parent key
    :param sep: separator string
    :param quiet: do not raise error
    :return: flatten dict
    :rtype: dict
    """
    items = []
    for k, v in d.items():

        if not quiet and sep in k:
            raise ValueError('Separator "%(sep)s" already in key, '
                             'this may lead unexpected behaviour, '
                             'choose another.' % dict(sep=sep))

        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatted_dict(v, new_key, sep=sep).items())
            if not v:  # empty dict
                items.append((new_key, v))
        else:
            items.append((new_key, v))
    return dict(items)


def nestted_dict(d, sep='.'):
    """
    Transform flatted dict to nested dict.

    :param d: dict
    :param sep: separator string
    :return: nested dict
    :rtype: dict
    """
    ret = {}
    for k, v in d.items():
        if sep in k:
            keys = k.split(sep)
            target = ret
            while len(keys) > 1:
                current_key = keys.pop(0)
                target = target.setdefault(current_key, {})
            else:
                assert len(keys) == 1
                target[keys[0]] = v
        else:
            ret[k] = v
    return ret
