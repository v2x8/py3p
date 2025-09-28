# -*- coding: utf-8 -*-
from builtins import classmethod, set, staticmethod
import sys

class exports:
    _blacklist = set()
    _whitelist = set()
    @classmethod
    def prepare(cls):
        from builtins import id, map, set
        import inspect
        f_globals = inspect.currentframe().f_back.f_globals
        cls._blacklist = set( map( id, f_globals.values() ) )
        cls._whitelist = set()
    @classmethod
    def include(cls, *args):
        from builtins import map, str
        cls._whitelist.update( map(str, args) )
    @classmethod
    def exclude(cls, *args):
        from builtins import id, map
        cls._blacklist.update( map(id, args) )
    @classmethod
    def export(cls):
        from builtins import id
        import inspect
        f_globals = inspect.currentframe().f_back.f_globals
        f_globals['__all__'] = [
            k for k, v in f_globals.items()
            if k in cls._whitelist or id(v) not in cls._blacklist
        ]
        return f_globals['__all__']

class EmptyType:
    __doc__ = 'The type of the Empty singleton.'
    __slots__ = ()
    _instance = None
    def __new__(cls):
        from builtins import object
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    def __bool__(self):
        return False
    def __repr__(self):
        return 'Empty'
    def __reduce__(self):
        return (EmptyType, ())

exports.prepare()
exports.include('exports')

Empty = EmptyType()

class safe:
    @staticmethod
    def __import__(name):
        from builtins import __import__
        from sys import modules
        module = modules.get(name)
        if module is not None:
            del modules[name]
        result = __import__(name)
        if module is not None:
            modules[name] = module
        return result
    @staticmethod
    def isinstance(obj, class_or_tuple):
        from builtins import AttributeError, TypeError, any, object, tuple, type
        from types import UnionType
        import typing
        if class_or_tuple is typing.Any:
            return True
        if class_or_tuple is type or safe.isinstance(class_or_tuple, type):
            mro = type.__getattribute__( type(obj), '__mro__' )
            return class_or_tuple in mro
        if safe.isinstance(class_or_tuple, tuple):
            return any( safe.isinstance(obj, cls) for cls in class_or_tuple )
        if safe.isinstance(class_or_tuple, UnionType):
            args = object.__getattribute__(class_or_tuple, '__args__')
            return safe.isinstance(obj, args)
        try:
            check = object.__getattribute__(class_or_tuple, '__instancecheck__')
            return check(obj)
        except AttributeError: pass
        msg = 'isinstance() arg 2 must be a type, a tuple of types, or a union'
        raise TypeError(msg)
    @staticmethod
    def delattr(obj, name):
        from builtins import object, type
        cls = type if safe.isinstance(obj, type) else object
        return cls.__delattr__(obj, name)
    @staticmethod
    def getattr(obj, name, default=Empty):
        from builtins import AttributeError, object, type
        try:
            cls = type if safe.isinstance(obj, type) else object
            return cls.__getattribute__(obj, name)
        except AttributeError:
            if default is not Empty:
                return default
            raise
    @staticmethod
    def hasattr(obj, name):
        from builtins import AttributeError
        try:
            safe.getattr(obj, name)
            return True
        except AttributeError:
            return False
    @staticmethod
    def setattr(obj, name, value):
        from builtins import object, type
        cls = type if safe.isinstance(obj, type) else object
        return cls.__setattr__(obj, name, value)

def getname(obj):
    from functools import partial, partialmethod
    from types import MethodType
    if ( result := safe.getattr(obj, '__qualname__', None) ) is not None:
        return result
    if ( result := safe.getattr(obj, '__name__', None) ) is not None:
        return result
    if safe.isinstance(obj, partial | partialmethod):
        if ( wrapped := safe.getattr(obj, '__wrapped__', None) ) is not None:
            return getname(wrapped)
        if ( keywords := safe.getattr(obj, 'keywords', None) ) is not None:
            if ( wrapped := keywords.get('wrapped') ) is not None:
                return getname(wrapped)
        if ( func := safe.getattr(obj, 'func', None) ) is not None:
            return getname(func)
    if safe.isinstance(obj, MethodType):
        if ( func := safe.getattr(obj, '__func__', None) ) is not None:
            return getname(func)
    return None

def hashable(obj):
    try:
        hash(obj)
        return True
    except TypeError:
        return False

