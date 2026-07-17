import numpy as np
from config import SAMPLE_RATE, NUM_CHANNELS
from engine.channel import Channel


class AudioEngine:
    """Master audio engine: manages channels and synthesizes audio offline."""

    def __init__(self):
        self.channels = [Channel(i) for i in range(NUM_CHANNELS)]
        self._master_volume = 0.8

    def _process_midi(self, msg):
        """Route a parsed MIDI message to the appropriate channel."""
        msg_type = msg.get("type")
        ch_idx = msg.get("channel", 0)
        if ch_idx >= NUM_CHANNELS:
            ch_idx = 0
        channel = self.channels[ch_idx]

        if msg_type == "note_on":
            if msg.get("velocity", 0) > 0:
                channel.note_on(msg["note"], msg["velocity"])
            else:
                channel.note_off(msg["note"])
        elif msg_type == "note_off":
            channel.note_off(msg["note"])
        elif msg_type == "control_change":
            self._process_cc(channel, msg["control"], msg["value"])

    def _process_cc(self, channel: Channel, cc: int, value: int):
        """Map CC messages to synth parameters."""
        try:
            from midi.cc_map import CC_MAP
        except ImportError:
            return

        normalized = value / 127.0
        if cc in CC_MAP:
            param, min_val, max_val = CC_MAP[cc]
            scaled = min_val + normalized * (max_val - min_val)
            channel.set_param(param, scaled)
        elif cc == 120 or cc == 123:  # All Sound Off / All Notes Off
            channel.all_notes_off()

    def render(self, events: list[dict], duration: float) -> np.ndarray:
        """Synthesize a track from a list of events.

        events: list of dicts, each containing 'time', 'type', 'channel', etc.
        duration: total duration in seconds.
        """
        # Sort events by time
        sorted_events = sorted(events, key=lambda x: x.get("time", 0.0))

        num_samples = int(duration * SAMPLE_RATE)
        out = np.zeros(num_samples, dtype=np.float64)

        event_idx = 0
        chunk_size = 128

        for start_sample in range(0, num_samples, chunk_size):
            end_sample = min(start_sample + chunk_size, num_samples)
            current_chunk_frames = end_sample - start_sample

            chunk_end_time = end_sample / SAMPLE_RATE

            while event_idx < len(sorted_events) and sorted_events[event_idx].get("time", 0.0) < chunk_end_time:
                self._process_midi(sorted_events[event_idx])
                event_idx += 1

            # Render all channels
            chunk_out = np.zeros(current_chunk_frames, dtype=np.float64)
            for ch in self.channels:
                chunk_out += ch.render(current_chunk_frames)

            out[start_sample:end_sample] = chunk_out

        out *= self._master_volume
        out = np.tanh(out)
        return out

    @property
    def master_volume(self) -> float:
        return self._master_volume

    @master_volume.setter
    def master_volume(self, value: float):
        self._master_volume = max(0.0, min(1.0, value))
