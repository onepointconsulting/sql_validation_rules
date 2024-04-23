from typing import TypedDict, Annotated, List, Union, Tuple
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator

FIELD_EXCLUSION_RULES = "exclusion_rules"


class AgentState(TypedDict):
    table: str
    field: str
    exclusion_rules: str
    chat_history: List[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    extraction_content: str
