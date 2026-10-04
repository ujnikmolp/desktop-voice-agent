"""工具注册与分发"""
from apps.system_status import get_system_status, get_battery_status
from apps.calculator import calculate
from apps.weather import get_weather
from apps.system_info import get_current_time, get_current_date
from apps.launcher import open_app
from apps.app_control import close_app
from apps.app_control import close_app, open_website
from apps.file_search import search_file, open_file, find_and_open
from memory.store import (
    save_memory, get_memory, list_memory, delete_memory, semantic_search
)


TOOL_MAP = {
    "open_app": open_app,
    "save_memory": save_memory,
    "get_memory": get_memory,
    "list_memory": list_memory,
    "delete_memory": delete_memory,
    "search_memory": semantic_search,
    "get_current_time": get_current_time,
    "get_current_date": get_current_date, 
    "get_weather": get_weather, 
    "calculate": calculate, 
    "get_system_status": get_system_status,
    "get_battery_status": get_battery_status, 
    "close_app": close_app,
    "open_website": open_website,
    "search_file": search_file,
    "open_file": open_file,
    "find_and_open": find_and_open,
}


TOOLS_SCHEMA = [
        {
        "type": "function",
        "function": {
            "name": "search_file",
            "description": "在常用目录搜索文件（不打开）。用户说'帮我找一下xxx'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "文件名关键词"}
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_file",
            "description": "用默认程序打开指定路径的文件。用户提供完整文件路径时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "文件完整路径"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_and_open",
            "description": "搜索并直接打开第一个匹配的文件。用户说'打开我的xxx'、'打开简历'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "文件名关键词"}
                },
                "required": ["keyword"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "打开网站，比如'打开B站'、'打开百度'、'打开知乎'、'打开github'等",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "网站名称，如'B站'、'百度'"}
                },
                "required": ["name"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "close_app",
            "description": "关闭电脑上正在运行的软件，比如微信、QQ、记事本等。用户说'关闭xxx'、'退出xxx'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "要关闭的软件名称"}
                },
                "required": ["app_name"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "get_system_status",
            "description": "获取电脑的 CPU、内存、磁盘使用率。当用户问'电脑卡不卡'、'内存用了多少'、'电脑状态'时调用",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_battery_status",
            "description": "获取电脑电池状态和电量。当用户问'电量还有多少'、'电池怎么样'时调用",
            "parameters": {"type": "object", "properties": {}}
        }
    },
        {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式。当用户说'帮我算一下'、'XX 加 XX 等于多少'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，比如 '123 * 456 + 789'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气。当用户问'XX天气怎么样'、'今天冷不冷'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，如'北京'、'上海'、'深圳'"
                    }
                },
                "required": ["city"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的具体时间（几点几分几秒）。当用户问'现在几点'、'现在时间'时调用",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "获取当前的日期（年月日、星期几）。当用户问'今天几号'、'今天星期几'时调用",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "打开电脑上的软件，比如微信、计算器、记事本、Steam等",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "要打开的软件名称"}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "保存一条信息，比如账号、密码、邮箱、地址、备忘等。用户说'记住xxx'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "要保存的项的名称"},
                    "value": {"type": "string", "description": "对应的值"}
                },
                "required": ["key", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "精确查询一条已保存的信息。当用户明确问'我的xxx是什么'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "要查询的项的名称"}
                },
                "required": ["key"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_memory",
            "description": (
                "语义检索记忆。当用户的问题模糊、无法确定具体 key 时调用，"
                "例如'我怎么联系别人'、'我之前说过什么关于工作的事'、'帮我找找相关的信息'。"
                "不要用于明确问某个 key 的场景。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "用户的自然语言查询"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_memory",
            "description": "列出所有已保存的信息。用户问'我记住了什么'时调用",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_memory",
            "description": "删除一条已保存的信息。用户说'忘掉xxx'时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "要删除的项的名称"}
                },
                "required": ["key"]
            }
        }
    }
]


def dispatch_tool(func_name: str, args: dict) -> str:
    """根据工具名调用对应的函数"""
    func = TOOL_MAP.get(func_name)
    if not func:
        return f"未知工具：{func_name}"
    try:
        return func(**args)
    except Exception as e:
        return f"工具执行失败：{e}"