from PIL import Image as pillow_image
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Файл')

    class Meta:
        model = Image
        fields = ('url', 'image',)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        image = cleaned_data.get('image')

        if url and image:
            raise ValidationError('Вы указали одновременно два поля, выберите что-то одно.')
        elif not url and not image:
            raise ValidationError('Пожалуйста, укажите хотя бы одно поле.')


class ResizeForm(forms.ModelForm):
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)

    class Meta:
        model = Image
        fields = ('width', 'height')

    def save(self, commit=True):
        image_obj = super().save()

        # Оставляем оргинал в Image.original_image
        if not image_obj.original_image:
            pic_copy = ContentFile(image_obj.image.read())
            new_pic = image_obj.image.name.split('/')[-1]
            image_obj.original_image.save(new_pic, pic_copy)

        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        # Новая картинка с учетом пользовательского ввода
        image_pil = pillow_image.open(image_obj.original_image)
        if not width:
            width = image_pil.size[0]
        if not height:
            height = image_pil.size[0]
        image_pil.thumbnail((width, height), pillow_image.ANTIALIAS)
        image_pil.save(image_obj.image.path)

        return image_obj
