import json
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from .state import PostState, TopicSuggestionState

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.7)


def research_agent(state: PostState) -> dict:
    """Research the topic and gather relevant context, trends, and insights."""
    system = SystemMessage(content="""You are a LinkedIn content researcher.
Your job is to analyze a topic and provide:
- Key trends and statistics related to the topic
- Common pain points or challenges in this area
- Relevant insights that would resonate with professionals
- Potential angles or perspectives to explore
Keep your research concise and actionable (200-300 words).""")

    human = HumanMessage(content=f"""Research this LinkedIn post topic:
Topic: {state['topic']}
Target Audience: {state['target_audience']}
Tone: {state['tone']}
Key Points to Cover: {', '.join(state['key_points']) if state['key_points'] else 'None specified'}

Provide research insights that will help create a compelling LinkedIn post.""")

    response = llm.invoke([system, human])
    return {
        "research": response.content,
        "messages": [{"role": "research_agent", "content": response.content}]
    }


def strategy_agent(state: PostState) -> dict:
    """Plan the post structure including hook, body, and CTA."""
    system = SystemMessage(content="""You are a LinkedIn content strategist.
Your job is to create a content plan for a LinkedIn post including:
- A powerful opening hook (first 2-3 lines that stop the scroll)
- Post structure (how to flow the content)
- Key message to emphasize
- Call-to-action (CTA) recommendation
- Optimal post length recommendation
Keep your strategy concise and actionable.""")

    human = HumanMessage(content=f"""Create a content strategy for this LinkedIn post:
Topic: {state['topic']}
Target Audience: {state['target_audience']}
Tone: {state['tone']}
Research Insights: {state['research']}
Key Points: {', '.join(state['key_points']) if state['key_points'] else 'None specified'}

Provide a clear content plan with hook, structure, and CTA.""")

    response = llm.invoke([system, human])
    return {
        "strategy": response.content,
        "messages": [{"role": "strategy_agent", "content": response.content}]
    }


def writer_agent(state: PostState) -> dict:
    """Write the LinkedIn post draft based on research and strategy."""
    revision_note = ""
    if state.get("revision_count", 0) > 0:
        revision_note = f"""
PREVIOUS DRAFT REVIEW FEEDBACK:
{state.get('review', '')}
Score: {state.get('review_score', 0)}/10

Please address the feedback and improve the post significantly."""

    system = SystemMessage(content="""You are an expert LinkedIn content writer.
Write engaging, authentic LinkedIn posts that:
- Start with a powerful hook in the first 1-3 lines
- Use short paragraphs (1-3 sentences max)
- Include white space for readability
- Have a clear narrative arc
- End with a strong CTA or question to drive engagement
- Feel authentic and human, not AI-generated
- Are between 150-300 words for optimal engagement
Do NOT include hashtags (those will be added later). Write only the post body.""")

    human = HumanMessage(content=f"""Write a LinkedIn post with these details:
Topic: {state['topic']}
Target Audience: {state['target_audience']}
Tone: {state['tone']}
Key Points: {', '.join(state['key_points']) if state['key_points'] else 'None specified'}

Research: {state['research']}
Content Strategy: {state['strategy']}
{revision_note}

Write the complete LinkedIn post now.""")

    response = llm.invoke([system, human])
    return {
        "draft": response.content,
        "revision_count": state.get("revision_count", 0) + 1,
        "messages": [{"role": "writer_agent", "content": response.content}]
    }


def reviewer_agent(state: PostState) -> dict:
    """Review the draft and provide a score and feedback."""
    system = SystemMessage(content="""You are a LinkedIn content quality reviewer.
Evaluate the post on these criteria (score each 1-10):
1. Hook strength (does it stop the scroll?)
2. Clarity and readability
3. Authenticity and tone match
4. Value provided to target audience
5. CTA effectiveness

Provide:
- Overall score (average of the above, rounded to nearest integer)
- Specific, actionable feedback
- What works well
- What needs improvement

Format your response as:
SCORE: [number]
FEEDBACK: [your detailed feedback]""")

    human = HumanMessage(content=f"""Review this LinkedIn post draft:

Topic: {state['topic']}
Target Audience: {state['target_audience']}
Tone: {state['tone']}

DRAFT:
{state['draft']}

Provide your quality assessment.""")

    response = llm.invoke([system, human])
    content = response.content

    # Parse score from response
    score = 7  # default
    for line in content.split('\n'):
        if line.startswith('SCORE:'):
            try:
                score = int(line.replace('SCORE:', '').strip())
            except ValueError:
                pass

    return {
        "review": content,
        "review_score": score,
        "messages": [{"role": "reviewer_agent", "content": content}]
    }


def formatter_agent(state: PostState) -> dict:
    """Add hashtags, emojis, and final formatting to the approved draft."""
    system = SystemMessage(content="""You are a LinkedIn post formatter.
Your job is to take a LinkedIn post draft and add:
- 3-5 relevant, strategic hashtags (mix of popular and niche)
- Tasteful emojis where appropriate (don't overdo it)
- Final formatting for maximum readability (proper line breaks, spacing)
- Ensure the post is polished and ready to publish

Return ONLY the final formatted post, nothing else.""")

    human = HumanMessage(content=f"""Format this approved LinkedIn post for publishing:

Topic: {state['topic']}
Target Audience: {state['target_audience']}

APPROVED DRAFT:
{state['draft']}

Add hashtags, emojis, and finalize the formatting. Return only the final post.""")

    response = llm.invoke([system, human])
    return {
        "final_post": response.content,
        "messages": [{"role": "formatter_agent", "content": response.content}]
    }


def topic_suggester_agent(state: TopicSuggestionState) -> dict:
    """Generate 8 LinkedIn post topic suggestions based on user context."""
    interests_str = ", ".join(state["interests"]) if state["interests"] else "not specified"
    recent = state.get("recent_experience", "").strip() or "nothing specific"

    system = SystemMessage(content="""You are a LinkedIn content strategist who helps professionals find compelling post topics.
Generate exactly 8 topic suggestions tailored to the user's background.

For each topic provide:
- title: A short, punchy topic title (max 10 words)
- description: Why this topic will resonate with their audience (1-2 sentences)
- angle: A specific angle or hook to make it stand out (1 sentence)

You MUST respond with valid JSON only — no markdown, no explanation, just a JSON array like:
[
  {"title": "...", "description": "...", "angle": "..."},
  ...
]""")

    human = HumanMessage(content=f"""Generate 8 LinkedIn post topic suggestions for this professional:

Industry: {state['industry']}
Role: {state['role']}
Interests / Expertise Areas: {interests_str}
Recent Experience / Context: {recent}

Return only the JSON array of 8 topic suggestions.""")

    response = llm.invoke([system, human])

    # Parse JSON topics
    try:
        topics = json.loads(response.content)
    except (json.JSONDecodeError, ValueError):
        # Fallback: extract JSON array from response if wrapped in extra text
        content = response.content
        start = content.find("[")
        end = content.rfind("]") + 1
        if start != -1 and end > start:
            try:
                topics = json.loads(content[start:end])
            except (json.JSONDecodeError, ValueError):
                topics = [{"title": response.content, "description": "", "angle": ""}]
        else:
            topics = [{"title": response.content, "description": "", "angle": ""}]

    return {
        "suggested_topics": topics,
        "messages": [{"role": "topic_suggester_agent", "content": str(topics)}]
    }
