# Masonite i18n
This project aims to bring internationalisation (*i18n*) tools and helpers to [Masonite Framework](https://masoniteproject.com).

## Code
The development code will be stored in the `master` branch and production ready code will be stored in the `production` branch.

### Code of Conduct
In all places where communication is needed (issues, pull requests, chat). Just stick to be a friendly, mature and nice person. Avoid unwanted conflict, toxic behaviour or feeding the troll.

### License
[MIT](LICENSE)

### Changelog
[Changelog](CHANGELOG.md)

### Blessing

[![This software is Blessed](https://img.shields.io/badge/blessed-100%25-770493.svg)](BLESSING.md)

## Internationalisation
Taken from [http://www.tonymarston.net](http://web.archive.org/web/20171005184233/http://www.tonymarston.net/php-mysql/internationalisation.html).

The term "internationalisation" is sometimes referred 
to as "globalisation" or "localisation", but what does it actually mean? 
The following description is taken from 
[java.sun.com](http://web.archive.org/web/20121004070052/http://docs.oracle.com/javase/1.4.2/docs/guide/intl/):

> Internationalisation is the process of designing an application so that it can be adapted to various languages and regions without engineering changes. Sometimes the term internationalisation is abbreviated as i18n, because there are 18 letters between the first "i" and the last "n."
> An internationalised program has the following characteristics:
>
> - With the addition of localization data, the same executable can run worldwide.
>
> - Textual elements, such as status messages and the GUI component labels, are not hard coded in the program. Instead they are stored outside the source code and retrieved dynamically.
>
> - Support for new languages does not require recompilation.
>
> - Culturally-dependent data, such as dates and currencies, appear in formats that conform to the end user's region and language.
>
> - It can be localized quickly.

Internationalisation in a software application covers the ability to communicate with a user in his/her own language. It can be said to exist at the following levels:

- Level 0: No internationalisation - the software cannot function in any language other than the one in which it was developed.

- Level 1: Uni-lingual - the software can work in a single language, but each installation can use a different language. The contents of the application database is uni-lingual and does not have any facilities to provide translations in other languages.

- Level 2: Multi-lingual - the software can work in several languages at the same time, and the application database contains translations of relevant text in all the supported languages. The relevant translation is retrieved as required.


## Core Desing
The main design is inspired on the implementations used in different projects, mainly: [Processwire](https://processwire.com), [Laravel](https://laravel.com) and [Rails](https://rubyonrails.org/). The goal is having a system that could be easily used and implement only the parts that are needed for a strong i18n support in *static* files. Unlike other frameworks or tools that try to do too much, this implementation will rely on the tools already provided by Python focusing only in the translation helpers. You could see the original discussion topic [here](https://github.com/MasoniteFramework/core/issues/235).

### Convention over configuration
In order to keep i18n smooth and simple it will be designed with sensible defaults and defined structures and conventions. But with the option to change them when needed.

### Explicit over implicit
Is best to know what are you doing. Too many times a framework do '*magic*' tricks behind scenes. The design will be focused on functions that do one thing well and be explicit about it.

### Pythonic as possible
The project would strive to design an API simple to use. Inspired by libs such as [Requests](http://docs.python-requests.org/en/master/). The API should be similar to gettext function calls in order to facilitate adoption.

### Focus on Static File Translation Only
Other more advanced tools like [Babel](http://babel.pocoo.org/en/latest/) implement localization functions like currency and date format. This project aims to bring just the needed tools for text translation (message, catalogs and pluralization) in static files.

In other words this project aims to bring *Level 1* internationalization support for Masonite applications.
*Level 2* should be reached by the developer of each application because it depends on the
context of each project's database.


### Translation Files
For storing the string translations it will be used [HJSON](https://hjson.org/) files. These have an advantage over [*po* and *mo*](https://es.wikipedia.org/wiki/Gettext) files since they could be easily edited without special tooling. They have an advantage over raw *json* files because they are more human friendly (tolerate trailing commas, have comments and multiline strings). Finally they are better than just python code because they could be easily swaped on runtime without much hazzle.

#### Storage
The translation files will be stored inside the `resources/lang/{name}` directory. Where `{name}` must be replaced with a desired language name (recommended an [ISO 639-1 or 639-2](http://www.loc.gov/standards/iso639-2/php/code_list.php) based name). The name is important since it will be matched against the lang param provided by the request middleware.

##### `default`
The special `resources/lang/default` directory will be used as the main translation and fallback language.

Using this structure any language could be the default translation, just put the correct files inside the default folder, no need for configuration. Optionally it can be configured to another default directory if desired too.

#### Config
The configuration file will be called `language.py` and it will be inside the `config` directory.

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

name = 'default'
title = 'Default'

intervals = {
    'few': {
        'from': 1,
        'to': 25
    },
    'many': {
        'from': 25,
        'to': '*'
    }
}

enabled = True
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
        ch/
            __init__.py
            resources--templates--welcome-html.py
            app--http--controllers--welcomecontroller-py.hjson
        es/
            __init__.py
            resources--templates--welcome-html.py
            app--http--controllers--welcomecontroller-py.hjson

```
