from src.domain.model.email_html_content import EmailHtmlContent
from src.domain.model.image_analysis_result import ImageAnalysisResult
from src.infra.gmail_smtp import GmailSMTP


class AlertNotificationService:
    def __init__(self,
                 list_image_analysis: list[ImageAnalysisResult],
                 recipient: str,
                 frame_count: int = 0,
                 best_frames_count: int = 0
    ):
        self.__recipient = recipient
        self.__frame_count = frame_count
        self.__best_frames_count = best_frames_count
        self.__email_content = EmailHtmlContent(
            subject='Sharp Object Analysis Result',
            html_code='',
            list_image_analysis=list_image_analysis
        )
        self.__gmail_smtp = GmailSMTP(recipient)

    def send_alert(self):
        print(f'sending alert to: {self.__recipient}')
        self.__email_content.html_code = self.__generate_html_content_alert()
        self.__gmail_smtp.send_email(self.__email_content)

    def notify_result(self, link: str):
        print(f'notifying result to: {self.__recipient}')
        self.__email_content.html_code = self.__generate_html_content_notify(link)
        self.__gmail_smtp.send_email(self.__email_content)

    def notify_error(self, error_message: str, link: str):
        print(f'notifying error to: {self.__recipient}')
        self.__email_content.html_code = self.__generate_html_error(error_message, link)
        self.__gmail_smtp.send_email(self.__email_content)

    def __generate_html_content_alert(self):
        html_content = f"""
        <html>
        <head>
            <title>⚠️ SHARP OBJECT DETECTED!</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f8f8f8; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                <h2 style="color: #d32f2f;">⚠️ Sharp Object Alert ⚠️</h2>
                <p><strong>Total frames extracted from the video:</strong> {self.__frame_count}</p>
                <p><strong>Number of frames analyzed:</strong> {self.__best_frames_count}</p>
                <p><strong>Number of objects detected:</strong> {len(self.__email_content.list_image_analysis)}</p>
                <hr>
        """

        for i, _ in enumerate(self.__email_content.list_image_analysis):
            html_content += f"""
            <p><strong>Detected object:</strong> {self.__email_content.list_image_analysis[i].object_type}</p>
            <p><strong>Description:</strong> {self.__email_content.list_image_analysis[i].details}</p>
            <img src="cid:image_{i}" alt="Image {i + 1}" style="width:100%; border-radius: 5px; margin-bottom: 10px;"/>
            <hr>
            """

        html_content += """
                <p style="color: red; font-weight: bold;">⚠️ Warning: Follow the necessary safety protocols!</p>
            </div>
        </body>
        </html>
        """

        return html_content

    def __generate_html_content_notify(self, link: str):
        message = "The video has been fully analyzed, and it has been concluded that there are no references to sharp objects!"
        html_content = f"""
                <html>
                <head>
                    <title>No Sharp Object Detected!</title>
                </head>
                <body style="font-family: Arial, sans-serif; background-color: #f8f8f8; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #4caf50;">✅ No Sharp Objects Found ✅</h2>
                        <p><strong>Total frames extracted from the video:</strong> {self.__frame_count}</p>
                        <p><strong>Number of frames analyzed:</strong> {self.__best_frames_count}</p>
                        <p><strong>Result:</strong> {message}</p>
                        <p><strong>Analyzed video:</strong> {link}</p>
                        <hr>
                        <p style="color: green; font-weight: bold;">Everything is safe!</p>
                    </div>
                </body>
                </html>
                """
        return html_content

    def __generate_html_error(self, error_message: str, link: str):
        html_content = f"""
        <html>
        <head>
            <title>An Error Occurred During Video Analysis</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f8f8f8; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                <h2 style="color: #d32f2f;">❌ Video Analysis Error ❌</h2>
                <p><strong>The following error occurred during the analysis:</strong></p>
                <p style="color: #d32f2f; font-weight: bold;">{error_message}</p>
                <p><strong>Analyzed video:</strong> {link}</p>
                <hr>
                <p style="color: red; font-weight: bold;">⚠️ Please try again later or contact support.</p>
            </div>
        </body>
        </html>
        """
        return html_content
