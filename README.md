# LinkedIn Post Generator — LangGraph Multi-Agent Pipeline

A multi-agent AI system built with LangGraph and Claude that generates high-quality LinkedIn posts through a pipeline of specialized agents.

## Agent Pipeline

```
START → Research → Strategy → Writer → Reviewer → [Revise if score < 7] → Formatter → END
```

| Agent | Role |
|-------|------|
| **Research Agent** | Gathers topic context, trends, and insights |
| **Strategy Agent** | Plans the hook, structure, and CTA |
| **Writer Agent** | Drafts the post (can revise based on feedback) |
| **Reviewer Agent** | Scores 1–10 and provides detailed feedback |
| **Formatter Agent** | Adds hashtags, emojis, and final polish |

The Reviewer → Writer loop runs up to **3 times** until the score reaches ≥ 7/10.

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Anthropic API key:
   ```bash
   cp .env.example .env
   ```

3. Run interactively:
   ```bash
   python main.py
   ```

## Programmatic Usage

```python
from main import generate_post

post = generate_post(
    topic="The future of remote work",
    tone="professional",
    target_audience="HR professionals and team leaders",
    key_points=["async communication", "trust over tracking", "outcome-based management"]
)

print(post)
```

## Tone Options

- `professional` — formal, data-driven
- `casual` — conversational, relatable
- `inspirational` — motivational, story-driven
- `educational` — how-to, structured insights
