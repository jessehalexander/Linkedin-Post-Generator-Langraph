"""Example: Generate LinkedIn posts programmatically."""

import os
from dotenv import load_dotenv

load_dotenv()

from main import generate_post

# Example 1: Tech leadership post
post1 = generate_post(
    topic="Why engineers who can communicate clearly advance faster in their careers",
    tone="inspirational",
    target_audience="software engineers and tech professionals",
    key_points=[
        "Technical skills get you hired, communication skills get you promoted",
        "Writing clarity = thinking clarity",
        "How to practice: daily writing habit"
    ]
)

print("=" * 60)
print("GENERATED POST:")
print("=" * 60)
print(post1)
