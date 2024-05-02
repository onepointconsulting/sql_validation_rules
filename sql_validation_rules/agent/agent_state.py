from typing import TypedDict, Annotated, List, Union, Sequence
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator

from sql_validation_rules.chain.sql_commands import SQLCommand

FIELD_VALIDATION_SQL_HISTORY = "validation_sql_history"
INTERMEDIATE_STEPS = "intermediate_steps"
AGENT_OUTCOME = "agent_outcome"
EXTRACTION_CONTENT = "extraction_content"


class AgentState(TypedDict):
    """The graph state."""

    # Agent
    table: str
    """The relational table to which the column is associated."""
    field: str
    """The name of the column for which the SQL validation rules are generated."""
    validation_sql_history: str
    """The rule types that were previously generated and we would like to exclude."""
    chat_history: List[BaseMessage]
    """The list with the message up to a certain point in time."""
    agent_outcome: Union[AgentAction, AgentFinish, None]
    """The last agent outcome which could be an agent action or an object marking the end of the agent execution."""
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    """List of actions and corresponding observations."""

    # Extraction
    extraction_content: SQLCommand
    """The extracted SQL command from the extraction LLMChain."""

    # Supervisor
    messages: Annotated[Sequence[BaseMessage], operator.add]
    """This annotation tells the graph that new messages will be added to the current state."""
    next: str
    """The 'next' field indicates where to route to next"""
