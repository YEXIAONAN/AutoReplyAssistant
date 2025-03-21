# AutoReplyAssistant

> 一个使用Python实现微信自动回复的脚本，它可以帮助你快速回复群内的信息。

### 技术实现🚀
1.使用**wxauto**作为主要库
2.使用**datetime**作为获取日期
3.使用**uiautomation**自动化进行控制操作

----

开箱即用，你只需要下载**.py**代码，放在一个合适的位置。随后修改代码中的

```python
# ===================== 配置区域 =====================
GROUP_NAME = "群聊名称"  # 目标群聊名称（必须完全一致）
ADMIN_NAME = "管理员名称"  # 管理员群昵称（必须完全一致）
REPLY_RULES = {
    1: {
        "pattern": r'^1$',  # 精确匹配纯数字1
        "template": """
回复词1

{date}
"""
    },
    2: {
        "pattern": r'^2$',  # 精确匹配纯数字2
        "template": """
回复词2

{date}
"""
    },
    3: {
        "pattern": r'^3$',  # 精确匹配纯数字3
        "template": """
回复词3

{date}
"""
    }

}
# =================== 配置区域结束 ====================
```

这一段，将里面需要修改的设置为自己的信息
