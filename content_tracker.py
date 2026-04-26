"""
Content Tracker - Tracks generated content to prevent duplicates
Ensures maximum variety and freshness in generated content
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

HISTORY_FILE = Path("content_history.json")
MAX_PHRASE_HISTORY = 500  # Keep last 500 phrases in memory
MAX_CATEGORY_HISTORY = 50  # Keep last 50 category uses


def load_history():
    """Load content history from file"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all required fields exist
                if "used_phrases" not in data:
                    data["used_phrases"] = []
                if "used_categories" not in data:
                    data["used_categories"] = []
                if "phrase_hashes" not in data:
                    data["phrase_hashes"] = []
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"[tracker] ⚠️ Warning: Could not load history file: {e}")
            return {"used_phrases": [], "used_categories": [], "phrase_hashes": []}
    return {"used_phrases": [], "used_categories": [], "phrase_hashes": []}


def save_history(history):
    """Save content history to file with cleanup"""
    # Cleanup old entries to prevent file bloat
    if len(history["used_phrases"]) > MAX_PHRASE_HISTORY:
        history["used_phrases"] = history["used_phrases"][-MAX_PHRASE_HISTORY:]
    if len(history["phrase_hashes"]) > MAX_PHRASE_HISTORY:
        history["phrase_hashes"] = history["phrase_hashes"][-MAX_PHRASE_HISTORY:]
    if len(history["used_categories"]) > MAX_CATEGORY_HISTORY:
        history["used_categories"] = history["used_categories"][-MAX_CATEGORY_HISTORY:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_phrase_hash(phrase):
    """Generate a unique hash for a phrase to detect near-duplicates"""
    # Normalize the phrase for comparison
    normalized = phrase["english"].lower().strip()
    # Remove common variations
    normalized = normalized.replace("  ", " ").replace(".", "").replace("!", "").replace("?", "")
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()


def is_phrase_duplicate(phrase, history):
    """Check if a phrase or similar phrase has been used before"""
    # Check exact match
    phrase_lower = phrase["english"].lower()
    if phrase_lower in history["used_phrases"]:
        return True

    # Check hash match (catches minor variations)
    phrase_hash = get_phrase_hash(phrase)
    if phrase_hash in history["phrase_hashes"]:
        return True

    return False


def filter_duplicate_phrases(phrases, history):
    """Filter out phrases that have been used before"""
    fresh_phrases = [p for p in phrases if not is_phrase_duplicate(p, history)]
    return fresh_phrases


def log_content_generation(category, phrases):
    """Log generated content to history"""
    history = load_history()

    # Add used phrases
    for phrase in phrases:
        phrase_lower = phrase["english"].lower()
        if phrase_lower not in history["used_phrases"]:
            history["used_phrases"].append(phrase_lower)
            history["phrase_hashes"].append(get_phrase_hash(phrase))

    # Add category with timestamp
    history["used_categories"].append({
        "category": category,
        "timestamp": datetime.now().isoformat()
    })

    save_history(history)
    print(f"[tracker] ✅ Logged {len(phrases)} phrases to history")


def suggest_fresh_category(categories, avoid_recent=5):
    """
    Suggest a category that hasn't been used recently
    Prioritizes categories not used in the last N runs
    """
    history = load_history()
    recent_categories = [c["category"] for c in history["used_categories"][-avoid_recent:]]

    # Find categories not in recent list
    available = [c for c in categories if c not in recent_categories]

    if available:
        import random
        selected = random.choice(available)
        print(f"[tracker] 📚 Selected fresh category: {selected}")
        return selected
    else:
        # All categories used recently, pick least recently used
        if history["used_categories"]:
            # Find category used longest time ago
            category_times = {}
            for cat in categories:
                uses = [c for c in history["used_categories"] if c["category"] == cat]
                if uses:
                    category_times[cat] = min(c["timestamp"] for c in uses)
                else:
                    category_times[cat] = "0000-00-00"  # Never used

            # Pick the one used longest ago
            least_recent = min(category_times, key=category_times.get)
            print(f"[tracker] 📚 All categories used recently, picking least recent: {least_recent}")
            return least_recent

        import random
        return random.choice(categories)


def print_generation_stats():
    """Print stats about generated content"""
    history = load_history()
    total_phrases = len(history.get("used_phrases", []))
    total_runs = len(history.get("used_categories", []))

    # Calculate category distribution
    category_counts = {}
    for entry in history.get("used_categories", []):
        cat = entry["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    most_used = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else "N/A"
    least_used = min(category_counts.items(), key=lambda x: x[1])[0] if category_counts else "N/A"

    print(f"📊 Content Stats:")
    print(f"   • Total phrases generated: {total_phrases}")
    print(f"   • Total runs: {total_runs}")
    print(f"   • Most used category: {most_used}")
    print(f"   • Least used category: {least_used}")
    print()


def get_recent_run_times(num_runs=5):
    """Get timestamps of recent runs to verify scheduling"""
    history = load_history()
    runs = history.get("used_categories", [])[-num_runs:]
    return [r["timestamp"] for r in runs]
