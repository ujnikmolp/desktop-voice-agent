"""天气查询工具（基于 wttr.in 免费 API）"""
import requests


def get_weather(city: str = "北京") -> str:
    """
    查询指定城市的当前天气。
    city: 城市名，支持中文（如"北京"、"上海"）或英文（如"Beijing"）
    """
    try:
        # wttr.in 免费 API，format 参数控制返回格式
        # %C=天气状况 %t=温度 %w=风速 %h=湿度
        url = f"https://wttr.in/{city}?format=%C+%t+%w+%h&lang=zh"
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return f"查询{city}天气失败，状态码：{r.status_code}"
        return f"{city}当前天气：{r.text.strip()}"
    except requests.Timeout:
        return "查询天气超时，请稍后再试"
    except Exception as e:
        return f"查询天气失败：{e}"