def pstr(obj, indent=1):
    from builtins import (  ValueError, bytes, dict, float, id, int,
                            len, list, map, set, str, sorted, tuple )
    if safe.isinstance(indent, list | tuple):
        indent = ''.join(indent)
    if not indent:
        indent = ''
    elif safe.isinstance(indent, bytes | float | int | str):
        try:
            indent = float(indent)
        except ValueError:
            pass
        try:
            indent = int(indent)
        except ValueError:
            pass
        else:
            indent = indent * ' '
    elif indent is True:
        indent = '\t'
    else:
        indent = str(indent)
    suffix = ' ' if indent == '' else '\n'
    memo = set()
    def check(obj, cls):
        if len(obj) == 0:
            if ( result := (
                '{}' if cls is dict else
                '[]' if cls is list else
                '()' if cls is tuple else
                'set()' if cls is set else
            None ) ) is not None: return result
        if id(obj) in memo:
            if ( result := (
                '{...}' if cls is dict else
                '[...]' if cls is list else
                '(...)' if cls is tuple else
                'set(...)' if cls is set else
            None ) ) is not None: return result
        memo.add( id(obj) )
    def _pstr(obj):
        if safe.isinstance(obj, dict):
            if ( result := check(obj, dict) ) is not None:
                return result
            def tostr(item):
                k, v = item
                lines = _pstr(v).splitlines()
                value = f'{suffix}{indent}'.join(lines)
                return f'{indent}{k}: {value}'
            data = f',{suffix}'.join( sorted( map( tostr, obj.items() ) ) )
            return f'{{{suffix}{data}{suffix}}}'
        def tostr(item):
            lines = _pstr(item).splitlines()
            value = f'{suffix}{indent}'.join(lines)
            return f'{indent}{value}'
        if safe.isinstance(obj, list):
            if ( result := check(obj, list) ) is not None:
                return result
            data = f',{suffix}'.join( map(tostr, obj) )
            return f'[{suffix}{data}{suffix}]'
        if safe.isinstance(obj, set):
            if ( result := check(obj, set) ) is not None:
                return result
            data = f',{suffix}'.join( sorted( map(tostr, obj) ) )
            return f'{{{suffix}{data}{suffix}}}'
        if safe.isinstance(obj, tuple):
            if ( result := check(obj, tuple) ) is not None:
                return result
            data = f',{suffix}'.join( map(tostr, obj) )
            return f'({suffix}{data}{suffix})'
        return str(obj)
    return _pstr(obj)

