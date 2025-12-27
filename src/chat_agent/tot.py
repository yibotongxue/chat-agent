from typing import List, Optional, Any, Callable
from dataclasses import dataclass

from .llm.base import BaseLLM
from .utils.types import InputData, OutputData

@dataclass
class State:
    goal: int
    available_numbers: List[int]
    decided_operation: str  # 确定的乘法
    decided_number: int  # 确定的数字


# 比如
# 3 3 8 8 -> 24
# 根节点： 3 3 8 8 -> 24
# 子节点1： 确定 3 和 乘法操作，则需要 3 8 8 -> 8

def parse_json(text: str) -> dict[str, Any] | None:
    pass

@dataclass
class ThoughtNode:
    """思维树节点 - 请补充必要字段"""
    state: State
    childrens: List['ThoughtNode']
    success_expression: Optional[str] = None
    # TODO: 添加其他字段

def evaluate(state: State, llm: BaseLLM) -> float:
    if len(state.available_numbers) == 1:
        return 1.0 if state.available_numbers[0] == state.goal else 0.0
    prompt = f"""
我们正在完成一个类似24点的游戏，但我们的目标和可用数字有所不同，可用数字包括：{state.available_numbers}，目标是达到数字 {state.goal}。
我们需要请你评估当前的状态，给出一个分数，表示从当前状态达到目标的可能性，数值从0-1的浮点数。请考虑以下因素：
1. 当前状态下，是否有直接的操作可以达到目标？如果有，分数为1.0。
2. 如果没有直接操作，评估通过一系列操作达到目标的可能性。
最终的结果使用JSON格式返回，包含一个字段 "score"，表示评估分数。例如：
```json
{"score": 0.75}
```
"""
    input_data = InputData(
        messages=[{"role": "system", "content": "你是一个评估游戏状态的AI助手。"},
                  {"role": "user", "content": prompt}],
        meta_data={}
    )
    output_data = llm.generate(input_data)
    response = output_data.response
    json_dict = parse_json(response)
    if json_dict and "score" in json_dict:
        return float(json_dict["score"])
    return 0.5

def thought_generator(state: State, llm: BaseLLM) -> list[State]:
    pass

class TreeOfThoughts:
    """Tree of Thoughts 实现"""
    def init(
        self,
        thought_generator: Callable,
        state_evaluator: Callable,
        goal_checker: Callable,
        llm: BaseLLM,
        # TODO: 添加其他必要参数
    ):
        # TODO: 实现
        self.thought_generator = lambda state: thought_generator(state, llm)
        self.state_evaluator = lambda state: evaluate(state, llm)
        self.goal_checker = goal_checker


    def search(self, initial_state: Any) -> Optional[ThoughtNode]:
        """执行搜索 - 至少实现一种搜索策略"""
        # TODO: 实现
        pass

class Point24Solver:
    """24点求解器"""
    def init(self, llm: BaseLLM):
        # TODO: 实现
        self.llm = llm

    def solve(self, numbers: List[int]) -> Optional[str]:
        """
        求解24点
        Args:
            numbers: 4个数字
        Returns:
            表达式字符串，无解返回None
        """
        # TODO: 实现
        tree = TreeOfThoughts(
            thought_generator=thought_generator,
            state_evaluator=evaluate,
            goal_checker=None,  # TODO: 实现目标检查器
            llm=self.llm,
        )
        initial_state = State(
            goal=24,
            available_numbers=numbers,
            decided_operation="",
            decided_number=0,
        )
        result_node = tree.search(initial_state)
        return result_node.success_expression if result_node else None