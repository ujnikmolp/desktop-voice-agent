# Agent 主流架构模式

## ReAct 模式
ReAct = Reasoning（推理）+ Acting（行动）。LLM 交替进行推理和行动：先思考
"我该做什么"，再执行动作，观察结果，再思考下一步。我的 Function Calling 实现
本质上是 ReAct 的简化版。

## Plan-and-Execute 模式
先规划完整步骤，再逐步执行。适合复杂多步任务。
对比 ReAct：ReAct 边走边想，Plan-and-Execute 先想好再走。优势是全局视角。

## Reflection 模式
Agent 执行完任务后自我反思"哪里做得不好"，然后改进。
适合需要高质量输出的场景，比如代码生成、写作。

## 多轮工具调用
实现方式：循环——LLM 返回 tool_calls → 执行 → 结果回传 → LLM 再判断。
直到 LLM 返回普通文本。循环上限一般设 5-10 轮。

## 如何选择 Agent 架构
简单任务：Function Calling 或 ReAct
复杂多步：Plan-and-Execute
高质量要求：Reflection
多角色协作：多 Agent 协同