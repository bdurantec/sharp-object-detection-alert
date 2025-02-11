from dataclasses import dataclass


@dataclass
class ImageAnalysisResult:
    details: str
    object_type: str
    image_stream: bytes
