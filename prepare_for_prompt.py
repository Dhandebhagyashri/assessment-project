# prepare_for_prompt.py
# Usage: edit INPUT_VIDEO path below, then run: python3 prepare_for_prompt.py

import os
from moviepy.editor import VideoFileClip
from PIL import Image

# === EDIT: put your chosen input path here ===
INPUT_VIDEO = "input_clip.mp4"   # <-- change if needed (e.g., "/mnt/data/...")
LAST_FRAME_IMG = "last_frame.png"
CLIP_ANALYSIS = "clip_analysis.txt"
AI_PROMPT = "ai_prompt.txt"

def safe_close(clip):
    try:
        if clip.audio:
            clip.audio.close_proc()
    except Exception:
        pass
    try:
        clip.reader.close()
    except Exception:
        pass

def main():
    if not os.path.exists(INPUT_VIDEO):
        print("ERROR: input video not found at", INPUT_VIDEO)
        return

    clip = VideoFileClip(INPUT_VIDEO)
    duration = clip.duration
    fps = getattr(clip, "fps", "unknown")
    w, h = clip.w, clip.h

    print(f"Loaded video: {INPUT_VIDEO}")
    print(f"Duration: {duration:.2f}s, FPS: {fps}, Resolution: {w}x{h}")

    # save last frame (a bit before the exact end to avoid out-of-bounds)
    t = max(0, duration - 0.05)
    frame = clip.get_frame(t)
    img = Image.fromarray(frame)
    img.save(LAST_FRAME_IMG)
    print("Saved last frame to", LAST_FRAME_IMG)

    # Write clip_analysis template
    with open(CLIP_ANALYSIS, "w", encoding="utf-8") as f:
        f.write(
"""Clip Analysis (fill these 2-3 sentences):
Tone (one word):
Key visuals (who/what/where):
Exact last frame description (one sentence) - IMPORTANT continuity anchor:
Audio (music/VO/SFX):

Write your 2-3 sentence analysis below:
"""
        )
    print("Created", CLIP_ANALYSIS)

    # Write ai prompt template (fill the anchor after viewing last_frame.png)
    with open(AI_PROMPT, "w", encoding="utf-8") as f:
        f.write(
f"""AI Video Generation Prompt (8-12 seconds continuation)

Start/continuity: The original clip ends on: <PASTE the one-sentence exact last-frame description here>

High-level: Create an 8-12 second photorealistic continuation of the provided clip. Match tone and lighting of the original clip. Aspect ratio 16:9, resolution 1920x1080, 24fps.

Scene 1 (0:00–0:03): [describe shot, camera move, lighting, action]. 
Scene 2 (0:03–0:07): [describe shot, VO exact text, on-screen text & durations]. 
Scene 3 (0:07–0:0[8–12]): [packshot/logo/CTA], show QR? [yes/no]. End card hold 1.5–2s.

Style notes: Match color grade (e.g., warm highlights, muted shadows), shallow depth-of-field, natural film grain. Deliver MP4 1920x1080 24fps, 8–12s.

EXAMPLE:
Start/continuity: original ends on a close-up of a steaming mug with warm left rim light.
Scene 1: slow push-in to the mug; steam visible; soft acoustic guitar enters.
Scene 2: medium shot of same person smiling and taking a sip; VO: "Start brighter." On-screen text: "Feel the difference" (1.8s).
Scene 3: dolly out to packshot; logo + CTA "Scan to try — 50% off", QR bottom-right. End card hold 1.5s.
"""
        )
    print("Created", AI_PROMPT)

    safe_close(clip)
    print("Done. Open", LAST_FRAME_IMG, "and edit", CLIP_ANALYSIS, "and", AI_PROMPT)

if __name__ == "__main__":
    main()
