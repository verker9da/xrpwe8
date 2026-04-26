"""
Main Bot Script - English to Arabic Learning Content Generator
Orchestrates the entire workflow: content generation, images, audio, video
"""

import os
import sys
import random
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from generate_content import generate_learning_content, save_content_to_file, CATEGORIES
from generate_images import generate_complete_image
from generate_audio import generate_all_audio, create_final_narration
from create_video import create_complete_video
from content_tracker import suggest_fresh_category, log_content_generation, print_generation_stats

# Upload module (optional - only if upload directory exists)
UPLOAD_MODULE_AVAILABLE = False
try:
    sys.path.insert(0, str(Path(__file__).parent / 'upload'))
    from upload_all import upload_to_all_platforms, generate_video_metadata
    UPLOAD_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"[main] ⚠️ Upload module not available: {e}")

load_dotenv()

# Configuration
NUM_PHRASES = 5  # Number of phrases per video
OUTPUT_DIR = Path("output")
IMAGES_DIR = Path("output/images")
AUDIO_DIR = Path("output/audio")

# Retry configuration for robustness
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5


def ensure_directories():
    """Create necessary directories"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)
    AUDIO_DIR.mkdir(exist_ok=True)

    # Clean previous outputs
    for f in IMAGES_DIR.glob("*.jpg"):
        f.unlink()
    for f in AUDIO_DIR.glob("*.mp3"):
        f.unlink()


def main():
    """Main workflow with retry logic for robustness"""

    print("="*80)
    print("🇸🇦 ARABIC LEARNING BOT - AUTOMATED CONTENT GENERATOR 🇸🇦")
    print("="*80)
    print()

    # Check API key
    if not os.getenv("POLLINATIONS_API_KEY"):
        print("❌ ERROR: POLLINATIONS_API_KEY not set in .env file!")
        print("Get your API key from: https://enter.pollinations.ai")
        sys.exit(1)

    # Check AI model
    ai_model = os.getenv("AI_MODEL")
    if not ai_model:
        print("❌ ERROR: AI_MODEL not set in .env file!")
        print("Set AI_MODEL=<model_name> in your .env file (e.g., openai, mistral, gemini)")
        sys.exit(1)

    print(f"🤖 AI Model: {ai_model}")
    print()

    for attempt in range(MAX_RETRIES):
        try:
            # Step 1: Choose fresh category (avoid recent repeats)
            category = suggest_fresh_category(CATEGORIES, avoid_recent=5)
            print(f"📚 Selected Category: {category}")
            print()

            # Step 2: Generate learning content with AI
            print("🤖 STEP 1: Generating learning content with AI...")
            print("-" * 80)

            phrases = generate_learning_content(category, NUM_PHRASES)

            # Save content
            content_file = OUTPUT_DIR / "content.json"
            save_content_to_file(phrases, category, str(content_file))

            # Log to tracker
            log_content_generation(category, phrases)

            print()
            print("📝 Generated Phrases:")
            for i, phrase in enumerate(phrases, 1):
                print(f"\n{i}. {phrase['english']}")
                print(f"   → {phrase['arabic']}")
                print(f"   🔊 [{phrase['pronunciation']}]")

            print()
            print("="*80)

            # Step 3: Generate images
            print("🎨 STEP 2: Generating stunning images...")
            print("-" * 80)

            image_files = []
            for i, phrase in enumerate(phrases):
                # Add category to phrase data for image generation
                phrase_with_category = {**phrase, "category": category}

                output_path = IMAGES_DIR / f"phrase_{i:02d}.jpg"
                generate_complete_image(phrase_with_category, str(output_path))
                image_files.append(str(output_path))
                print()

            print(f"✅ Generated {len(image_files)} beautiful images!")
            print()
            print("="*80)

            # Step 4: Generate audio (dual-language TTS)
            print("🎙️ STEP 3: Generating dual-language audio...")
            print("-" * 80)

            audio_files = generate_all_audio(phrases, str(AUDIO_DIR))

            # Create final narration
            final_audio = OUTPUT_DIR / "narration.mp3"
            create_final_narration(audio_files, str(final_audio))

            print()
            print("="*80)

            # Step 5: Create video
            print("🎬 STEP 4: Creating video...")
            print("-" * 80)

            final_video = OUTPUT_DIR / "final_video.mp4"
            create_complete_video(
                phrases,
                str(IMAGES_DIR),
                str(final_audio),
                str(final_video),
                audio_files
            )

            print()
            print("="*80)
            print("✅ WORKFLOW COMPLETE!")
            print("="*80)
            print()

            # Print stats
            print_generation_stats()

            print(f"📁 Video saved: {final_video}")
            print(f"📊 Category: {category}")
            print(f"📝 Phrases: {NUM_PHRASES}")
            print()

            # Step 5: Upload to social media (if enabled)
            if UPLOAD_MODULE_AVAILABLE:
                print("="*80)
                print("🚀 STEP 5: Uploading to social media platforms...")
                print("-"*80)

                try:
                    # Load content for metadata
                    import json
                    content_file_path = OUTPUT_DIR / "content.json"
                    with open(content_file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)

                    # Category translation mapping
                    category_map = {
                        'التحيات اليومية': 'Daily Greetings',
                        'العبارات الشائعة': 'Common Phrases',
                        'الطعام والطعام': 'Food & Dining',
                        'أساسيات السفر': 'Travel Essentials',
                        'الأرقام والوقت': 'Numbers & Time',
                        'العائلة والعلاقات': 'Family & Relationships',
                        'التسوق': 'Shopping',
                        'الاتجاهات': 'Directions',
                        'الطقس': 'Weather',
                        'العواطف والمشاعر': 'Emotions & Feelings',
                        'العمل والأعمال': 'Work & Business',
                        'الصحة والجسد': 'Health & Body',
                        'الألوان والأوصاف': 'Colors & Descriptions',
                        'الحيوانات': 'Animals',
                        'الهوايات والأنشطة': 'Hobbies & Activities',
                        'الدافع': 'Motivation',
                        'الحب': 'Love',
                        'النجاح': 'Success',
                        'الحكمة': 'Wisdom',
                        'السعادة': 'Happiness',
                    }

                    category_english = category_map.get(category, category)
                    metadata = generate_video_metadata(
                        category_english=category_english,
                        category_arabic=category,
                        phrases=phrases
                    )

                    # Upload to all configured platforms
                    upload_results = upload_to_all_platforms(
                        video_path=str(final_video),
                        metadata=metadata
                    )

                    # Count successes
                    success_count = sum(1 for r in upload_results.values() if r.get('status') == 'success')
                    if success_count > 0:
                        print(f"✅ Uploaded to {success_count} platform(s)!")
                    else:
                        print("⚠️ No platforms configured. Add credentials to .env to enable uploads.")

                except Exception as e:
                    print(f"⚠️ Upload step failed: {e}")
                    print("Continuing anyway (video was generated successfully)")
            else:
                print("⚠️ Upload module not available - skipping social media upload")
                print("   Install upload dependencies: pip install -r upload/requirements.txt")

            print()
            print("="*80)
            print("✅ ALL DONE!")
            print("="*80)
            print()

            return True

        except Exception as e:
            print()
            print("="*80)
            print(f"❌ ERROR (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            print("="*80)
            import traceback
            traceback.print_exc()
            print()

            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retrying in {RETRY_DELAY_SECONDS} seconds...")
                import time
                time.sleep(RETRY_DELAY_SECONDS)
                print()
            else:
                print("❌ All retry attempts failed. Please check logs and try again.")
                return False

    return False


if __name__ == "__main__":
    ensure_directories()
    success = main()
    sys.exit(0 if success else 1)
