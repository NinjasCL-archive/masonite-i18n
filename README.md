# Masonite i18n
This project aims to bring internationalization (*i18n*) tools and helpers to [Masonite Framework](https://masoniteproject.com).

## Code
The development code will be stored in the `master` branch and production ready code will be stored in the `production` branch.

### Code of Conduct
In all places where communication is needed (issues, pull requests, chat). Just stick to be a friendly, mature and nice person. Avoid unwanted conflict, toxic behaviour or feeding the troll.

### License
[MIT](LICENSE)

### Changelog
[Changelog](CHANGELOG.md)

## Core Desing
The main design is inspired on the implementations used in different projects, mainly: [Processwire](https://processwire.com), [Laravel](https://laravel.com) and [Rails](https://rubyonrails.org/). The goal is having a system that could be easily used and implement only the parts that are needed for a strong i18n support in *static* files. Unlike other frameworks or tools that try to do too much, this implementation will rely on the tools already provided by Python focusing only in the translation helpers. You could see the original discussion topic [here](https://github.com/MasoniteFramework/core/issues/235).

### Convention over configuration
In order to keep i18n smooth and simple it will be designed with sensible defaults and defined structures and conventions. But with the option to change them when needed.

### Explicit over implicit
Is best to know what are you doing. Too many times a framework do '*magic*' tricks behind scenes. The design will be focused on functions that do one thing well and be explicit about it.

### Pythonic as possible
The project would strive to design an API simple to use. Inspired by libs such as [Requests](http://docs.python-requests.org/en/master/). The API should be similar to gettext function calls in order to facilitate adoption.

### Focus on Translation Only
Other more advanced tools like [Babel](http://babel.pocoo.org/en/latest/) implement localization functions like currency and date format. This project aims to bring just the needed tools for text translation (message, catalogs and pluralization).


### Translation Files
For storing the string translations it will be used [HJSON](https://hjson.org/) files. These have an advantage over [*po* and *mo*](https://es.wikipedia.org/wiki/Gettext) files since they could be easily edited without special tooling. They have an advantage over raw *json* files because they are more human friendly (tolerate trailing commas, have comments and multiline strings). Finally they are better than just python code because they could be easily swaped on runtime without much hazzle.

#### Why use files instead of database rows?
The main reason is that you should keep your translation files in version controlled repository. Your project evolves over time and translations should be alongside the code that use them. If you store them in a database you risk forgetting to backup the latest version or have conflicting changes between versions. 

This *only applies to static content*. Dynamic content translations must be stored in the same place as the content (database). But the implementation depends on each project and is beyond this translation tool.

#### Storage
The translation files will be stored inside the `resources/lang/{name}` directory. Where `{name}` must be replaced with a desired language name (recommended an [ISO 639-1 or 639-2](http://www.loc.gov/standards/iso639-2/php/code_list.php) based name). The name is important since it will be matched against the lang param provided by the request middleware.

##### `default`
The special `resources/lang/default` directory will be used as the main translation and fallback language.

Using this structure any language could be the default translation, just put the correct files inside the default folder, no need for configuration. Optionally it can be configured to another default directory if desired too.

#### Config
The configuration file will be called `lang.py` and it will be inside the `config` directory.

The contents would be similar to:

```python

    """
    |--------------------------------------------------------------------------
    | Application Locale Configuration
    |--------------------------------------------------------------------------
    |
    | The application locale determines the default locale that will be used
    | by the translation service provider. You are free to set this value
    | to any of the locales which will be supported by the application.
    |
    """

    LOCALE = 'default'
    
    """
    |--------------------------------------------------------------------------
    | Application Fallback Locale
    |--------------------------------------------------------------------------
    |
    | The fallback locale determines the locale to use when the current one
    | is not available. You may change the value to correspond to any of
    | the language folders that are provided through your application.
    |
    """

    LOCALE_FALLBACK = 'default'
    
```

#### Directory Files
The language directory would consist of several files. One named `__init__.py` and the `hjson` files containing the translation content.

##### `__init__.py`
This file contains the needed data for the system to detect the language as valid.


- `name` (required, string): The same as the directory name.
- `title` (required, string): A friendly name for the language.
- `enabled` (optional, bool, default=True): Tells if the language is active or not.

###### Example

```python
name = 'en'
title = 'English'
enabled = True
```

##### `locale.hjson`
This file is optional and contains the locale information related to the language. The only really used part is the `intervals` key. Other keys are optional and should be filled as needed.

###### Example

```hjson
{
	intervals : {
	  	# These intervals are used in translation functions
	  	# In order to pluralize strings.
	  	few : {
	  		from : 1
	  		to : 25
	  	}
	  	many : {
	  		from : 25
	  		to : *
	  	}
	  	other : {
	  		from : 1000
	  		to : 10001
	  	}
  }
}
```

###### Example with additional info
The additional info could be anything that can be used for localization purposes using other tools or functions.

```hjson
{
  intervals : {
  	# These intervals are used in translation functions
  	# In order to pluralize strings.
  	few : {
  		from : 1
  		to : 25
  	}
  	many : {
  		from : 25
  		to : *
  	}
  	other : {
  		from : 1000
  		to : 10001
  	}
  }
  
  # Information obtained from http://www.localeplanet.com
  country: US
  country_name: United States
  currency : {
	  symbol: US$
	  code: USD
	  symbol_native: $
	  decimal_digits: 2
	  rounding: 0
  }
  date_format_symbols:
  {
    am_pm:
    [
      AM
      PM
    ]
    day_name:
    [
      Sunday
      Monday
      Tuesday
      Wednesday
      Thursday
      Friday
      Saturday
    ]
    day_short:
    [
      Sun
      Mon
      Tue
      Wed
      Thu
      Fri
      Sat
    ]
    era:
    [
      BC
      AD
    ]
    era_name:
    [
      Before Christ
      Anno Domini
    ]
    month_name:
    [
      January
      February
      March
      April
      May
      June
      July
      August
      September
      October
      November
      December
    ]
    month_short:
    [
      Jan
      Feb
      Mar
      Apr
      May
      Jun
      Jul
      Aug
      Sep
      Oct
      Nov
      Dec
    ]
    order_full: MDY
    order_long: MDY
    order_medium: MDY
    order_short: MDY
  }
  decimal_format_symbols:
  {
    decimal_separator: .
    grouping_separator: ","
    minus: -
  }
  language_code: en
  language_name: English
  locale: en-US-POSIX
  locale_underscore: en_US-POSIX
  locale_name: English (United States, Computer)
}
```

##### `{translation-file}.hjson`
All files would be stored in the same folder and the naming convention would be the following:

- Directory separators (`/` or `\`) would be standarized as double dash `--` except the root that would be ommited.
- Extension dot (`.`) would be replaced with a single dash `-`.
- Trimmed spaces.
- Lowercase.
- Hjson valid.

###### Example

`./resources/templates/welcome.html` would be standarized as `resources--templates--welcome-html.hjson`

The content of each translation file would be similar to the following example:

`resources--templates--welcome-html.hjson`

```hjson
{
	file : 'resources/templates/welcome.html' # Required
	textdomain : 'resources--templates--welcome-html' # Required
	language : { # Optional
	  name : 'en'
	  title: 'English' 
	}
	translations : { # Required
	    '{hash}' : {
	        'original' : '', # Optional
	        'comment' : '', # Optional
	        'note' : '', # Optional
	        'text' : '' # Required
	    }
	}
}
```

`file` 

Would store the path to the file beign translated.

`textdomain`

Inspired by Processwire. Textdomains are used to ensure that only the necessary translations are kept in memory at the same time, and that there aren't namespace collisions of unrelated translations.

Each file is considered it's own textdomain and the textdomain is nothing more than the filename (including path) from the root of the Masonite installation. The textdomain is not loaded by Masonite until a function call from a given file requests a translation for a phrase. The textdomain consists of all translation phrases for the current language in one Python file.

The developer using translation function calls does not have to think about textdomains, as it is something that Masonite figures out behind the scenes. However, if a developer does want to override the textdomain from the curent file for a given translation, they can do so by specifying the filename (including path) in the function calls.

`language`

The language of the translations. Used for informational purposes.

`translations`

Would store the translations for the textdomain inside a dictionary. Each dictionary key would be a hash (ex *sha256*) of the original text.

- `original` : Stores the original text for translation.
- `comment` : A comment to help translation process.
- `note` : An additional note for complementing the comment.
- `text` : The translation for the original text. If the translation is the same as the original. Use an equal sign (=) as the translation text in order to mark the original as translated.

Basically any file could be translated. Since the translation files would be generated with a craft command that would detect translation function calls and create the respective translation files.

For example `app/http/controllers/WelcomeController.py` would be stored like

```
resources/
    lang/
        default/
            __init__.py
            locale.hjson
        ch/
            __init__.py
            locale.hjson
            resources--templates--welcome-html.py
            app--http--controllers--welcomecontroller-py.hjson
        es/
            __init__.py
            locale.hjson
            resources--templates--welcome-html.py
            app--http--controllers--welcomecontroller-py.hjson

```