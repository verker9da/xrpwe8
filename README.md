# 🇸🇦 Velocity Arabic - Automated Learning Content Generator

**Automated Arabic learning video generator for social media**

Generates educational videos with:
- ✅ AI-generated Arabic phrases with English translations
- ✅ Professional text-to-speech (Edge TTS - English + Arabic voices)
- ✅ Beautiful Islamic-inspired gradient backgrounds with text overlays
- ✅ RTL Arabic text support
- ✅ Perfect audio-video synchronization
- ✅ Velocity Arabic branding

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up API Key

Copy `.env.example` to `.env` and add your Pollinations API key:

```bash
POLLINATIONS_API_KEY=your_api_key_here
```

Get your free API key from: https://enter.pollinations.ai

### Step 3: Generate Video

```bash
python main.py
```

This will:
1. Generate 5 unique Arabic learning phrases with AI
2. Create beautiful images with Arabic text (RTL support)
3. Generate dual-language audio (English + Arabic)
4. Combine everything into a video

---

## 📁 Output

Generated files will be in:
- `output/images/` - Generated images with Arabic text
- `output/audio/` - Audio files (English + Arabic)
- `output/final_video.mp4` - Final video ready to upload

---

## 🎨 Features

### Arabic Categories (20 total)
- التحيات اليومية (Daily Greetings)
- العبارات الشائعة (Common Phrases)
- الطعام والطعام (Food & Dining)
- أساسيات السفر (Travel Essentials)
- الأرقام والوقت (Numbers & Time)
- العائلة والعلاقات (Family & Relationships)
- التسوق (Shopping)
- الاتجاهات (Directions)
- الطقس (Weather)
- العواطف والمشاعر (Emotions & Feelings)
- العمل والأعمال (Work & Business)
- الصحة والجسد (Health & Body)
- الألوان والأوصاف (Colors & Descriptions)
- الحيوانات (Animals)
- الهوايات والأنشطة (Hobbies & Activities)
- الدافع (Motivation)
- الحب (Love)
- النجاح (Success)
- الحكمة (Wisdom)
- السعادة (Happiness)

### Voice Configuration
- **English**: en-US-GuyNeural (Male)
- **Arabic**: ar-SA-HamedNeural (Male, Saudi Arabia)

### Video Specifications
- **Resolution**: 1080x1920 (9:16 vertical)
- **Format**: MP4 (H.264 + AAC)
- **Duration**: ~30-60 seconds (5 phrases)
- **Frame Rate**: 30 FPS

---

## 🎬 Video Structure

Each video contains:
1. Category title at top (English)
2. English phrase (with dark blue background)
3. Arabic translation (with brown/gold background)
4. Pronunciation guide (phonetic for English speakers)

Audio plays:
- English phrase → pause (1s) → Arabic phrase → pause (1s)

---

## 📝 Content History

All generated phrases are tracked in `content_history.json` to prevent duplicates.

---

## 🔧 Troubleshooting

### Arabic Font Issues
If Arabic text doesn't display properly:
1. Download an Arabic font (e.g., Arial, Amiri, Scheherazade)
2. Place it in the `fonts/` folder
3. Update `ARABIC_FONT_PATHS` in `generate_images.py`

### FFmpeg Not Found
Install FFmpeg:
- **Windows**: Download from https://ffmpeg.org/download.html
- **Linux**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Audio Generation Fails
Ensure you have internet connection (Edge TTS requires online access).

---

## 📄 License

Educational purposes only. Respect API terms of service.

---

**Made with ❤️ for Arabic learners worldwide**

🇸🇦 Learn Arabic with Velocity Arabic! 🇸🇦
