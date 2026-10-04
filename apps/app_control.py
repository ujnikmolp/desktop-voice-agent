"""软件控制工具：打开/关闭软件"""
import subprocess


# 常见软件 → 进程名映射
PROCESS_MAP = {
    "微信": ["Weixin.exe", "WeChatAppEx.exe", "WeChat.exe"],
    "QQ": ["QQ.exe"],
    "记事本": ["notepad.exe"],
    "计算器": ["Calculator.exe", "calc.exe"],
    "画图": ["mspaint.exe"],
    "Chrome": ["chrome.exe"],
    "Edge": ["msedge.exe"],
    "网易云音乐": ["cloudmusic.exe"],
    "QQ音乐": ["QQMusic.exe"],
    "钉钉": ["DingTalk.exe"],
    "飞书": ["Feishu.exe", "Lark.exe"],
}


def close_app(app_name: str) -> str:
    """根据软件名关闭对应程序"""
    # 精确匹配
    if app_name in PROCESS_MAP:
        proc_name = PROCESS_MAP[app_name]
        return _kill_process(proc_name, app_name)

    # 模糊匹配
    for name, proc in PROCESS_MAP.items():
        if app_name in name or name in app_name:
            return _kill_process(proc, name)

    return f"没有找到名为'{app_name}'的软件，无法关闭"


def _kill_process(proc_names, display_name: str) -> str:
    """执行 taskkill（支持多个进程名）"""
    if isinstance(proc_names, str):
        proc_names = [proc_names]

    killed_any = False
    for proc in proc_names:
        try:
            result = subprocess.run(
                f'taskkill /IM "{proc}" /F',
                shell=True, capture_output=True, text=True, encoding="gbk",
            )
            if result.returncode == 0:
                killed_any = True
        except Exception:
            pass

    if killed_any:
        return f"已关闭{display_name}"
    return f"关闭{display_name}失败，可能没在运行"


def open_url(url: str) -> str:
    """打开网址"""
    import webbrowser
    
    # 没带 http 前缀的自动补 https
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    try:
        webbrowser.open(url)
        return f"已打开 {url}"
    except Exception as e:
        return f"打开失败：{e}"


def open_website(name: str) -> str:
    """根据网站名打开对应网址"""
    SITE_MAP = {
        "b站": "https://www.bilibili.com",
        "哔哩哔哩": "https://www.bilibili.com",
        "bilibili": "https://www.bilibili.com",
        "百度": "https://www.baidu.com",
        "知乎": "https://www.zhihu.com",
        "淘宝": "https://www.taobao.com",
        "京东": "https://www.jd.com",
        "github": "https://github.com",
        "csdn": "https://www.csdn.net",
        "youtube": "https://www.youtube.com",
        "谷歌": "https://www.google.com",
    }
    
    name_lower = name.lower()
    for key, url in SITE_MAP.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return open_url(url)
    
    # 不是常见网站，当网址处理
    if "." in name:
        return open_url(name)
    
    return f"没有找到'{name}'对应的网站"