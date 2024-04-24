from typing import TypedDict, Annotated, List, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator

from sql_validation_rules.chain.sql_commands import SQLCommand

FIELD_EXCLUSION_RULES = "exclusion_rules"


class AgentState(TypedDict):
    """The graph state."""
    table: str
    """The relational table to which the column is associated."""
    field: str
    """The name of the column for which the SQL validation rules are generated."""
    exclusion_rules: str
    """The rule types that were previously generated and we would like to exclude."""
    chat_history: List[BaseMessage]
    """The list with the message up to a certain point in time."""
    agent_outcome: Union[AgentAction, AgentFinish, None]
    """The last agent outcome which could be an agent action or an object marking the end of the agent execution."""
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    """List of actions and corresponding observations."""
    extraction_content: SQLCommand
    """The extracted SQL command from the extraction LLMChain."""
