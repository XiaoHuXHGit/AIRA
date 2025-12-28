"""
我怕我忘了这个东西是干什么用的，因为定义的真的很抽象。所以我写一个详细的注释。
本文件在架构中的位置，是智能体连接硬件，UI，或者是三方插件的接口：
Persona / Emotion / Goal
        ↓
   Decision Core
        ↓
      Intent          ← 这里是“意识的出口”
        ↓
Embodiment / Skill / UI


"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


# Intent 顶层分类
class IntentType(Enum):
    """
    Intent 的宏观分类，用于：调度优先级判断，路由到不同执行子系统，安全与隔离控制
    """
    SPEAK = "speak"
    # 对外表达内容（文本 / 语言 / 表情）
    # 由 Embodiment 决定“怎么说”
    ACT = "act"
    # 期望发生某个外部变化
    # 不描述操作步骤，只描述“想要的结果”
    THINK = "think"
    # 内部思考 / 推理 / 自省
    # ❗ 永远不允许直接对外执行
    WAIT = "wait"
    # 主动等待 / 空闲
    # 是一种明确的决策结果，而不是“什么都没想出来”
    SYSTEM = "system"
    # 系统级意图
    # 改变 Agent 的运行状态或存在方式


# Intent 通用封装
@dataclass
class Intent:
    """
    所有 Intent 的统一封装结构
    Agent Orchestrator 只认这个结构，
    不关心内部 payload 的具体类型
    """
    type: IntentType
    # Intent 的类别（说话 / 行为 / 思考 等）
    payload: Dict[str, Any]
    # 具体 Intent 数据（结构化，不是自然语言）
    priority: int = 0
    # 意图优先级
    # 用于决定是否打断当前行为（越大越重要）
    confidence: float = 1.0
    # Agent 对该意图的确信程度
    # 可用于：
    # - 低信心时请求确认
    # - 低信心时降级执行


# 具体 Intent Schema
@dataclass
class SpeakIntent:
    """
    说话 / 表达意图
    表达“我要说什么”，
    而不是“我要怎么说”
    """
    text: str
    # 要表达的语义内容（已经去除推理过程）
    emotion: Optional[str] = None
    # 粗粒度情绪标签（如 calm / happy / sad）
    # 不绑定具体表情或声学参数
    target: Optional[str] = None
    # 面向对象
    # 例如：user / group / self


@dataclass
class ActIntent:
    """
    行为意图
    描述“我希望发生什么变化”，
    而不是“我打算怎么操作”
    """
    action: str
    # 抽象行为名称
    # 例如：open_app / play_music / send_message
    params: Dict[str, Any]
    # 行为意图参数
    # 是“意图级”的，而不是“实现级”的


@dataclass
class ThinkIntent:
    """
    内部思考意图
    用于：推理，自省，规划草稿，情绪整理
    该 Intent 永远不会被 Embodiment 执行
    """
    thought: str
    # 内部思考内容
    # 不保证对用户可读


@dataclass
class WaitIntent:
    """
    主动等待意图
    用于：Idle，等待输入，降低系统负载
    """
    duration: Optional[float] = None
    # 等待时长（秒）
    # None 表示无限期等待，直到被打断
