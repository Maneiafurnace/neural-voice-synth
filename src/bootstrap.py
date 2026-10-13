"""Composition root: assemble ingest -> processors -> output driver.

The pipeline is a bounded producer/consumer graph. Handlers push jobs
onto an ingress queue; processors are workers that transform a job;
the output driver is the terminal sink. See `src/pipeline/` for the
generic machinery.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.config.schema import EngineConfig
from src.handlers.text_ingest import TextIngestHandler
from src.handlers.voice_picker import VoicePickerHandler
from src.models.acoustic_loader import AcousticModel
from src.models.vocoder_loader import VocoderModel
from src.pipeline.executor import PipelineExecutor
from src.pipeline.queue import BoundedJobQueue
from src.processors.phoneme import PhonemeProcessor
from src.processors.acoustic import AcousticProcessor
from src.processors.vocoder import VocoderProcessor
from src.processors.postprocess import PostProcessProcessor
from src.drivers.file_driver import FileOutputDriver
from src.drivers.wasapi_driver import WasapiOutputDriver


@dataclass(slots=True)
class Pipeline:
    executor: PipelineExecutor

    def submit(self, *, text: str, voice: str, out, stream: bool):
        return self.executor.submit(text=text, voice=voice, out=out, stream=stream)

    def run_until_complete(self, job):
        return self.executor.run_until_complete(job)


def build_pipeline(cfg: EngineConfig) -> Pipeline:
    queue = BoundedJobQueue(maxsize=cfg.engine.queue_depth)

    handlers = [
        TextIngestHandler(cfg),
        VoicePickerHandler(cfg),
    ]
    acoustic = AcousticModel(cfg.model.acoustic, device=cfg.engine.device)
    vocoder = VocoderModel(cfg.model.vocoder, device=cfg.engine.device)

    processors = [
        PhonemeProcessor(cfg),
        AcousticProcessor(cfg, acoustic),
        VocoderProcessor(cfg, vocoder),
        PostProcessProcessor(cfg),
    ]

    driver = (
        WasapiOutputDriver(cfg) if cfg.output.driver == "wasapi" else FileOutputDriver(cfg)
    )

    executor = PipelineExecutor(
        queue=queue,
        handlers=handlers,
        processors=processors,
        driver=driver,
        num_workers=cfg.engine.num_workers,
    )
    return Pipeline(executor=executor)