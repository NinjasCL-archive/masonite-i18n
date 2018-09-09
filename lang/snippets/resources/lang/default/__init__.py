# coding: utf-8

""" Language Locale Configuration File

This file stores the data used in the masonite-i18n package.
You can optionally add additional data if needed.

Examples: currency symbols, date format, money format

Attributes:

    ## Required

    name (string, required): Must be url valid. Used in routes and other places
    for lang identification. The convention is to match the directory name.

    title (string, required): Used for descriptions in logs or other places

    intervals = {{
        'few' : (dict, required, default=1,25): Stores the 'few'
                interval used in plural translation function.

        'many' : (dict, required, default=25,*): Stores the 'many'
                interval used in plural translation function.
    }}

    ## Optional

    enabled (bool, optional, default=True): Tells if the language is
            available for use.

"""

# Required
name = "{name}"
title = "{title}"

# These intervals are used in translation functions
# In order to pluralize strings.
# Only few and many are required.
intervals = {{"few": {{"from": 1, "to": 25}}, "many": {{"from": 25, "to": "*"}}}}

# Optional
enabled = True
