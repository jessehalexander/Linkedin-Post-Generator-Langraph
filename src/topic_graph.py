from langgraph.graph import StateGraph, START, END
from .state import TopicSuggestionState
from .agents import topic_suggester_agent


def build_topic_graph() -> StateGraph:
    """Build and compile the topic suggestion graph."""
    graph = StateGraph(TopicSuggestionState)
    graph.add_node("topic_suggester", topic_suggester_agent)
    graph.add_edge(START, "topic_suggester")
    graph.add_edge("topic_suggester", END)
    return graph.compile()


topic_graph = build_topic_graph()
