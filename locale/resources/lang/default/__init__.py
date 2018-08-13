# -*- coding: utf-8 -*-

''' Locale Configuration File

This file stores the data used in the masonite-i18n package.
You can optionally add additional data if needed.

Examples: currency symbols, date format, money format

Attributes:

    ## Required

    name (string, required): Must be url valid. Used in routes and other places
    for locale identification. The convention is to match the directory name.

    title (string, required): Used for descriptions in logs or other places

    ## Optional

    enabled (bool, optional, default=True): Tells if the language is available for use.

    intervals = {
        'few' : (string, optional, default=1,25): Stores the 'few' interval used in _n() translation function.
        'many' : (string, optional, default=25,*): Stores the 'many' interval used in _n() translation function.
        'other' : (string, optional, default=*): Stores the 'other' interval used in _n() translation function.
    }
'''

# Required
name = 'default'
title = 'Default'

# Optional
enabled = True
intervals = {
    'few' : '1,25',
    'many' : '25,*',
    'other' : '*'
}

# Custom
