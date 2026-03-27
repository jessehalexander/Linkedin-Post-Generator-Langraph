#!/usr/bin/env python3
"""LinkedIn Post Generator - LangGraph Agent Pipeline"""

import os
from dotenv import load_dotenv
from src.graph import linkedin_graph
from src.topic_graph import topic_graph

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


def suggest_topics(
    industry: str,
    role: str,
    interests: list[str] = None,
    recent_experience: str = ""
) -> list[dict]:
    """Generate LinkedIn post topic suggestions based on user context.

    Args:
        industry: User's industry (e.g. "Software Engineering", "Marketing")
        role: User's current role (e.g. "Senior Engineer", "Product Manager")
        interests: List of expertise areas or interests
        recent_experience: Optional context like "just led a product launch"

    Returns:
        List of dicts with keys: title, description, angle
    """
    if interests is None:
        interests = []

    initial_state = {
        "industry": industry,
        "role": role,
        "interests": interests,
        "recent_experience": recent_experience,
        "suggested_topics": [],
        "messages": []
    }

    final_state = topic_graph.invoke(initial_state)
    return final_state["suggested_topics"]


def _print_topic_suggestions(topics: list[dict]) -> None:
    """Print numbered topic suggestions to the console."""
    print("\n" + "="*60)
    print("SUGGESTED LINKEDIN POST TOPICS:")
    print("="*60)
    for i, topic in enumerate(topics, 1):
        print(f"\n{i}. {topic.get('title', 'N/A')}")
        if topic.get("description"):
            print(f"   {topic['description']}")
        if topic.get("angle"):
            print(f"   Angle: {topic['angle']}")
    print("\n" + "="*60)


def main():
    """Interactive CLI for the LinkedIn Post Generator."""
    print("\n" + "="*60)
    print("  LinkedIn Post Generator powered by LangGraph + Claude")
    print("="*60 + "\n")
    print("What would you like to do?")
    print("  1. Suggest topics for me")
    print("  2. I already have a topic")
    choice = input("\nEnter choice [1/2]: ").strip() or "2"

    topic = ""

    if choice == "1":
        print("\n--- Topic Suggester ---")
        industry = input("Your industry (e.g. Software, Marketing, Finance): ").strip() or "Technology"
        role = input("Your role (e.g. Software Engineer, Product Manager): ").strip() or "Professional"
        print("Your interests/expertise areas (separated by '|', or press Enter to skip): ")
        interests_input = input().strip()
        interests = [i.strip() for i in interests_input.split("|") if i.strip()] if interests_input else []
        print("Any recent experience or context? (press Enter to skip): ")
        recent_experience = input().strip()

        print("\nGenerating topic suggestions...")
        topics = suggest_topics(
            industry=industry,
            role=role,
            interests=interests,
            recent_experience=recent_experience
        )
        _print_topic_suggestions(topics)

        print("Enter a number to select a topic, or type your own topic: ")
        selection = input().strip()

        if selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(topics):
                topic = topics[idx]["title"]
                print(f"\nSelected: {topic}")
            else:
                print("Invalid selection, please enter your own topic.")
                topic = input("Topic: ").strip()
        else:
            topic = selection

    else:
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
