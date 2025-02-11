from dataclasses import dataclass, field

from src.domain.model.image_analysis_result import ImageAnalysisResult


@dataclass
class EmailHtmlContent:
    subject: str
    html_code: str
    list_image_analysis: list[ImageAnalysisResult] = field(default_factory=list)
