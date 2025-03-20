# -*- coding: utf-8 -*-
# 修复Windows中文编码问题
import sys
import locale

if sys.platform.startswith('win'):
    locale.setlocale(locale.LC_ALL, 'chinese')
    sys.stdout.reconfigure(encoding='utf-8')

from wxauto import WeChat
from uiautomation import SendKeys
import time
from datetime import datetime
import re

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

# 初始化微信客户端
wx = WeChat()


def is_triggered(msg, pattern):
    """正则验证触发条件"""
    try:
        return re.fullmatch(pattern, msg.strip()) is not None
    except re.error:
        return False


def format_reply(template):
    """生成带日期的回复内容"""
    today = datetime.now().strftime('%Y年%m月%d日')
    return template.replace("{date}", today).strip().replace('\n', '{Shift}{Enter}')


def send_message(text):
    """发送多行消息"""
    SendKeys(text, waitTime=0.1)
    SendKeys('{Enter}')


def main():
    last_trigger = ""  # 防重复触发记录
    print(f"[{datetime.now()}] 微信机器人已启动 | 管理员: {ADMIN_NAME}")

    while True:
        try:
            # 切换到目标群聊
            wx.ChatWith(GROUP_NAME)

            # 获取最新消息
            msgs = wx.GetAllMessage()
            if not msgs:
                time.sleep(3)
                continue

            # 解析消息信息
            last_sender = msgs[-1][0].strip()  # 发送者
            current_msg = msgs[-1][1].strip()  # 消息内容

            # 管理员权限验证
            if last_sender != ADMIN_NAME:
                print(f"[过滤] 非管理员消息 [{last_sender}]: {current_msg[:20]}...")
                time.sleep(3)
                continue

            # 防重复触发检测
            if current_msg == last_trigger:
                time.sleep(3)
                continue
            last_trigger = current_msg

            # 遍历触发规则
            for number, rule in REPLY_RULES.items():
                if is_triggered(current_msg, rule["pattern"]):
                    reply_text = format_reply(rule["template"])
                    send_message(reply_text)
                    print(f"[触发] 数字 {number} | 内容: {reply_text[:30]}...")
                    time.sleep(3)  # 发送间隔保护
                    break

            time.sleep(3)
        except Exception as e:
            print(f"[异常] {str(e)}")
            time.sleep(5)


if __name__ == "__main__":
    main()