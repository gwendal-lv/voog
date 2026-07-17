import numpy as np
from config import SAMPLE_RATE

def _poly_blep(t: np.ndarray, dt: np.ndarray) -> np.ndarray:
    """Vectorized PolyBLEP for band-limiting discontinuities."""
    res = np.zeros_like(t)
    
    # Case: 0 <= t < dt
    mask_low = t < dt
    u = t[mask_low] / dt[mask_low]
    res[mask_low] = u + u - u*u - 1.0
    
    # Case: 1 - dt < t < 1
    mask_high = t > (1.0 - dt)
    u = (t[mask_high] - 1.0) / dt[mask_high]
    res[mask_high] = u*u + u + u + 1.0
    
    return res


WAVEFORMS = ["sine", "saw", "square", "triangle"]


class Oscillator:
    def __init__(self):
        self.waveform: str = "saw"
        self.octave: int = 0          # -2..+2
        self.semitone: int = 0        # -12..+12
        self.detune: float = 0.0      # cents
        self.level: float = 1.0
        self.pulse_width: float = 0.5
        self.phase: float = 0.0       # 0..1 accumulator

    def render(self, freq: float, n_samples: int, pitch_mod: np.ndarray | None = None) -> np.ndarray:
        """Render n_samples at the given base frequency (Hz). Returns mono float64 array."""
        # Apply octave, semitone, detune
        f = freq * (2.0 ** self.octave) * (2.0 ** (self.semitone / 12.0)) * (2.0 ** (self.detune / 1200.0))
        if self.level <= 0.0:
            return np.zeros(n_samples, dtype=np.float64)

        # Phase increment per sample
        if pitch_mod is not None:
            # pitch_mod in semitones
            freqs = f * (2.0 ** (pitch_mod / 12.0))
            increments = freqs / SAMPLE_RATE
        else:
            increments = np.full(n_samples, f / SAMPLE_RATE, dtype=np.float64)

        # Build phase ramp (vectorized)
        cumulative = np.cumsum(increments)
        phases = (self.phase + cumulative - increments) % 1.0
        self.phase = float((self.phase + cumulative[-1]) % 1.0)

        # Parametric waveform generation
        if self.waveform == "sine":
            out = np.sin(2.0 * np.pi * phases)
        elif self.waveform == "saw":
            # Naive saw
            out = 2.0 * phases - 1.0
            # PolyBLEP correction for step at 0/1
            out -= _poly_blep(phases, increments)
        elif self.waveform == "square":
            pw = self.pulse_width
            # Naive square
            out = np.where(phases < pw, 1.0, -1.0)
            # PolyBLEP correction for steps at 0 and pulse_width
            out += _poly_blep(phases, increments)
            out -= _poly_blep((phases + 1.0 - pw) % 1.0, increments)
        elif self.waveform == "triangle":
            # Naive triangle (high-frequency content drops at 1/n^2, low aliasing)
            out = 2.0 * np.abs(2.0 * phases - 1.0) - 1.0
        else:
            out = np.zeros(n_samples, dtype=np.float64)

        return out * self.level

    def reset_phase(self):
        self.phase = 0.0
