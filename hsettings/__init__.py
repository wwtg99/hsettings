"""
HSettings
---------

Description
===========

Hybrid settings from multiple sources.

Load settings from dict, json file, yaml file, environment or other sources, merge into one dict-like object.
Support some useful methods to search and operate in the deep dict.

"""
from .hsettings import Settings, NOTSET


__author__ = 'wuwentao'
__author_email__ = 'wwtg99@126.com'
__prog__ = 'hsettings'
__version__ = '0.1.5'
__descr__ = 'Python hybrid settings from multiple sources.'

__all__ = ['Settings', 'NOTSET']
