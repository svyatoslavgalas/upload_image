from django.db import models
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


class Image(models.Model):
    original_image = models.ImageField('Оригинальное изображение', upload_to='gallery/', blank=True, null=True)
    image = models.ImageField('Файл', upload_to='gallery/')
    alt = models.CharField('Альтернативный текст', max_length=256, blank=True, null=True)
    url = models.URLField('Ссылка', max_length=256, blank=True, null=True)

    def __str__(self):
        if self.alt:
            return self.alt
        return str(self.image)

    def get_image_by_url(self):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(self.url).read())
        img_temp.flush()
        self.image.save(f"image_{self.pk}.jpg", File(img_temp))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.url and not self.image:
            self.get_image_by_url()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
