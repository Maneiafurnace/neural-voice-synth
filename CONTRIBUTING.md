# Contributing to neural-voice-synth

Thanks for wanting to push the tater forward. This is a hobbyist/educational
open-source TTS engine. Treat it like any other pipeline repo — small,
reviewable PRs, tests that pass, no drive-by rewrites of the vocoder.

## Dev setup

```bash
git clone https://github.com/<you>/neural-voice-synth
cd neural-voice-synth
python -m venv .venv
. .venv/Scripts/activate   # Windows
pip install -e ".[dev]"
python -m pytest tests/ -q
```

Model checkpoints are **not** committed. The ingest service pulls them
from the release mirror on first run, or you drop them into
`models/checkpoints/` yourself.

## What we're looking for

- New phonemizer backends (espeak-ng, gruut, custom G2P rules).
- New output drivers (WASAPI exclusive, ASIO, virtual-mic loopback).
- Vocoder quality work: HiFi-GAN variants, BigVGAN, diffusion post-net.
- Streaming/chunked synthesis for low-latency pipelines.
- Windows packaging (PyInstaller onefile, MSIX, winget manifest).

## What we're not looking for

- Anything that phones home. This tool runs offline by default.
- Bundled voice cloning of public figures. Reference voices are
  user-supplied; see `SECURITY.md`.
- Refactors that swap the pipeline executor without a benchmark.

## PR checklist

- [ ] `python -m pytest tests/ -q` green
- [ ] `python -m ruff check src/` clean
- [ ] New handler/processor has a docstring with input/output contract
- [ ] No new hard dependency unless it's in `pyproject.toml` extras
- [ ] If you touch the vocoder, attach a sample WAV in the PR description

## Commit style

`area: short imperative` — e.g. `ingest: add chunked wav reader`,
`vocoder: fix mel filterbank edge at 8kHz`, `drivers: WASAPI exclusive`.

## Code of conduct

Be normal. Roast the code, not the person.