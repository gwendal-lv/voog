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

A VOOG preset (or "patch") is defined as a hierarchical dictionary. It consists of **41 parameters** in total. Below are the parameters available for customization:

### Global (2 parameters)
- `name`: **Patch Name** — The display name of the preset.
- `master_volume`: **Master Volume** — Global output volume level (0.0 to 1.0).

### Oscillators (18 parameters)
A list containing 3 oscillator configurations (6 parameters each).
- `waveform`: **Waveform** — Shape of the oscillator: `sine`, `saw`, `square`, or `triangle`.
- `octave`: **Octave** — Transposition in octaves (-2 to +2).
- `semitone`: **Semitone** — Transposition in semitones (-12 to +12).
- `detune`: **Detune** — Fine tuning in cents.
- `level`: **Oscillator Level** — Individual volume of the oscillator (0.0 to 1.0).
- `pulse_width`: **Pulse Width** — Duty cycle of the square wave (0.0 to 1.0).

### Noise (2 parameters)
- `noise_type`: **Noise Type** — Color of the noise generator: `white` or `pink`.
- `level`: **Noise Level** — Volume of the noise generator (0.0 to 1.0).

### Filter (4 parameters)
- `cutoff`: **Cutoff Frequency** — Filter cutoff frequency in Hertz (Hz).
- `resonance`: **Resonance** — Filter resonance or regeneration (0.0 to 1.0).
- `env_amount`: **Envelope Amount** — Filter envelope modulation depth (in semitones).
- `key_tracking`: **Keyboard Tracking** — How much the cutoff follows the note pitch (0.0 to 1.0).

### Envelopes (8 parameters)
Two standard ADSR envelopes (4 parameters each) for the filter (`filter_adsr`) and amplitude (`amp_adsr`).
- `attack`: **Attack Time** — Time to reach peak level (seconds).
- `decay`: **Decay Time** — Time to drop to sustain level (seconds).
- `sustain`: **Sustain Level** — Constant level while note is held (0.0 to 1.0).
- `release`: **Release Time** — Time to fade out after note release (seconds).

### LFO (5 parameters)
- `waveform`: **LFO Waveform** — Shape of the LFO: `sine`, `saw`, `square`, or `triangle`.
- `rate`: **LFO Rate** — Frequency of modulation in Hertz (Hz).
- `depth`: **Modulation Depth** — Intensity of the modulation effect (0.0 to 1.0).
- `destination`: **Modulation Destination** — Target of the LFO: `filter`, `pitch`, or `amp`.
- `key_sync`: **Key Sync** — If enabled, LFO phase resets on every new note (boolean).

### Glide (2 parameters)
- `time`: **Glide Time** — Portamento duration in seconds.
- `mode`: **Glide Mode** — Transition mode: `off`, `always`, or `legato`.

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

