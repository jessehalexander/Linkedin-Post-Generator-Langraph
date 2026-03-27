#!/usr/bin/env python3
"""LinkedIn Post Generator - LangGraph Agent Pipeline"""

import os
from dotenv import load_dotenv
from src.graph import linkedin_graph

load_dotenv()


def generate_post(
    topic: str,
    tone: str = "professional",
    target_audience: str = "professionals",
    key_points: list[str] = None
) -> str:
    """Generate a LinkedIn post using the multi-agent pipeline.

    Args:
        topic: The main topic or idea for the post
        tone: Writing tone - "professional", "casual", "inspirational", "educational"
        target_audience: Who the post is targeting
        key_points: Optional list of specific points to cover

    Returns:
        The final formatted LinkedIn post
    """
    if key_points is None:
        key_points = []

    initial_state = {
        "topic": topic,
        "tone": tone,
        "target_audience": target_audience,
        "key_points": key_points,
        "research": "",
        "strategy": "",
        "draft": "",
        "review": "",
        "review_score": 0,
        "revision_count": 0,
        "final_post": "",
        "messages": []
    }

    print(f"\n{'='*60}")
    print(f"LinkedIn Post Generator - LangGraph Pipeline")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    print(f"Tone: {tone}")
    print(f"Target Audience: {target_audience}")
    print(f"{'='*60}\n")

    # Stream the graph execution for visibility
    for step in linkedin_graph.stream(initial_state, stream_mode="values"):
        # Show progress
        if step.get("research") and not step.get("strategy"):
            print("✓ Research complete")
        elif step.get("strategy") and not step.get("draft"):
            print("✓ Strategy complete")
        elif step.get("draft") and not step.get("review"):
            print(f"✓ Draft written (revision #{step.get('revision_count', 1)})")
        elif step.get("review"):
            score = step.get("review_score", 0)
            print(f"✓ Review complete — Score: {score}/10")
        elif step.get("final_post"):
            print("✓ Post formatted and finalized\n")

    # Get final state
    final_state = linkedin_graph.invoke(initial_state)
    return final_state["final_post"]


def main():
    """Interactive CLI for the LinkedIn Post Generator."""
    print("\n" + "="*60)
    print("  LinkedIn Post Generator powered by LangGraph + Claude")
    print("="*60 + "\n")

    # Get user input
    topic = input("Enter your post topic or idea: ").strip()
    if not topic:
        print("Error: Topic cannot be empty.")
        return

    print("\nTone options: professional, casual, inspirational, educational")
    tone = input("Select tone [professional]: ").strip() or "professional"

    target_audience = input("Target audience [professionals]: ").strip() or "professionals"

    print("Key points to cover (press Enter to skip, or enter points separated by '|'): ")
    key_points_input = input().strip()
    key_points = [p.strip() for p in key_points_input.split("|") if p.strip()] if key_points_input else []

    # Generate the post
    final_post = generate_post(
        topic=topic,
        tone=tone,
        target_audience=target_audience,
        key_points=key_points
    )

    print("\n" + "="*60)
    print("FINAL LINKEDIN POST:")
    print("="*60)
    print(final_post)
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
