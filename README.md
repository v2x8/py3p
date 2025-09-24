# py3p - Python 3 Plus Libraries
## Language
- [简体中文](README.zh-CN.md)
## Contents
- [Introduction](#introduction)
- [Features](#features)
    - [py3p.exports](#py3pexports)
    - [py3p.Empty](#py3pempty)
    - [py3p.safe](#py3psafe)
    - [py3p.pstr](#py3ppstr)
    - [py3p.getname](#py3pgetname)
- [License](#license)
## Introduction
The repository is an enhanced toolkit extending the python 3.10+ standard library.
## Features
### **py3p.exports**
#### Dynamic `__all__` Generation
- Automatically generates variables list for `from module import *`
- Supports adding variable names to the whitelist or objects to the blacklist
#### Export Rules
| Whitelist | Blacklist | Exported? |
|:---:|:---:|:---:|
| ✅ | ✅ | ✅ |
| ✅ | ❌ | ✅ |
| ❌ | ✅ | ❌ |
| ❌ | ❌ | ✅ |
#### Function Descriptions
- `exports.prepare(cls) @classmethod`
    > Add current global variables to the blacklist and reset the whitelist
- `exports.include(cls, *args) @classmethod`
    > Add variable names to the whitelist
- `exports.exclude(cls, *args) @classmethod`
    > Add objects to the blacklist
- `exports.export(cls) @classmethod`
    > Export variables that are either in the whitelist or not in the blacklist
### **py3p.Empty**
#### Resolving the ambiguity of `None` as a default parameter
- Serves to differentiate **an argument that was not provided** from **an argument explicitly set to `None`**
- Particularly useful for functions that require a default value but also accept `None` as a valid input
#### Behavior
- `Empty` is a singleton of the `EmptyType` class, supporting serialization and deserialization
- Boolean evaluation of `Empty` is `False`
- String representation of `Empty` is `'Empty'`
### **py3p.safe**
#### A safer set of `builtins` functions
- `safe.__import__`
    > Imports a module. Unlike `builtins.__import__`, this version disables the module cache
- `safe.isinstance`
    > Checks an object’s type. Unlike `builtins.isinstance`, it ignores class-level overrides.
- `safe.delattr`
    > Deletes an attribute. Unlike `builtins.delattr`, it ignores class-level overrides.
- `safe.getattr`
    > Get an attribute. Unlike `builtins.getattr`, it ignores class-level overrides.
- `safe.hasattr`
    > Checks if an attribute exists. Unlike `builtins.hasattr`, it ignores class-level overrides.
- `safe.setattr`
    > Set an attribute. Unlike `builtins.setattr`, it ignores class-level overrides.
### **py3p.pstr**
#### A pretty version of the `builtins.str` function
- Supports a custom `indent` parameter for indentation, automatically detecting and handling all types
- Recommended `indent` types: `bool`, `int`, or `str`.
#### `indent` handling
| Type | Special Value | Behavior |
|:---|:---|:---|
| `list` `tuple` | | Joined into a `str` and handled as string |
| `bytes` `str` | Convertible to `float` or `int` | Converted to the corresponding type |
| `float` | | Converted to `int` (rounded down) |
| `int` | `> 0` | Specifies the number of spaces for indentation |
| `int` | `< 0` | Output is a single-line string |
| `bool` | `True` | Uses `\t` for indentation |
| | Boolean equivalent of `True` | Converted and handled as `str` |
| | Boolean equivalent of `False` | Output is a single-line string |
### **py3p.getname**
#### Get the name of a callable object
- Supports common classes, functions, and methods, including functions decorated with `functools.wraps`
- Supports `functools.partial` and `functools.partialmethod` objects
- Returns None for unsupported objects
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
