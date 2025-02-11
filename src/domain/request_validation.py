import re


def __is_valid_google_drive_link(url: str) -> bool:
    pattern = r'https:\/\/drive\.google\.com\/uc\?id=([a-zA-Z0-9_-]+)'

    if re.match(pattern, url):
        return True
    else:
        return False


def __is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_request(google_drive_video_link: str, alert_contact_email: str) -> tuple[str, str]:
    if not google_drive_video_link or not __is_valid_google_drive_link(google_drive_video_link):
        raise ValueError(
            "Link do Google Drive inválido ou ausente. Formato esperado: https://drive.google.com/uc?id=ID_PRESENTE_NO_LINK"
        )

    if not alert_contact_email or not __is_valid_email(alert_contact_email):
        raise ValueError('E-mail de contato inválido ou ausente')
