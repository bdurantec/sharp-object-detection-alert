import os

from dotenv import load_dotenv

from src.application.main import start_execution
from src.domain.request_validation import is_valid_request

load_dotenv()


def sharp_object_analysis():
    try:
        google_drive_video_link = os.getenv('GOOGLE_DRIVE_VIDEO_LINK')
        alert_contact_email = os.getenv('ALERT_CONTACT_EMAIL')

        is_valid_request(google_drive_video_link, alert_contact_email)
        start_execution(google_drive_video_link, alert_contact_email)

    except ValueError as e:
        print(f"Validation error: {e}")
        raise
    except KeyError as e:
        print(f"Missing environment variable: {e}")
        raise

    except Exception as e:
        print("An unexpected error occurred")
        raise


if __name__ == "__main__":
    sharp_object_analysis()
