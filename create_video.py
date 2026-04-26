"""
Video Creator for Arabic Learning Content
Creates engaging videos with images, audio, and subtitles
"""

import os
import json
import subprocess
from pathlib import Path

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30


def get_audio_duration(audio_file: str) -> float:
    """Get audio duration in seconds"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 2.0


def create_video_from_images_and_audio(
    image_files: list,
    audio_files: list,
    output_file: str
):
    """
    Create video from images and audio
    Each image displays for the duration of its corresponding audio
    """

    print(f"[video] Creating video from {len(image_files)} images...")

    temp_clips = []

    for i, img_path in enumerate(image_files):
        audio_info = audio_files[i]
        duration = audio_info['duration']
        print(f"  Image {i+1}/{len(image_files)}: {duration:.2f}s")

        temp_clip = Path(output_file).parent / f"temp_clip_{i:02d}.mp4"
        temp_clips.append(temp_clip)

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={FPS}",
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            str(temp_clip)
        ]

        subprocess.run(cmd, check=True, capture_output=True)

    # Concatenate clips
    print("[video] Concatenating clips...")
    temp_video = Path(output_file).parent / "temp_video.mp4"
    concat_file = Path(output_file).parent / "concat_list.txt"

    with open(concat_file, "w", encoding="utf-8") as f:
        for clip in temp_clips:
            path_str = str(clip.resolve()).replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{path_str}'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy", str(temp_video)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    # Combine all audio files using ffmpeg
    print("[video] Combining audio files...")
    audio_concat_file = Path(output_file).parent / "audio_list.txt"
    with open(audio_concat_file, "w", encoding="utf-8") as f:
        for audio_info in audio_files:
            combined_path = Path(audio_info["combined"]).resolve()
            if combined_path.exists():
                path_str = str(combined_path).replace("\\", "/").replace("'", "'\\''")
                f.write(f"file '{path_str}'\n")

    combined_audio = Path(output_file).parent / "combined_audio.mp3"
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(audio_concat_file), "-c:a", "copy", str(combined_audio)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"[video] Warning: Audio concat failed, using alternative method...")
        # Alternative: use filter_complex to concatenate
        input_args = []
        filter_parts = []
        for audio_info in audio_files:
            input_args.extend(["-i", str(audio_info["combined"])])
            filter_parts.append(f"[{len(input_args)//2-1}:a]")
        
        filter_complex = "".join(filter_parts) + f"concat=n={len(audio_files)}:v=0:a=1[outa]"
        
        cmd = [
            "ffmpeg", "-y"] + input_args + [
            "-filter_complex", filter_complex,
            "-map", "[outa]", "-c:a", "aac", str(combined_audio)
        ]
        subprocess.run(cmd, capture_output=True, check=True)

    # Add audio to video
    print("[video] Adding audio to video...")
    audio_duration = get_audio_duration(str(combined_audio))
    print(f"[video] Audio duration: {audio_duration:.2f}s")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(combined_audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    # Verify
    video_duration = get_audio_duration(str(output_file))
    print(f"[video] ✓ Video created: {Path(output_file).name} ({video_duration:.2f}s)")

    # Cleanup
    for clip in temp_clips:
        if clip.exists():
            clip.unlink()
    if temp_video.exists():
        temp_video.unlink()
    if concat_file.exists():
        concat_file.unlink()
    if audio_concat_file.exists():
        audio_concat_file.unlink()
    if combined_audio.exists():
        combined_audio.unlink()


def create_complete_video(
    phrases: list,
    images_dir: str,
    audio_file: str,
    output_file: str,
    audio_files: list
):
    """
    Create complete video from phrases, images, and audio
    """
    image_files = sorted([str(p) for p in Path(images_dir).glob("phrase_*.jpg")])
    
    if len(image_files) != len(audio_files):
        print(f"[video] ⚠️ Warning: {len(image_files)} images, {len(audio_files)} audio files")
    
    create_video_from_images_and_audio(image_files, audio_files, output_file)
    
    return output_file


if __name__ == "__main__":
    print("Video creator module - run main.py to generate videos")
