# LLM Function Calling / Tool Use 机制

## Function Calling 是什么
Function Calling 是 LLM 的一种能力：开发者用 JSON Schema 描述可用工具（名字、参数、
参数类型），LLM 根据用户问题返回要调用哪个工具、传什么参数。程序端解析这个结构化输出，
执行真正的函数，再把结果回传给 LLM，让它生成自然语言回复。

## Function Calling 核心流程
1. 开发者定义工具（JSON Schema）：工具名、描述、参数
2. 用户输入问题
3. LLM 判断是否需要调用工具，返回 tool_calls
4. 程序端解析 tool_calls，分发到对应函数执行
5. 把执行结果作为 tool 消息回传给 LLM
6. LLM 生成最终自然语言回复

## 为什么用 Function Calling
1. 结构化输出：LLM 返回 JSON，程序端可以安全解析、校验参数
2. 避免歧义：不用解析自然语言指令
3. 更安全：参数有类型约束
4. 可扩展：新增工具只需定义 Schema

## 可扩展的工具注册与调度框架怎么设计
三部分：
1. TOOLS_SCHEMA：给 LLM 看的工具定义列表（JSON Schema）
2. TOOL_MAP：工具名到实际函数的映射字典
3. dispatch_tool：根据工具名分发到对应函数，带异常捕获

新增工具步骤：
1. 在 TOOLS_SCHEMA 加一条工具定义
2. 在 TOOL_MAP 注册函数
主逻辑完全不用改——这叫"声明式注册"。

## 多轮工具调用
LLM 可以连续调用多个工具。实现方式：只要 LLM 还返回 tool_calls，就继续执行并把
结果回传，直到 LLM 返回普通文本。循环上限一般设 5-10 轮，避免无限调用。