from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Image
from .forms import ResizeForm


class ImageTestCase(TestCase):
    def setUp(self):
        test_image = SimpleUploadedFile(name='3.jpg',
                                        content=open('3.jpg', 'rb').read(),
                                        content_type='image/jpeg')
        Image.objects.create(image=test_image, alt='Изображение девушки')
        Image.objects.create(url='https://i.ytimg.com/vi/Cp4Rxh1ZqzA/sddefault.jpg', alt='Нуар')

    def test_created_images(self):
        """Проверка создания изображений по пути проекта и ссылке из интернета"""
        image_woman = Image.objects.get(alt='Изображение девушки')
        image_noire = Image.objects.get(alt='Нуар')
        self.assertEqual(image_woman.alt, 'Изображение девушки')
        self.assertEqual(image_noire.alt, 'Нуар')

    def test_resize_form(self):
        """Проверка данных в форме изменения изображения"""
        data = {'width': 100, 'height': 100}
        form = ResizeForm(data=data)
        self.assertTrue(form.is_valid())
