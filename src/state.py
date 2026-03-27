from typing import TypedDict, Annotated, Optional
import operator


class TopicSuggestionState(TypedDict):
    # User context
    industry: str
    role: str
    interests: list[str]
    recent_experience: str  # optional context like "just finished a big project", "attended a conference"

    # Agent outputs
    suggested_topics: list[dict]  # list of {"title": str, "description": str, "angle": str}
    messages: Annotated[list, operator.add]


class PostState(TypedDict):
    # Input
    topic: str
    tone: str  # e.g. "professional", "casual", "inspirational", "educational", "thought_leadership"
    target_audience: str
    key_points: list[str]
    opinion_angle: str  # the author's specific take or opinion on the topic (optional)

    # Agent outputs
    research: str
    strategy: str
    draft: str
    review: str
    review_score: int  # 1-10
    revision_count: int
    final_post: str

    # Control
    messages: Annotated[list, operator.add]
