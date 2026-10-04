"""数学计算工具"""
import re


def calculate(expression: str) -> str:
    """计算数学表达式，比如 '2 + 3 * 4'"""
    try:
        # 安全校验：只允许数字、运算符、括号、小数点、空格
        if not re.match(r'^[\d\s\+\-\*/\(\)\.]+$', expression):
            return "表达式包含非法字符，只能包含数字和 + - * / ( ) . 空格"

        # 计算
        result = eval(expression)

        # 如果是浮点数，保留合适位数
        if isinstance(result, float):
            result = round(result, 6)

        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "除数不能为 0"
    except Exception as e:
        return f"计算失败：{e}"