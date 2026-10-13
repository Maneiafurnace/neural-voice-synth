# Security Policy — neural-voice-synth

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security only |
| < 0.5   | no        |

## Threat model

`neural-voice-synth` is an offline desktop TTS engine. It reads audio
reference files and text input, runs local inference, and writes audio
out. The realistic attack surfaces are:

1. **Malicious model checkpoints.** A `.pt`/`.onnx` file can carry a
   pickled payload. We load checkpoints with `weights_only=True` where
   possible; ONNX is loaded via the onnxruntime C API, not `eval`.
2. **Malicious reference WAVs.** Header-parsing bugs in audio decoders
   are a classic RCE vector. We bounds-check chunk sizes in
   `src/ingest/wav_reader.py` and reject non-PCM payloads.
3. **Text input.** No eval, no templating of user text into shell or
   `subprocess`. Phonemizer backends are called with argv lists, never
   `shell=True`.

## Reporting a vulnerability

Open a **private** security advisory on the GitHub repo, or email the
maintainer listed in `pyproject.toml`. Include: version, OS, a minimal
repro (input file + command), and the crash/ASAN trace if you have one.
We aim to respond within 72h.

## Not in scope

- Voice cloning of public figures — this is a user-policy issue, not a
  code CVE. Report to the maintainer as a policy concern.
- "It sounds bad" — vocoder quality is a feature request, not a vuln.
- Model weight mirror downtime.

## Hardening checklist for users

- Only load checkpoints from the official release mirror or ones you
  trained yourself.
- Run the tool under a non-admin Windows account.
- Keep `config/local.toml` out of git — it may reference private voice
  references.