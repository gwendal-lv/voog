# VOOG

**Virtual Analog Synthesizer** — a Moog-style polyphonic synthesizer engine built in Python.
Forked from https://github.com/gpasquero/voog.

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

## Preset structure

A VOOG preset (or "patch") is defined as a hierarchical dictionary. It consists of **41 parameters** in total. Below is the structure of a preset:

```
{
  "name": <string>,             // Name of the preset
  "master_volume": <float>,     // Global volume level [0.0 to 1.0]
  "oscillators": [              // List of 3 oscillators
    {
      "waveform": <string>,     // "sine", "saw", "square", or "triangle"
      "octave": <int>,          // Octave offset [-2 to +2]
      "semitone": <int>,        // Semitone offset [-12 to +12]
      "detune": <float>,        // Fine tuning in cents [-100.0 to 100.0]
      "level": <float>,         // Individual volume [0.0 to 1.0]
      "pulse_width": <float>    // Pulse width for square wave [0.0 to 1.0]
    }
  ],
  "noise": {                    // Noise generator
    "noise_type": <string>,     // "white" or "pink"
    "level": <float>            // Noise volume level [0.0 to 1.0]
  },
  "filter": {
    "cutoff": <float>,          // Filter cutoff frequency in Hz [20.0 to 20000.0]
    "resonance": <float>,       // Resonance level [0.0 to 1.0]
    "env_amount": <float>,      // Filter envelope modulation depth in semitones [0.0 to 48.0]
    "key_tracking": <float>     // Cutoff tracking of note pitch [0.0 to 1.0]
  },
  "filter_adsr": {              // Filter envelope
    "attack": <float>,          // Attack time in seconds [min 0.001]
    "decay": <float>,           // Decay time in seconds [min 0.001]
    "sustain": <float>,         // Sustain level [0.0 to 1.0]
    "release": <float>          // Release time in seconds [min 0.001]
  },
  "amp_adsr": {                 // Amplitude envelope
    "attack": <float>,          // Attack time in seconds [min 0.001]
    "decay": <float>,           // Decay time in seconds [min 0.001]
    "sustain": <float>,         // Sustain level [0.0 to 1.0]
    "release": <float>          // Release time in seconds [min 0.001]
  },
  "lfo": {
    "waveform": <string>,       // LFO shape: "sine", "triangle", "saw", or "square"
    "rate": <float>,            // Modulation rate in Hz [0.1 to 20.0]
    "depth": <float>,           // Modulation intensity [0.0 to 1.0]
    "destination": <string>,    // LFO target: "filter", "pitch", or "amp"
    "key_sync": <bool>          // If true, LFO phase resets on every new note
  },
  "glide": {
    "time": <float>,            // Portamento duration in seconds [0.0 to 2.0]
    "mode": <string>            // Glide mode: "off", "always", or "legato"
  }
}
```

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

