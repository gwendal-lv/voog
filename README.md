# VOOG

**Virtual Analog Synthesizer** — a Moog-style polyphonic synthesizer engine built in Python.

This repository is designed to be a lightweight, dependency-minimal synthesizer engine that can be easily copy-pasted into other Python projects. It focuses on offline synthesis of audio from event lists.

## Features

- **3 oscillators** with sine, saw, square, and triangle waveforms
- **Moog ladder filter** (24dB/oct) with resonance and envelope modulation (Numba-accelerated)
- **Dual ADSR envelopes** for amplitude and filter
- **LFO** with 4 waveforms and 3 modulation destinations (filter, pitch, amp)
- **Glide/portamento** with off, always, and legato modes
- **Noise generator** (white/pink)
- **4 multitimbral channels**, 8-voice polyphony each
- **19 built-in presets** from deep sub basses to screaming leads

## Usage

VOOG is intended to be used as a library. You can synthesize audio by creating an `AudioEngine` and passing a list of events to the `render` method.

A track is defined as a list of dictionaries, where each dictionary represents a MIDI-like event:
```python
events = [
    {"time": 0.0, "type": "note_on", "channel": 0, "note": 60, "velocity": 100},
    {"time": 1.0, "type": "note_off", "channel": 0, "note": 60, "velocity": 0},
]
```

See `audio_demo_minimal.py` for a complete example of offline rendering and visualization.

## Architecture

- `dsp/` — Signal processing modules (oscillators, filters, envelopes, etc.)
- `engine/` — Synthesis engine and voice management
- `patch/` — Patch data structures and 19 built-in presets
- `midi/` — MIDI CC mapping for parameter modulation
- `config.py` — Global synthesis parameters (sample rate, voice count, etc.)

## Dependencies

- **NumPy** (required)
- **Numba** (optional, for faster filter processing)
- **Librosa** & **Matplotlib** (only for the demo visualization)

## License

MIT
