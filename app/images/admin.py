from django.contrib import admin
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('description', 'uploaded_at', 'ocr_text')
    readonly_fields = ('ocr_text', 'annotated_image', 'uploaded_at')
