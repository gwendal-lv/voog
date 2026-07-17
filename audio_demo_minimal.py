import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf

from engine.audio_engine import AudioEngine
from patch.default_patches import DEFAULT_PATCHES

def main():
    engine = AudioEngine()

    # Load patches for different channels as in test_audio.py
    engine.channels[0].set_patch(DEFAULT_PATCHES["Bass Voog"].copy())
    engine.channels[1].set_patch(DEFAULT_PATCHES["Lead Saw"].copy())
    engine.channels[2].set_patch(DEFAULT_PATCHES["Pad Strings"].copy())

    events = []
    t = 0.3 # Initial offset

    # --- Bass line (replicating test_audio.py logic) ---
    print(">> Preparing Bass Moog events...")
    for note in [40, 40, 43, 45, 40, 40, 47, 45]:
        events.append({"time": t, "type": "note_on", "channel": 0, "note": note, "velocity": 100})
        t += 0.3
        events.append({"time": t, "type": "note_off", "channel": 0, "note": note, "velocity": 0})
        t += 0.05
    
    t += 0.3
    
    # --- Lead melody (replicating test_audio.py logic) ---
    print(">> Preparing Lead Saw events...")
    melody = [(60, 0.4), (64, 0.4), (67, 0.4), (72, 0.8),
              (71, 0.2), (67, 0.2), (64, 0.4), (60, 0.8)]
    for note, dur in melody:
        events.append({"time": t, "type": "note_on", "channel": 1, "note": note, "velocity": 90})
        t += dur
        events.append({"time": t, "type": "note_off", "channel": 1, "note": note, "velocity": 0})
        t += 0.05

    t += 0.3
    
    # --- Pad chord (replicating test_audio.py logic) ---
    print(">> Preparing Pad Strings chord events...")
    chord = [60, 64, 67, 72]
    for n in chord:
        events.append({"time": t, "type": "note_on", "channel": 2, "note": n, "velocity": 80})
    t += 3.0
    for n in chord:
        events.append({"time": t, "type": "note_off", "channel": 2, "note": n, "velocity": 0})
    
    # Final tail
    total_duration = t + 2.0
    
    print(f"Synthesizing {total_duration:.2f} seconds of audio...")
    audio = engine.render(events, total_duration)
    
    print(f"Synthesis complete. Max amplitude: {np.max(np.abs(audio)):.4f}")

    sf.write("demo/audio_demo.wav", audio, 44100)
    
    # Visualization
    print("Plotting waveform envelope...")
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(audio, sr=44100, color='blue')
    plt.title("VOOG Offline Synthesis Demo - Waveform Envelope")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot or show it
    output_plot = "demo/audio_demo_waveform.png"
    plt.savefig(output_plot)
    print(f"Waveform plot saved to {output_plot}")
    
    # Optional: show it if in an interactive environment
    # plt.show()

if __name__ == "__main__":
    main()
