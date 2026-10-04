"""文件搜索工具"""
import os
import subprocess
from pathlib import Path


# 默认搜索目录（可自己加）
DEFAULT_SEARCH_DIRS = [
    Path(os.path.expanduser("~")) / "Desktop",
    Path(os.path.expanduser("~")) / "Documents",
    Path(os.path.expanduser("~")) / "Downloads",
    Path("D:/AAA投递简历"),          # 你的简历目录
    Path("D:/AI/learn"),             # 工作目录
]


def search_file(keyword: str, search_dir: str = "", max_results: int = 5) -> str:
    """
    在指定目录或默认目录搜索文件名包含关键词的文件。
    
    Args:
        keyword: 文件名关键词
        search_dir: 可选，指定搜索目录（如 "D:/AAA投递简历"）
        max_results: 最多返回多少个结果
    """
    if not keyword.strip():
        return "请提供要搜索的关键词"

    # 确定搜索目录
    if search_dir and os.path.exists(search_dir):
        dirs = [Path(search_dir)]
    else:
        dirs = DEFAULT_SEARCH_DIRS

    results = []
    for d in dirs:
        if not d.exists():
            continue
        try:
            for f in d.rglob(f"*{keyword}*"):
                if f.is_file():
                    results.append(str(f))
                    if len(results) >= max_results:
                        break
            if len(results) >= max_results:
                break
        except Exception:
            continue

    if not results:
        dirs_str = ", ".join(str(d) for d in dirs)
        return f"没有找到包含'{keyword}'的文件（已搜索：{dirs_str}）"

    lines = [f"- {r}" for r in results]
    return f"找到 {len(results)} 个文件：\n" + "\n".join(lines)


def open_file(filepath: str) -> str:
    """用默认程序打开指定路径的文件"""
    if not os.path.exists(filepath):
        return f"文件不存在：{filepath}"
    try:
        os.startfile(filepath)
        return f"已打开：{os.path.basename(filepath)}"
    except Exception as e:
        return f"打开失败：{e}"


def find_and_open(keyword: str, search_dir: str = "") -> str:
    """
    搜索并打开第一个匹配的文件。
    
    Args:
        keyword: 文件名关键词
        search_dir: 可选，指定搜索目录
    """
    if not keyword.strip():
        return "请提供要搜索的关键词"

    if search_dir and os.path.exists(search_dir):
        dirs = [Path(search_dir)]
    else:
        dirs = DEFAULT_SEARCH_DIRS

    for d in dirs:
        if not d.exists():
            continue
        try:
            for f in d.rglob(f"*{keyword}*"):
                if f.is_file():
                    os.startfile(str(f))
                    return f"已打开：{f.name}"
        except Exception:
            continue

    return f"没有找到包含'{keyword}'的文件"


def list_directory(dir_path: str, max_results: int = 20) -> str:
    """列出目录下的文件（可选功能）"""
    if not os.path.exists(dir_path):
        return f"目录不存在：{dir_path}"
    try:
        items = []
        for item in Path(dir_path).iterdir():
            items.append(f"{'[目录]' if item.is_dir() else '[文件]'} {item.name}")
            if len(items) >= max_results:
                break
        if not items:
            return f"目录为空：{dir_path}"
        return f"{dir_path} 下的内容：\n" + "\n".join(items)
    except Exception as e:
        return f"读取目录失败：{e}"