import pytest
from apps.app_control import close_app
from core.tools import dispatch_tool

# 测试用例 1：正向测试 - 关闭一个不存在的软件，看是否返回安全提示
def test_close_app_not_exist():
    result = close_app("绝对不存在的软件XYZ")
    assert "没有找到" in result

# 测试用例 2：异常测试 - 故意传入不存在的工具名，看系统能否兜底
def test_dispatch_invalid_tool():
    result = dispatch_tool("hack_system", {})
    assert "未知工具" in result

# 测试用例 3：参数缺失测试 - 调用工具但不传参数
def test_dispatch_missing_params():
    result = dispatch_tool("open_app", {}) # 不传 app_name
    assert "失败" in result or "未知" in result