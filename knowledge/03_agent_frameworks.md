# Agent 框架与协议

## LangChain 是什么
LangChain 是构建 LLM 应用的主流框架，提供 Chain、Agent、Tool、Memory、Retriever
等组件，把 LLM 应用的常见模式封装成可复用模块。我手写过 Function Calling 的完整
调度循环，理解底层机制后，再用 LangChain 会更快上手。

## LlamaIndex 是什么
LlamaIndex 是专注 RAG 和数据索引的框架，擅长文档加载、切分、索引、检索。
对比 LangChain：LangChain 更通用，LlamaIndex 更专注 RAG。

## MCP 是什么
MCP（Model Context Protocol，模型上下文协议）是 Anthropic 提出的开放协议，
定义 LLM 和外部工具之间如何通信。核心价值是标准化——让同一个工具能被不同 LLM 复用。

## MCP 和 Function Calling 的区别
Function Calling 是 LLM 层面的能力，由模型直接决定调用哪个工具。
MCP 是协议层面的标准，定义 LLM 和工具之间如何通信。
简单说：Function Calling 是"模型决策"，MCP 是"标准化接口"。两者可以配合使用。

## 多 Agent 协同是什么
多 Agent 协同是让多个 Agent 分工合作完成复杂任务。常见模式：
1. 主管 Agent + 执行 Agent：主管拆解任务
2. 流水线模式：Agent 依次处理
3. 辩论模式：多个 Agent 各给方案，再综合
典型框架：AutoGen、CrewAI。