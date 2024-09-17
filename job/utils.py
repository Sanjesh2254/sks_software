import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from google.oauth2 import service_account
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import io

logger = logging.getLogger(__name__)

def get_drive_service():
    credentials = service_account.Credentials.from_service_account_info(settings.GOOGLE_SERVICE_ACCOUNT_INFO)
    service = build('drive', 'v3', credentials=credentials)
    return service

def upload_to_google_drive(file):
    service = get_drive_service()
    folder_id = settings.GOOGLE_DRIVE_FOLDER_ID  # Assume this is added to settings

    file_metadata = {
        'name': file.name,
        'mimeType': file.content_type,
        'parents': [folder_id]
    }

    try:
        if isinstance(file, InMemoryUploadedFile):
            media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.content_type)
        elif isinstance(file, TemporaryUploadedFile):
            media = MediaFileUpload(file.temporary_file_path(), mimetype=file.content_type)
        else:
            raise ValueError("Unsupported file type")

        logger.debug(f"Uploading file: {file_metadata['name']}")
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return uploaded_file.get('webViewLink')

    except Exception as e:
        logger.error(f"Upload error: {e}")
        return None






from django.core.mail import send_mail
from django.conf import settings

def send_interview_email(candidate_email, interview_date, interview_time):
    subject = 'Interview Invitation'
    message = f'''
    Dear Candidate,

    We are pleased to inform you that you have been shortlisted for an interview with our company.

    Interview Details:
    Date: {interview_date}
    Time: {interview_time}

    Please reply to this email to confirm your availability.

    Best regards,
    Your Company Name
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [candidate_email]

    send_mail(subject, message, from_email, recipient_list)


