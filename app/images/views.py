import os
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .models import UploadedImage
from .ocr_utils import run_ocr_and_annotate


def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, 'images/image_list.html', {'images': images})


def image_upload(request):
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        image_file = request.FILES.get('image')

        if not image_file or not description:
            return render(request, 'images/upload.html', {
                'error': 'Kérlek töltsd ki a leírást és válassz képet.'
            })

        ocr_text, annotated_bytes = run_ocr_and_annotate(image_file)

        obj = UploadedImage(description=description, ocr_text=ocr_text)
        image_file.seek(0)
        obj.image.save(image_file.name, image_file, save=False)

        base_name = os.path.splitext(image_file.name)[0]
        obj.annotated_image.save(
            f"annotated_{base_name}.png",
            ContentFile(annotated_bytes.read()),
            save=False
        )
        obj.save()
        return redirect('image_detail', pk=obj.pk)

    return render(request, 'images/upload.html')


def image_detail(request, pk):
    obj = get_object_or_404(UploadedImage, pk=pk)
    return render(request, 'images/image_detail.html', {'obj': obj})


def health(request):
    return HttpResponse('OK')
