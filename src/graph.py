from langgraph.graph import StateGraph, START, END
from .state import PostState
from .agents import research_agent, strategy_agent, writer_agent, reviewer_agent, formatter_agent


def should_revise(state: PostState) -> str:
    """Decide whether to revise the draft or proceed to formatting."""
    score = state.get("review_score", 0)
    revision_count = state.get("revision_count", 0)

    # Revise if score < 7 and haven't exceeded 3 revisions
    if score < 7 and revision_count < 3:
        return "revise"
    return "approve"


def build_graph() -> StateGraph:
    """Build and compile the LinkedIn post generator graph."""
    graph = StateGraph(PostState)

    # Add nodes
    graph.add_node("research", research_agent)
    graph.add_node("strategy", strategy_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("reviewer", reviewer_agent)
    graph.add_node("formatter", formatter_agent)

    # Add edges
    graph.add_edge(START, "research")
    graph.add_edge("research", "strategy")
    graph.add_edge("strategy", "writer")
    graph.add_edge("writer", "reviewer")

    # Conditional edge: revise or approve
    graph.add_conditional_edges(
        "reviewer",
        should_revise,
        {
            "revise": "writer",
            "approve": "formatter"
        }
    )

    graph.add_edge("formatter", END)

    return graph.compile()


# Singleton compiled graph
linkedin_graph = build_graph()