def excepthook(exctype, value, traceback):
    from builtins import (  complex, float, int, len, map, max,
                            print, range, reversed, str, type )
    from sys import stderr
    text = name = safe.getattr(exctype, '__qualname__')
    args = safe.getattr(value, 'args')
    if args:
        for arg in args:
            if safe.isinstance(arg, complex | float | int):
                lines = str( args if len(args) > 1 else arg )
                msg = lines.replace('\n', '\\n')
                text = f'{name}: {msg}'
                break
        else:
            split = '\n' + ( len(name) + 2 ) * ' '
            lines = '\n'.join( map(str, args) )
            msg = split.join( lines.splitlines() )
            text = f'{name}: {msg}'
    print(text, file=stderr)
    tracebacks = []
    while traceback:
        file = traceback.tb_frame.f_code.co_filename
        func = traceback.tb_frame.f_code.co_qualname
        line = str(traceback.tb_frame.f_lineno)
        tracebacks.append( { 'file': file, 'func': func, 'line': line } )
        traceback = traceback.tb_next
    width_file = max( ( len( tb['file'] ) for tb in tracebacks ), default=0 )
    width_line = max( ( len( tb['line'] ) for tb in tracebacks ), default=0 )
    def perror(tracebacks):
        for traceback in tracebacks:
            file = traceback['file']
            if file.startswith('<') and file.endswith('>'):
                file = file.center(width_file)
            else:
                file = file.ljust(width_file)
            line = traceback['line'].rjust(width_line)
            func = traceback['func'].replace('.<locals>', '.-')
            print(f'    at <{file}:{line}> {func}', file=stderr)
    count = len(tracebacks)
    for size in range( 1, count // 2 + 1 ):
        for i in range( count - size * 2 + 1 ):
            offset = i + size
            block = tracebacks[i:offset]
            for j in range(offset, count, size):
                offset = j + size
                if offset <= count:
                    if tracebacks[j:offset] == block:
                        continue
                    block = None
                break
            if block is not None:
                perror( reversed(block) )
                print('    ...', file=stderr)
                tracebacks = tracebacks[:i]
                break
        else:
            continue
        break
    perror( reversed( tracebacks ) )
    for k, v in { 'cause': 'cause', 'context': 'occur' }.items():
        if ( exc := safe.getattr(value, f'__{k}__', None) ) is not None:
            print(f'- {v} -', file=stderr)
            traceback = safe.getattr(exc, '__traceback__')
            excepthook( type(exc), exc, traceback )
            return

_excepthook_new = excepthook
_excepthook_old = sys.excepthook

def excepthook(exctype, value, traceback):
    frame_globals = traceback.tb_frame.f_globals
    if frame_globals.get('excepthook') is excepthook:
        _excepthook_new(exctype, value, traceback)
    elif getattr( frame_globals.get('py3p'), 'excepthook', None ) is excepthook:
        _excepthook_new(exctype, value, traceback)
    else:
        _excepthook_old(exctype, value, traceback)

sys.excepthook = excepthook

def decorator(obj):
    from builtins import callable, map, set, type
    from functools import wraps
    if ( Decorators := safe.getattr(decorator, 'Decorators', None) ) is None:
        class Decorators:
            def __init__(self):
                self.data = set()
            def __contains__(self, value):
                while value is not None:
                    if value in self.data:
                        return True
                    value = safe.getattr(value, '__wrapped__', None)
                return False
            def __repr__(self):
                return '(' + ', '.join( map(getname, self.data) ) + ')'
        decorator.Decorators = Decorators
        decorator._decorators_ = Decorators()
        decorator._decorators_.data.add(decorator)
    def decoratable(obj, decorator):
        if callable(obj):
            decorators = safe.getattr(obj, '_decorators_', None)
            if decorators is None:
                return safe.hasattr(obj, '__dict__')
            else:
                return not decorator in decorators
        return False
    def decorate(obj, decorator):
        decorators = safe.getattr(obj, '_decorators_', None)
        if decorators is None:
            decorators = Decorators()
            safe.setattr(obj, '_decorators_', decorators)
        decorators.data.add(decorator)
    if decoratable(obj, decorator):
        if not safe.isinstance(obj, type):
            decorate(obj, decorator)
            @wraps(obj)
            def wrapper(arg, *args, **kwargs):
                if decoratable(arg, obj):
                    decorate(arg, obj)
                    return obj(arg, *args, **kwargs)
                return arg
            return wrapper
        if ( __call__ := safe.getattr(obj, '__call__', None) ) is not None:
            decorate(obj, decorator)
            @wraps(__call__)
            def wrapper(self, arg, *args, **kwargs):
                if decoratable(arg, obj):
                    decorate(arg, obj)
                    return __call__(self, arg, *args, **kwargs)
                return arg
            safe.setattr(obj, '__call__', wrapper)
        if ( __get__ := safe.getattr(obj, '__get__', None) ) is not None:
            decorate(obj, decorator)
            @wraps(__get__)
            def wrapper(self, arg, *args, **kwargs):
                if decoratable(arg, obj):
                    decorate(arg, obj)
                    return __get__(self, arg, *args, **kwargs)
                return arg
            safe.setattr(obj, '__get__', wrapper)
    return obj

@decorator
def auto_decorator(func):
    from builtins import callable, classmethod, type
    from functools import wraps
    func = decorator(func)
    if safe.isinstance(func, type):
        return func
    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        if safe.isinstance(obj, type):
            __dict__ = safe.getattr(obj, '__dict__', None)
            if __dict__ is not None:
                for k, v in __dict__.items():
                    if callable(v):
                        safe.setattr( obj, k, func(v, *args, **kwargs) )
                    if safe.isinstance(v, classmethod):
                        attr = safe.getattr(v, '__func__')
                        attr = func(attr, *args, **kwargs)
                        safe.setattr( obj, k, classmethod(attr) )
        return func(obj, *args, **kwargs)
    return wrapper

@decorator
class decorators:
    def __init__(self, *args):
        from builtins import TypeError, set
        for arg in args:
            if not decorator in safe.getattr( arg, '_decorators_', set() ):
                name = getname(arg)
                raise TypeError(f'{name} is not a traceable decorator')
        self.decorators = args
    def __call__(self, obj):
        for decorator in self.decorators:
            obj = decorator(obj)
        return obj
    def __repr__(self):
        from builtins import map
        args = ', '.join( map(getname, self.decorators) )
        return f'decorators({args})'
    def __init_subclass__(cls, *args, **kwargs):
        from builtins import TypeError
        raise TypeError(f'type "decorators" is not an acceptable base type')

@decorator
def final(cls):
    from builtins import TypeError, type
    if safe.isinstance(cls, type):
        name = safe.getattr(cls, '__qualname__')
        def __init_subclass__(cls, *args, **kwargs):
            raise TypeError(f'type "{name}" is not an acceptable base type')
        __init_subclass__.__qualname__ = f'{name}.__init_subclass__'
        safe.setattr(cls, '__init_subclass__', __init_subclass__)
    return cls

@decorators(decorator, final)
class protected:
    def __init__(self, *args):
        from builtins import TypeError, type
        for arg in args:
            if not ( arg is None or safe.isinstance(arg, type) ):
                name = getname(arg)
                raise TypeError(f'{name} is not a type')
        self.args = args
    def __call__(self, func):
        from builtins import AttributeError, type
        from functools import wraps
        if safe.isinstance(func, type):
            return func
        classes = self.args
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func = wrapper.__wrapped__
            for value in safe.getattr( type(self), '__dict__', {} ).values():
                while not (value is None or value is func):
                    value = safe.getattr(value, '__wrapped__', None)
                if value is func:
                    return func(self, *args, **kwargs)
            attr = safe.getattr(func, '__name__')
            for cls in classes:
                if cls is None:
                    return None
                if ( func := safe.getattr(cls, attr, None) ) is not None:
                    return func(self, *args, **kwargs)
            name = safe.getattr( type(self), '__qualname__' )
            msg = f'"{name}" object has no attribute "{attr}"'
            raise AttributeError(msg)
        return wrapper
    def __repr__(self):
        from builtins import map
        args = ', '.join( map(getname, self.args) )
        return f'protected({args})'

@decorator
def private(func):
    from builtins import AttributeError, type
    from functools import wraps
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        for k, v in safe.getattr( type(self), '__dict__', {} ).items():
            while not (v is None or v is func):
                v = safe.getattr(v, '__wrapped__', None)
            if v is func:
                return func(self, *args, **kwargs)
        name = safe.getattr( type(self), '__qualname__' )
        attr = safe.getattr(func, '__name__')
        raise AttributeError(f'"{name}" object has no attribute "{attr}"')
    return wrapper

@auto_decorator
def monitor(func):
    from builtins import (  TypeError, all, callable, dict,
                            eval, len, list, map, min, next,
                            range, repr, set, str, tuple, type )
    from inspect import Parameter, signature, stack
    from types import MethodType, FunctionType
    from typing import Iterable
    from functools import wraps
    def check(obj, classes, f_locals={}):
        if classes is None:
            return obj is None
        mro_cls = safe.getattr( type(classes), '__mro__' )
        if str in mro_cls:
            classes = eval(classes, locals=f_locals)
            return check(obj, classes, f_locals)
        mro_obj = safe.getattr( type(obj), '__mro__' )
        if list in mro_cls:
            return all( check(obj, item, f_locals) for item in classes )
        if range in mro_cls:
            return int in mro_obj and obj in classes
        if set in mro_cls:
            return hashable(obj) and obj in classes
        if FunctionType in mro_cls:
            return classes(obj)
        return safe.isinstance(obj, classes)
    def parse(classes, f_locals={}):
        if classes is None:
            return 'None'
        if safe.isinstance(classes, list):
            return '[' + ', '.join( map(parse, classes) ) + ']'
        if safe.isinstance(classes, tuple):
            return '(' + ', '.join( map(parse, classes) ) + ')'
        if safe.isinstance(classes, str):
            classes = eval(classes, locals=f_locals)
            return repr(classes)
        if safe.isinstance(classes, type):
            return safe.getattr(classes, '__qualname__')
        if callable(classes):
            name = getname(classes)
            return f'{name}()'
        return repr(classes)
    def getcls(obj):
        if safe.isinstance(obj, str):
            result = repr(f'"{obj}')[2:-1]
            return f"str:'{result}'"
        if safe.isinstance(obj, type):
            result = safe.getattr(obj, '__name__')
            return f'type:{result}'
        result = parse( type(obj) )
        return result if safe.isinstance(obj, Iterable) else f'{result}:{obj}'
    if safe.isinstance(func, type):
        return func
    obj = func
    while True:
        if safe.isinstance(obj, MethodType):
            obj = safe.getattr(obj, '__func__')
        elif ( wrapped := safe.getattr(obj, '__wrapped__', None) ) is not None:
            obj = wrapped
        else:
            break
    if ( code := safe.getattr(obj, '__code__', None) ) is None:
        return func
    if ( annos := safe.getattr(obj, '__annotations__', None) ) is None:
        return func
    if ( parc_ := safe.getattr(code, 'co_argcount', None) ) is None:
        return func
    if ( vars_ := safe.getattr(code, 'co_varnames', None) ) is None:
        return func
    defs_ = safe.getattr(obj, '__defaults__')
    defc_ = 0 if defs_ is None else len(defs_)
    pars = signature(obj).parameters.values()
    args_gen = ( v.name for v in pars if v.kind == Parameter.VAR_POSITIONAL )
    kwargs_gen = ( v.name for v in pars if v.kind == Parameter.VAR_KEYWORD )
    func_name = getname(obj)
    args_name = next(args_gen, None)
    kwargs_name = next(kwargs_gen, None)
    @wraps(func)
    def wrapper(*args, **kwargs):
        f_locals = stack()[1].frame.f_locals
        argc = len(args)
        if args_name is None:
            if argc > parc_:
                msg = ( f'{func_name}() takes {parc_} positional' +
                        f' arguments but {argc} were given'       )
                raise TypeError(msg)
            if argc < ( minc := parc_ - defc_ ):
                miss = [ repr( vars_[i] ) for i in range(argc, minc) ]
                args = miss[-1]
                if ( argc := len(miss) ) != 1:
                    args = ', '.join( miss[:-1] + [f'and {args}'] )
                msg = ( f'{func_name}() is missing at least {argc}' +
                        f' required positional arguments: {args}'  )
                raise TypeError(msg)
        for i in range( min(argc, parc_) ):
            name = vars_[i]
            if name in annos and not check(args[i], annos[name], f_locals):
                cls = getcls( args[i] )
                classes = parse(annos[name], f_locals)
                msg = ( f'argument "{name}" ({cls}) is '  +
                        f'not an instance like {classes}' )
                raise TypeError(msg)
        if args_name is not None and args_name in annos:
            anno = annos[args_name]
            for i in range(parc_, argc):
                if not check(args[i], anno, f_locals):
                    cls = getcls( args[i] )
                    classes = parse(anno, f_locals)
                    index = i - parc_
                    msg = ( f'item {index} of argument "{args_name}" '   +
                            f'({cls}) is not an instance like {classes}' )
                    raise TypeError(msg)
        if kwargs:
            for k, v in kwargs.items():
                if k in vars_:
                    if k in annos and not check(v, annos[k], f_locals):
                        cls = getcls(v)
                        classes = parse(annos[k], f_locals)
                        msg = ( f'argument "{k}" ({cls}) is not' +
                                f' an instance like {classes}'   )
                        raise TypeError(msg)
                elif kwargs_name is None:
                    msg = f'{func_name}() got unexpected keyword argument(s)'
                    raise TypeError(msg)
                elif kwargs_name in annos:
                    anno = annos[kwargs_name]
                    if safe.isinstance(anno, dict) and k in anno:
                        anno = anno[k]
                    if not check(v, anno, f_locals):
                        cls = getcls(v)
                        classes = parse(anno, f_locals)
                        msg = ( f'value of key "{k}" of argument' +
                                f' "{kwargs_name}" ({cls}) is '   +
                                f'not an instance like {classes}' )
                        raise TypeError(msg)
        result = obj(*args, **kwargs)
        if 'return' in annos:
            anno = annos['return']
            if not check(result, anno, f_locals):
                cls = getcls(result)
                classes = parse(anno, f_locals)
                msg = ( f'the return value ({cls}) is '   +
                        f'not an instance like {classes}' )
                raise TypeError(msg)
        return result
    return wrapper

exports.exclude(_excepthook_new)
exports.exclude(_excepthook_old)
exports.export()
