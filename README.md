# py3p - Python 3 Plus Libraries
## Language
- [简体中文](README.zh-CN.md)
## Contents
- [Introduction](#introduction)
- [Features](#features)
    - [py3p.exports](#py3pexports)
    - [py3p.Empty](#py3pempty)
    - [py3p.safe](#py3psafe)
    - [py3p.flatten](#py3pflatten)
    - [py3p.getname](#py3pgetname)
    - [py3p.hashable](#py3phashable)
    - [py3p.pstr](#py3ppstr)
    - [py3p.excepthook](#py3pexcepthook)
    - [py3p.decorator](#py3pdecorator)
    - [py3p.auto_decorator](#py3pauto_decorator)
    - [py3p.decorators](#py3pdecorators)
    - [py3p.final](#py3pfinal)
    - [py3p.protected](#py3pprotected)
    - [py3p.private](#py3pprivate)
    - [py3p.monitor](#py3pmonitor)
    - [py3p.NameSpace](#py3pnamespace)
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
### **py3p.flatten**
#### Flatten lists or tuples
- Accepts any number of arguments and automatically combines them into a new tuple as the starting point for flattening
- Only lists and tuples are recursively flattened, other iterable objects remain unchanged
- In the presence of self-references or cross-references, only the outermost occurrence is expanded, preventing infinite recursion
- Uses a generator to yield the final elements, supporting lazy iteration
### **py3p.getname**
#### Get the name of a callable object
- Supports common classes, functions, and methods, including functions decorated with `functools.wraps`
- Supports `functools.partial` and `functools.partialmethod` objects
- Returns None for unsupported objects
### **py3p.hashable**
#### Determine whether an object is hashable
Usually, immutable objects are hashable.
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
### **py3p.excepthook**
#### Proxy for `sys.excepthook`
- If the global variable `excepthook` or `py3p.excepthook` is valid, the modified `excepthook` will be used
- If both `excepthook` and `py3p.excepthook` are invalid, the official default `excepthook` will be used
#### Behavior
> When an exception is raised, if the modified `excepthook` is used, the error message behaves as follows
- If the exception has 0 arguments, only the exception type is displayed
- If the exception has 1 argument, the error message displays the exception type and the argument string
- If the exception has multiple arguments and includes any of `complex`, `float`, or `int`, the error message is condensed into a single line tuple
- If the exception has multiple arguments and none of them are `complex`, `float`, or `int`, the error message is expanded into multi-line strings
- When expanded into multiple lines, everything except the exception type is left-aligned
> When an exception is raised, if the modified `excepthook` is used, the stack trace behaves as follows
- After the error message, the stack trace is output in the format: `at <{file}:{line}> {func}`
- `file` is left-aligned, but if it starts and ends with `<>`, it is center-aligned instead
- `line` is right-aligned
- `func` is left-aligned
- When an infinite recursion causes a stack overflow, the output merges the repeating stack frames and prints them only once, followed by `...` to indicate omission.
### **py3p.decorator**
#### A decorator for decorators
- A decorated decorator cannot be applied repeatedly to the same object.
- When a decorated decorator is applied to a valid object, it attaches a decorator chain `_decorators_` to that object.
- The decorator chain only records decorators decorated with `py3p.decorator`, and it may be interrupted by non-compliant decorators.
#### Behavior Example
`@DecoratorA` is a decorator object wrapped by `@py3p.decorator`
- When `@DecoratorA` decorates `object_a` for the first time, `DecoratorA` is added to `object_a._decorators_`
- When `@DecoratorA` decorates `object_a` again, `object_a` will not be decorated twice
``` python
@py3p.decorator
def DecoratorA(arg):
    print("@DecoratorA")
    return arg

@DecoratorA
def object_a(): pass            # output: @DecoratorA

print(object_a._decorators_)    # output: (DecoratorA)

object_a = DecoratorA(object_a)

print(object_a._decorators_)    # output: (DecoratorA)
```
### **py3p.auto_decorator**
#### A decorator applied to class-decorator functions
- When a decorator function wrapped with `py3p.auto_decorator` is applied to a class, all of the class’s callable methods will be automatically decorated with that decorator
- If `py3p.auto_decorator` is applied directly to a class, its behavior is the same as `py3p.decorator`
- Since static methods behave like regular functions, they are not considered class methods and will not be automatically decorated
#### Behavior Example
`@DecoratorA` is a decorator function wrapped by `@py3p.auto_decorator`
- When `@DecoratorA` decorates `ClassA`, its regular method `method_a` is automatically decorated
- When `@DecoratorA` decorates `ClassA`, its class method `method_b` is automatically decorated
- When `@DecoratorA` decorates `ClassA`, its static method `method_c` is not automatically decorated
``` python
@py3p.auto_decorator
def DecoratorA(arg):
    return arg

@DecoratorA
class ClassA:
    def method_a(self): pass
    @classmethod
    def method_b(cls): pass
    @staticmethod
    def method_c(): pass

print(ClassA.method_a._decorators_) # output: (DecoratorA)
print(ClassA.method_b._decorators_) # output: (DecoratorA)
print(ClassA.method_c._decorators_) # AttributeError: 'function' object has no attribute '_decorators_'
```
### **py3p.decorators**
#### Apply multiple decorators (that were created with `py3p.decorator`) to the same object
- `@py3p.decorators` requires at least one argument
- When multiple arguments are given, they are applied from left to right in order
- `py3p.decorators` cannot be subclassed
#### Example behavior
``` python
@py3p.decorators(decorator1, decorator2)
def function(): pass
```
is roughly equivalent to
``` python
def function(): pass
function = decorator1(function)
function = decorator2(function)
```
### **py3p.final**
#### Access control decorator: forbid class inheritance
When attempting to inherit from a class decorated with `@final`, it raises `TypeError: type "{name}" is not an acceptable base type`
### **py3p.protected**
#### Access control decorator: Replacement Method Inheritance Chain
The decorator takes a method-specific inheritance chain as its argument, which overrides the class-level inheritance chain
### **py3p.private**
#### Access control decorator: Prevent Method Inheritance
Methods decorated with this will not be allowed to be called by objects of any class other than the current one. This does not apply to class methods or static methods
### **py3p.monitor**
#### Decorator: Runtime Type Monitor
> During function calls, it checks whether the input arguments and the return value match the type annotations
- When applied to a class, it automatically applies to all methods of the class
- Type annotations can be nested
- If unsupported types appear in type annotations, it raises the official error message
- If data types conflict with type annotations, it raises a detailed error message
#### Recommended Type Annotations
| Annotation | Meaning |
| :---: | :---: |
| `None` | Only allows the argument to be `None` |
| `str` | Dynamically parsed type |
| `type` | Single type check |
| `tuple` `Union` | Any one of them is acceptable |
| `list` | All elements must satisfy the condition |
| `set` | Hashable valid values enumeration |
| `range` | Integer value range |
| `function` | Custom validator function |
| `dict` | Fine-grained annotation applied only to `**` parameters |
### **py3p.NameSpace**
#### Enhanced `dict`
- Inherits from `dict` and retains all basic `dict` functionalities
- Allows data access via attribute-style notation, following a data-first access rule
- When accessing nested data, if any parent namespace in the path does not exist, it is automatically created
- Assigning `None` to a key automatically deletes the corresponding data, keeping the namespace clean
- Provides a `prune()` method to recursively remove empty `NameSpace` objects
- Compatible with type checks using `@py3p.monitor`
#### Access Rules
| Data Exists | Attribute Exists | Get Behavior | Set Behavior |
| :---: | :---: | :--- | :--- |
| ✅ | ✅ | Returns the data | Updates the data |
| ✅ | ❌ | Returns the data | Updates the data |
| ❌ | ✅ | Returns the attribute | Creates the data |
| ❌ | ❌ | Returns a newly created empty `NameSpace` | Creates the data |
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
