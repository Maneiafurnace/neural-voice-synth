"""Entry point for the `nvs` console script.

Wires the bootstrap config into the pipeline and drains the queue.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.bootstrap import build_pipeline
from src.config.loader import load_config
from src.utils.logging import get_logger


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="nvs", description="neural-voice-synth TTS engine")
    p.add_argument("text", nargs="?", help="text to synthesize (omit for --file)")
    p.add_argument("--file", type=Path, help="read text from a UTF-8 file")
    p.add_argument("--voice", default="default", help="voice profile name from voices/")
    p.add_argument("--out", type=Path, help="output wav path (default: out/<hash>.wav)")
    p.add_argument("--config", type=Path, default=None, help="override config toml")
    p.add_argument("--device", choices=["cpu", "cuda", "dml"], help="inference device")
    p.add_argument("--stream", action="store_true", help="stream chunks to output driver")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    cfg = load_config(args.config)
    log = get_logger("nvs", cfg)

    if args.device:
        cfg.engine.device = args.device

    text = args.text
    if args.file:
        text = args.file.read_text(encoding="utf-8")
    if not text:
        log.error("no input text provided")
        return 2

    pipeline = build_pipeline(cfg)
    job = pipeline.submit(text=text, voice=args.voice, out=args.out, stream=args.stream)
    result = pipeline.run_until_complete(job)
    log.info("wrote %s (%.2fs audio, %.0fms wall)",
             result.path, result.duration_s, result.wall_ms)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())