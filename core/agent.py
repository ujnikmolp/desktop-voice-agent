"""Agent 核心：LLM 调用 + 工具编排 + 知识库注入"""
import json
from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL
from core.prompts import SYSTEM_PROMPT
from core.tools import TOOLS_SCHEMA, dispatch_tool
from memory.knowledge_base import search_knowledge


_client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def chat(user_input: str, verbose: bool = True) -> str:
    """处理一轮用户输入，返回 Agent 的回复"""
    # 1. 检索知识库
    kb_results = search_knowledge(user_input, top_k=3)

    if kb_results:
        kb_context = "\n\n".join(
            f"【参考资料 {i+1}】\n{r['content']}"
            for i, r in enumerate(kb_results)
        )
        system_content = (
            SYSTEM_PROMPT
            + "\n\n以下是参考资料，请优先基于这些资料回答。"
            + "如果资料里没有相关内容，就正常回答：\n\n"
            + kb_context
        )
    else:
        system_content = SYSTEM_PROMPT

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_input}
    ]

    response = _client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if not msg.tool_calls:
        return msg.content

    messages.append(msg)
    for tool_call in msg.tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        if verbose:
            print(f"[Agent 调用] {func_name}({args})")

        result = dispatch_tool(func_name, args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

    final = _client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return final.choices[0].message.content