"""
Agent Orchestrator（智能体调度中枢）

职责：
- 管理会话生命周期
- 组装上下文（但不理解内容）
- 请求 Decision Core 生成 Intent
- 对 Intent 进行路由、调度、过滤
- 将 Intent 交给正确的执行子系统

明确不做：
- 不生成 Intent
- 不调用模型
- 不执行具体行为
- 不直接接触硬件 / UI / API
"""

from typing import Optional

from agent.intent import Intent, IntentType


class AgentOrchestrator:
    """
    Agent 的调度中枢
    这是整个系统中：
    最“无聊”但最不能写错的模块
    """
    def __init__(self):
        # 当前会话（Session）
        self._session = None

        # Decision Core（决策模块，占位）
        self._decision_core = None

        # Intent 执行路由（占位）
        self._intent_router = None

    # 生命周期管理
    def start(self) -> None:
        """
        启动 Agent
        初始化会话、准备各子系统
        """
        # TODO: 初始化 session
        # TODO: 绑定 decision core
        # TODO: 绑定 intent router
        pass

    def shutdown(self) -> None:
        """
        关闭 Agent
        优雅停止当前行为、保存必要状态
        """
        pass

    # 输入入口
    def handle_input(self, input_data: object) -> Optional[Intent]:
        """
        Agent 的统一输入入口
        input_data 可以是：
        用户文本，语音转写结果，系统事件，定时触发信号
        Orchestrator 不解析具体内容，
        只负责把它交给 Decision Core
        """
        # 组装上下文（占位）
        context = self._build_context(input_data)
        # 请求决策模块生成 Intent
        intent = self._request_intent(context)
        # 调度 / 路由 Intent
        self._dispatch_intent(intent)

        return intent

    # 内部调度逻辑
    def _build_context(self, input_data: object) -> object:
        """
        构建上下文
        包含 Session 状态、Memory 视图、Persona 快照
        Orchestrator 不理解 Context 结构
        """
        # TODO: 调用 ContextBuilder
        return input_data  # 占位

    def _request_intent(self, context: object) -> Intent:
        """
        向 Decision Core 请求 Intent
        Orchestrator 不关心 Intent 是怎么生成的
        """
        if self._decision_core is None:
            raise RuntimeError("Decision core not set")
        return self._decision_core.generate_intent(context)

    def _dispatch_intent(self, intent: Intent) -> None:
        """
        根据 Intent 类型进行调度
        校验 Intent 合法性、根据 type 路由到不同执行系统
        """
        if intent is None:
            return

        # 基础安全校验
        self._validate_intent(intent)

        # 路由
        if self._intent_router is None:
            raise RuntimeError("Intent router not set")

        self._intent_router.route(intent)

    def _validate_intent(self, intent: Intent) -> None:
        """
        Intent 的基础合法性校验
        这里只做“结构级”校验，不做语义级判断
        """
        if not isinstance(intent, Intent):
            raise TypeError("Invalid intent type")

        if not isinstance(intent.type, IntentType):
            raise ValueError("Intent has invalid type")
