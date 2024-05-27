from django.urls import path,include
from .views import upload_video,add_conversation

app_name = "core"
urlpatterns = [
    path("upload-video", upload_video),
    path("random-answer", add_conversation, name='add_conversation'),
]
