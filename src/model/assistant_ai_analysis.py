from dataclasses import dataclass


@dataclass
class AssistantAIAnalysis:
    has_sharp_object: bool
    details: str = 'sharp object not found'
    object_type: str = 'not_found'
