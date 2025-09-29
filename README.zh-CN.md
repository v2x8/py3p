# py3p - Python 3 Plus Libraries
## 语言
- [English](README.md)
## 目录
- [简介](#简介)
- [功能](#功能)
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
- [许可](#许可)
## 简介
本仓库是一个基于 python 3.10+ 标准库的增强型扩展工具集。
## 功能
### **py3p.exports**
#### 动态生成 `__all__`
- 自动生成供 `from module import *` 导入的变量列表
- 支持将变量名加入白名单或将对象加入黑名单
#### 导出规则
| 是否在白名单中 | 是否在黑名单中 | 是否导出 |
| :---: | :---: | :---: |
| ✅ | ✅ | ✅ |
| ✅ | ❌ | ✅ |
| ❌ | ✅ | ❌ |
| ❌ | ❌ | ✅ |
#### 函数说明
- `exports.prepare(cls) @classmethod`
    > 将当前全局变量加入黑名单并重置白名单
- `exports.include(cls, *args) @classmethod`
    > 将变量名加入白名单
- `exports.exclude(cls, *args) @classmethod`
    > 将对象加入黑名单
- `exports.export(cls) @classmethod`
    > 将在白名单中或不在黑名单中的变量导出
### **py3p.Empty**
#### 消除 `None` 作为参数默认值的歧义
- 用于区分 **未传入参数** 和 **传入 None**
- 仅在需要默认参数但函数接受包括 `None` 在内的普通参数时使用
#### 逻辑行为
- `Empty` 是 `EmptyType` 的单例，支持序列化和反序列化
- `Empty` 的布尔表现为 `False`
- `Empty` 的字符串表现为 `'Empty'`
### **py3p.safe**
#### 一组更加安全的 `builtins` 函数
- `safe.__import__`
    > 导入模块，相比 `builtins.__import__`，禁用了模块缓存机制
- `safe.isinstance`
    > 判断实例类型，相比 `builtins.isinstance`，禁用了类方法影响
- `safe.delattr`
    > 删除属性，相比 `builtins.delattr`，禁用了类方法影响
- `safe.getattr`
    > 获取属性值，相比 `builtins.getattr`，禁用了类方法影响
- `safe.hasattr`
    > 判断属性是否存在，相比 `builtins.hasattr`，禁用了类方法影响
- `safe.setattr`
    > 设置属性值，相比 `builtins.setattr`，禁用了类方法影响
### **py3p.flatten**
#### 展开列表或元组
- 接受任意数量参数，自动将它们组合成一个新的元组作为展开的起点
- 仅展开列表和元组，其他可迭代对象保持原样，不会被展开
- 如果存在自引用或交叉引用，仅展开最外层对象，防止无限递归
- 使用生成器输出最终元素，支持惰性迭代
### **py3p.getname**
#### 获取可调用对象的名字
- 支持常见的类，函数和方法，包括被 `functools.wraps` 装饰过的函数
- 支持 `functools.partial` 和 `functools.partialmethod` 对象
- 对于不支持的对象，返回值为 None
### **py3p.hashable**
#### 判断一个对象是否可以哈希
通常不可变对象都是可哈希的
### **py3p.pstr**
#### `builtins.str` 函数的美化版本
- 支持使用参数 `indent` 自定义缩进，对所有类型自动识别并处理
- 推荐 `indent` 使用 `bool`、`int` 或 `str` 类型
#### `indent` 识别
| 类型 | 特殊值 | 处理 |
| :--- | :--- | :--- |
| `list` `tuple` | | 连接为 `str` 类型处理 |
| `bytes` `str` | 可被转换为 `float` 或 `int` | 转换为相应类型处理 |
| `float` | | 转换为 `int` 类型处理 (向下取整) |
| `int` | `> 0` | 指定缩进空格数量 |
| `int` | `< 0` | 返回值为单行字符串 |
| `bool` | `True` | 使用 `\t` 缩进 |
| | 布尔表现为 `True` | 转换为 `str` 类型处理 |
| | 布尔表现为 `False` | 返回值为单行字符串 |
### **py3p.excepthook**
#### 代理 `sys.excepthook`
- 如果全局变量 `excepthook` 或 `py3p.excepthook` 有效，使用经过修改的 `excepthook`
- 如果全局变量 `excepthook` 和 `py3p.excepthook` 无效，使用官方提供的 `excepthook`
#### 行为
> 抛出异常时，如果使用经过修改的 `excepthook`，报错信息会存在以下行为
- 如果异常的参数数量为 0，报错信息只展示异常类型
- 如果异常的参数数量为 1，报错信息展示异常类型和参数字符串
- 如果异常有多个参数，且包含 `complex`、`float` 或 `int` 其一，报错信息会集中到一行输出为元组
- 如果异常有多个参数，且不包含 `complex`、`float` 或 `int`，报错信息会展开为多行字符串输出
- 报错信息展开为多行字符串输出时，除了异常类型以外其他部分左对齐
> 抛出异常时，如果使用经过修改的 `excepthook`，报错堆栈会存在以下行为
- 输出报错信息后，以 `at <{file}:{line}> {func}` 形式输出报错堆栈
- `file` 以左对齐形式输出，但如果以 `<>` 开头和结尾，将以居中对齐形式输出
- `line` 以右对齐形式输出
- `func` 以左对齐形式输出
- 输出时会合并因无限递归导致的栈溢出产生的周期性重复栈，只输出一次，之后用 `...` 省略
### **py3p.decorator**
#### 应用于装饰器的装饰器
- 被装饰的装饰器不能重复应用在同一个对象上
- 被装饰的装饰器应用于有效对象上时，会在对象中添加装饰器链 `_decorators_`
- 装饰器链只会记录被 `py3p.decorator` 装饰的装饰器，且可能被不合规的装饰器截断
#### 行为示例
`@DecoratorA` 是一个被 `@py3p.decorator` 装饰过的装饰器对象
- `@DecoratorA` 首次装饰对象 `object_a`，会在 `object_a._decorators_` 中添加 `DecoratorA`
- `@DecoratorA` 再次装饰对象 `object_a`，`object_a` 不会被二次装饰
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
#### 应用于类装饰器函数的装饰器
- 被装饰的装饰器函数应用于类上时，该类的所有可调用方法都会应用被装饰的装饰器函数
- 如果把 `py3p.auto_decorator` 应用于类，它的行为与 `py3p.decorator` 相同
- 由于静态方法的行为与函数类似，所以不被判定为被装饰类的方法
#### 行为示例
`@DecoratorA` 是一个被 `@py3p.auto_decorator` 装饰过的装饰器函数
- `@DecoratorA` 装饰类 `ClassA`，`ClassA` 的常规方法 `method_a` 被自动装饰
- `@DecoratorA` 装饰类 `ClassA`，`ClassA` 的类方法 `method_b` 被自动装饰
- `@DecoratorA` 装饰类 `ClassA`，`ClassA` 的静态方法 `method_c` 没有被自动装饰
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
#### 应用多个被 `py3p.decorator` 装饰过的装饰器到同一个对象
- `@py3p.decorators` 需要至少一个参数
- 有多个参数时，装饰顺序为从左到右依次装饰
- `py3p.decorators` 不能被继承
#### 行为示例
``` python
@py3p.decorators(decorator1, decorator2)
def function(): pass
```
基本等价于
``` python
def function(): pass
function = decorator1(function)
function = decorator2(function)
```
### **py3p.final**
#### 权限装饰器，禁止类被继承
当尝试继承被 `@final` 装饰的类时，报错 `TypeError: type "{name}" is not an acceptable base type`
### **py3p.protected**
#### 权限装饰器，替换方法继承链
装饰器参数为该方法特有的继承链，替代类继承链生效
### **py3p.private**
#### 权限装饰器，禁止方法被继承
被装饰的方法将不允许被非当前类对象调用，不适用于类方法和静态方法
### **py3p.monitor**
#### 装饰器，运行时类型监控器
> 在函数调用时，检查传入的参数和函数的返回值是否符合类型注解
- 应用于类时自动应用于类的方法
- 类型注解允许嵌套使用
- 当类型注解中出现不支持的类型时，产生官方的报错信息
- 当数据类型与类型注解发生冲突时，产生详细的报错信息
#### 推荐使用的类型注解
| 注解类型 | 含义 |
| :---: | :---: |
| `None` | 仅允许参数为 `None` |
| `str` | 动态解析类型 |
| `type` | 单一类型检查 |
| `tuple` `Union` | 满足其中之一即可 |
| `list` | 必须全部满足 |
| `set` | 可哈希的有效值枚举 |
| `range` | 整数数值范围 |
| `function` | 自定义验证器函数 |
| `dict` | 仅应用于 `**` 参数的精细化注解 |
### **py3p.NameSpace**
#### 增强型 `dict`
- 继承自 `dict`，具有 `dict` 的基本特性
- 可以像访问属性一样访问数据，遵循数据优先访问规则
- 访问深层数据时，如果路径中的父命名空间不存在会自动创建
- 赋值 `None` 会自动删除对应的数据，保持命名空间整洁
- 提供 `prune()` 方法，用于递归清理空的 `NameSpace`
- 接受 `@py3p.monitor` 的类型检查
#### 访问规则
| 数据存在 | 属性存在 | 获取行为 | 赋值行为 |
| :---: | :---: | :--- | :--- |
| ✅ | ✅ | 返回数据 | 更新数据 |
| ✅ | ❌ | 返回数据 | 更新数据 |
| ❌ | ✅ | 返回属性 | 创建数据 |
| ❌ | ❌ | 返回新建的空 `NameSpace` | 创建数据 |
## 许可
本项目使用 **MIT License** 开源许可协议，详情参见 [LICENSE](LICENSE) 文件。
