import numpy as np

from src.domain.model.assistant_ai_analysis import AssistantAIAnalysis
from src.domain.model.image_analysis_result import ImageAnalysisResult
from src.domain.service.alert_notification_service import AlertNotificationService
from src.domain.service.sharp_object_alert_service import SharpObjectDetectionService
from src.infra.yolo_frame_selection import YoloFrameSelection


def start_execution(google_drive_video_link: str, alert_contact_email: str):
    try:
        yolo_frame_selection = YoloFrameSelection(google_drive_video_link)
        frame_count, best_frames = yolo_frame_selection.extract_better_frames_with_objects()
        sharp_object_frames = select_frames_with_sharp_object(best_frames, yolo_frame_selection)

        send_alert_if_has_sharp_object(
            sharp_object_frames=sharp_object_frames,
            frame_count=frame_count,
            alert_contact_email=alert_contact_email,
            google_drive_video_link=google_drive_video_link,
            best_frames_count=len(best_frames)
        )
    except RuntimeError as e:
        AlertNotificationService(
            list_image_analysis=[],
            recipient=alert_contact_email
        ).notify_error(e.__str__(), google_drive_video_link)
        raise


def select_frames_with_sharp_object(best_frames: list[np.ndarray], yolo_frame_selection):
    sharp_object_frames: list[ImageAnalysisResult] = []
    for frame in best_frames:
        detection_service = SharpObjectDetectionService()
        frame_as_byte: bytes = yolo_frame_selection.parse_to_byte(frame)

        result: AssistantAIAnalysis = detection_service.verify_image_sharp_object(frame_as_byte)

        if result.has_sharp_object:
            sharp_object_frames.append(
                ImageAnalysisResult(
                    object_type=result.object_type,
                    details=result.details,
                    image_stream=frame_as_byte
                )
            )

    return sharp_object_frames


def send_alert_if_has_sharp_object(
        frame_count: int,
        sharp_object_frames:
        list[ImageAnalysisResult],
        alert_contact_email: str,
        google_drive_video_link: str,
        best_frames_count: int
):
    alert_notification_service = AlertNotificationService(
        list_image_analysis=sharp_object_frames,
        recipient=alert_contact_email,
        frame_count=frame_count,
        best_frames_count=best_frames_count
    )
    if sharp_object_frames:
        alert_notification_service.send_alert()
    else:
        alert_notification_service.notify_result(google_drive_video_link)
