import json
import os

from openai import OpenAI

from src.domain.model.assistant_ai_analysis import AssistantAIAnalysis


class OpenAIAssistant:
    def __init__(self):
        self.__client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        self.__assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
        self.__thread = self.__client.beta.threads.create()

    def interpret_image_processing(self, text: str) -> AssistantAIAnalysis:
        try:
            self.__client.beta.threads.messages.create(
                thread_id=self.__thread.id,
                role='user',
                content=text
            )

            run = self.__client.beta.threads.runs.create_and_poll(
                thread_id=self.__thread.id,
                assistant_id=self.__assistant_id
            )

            if run.status == 'completed':
                messages = self.__client.beta.threads.messages.list(
                    thread_id=self.__thread.id
                )
                text = messages.data[0].content[0].text.value
                json_data = json.loads(text.strip())

                return AssistantAIAnalysis(
                    details=json_data['details'],
                    has_sharp_object=json_data['has_sharp_object'],
                    object_type=json_data['object_type']
                )
        except Exception:
            raise
