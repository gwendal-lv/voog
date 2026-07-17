import argparse
from engine.audio_engine import AudioEngine
from patch.default_patches import DEFAULT_PATCHES

def main():
    parser = argparse.ArgumentParser(
        prog="voog",
        description="VOOG — Virtual Moog polyphonic synthesizer (Offline)",
    )
    parser.add_argument("--patch", type=str, default="Bass Voog", help="Patch name to demo")
    parser.add_argument("--note", type=int, default=36, help="MIDI note to play")
    parser.add_argument("--duration", type=float, default=2.0, help="Duration in seconds")
    args = parser.parse_args()

    engine = AudioEngine()
    if args.patch in DEFAULT_PATCHES:
        engine.channels[0].set_patch(DEFAULT_PATCHES[args.patch].copy())
    
    events = [
        {"time": 0.0, "type": "note_on", "channel": 0, "note": args.note, "velocity": 100},
        {"time": args.duration * 0.8, "type": "note_off", "channel": 0, "note": args.note, "velocity": 0},
    ]
    
    print(f"Synthesizing {args.duration}s of {args.patch}...")
    audio = engine.render(events, args.duration)
    print(f"Synthesis complete. Result shape: {audio.shape}")
    print("Use audio_demo_minimal.py for a full demo with visualization.")

if __name__ == "__main__":
    main()
