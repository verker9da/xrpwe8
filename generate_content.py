"""
Arabic Learning Content Generator
Generates English-to-Arabic learning phrases with categories
"""

import os
import json
import requests
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")

# Validate required environment variables
if not AI_MODEL:
    raise ValueError("AI_MODEL environment variable is required! Set it in .env file")

# Learning categories in Arabic (with English for reference)
CATEGORIES = [
    "التحيات اليومية",  # Daily Greetings
    "العبارات الشائعة",  # Common Phrases
    "الطعام والطعام",  # Food & Dining
    "أساسيات السفر",  # Travel Essentials
    "الأرقام والوقت",  # Numbers & Time
    "العائلة والعلاقات",  # Family & Relationships
    "التسوق",  # Shopping
    "الاتجاهات",  # Directions
    "الطقس",  # Weather
    "العواطف والمشاعر",  # Emotions & Feelings
    "العمل والأعمال",  # Work & Business
    "الصحة والجسد",  # Health & Body
    "الألوان والأوصاف",  # Colors & Descriptions
    "الحيوانات",  # Animals
    "الهوايات والأنشطة",  # Hobbies & Activities
    "الدافع",  # Motivation
    "الحب",  # Love
    "النجاح",  # Success
    "الحكمة",  # Wisdom
    "السعادة",  # Happiness
]

# English names for categories (for display/filenames)
CATEGORIES_ENGLISH = {
    "التحيات اليومية": "Daily Greetings",
    "العبارات الشائعة": "Common Phrases",
    "الطعام والطعام": "Food & Dining",
    "أساسيات السفر": "Travel Essentials",
    "الأرقام والوقت": "Numbers & Time",
    "العائلة والعلاقات": "Family & Relationships",
    "التسوق": "Shopping",
    "الاتجاهات": "Directions",
    "الطقس": "Weather",
    "العواطف والمشاعر": "Emotions & Feelings",
    "العمل والأعمال": "Work & Business",
    "الصحة والجسد": "Health & Body",
    "الألوان والأوصاف": "Colors & Descriptions",
    "الحيوانات": "Animals",
    "الهوايات والأنشطة": "Hobbies & Activities",
    "الدافع": "Motivation",
    "الحب": "Love",
    "النجاح": "Success",
    "الحكمة": "Wisdom",
    "السعادة": "Happiness",
}


def generate_learning_content(category: str, num_phrases: int = 5) -> list:
    """
    Generate English-Arabic learning phrases using Pollinations AI

    Returns list of dicts with:
    - english: English phrase
    - arabic: Arabic translation
    - pronunciation: Phonetic pronunciation guide
    - context: Usage context/example
    """

    if not POLLINATIONS_API_KEY:
        raise ValueError("POLLINATIONS_API_KEY not set!")

    system_prompt = (
        "You are an Arabic language teacher creating educational content. "
        "Generate practical, commonly-used phrases for language learners. "
        "IMPORTANT: Create COMPLETE sentences with NO blanks, NO underscores, NO placeholders. "
        "Every phrase must be a full, natural sentence that can be spoken aloud. "
        "Avoid phrases like 'I'm allergic to ____' - instead use specific examples like 'I'm allergic to cats'. "
        "Return ONLY valid JSON array format with no additional text."
    )

    user_prompt = (
        f"Create {num_phrases} essential {category} phrases for English speakers learning Arabic. "
        f"For each phrase, provide: "
        f"1. English phrase (natural, conversational, COMPLETE sentence with NO blanks or underscores) "
        f"2. Arabic translation (correct, native-level, COMPLETE sentence in Arabic script) "
        f"3. Pronunciation guide (simple phonetic spelling for English speakers) "
        f"4. Context (when/how to use it, 1 short sentence) "
        f"\n\nIMPORTANT RULES: "
        f"- NO blanks (____) or placeholders "
        f"- Use specific examples (e.g., 'I'm allergic to cats' not 'I'm allergic to ____') "
        f"- Every phrase must be speakable by text-to-speech "
        f"- Make phrases practical and commonly used "
        f"\n\nReturn as JSON array: "
        f'[{{"english": "...", "arabic": "...", "pronunciation": "...", "context": "..."}}]'
    )

    # Use Pollinations AI chat completions endpoint
    url = "https://gen.pollinations.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {POLLINATIONS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 1.0  # Maximum creativity for unique content every time
    }

    print(f"[content] Generating {num_phrases} phrases for: {category}")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()

            # Extract JSON from response (handle markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Parse JSON
            phrases = json.loads(content)

            # Validate structure
            if isinstance(phrases, list) and len(phrases) > 0:
                for phrase in phrases:
                    if not all(k in phrase for k in ["english", "arabic", "pronunciation", "context"]):
                        raise ValueError("Invalid phrase structure")

                print(f"[content] ✅ Generated {len(phrases)} phrases successfully!")
                return phrases
            else:
                raise ValueError("Invalid response format")

        except Exception as e:
            print(f"[content] ⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt == max_retries - 1:
                raise

    raise Exception("Failed to generate content after all retries")


def save_content_to_file(phrases: list, category: str, output_file: str = "content.json"):
    """Save generated content to JSON file"""

    content = {
        "category": category,
        "phrases": phrases,
        "total": len(phrases)
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"[content] Saved to {output_file}")
    return content


if __name__ == "__main__":
    # Test generation
    import random

    category = random.choice(list(CATEGORIES_ENGLISH.keys()))
    phrases = generate_learning_content(category, num_phrases=5)
    save_content_to_file(phrases, category)

    print("\n" + "="*60)
    print(f"Sample phrases from '{category}':")
    print("="*60)
    for i, phrase in enumerate(phrases, 1):
        print(f"\n{i}. {phrase['english']}")
        print(f"   Arabic: {phrase['arabic']}")
        print(f"   Pronunciation: {phrase['pronunciation']}")
        print(f"   Context: {phrase['context']}")
