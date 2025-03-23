from django.urls import path
from .views import UploadGrafoView

urlpatterns = [
    path('upload/', UploadGrafoView.as_view(), name='upload_grafo'),  # Remova o 'api/' daqui
]
