"""系统信息工具：时间、日期等"""
from datetime import datetime


def get_current_time() -> str:
    """获取当前日期和时间"""
    now = datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[now.weekday()]
    return f"现在是 {now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekday}"


def get_current_date() -> str:
    """获取当前日期"""
    now = datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return f"今天是 {now.strftime('%Y年%m月%d日')} {weekdays[now.weekday()]}"