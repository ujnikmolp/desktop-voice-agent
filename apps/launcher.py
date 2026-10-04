"""软件扫描与打开模块"""
import os
import subprocess
from pathlib import Path

# 排除关键词
EXCLUDE_KEYWORDS = [
    "卸载", "Uninstall", "uninstall", "Manual", "manual",
    "Documentation", "Release notes", "Release Notes",
    "Quickstart", "Sample", "Replays", "Logs and errors",
    "检查更新", "配置 Java", "关于 Java", "Deactivate"
]


def _is_excluded(name: str) -> bool:
    return any(kw in name for kw in EXCLUDE_KEYWORDS)


def scan_desktop_apps() -> dict:
    """扫描桌面和开始菜单的快捷方式，返回 {软件名: 路径}"""
    apps = {}
    scan_dirs = [
        Path(os.path.expanduser("~")) / "Desktop",
        Path("C:/Users/Public/Desktop"),
        Path(os.path.expanduser("~")) / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs",
        Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs"),
    ]

    for d in scan_dirs:
        if not d.exists():
            continue
        for lnk in d.rglob("*.lnk"):
            name = lnk.stem
            if not _is_excluded(name):
                apps[name] = str(lnk)

    # 系统自带程序
    apps.update({
        "计算器": "calc.exe",
        "记事本": "notepad.exe",
        "画图": "mspaint.exe",
        "命令提示符": "cmd.exe",
        "任务管理器": "taskmgr.exe",
        "资源管理器": "explorer.exe",
    })
    return apps


# 全局软件表（模块加载时扫描一次）
APP_PATHS = scan_desktop_apps()


def open_app(app_name: str) -> str:
    """根据软件名打开对应程序"""
    if app_name in APP_PATHS:
        try:
            subprocess.Popen(f'start "" "{APP_PATHS[app_name]}"', shell=True)
            return f"已成功打开{app_name}"
        except Exception as e:
            return f"打开{app_name}失败：{e}"

    # 模糊匹配
    for name in APP_PATHS:
        if app_name in name or name in app_name:
            try:
                subprocess.Popen(f'start "" "{APP_PATHS[name]}"', shell=True)
                return f"已打开{name}"
            except Exception as e:
                return f"打开{name}失败：{e}"

    return f"没有找到名为'{app_name}'的软件"