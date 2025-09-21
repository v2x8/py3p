# py3p - Python 3 Plus Libraries
## 语言
- [English](README.md)
## 目录
- [简介](#简介)
- [功能](#功能)
    - [py3p.exports](#py3pexports)
- [许可](#许可)
## 简介
本仓库是一个基于 python 3 标准库的增强型扩展工具集。
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
## 许可
本项目使用 **MIT License** 开源许可协议，详情参见 [LICENSE](LICENSE) 文件。
