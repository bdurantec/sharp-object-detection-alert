import os

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures, ImageAnalysisResult
from azure.core.credentials import AzureKeyCredential


class AzureComputerVision:
    def __init__(self):
        endpoint = os.getenv("VISION_ENDPOINT")
        key = os.getenv("VISION_KEY")
        self.__client = ImageAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

    def analyze_image(self, image_stream: bytes) -> dict:
        try:
            result: ImageAnalysisResult = self.__client.analyze(
                image_data=image_stream,
                visual_features=[
                    VisualFeatures.CAPTION,
                    VisualFeatures.OBJECTS,
                    VisualFeatures.TAGS,
                    VisualFeatures.DENSE_CAPTIONS,
                    VisualFeatures.PEOPLE,
                    VisualFeatures.READ
                ],
                gender_neutral_caption=False,
                language='en'
            )
            return result.__dict__

        except Exception as e:
            print(f'Error analyzing image: {e}')
            raise
