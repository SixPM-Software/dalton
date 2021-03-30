# Dalton

![PyPI](https://img.shields.io/pypi/v/daltonapi) ![GitHub](https://img.shields.io/github/license/stuckatsixpm/dalton) [![Documentation Status](https://readthedocs.org/projects/dalton/badge/?version=latest)](https://dalton.readthedocs.io/en/latest/?badge=latest) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/06863e11a0f04b20bc45cbb920c9f3de)](https://www.codacy.com/gh/stuckatsixpm/dalton/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=stuckatsixpm/dalton&amp;utm_campaign=Badge_Grade) [![CI Workflow](https://github.com/stuckatsixpm/dalton/actions/workflows/CI%20Workflow.yml/badge.svg)](https://github.com/stuckatsixpm/dalton/actions/workflows/CI%20Workflow.yml) 

**Note that this is an alpha release of the project, and large changes may occur, however it is intended to keep the access paths to functions and classes the same.**

This Python package provides a wrapper providing read-only access to the Atomic Assets API on the WAX blockchain. Full docs being assembled at [Read the Docs](https://dalton.readthedocs.io/en/latest/).

- [Dalton](#dalton)
  - [Features](#features)
    - [In development](#in-development)
  - [Installation](#installation)
  - [Examples](#examples)
    - [Creating an Atom object](#creating-an-atom-object)
    - [Retrieving an asset](#retrieving-an-asset)
    - [Retrieving assets based on criteria](#retrieving-assets-based-on-criteria)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [Attribution](#attribution)
  - [Contact me](#contact-me)

## Features

*   `Atom` class for accessing Atomic Asset Data
*   Pythonic classes for Atomic Assets, Templates, Schemas, Collections, Transfer events, with 
*   A growing collection of class methods for working with API data.

### In development

Have a look at our roadmap [here](https://github.com/stuckatsixpm/dalton/projects/1).

## Installation

The recommended method of installation is through PyPI and pip
```
python -m pip install daltonapi
```
*Fun fact: This package is named after John Dalton, a pioneer of Atomic Theory.*

## Examples

### Creating an Atom object

The main class of the Dalton package is the Atom class, which is used as an interface to the API
``` 
>>> from daltonapi.api import Atom

>>> atom = Atom()
```

### Retrieving an asset
Once you have created an Atom, it's simple to get information about an asset.

``` 
>>> my_asset = atom.get_asset("1099519242825")
>>> print(my_asset)
Asset 1099519242825: creekdrops21 -   Bitcoin #1/21 (Max Supply: 21)
>>>
>>> # get link to asset's primary image
>>> print(my_asset.image)
https://ipfs.io/ipfs/QmUn8kvvHFrJK2mSsiPFNRMmmehnRoNJsqTP4XTVsemgrc
>>>
>>> # get asset collection, which is a Collection object
>>> collection = my_asset.collection
>>> print("Author:",collection.author)
Author: creek.gm
```

### Retrieving assets based on criteria
To get assets based on some criteria, you can use `Atom.get_assets`, which will return a list based on criteria passed. Currently, `get_assets` accepts owner, template, schema, and/or collection as either strings or Class Objects. 
```
>>> # Get assets using owner and template as strings
>>> assets = atom.get_assets(owner="someowner123", template = "12345")
>>>
>>> # Get assets using collection class object
>>> assets = atom.get_assets(collection=my_asset.collection)
```

## Documentation
Full documentation is being assembled at [Read the Docs](https://dalton.readthedocs.io/en/latest/).

## Contributing
See [Contributing](CONTRIBUTING.md).

Alternatively, if you would like to sponsor me, consider donating some WAX to the address `daltonpython`.
![https://i.imgur.com/rWbgGW3.png](https://i.imgur.com/rWbgGW3.png)

## Attribution
*   [WAX team](https://github.com/worldwide-asset-exchange) for development of the WAX blockchain.
*   [Pink.network](https://github.com/pinknetworkx) for development of atomic assets.
*   [PurpleBooth](https://gist.github.com/PurpleBooth) for Contributing Template.

## Contact me
*   Twitter: [@stuckat6pm](https://twitter.com/stuckat6pm)
