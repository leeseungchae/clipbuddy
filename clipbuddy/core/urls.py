from django.urls import path,include
from .views import upload_video,add_conversation

app_name = "core"
urlpatterns = [
    path("upload-video", upload_video),
    path("add_conversation", add_conversation),
]
