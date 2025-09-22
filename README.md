# py3p - Python 3 Plus Libraries
## Language
- [简体中文](README.zh-CN.md)
## Contents
- [Introduction](#introduction)
- [Features](#features)
    - [py3p.exports](#py3pexports)
        - [py3p.Empty](#py3pempty)
- [License](#license)
## Introduction
The repository is an enhanced toolkit extending the python 3 standard library.
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
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
