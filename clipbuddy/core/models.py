from django.db import models
from django.utils import timezone
from datetime import timedelta
class UploadSession(models.Model):
    user_id = models.CharField(max_length=255, unique=True)  # 사용자 ID를 저장하는 필드
    upload_status = models.CharField(max_length=50, default='incomplete')  # 업로드 상태를 저장하는 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 레코드가 생성된 시간
 
    def __str__(self):
        return f"UploadSession(user_id={self.user_id}, status={self.upload_status})"
    
class Conversation(models.Model):
    session = models.ForeignKey(UploadSession, on_delete=models.CASCADE, related_name='conversations')
    message = models.TextField()  # 대화 내용을 저장하는 필드
    timestamp = models.DateTimeField(auto_now_add=True)  # 대화가 기록된 시간

    def __str__(self):
        return f'Conversation(session_id={self.session_id}, message="{self.message[:20]}...", timestamp={self.timestamp})'
