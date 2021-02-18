from django.shortcuts import render, redirect

from .models import Image
from .forms import (ImageForm, ResizeForm)


def image_list(request):
    images = Image.objects.all()
    ctx = {
        'images': images,
    }
    return render(request, 'images/list.html', ctx)


def image_detail(request, image_id):
    image = Image.objects.get(pk=image_id)
    form = ResizeForm(request.POST or None, request.FILES or None, instance=image)
    if form.is_valid():
        form.save()
        return redirect('gallery:detail', image_id)
    ctx = {
        'image': image,
        'form': form,
    }
    return render(request, 'images/detail.html', ctx)


def image_add(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        img = form.save()
        return redirect('gallery:detail', img.pk)
    ctx = {
        'form': form,
    }
    return render(request, 'images/form.html', ctx)

