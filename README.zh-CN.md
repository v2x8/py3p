# py3p - Python 3 Plus Libraries
## 语言
- [English](README.md)
## 目录
- [简介](#简介)
- [功能](#功能)
    - [py3p.exports](#py3pexports)
    - [py3p.Empty](#py3pempty)
    - [py3p.safe](#py3psafe)
    - [py3p.pstr](#py3ppstr)
    - [py3p.getname](#py3pgetname)
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
|:---:|:---:|:---:|
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
### **py3p.pstr**
#### `builtins.str` 函数的美化版本
- 支持使用参数 `indent` 自定义缩进，对所有类型自动识别并处理
- 推荐 `indent` 使用 `bool`、`int` 或 `str` 类型
#### `indent` 识别
| 类型 | 特殊值 | 处理 |
|:---|:---|:---|
| `list` `tuple` | | 连接为 `str` 类型处理 |
| `bytes` `str` | 可被转换为 `float` 或 `int` | 转换为相应类型处理 |
| `float` | | 转换为 `int` 类型处理 (向下取整) |
| `int` | `> 0` | 指定缩进空格数量 |
| `int` | `< 0` | 返回值为单行字符串 |
| `bool` | `True` | 使用 `\t` 缩进 |
| | 布尔表现为 `True` | 转换为 `str` 类型处理 |
| | 布尔表现为 `False` | 返回值为单行字符串 |
### **py3p.getname**
#### 获取可调用对象的名字
- 支持常见的类，函数和方法，包括被 `functools.wraps` 装饰过的函数
- 支持 `functools.partial` 和 `functools.partialmethod` 对象
- 对于不支持的对象，返回值为 None
## 许可
本项目使用 **MIT License** 开源许可协议，详情参见 [LICENSE](LICENSE) 文件。
