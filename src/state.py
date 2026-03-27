from typing import TypedDict, Annotated, Optional
import operator


class PostState(TypedDict):
    # Input
    topic: str
    tone: str  # e.g. "professional", "casual", "inspirational", "educational"
    target_audience: str
    key_points: list[str]

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
