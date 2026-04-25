from django.db import models


class UploadedImage(models.Model):
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='uploads/')
    ocr_text = models.TextField(blank=True)
    annotated_image = models.ImageField(upload_to='annotated/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.description
