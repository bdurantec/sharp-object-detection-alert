from src.domain.model.assistant_ai_analysis import AssistantAIAnalysis
from src.infra.azure_computer_vision import AzureComputerVision
from src.infra.open_ai_assistant import OpenAIAssistant


class SharpObjectDetectionService:
    def __init__(self):
        self.__computer_vision_client = AzureComputerVision()
        self.__open_ai_client = OpenAIAssistant()

    def verify_image_sharp_object(self, frame: bytes) -> AssistantAIAnalysis:
        image_processing_result: dict = self.__computer_vision_client.analyze_image(
            image_stream=frame
        )

        analysis_result: AssistantAIAnalysis = self.__open_ai_client.interpret_image_processing(
            text=image_processing_result.__str__()
        )

        return analysis_result
