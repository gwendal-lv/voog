import shutil
import os
from pathlib import Path

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf

from engine.audio_engine import AudioEngine
from patch.default_patches import DEFAULT_PATCHES
from patch.patch import Patch


def main():
    # Ensure demo directories exist
    demo_dir = Path("demo")
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    os.makedirs("demo/base_osc_shapes", exist_ok=True)
    os.makedirs("demo/sequences", exist_ok=True)

    
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
    
    print(f"Synthesizing {total_duration:.2f} seconds of audio (multi-preset)...")
    audio = engine.render(events, total_duration)
    
    print(f"Multi-preset synthesis complete. Max amplitude: {np.max(np.abs(audio)):.4f}")

    sf.write("demo/sequences/audio_multi_preset.wav", audio, 44100)
    
    # Visualization
    print("Plotting multi-preset waveform envelope...")
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(audio, sr=44100, color='blue')
    plt.title("VOOG Offline Synthesis Demo - Multi-Preset Sequence")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    output_plot = "demo/sequences/audio_multi_preset_waveform.png"
    plt.savefig(output_plot)
    print(f"Waveform plot saved to {output_plot}")
    plt.close()

    # --- Generate 19 more sequences with single default presets ---
    print("\n>> Generating 19 single-preset sequences...")
    for patch_name, patch in DEFAULT_PATCHES.items():
        print(f"   Rendering sequence for patch: {patch_name}")
        seq_engine = AudioEngine()
        # Apply the patch to all channels used in the sequence
        for ch in range(3):
            seq_engine.channels[ch].set_patch(patch.copy())
        
        seq_audio = seq_engine.render(events, total_duration)
        safe_name = patch_name.lower().replace(" ", "_")
        wav_path = f"demo/sequences/{safe_name}.wav"
        sf.write(wav_path, seq_audio, 44100)

    # --- New Demos for individual waveforms ---
    # Requested: sin, square, tri, saw (3s note, at 220Hz and 1760Hz)
    wf_map = {
        "sin": "sine",
        "square": "square",
        "tri": "triangle",
        "saw": "saw"
    }
    
    sr = 44100
    test_cases = [
        {"freq": 220, "note": 57, "suffix": "_220Hz"},
        {"freq": 1760, "note": 93, "suffix": "_1760Hz"}
    ]

    for tc in test_cases:
        f0 = tc["freq"]
        midi_note = tc["note"]
        suffix = tc["suffix"]
        
        for label, engine_wf in wf_map.items():
            print(f"\n>> Generating {label} demo at {f0}Hz...")
            # Fresh engine for each waveform to avoid any channel interference
            wf_engine = AudioEngine()
            
            # Create a simple patch for this waveform
            patch = Patch(name=f"{label.capitalize()} Demo {f0}Hz")
            patch.oscillators[0].waveform = engine_wf
            patch.oscillators[0].level = 1.0
            patch.oscillators[1].level = 0.0
            patch.oscillators[2].level = 0.0
            
            wf_engine.channels[0].set_patch(patch)
            
            # 3 seconds note
            wf_events = [
                {"time": 0.0, "type": "note_on", "channel": 0, "note": midi_note, "velocity": 100},
                {"time": 3.0, "type": "note_off", "channel": 0, "note": midi_note, "velocity": 0},
            ]
            
            # Render 4 seconds to catch the release tail
            wf_audio = wf_engine.render(wf_events, 4.0)
            
            # 1. Save .wav
            wav_path = f"demo/base_osc_shapes/{label}{suffix}.wav"
            sf.write(wav_path, wf_audio, sr)
            print(f"   Saved {wav_path}")
            
            # 2. Create the 3-line analysis plot
            fig, axes = plt.subplots(3, 1, figsize=(10, 12))
            
            # Row 1: Envelope
            librosa.display.waveshow(wf_audio, sr=sr, ax=axes[0], color='blue')
            axes[0].set_title(f"{label.capitalize()} ({f0}Hz) - Waveform Envelope")
            axes[0].set_ylabel("Amplitude")
            axes[0].grid(True, alpha=0.3)
            
            # Row 2: Spectrogram
            D = librosa.amplitude_to_db(np.abs(librosa.stft(wf_audio)), ref=np.max)
            img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', ax=axes[1])
            axes[1].set_title(f"{label.capitalize()} ({f0}Hz) - Spectrogram")
            fig.colorbar(img, ax=axes[1], format="%+2.0f dB")
            
            # Row 3: Zoom on 4 periods during sustain (e.g., at t=1.5s)
            zoom_start_t = 1.5
            zoom_dur = 4 / f0
            start_idx = int(zoom_start_t * sr)
            end_idx = int((zoom_start_t + zoom_dur) * sr)
            
            zoom_data = wf_audio[start_idx:end_idx]
            t_zoom = np.linspace(zoom_start_t, zoom_start_t + zoom_dur, len(zoom_data))
            
            axes[2].plot(t_zoom, zoom_data, color='red')
            axes[2].set_title(f"{label.capitalize()} ({f0}Hz) - Zoom (4 periods during sustain)")
            axes[2].set_xlabel("Time (s)")
            axes[2].set_ylabel("Amplitude")
            axes[2].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plot_path = f"demo/base_osc_shapes/{label}{suffix}_analysis.png"
            plt.savefig(plot_path)
            plt.close(fig) # Close to free memory
            print(f"   Saved {plot_path}")

    # Optional: show it if in an interactive environment
    # plt.show()

if __name__ == "__main__":
    main()
