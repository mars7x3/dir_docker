from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    slug = models.SlugField(primary_key=True, verbose_name='Слаг')
    parent = models.ForeignKey('self',
                               on_delete=models.DO_NOTHING,
                               related_name='children',
                               blank=True, null=True,
                               verbose_name='Родительская категория')

    def __str__(self):
        if self.parent:
            return f'{self.parent} | {self.name}'
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Resume(models.Model):
    STATUS_RESUME = (
        ('Надо сделать', 'Надо сделать'),
        ('Могу сделать', 'Могу сделать'),
    )
    status = models.CharField(choices=STATUS_RESUME,
                              max_length=30,
                              default='Активна',
                              verbose_name='Статус')

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='user',
                                verbose_name='Пользователь',)
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=100, verbose_name="Телефон")
    title = models.CharField(max_length=300, verbose_name="Название")
    category = models.ForeignKey(Category,
                                 on_delete=models.DO_NOTHING,
                                 related_name='resume',
                                 verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена")
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания')

    image = models.ImageField(upload_to='products',
                              verbose_name='Изображение',
                              default='products/def_image.png')
    address = models.CharField(max_length=300, verbose_name="Адрес")

    def get_absolut_url(self):
        from django.urls import reverse
        return reverse('resume', kwargs={'resume_id': self.id})


class Review(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='resumes')
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                 related_name='author',
                                 verbose_name='Пользователь',
                                 blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING,
                               related_name='replies',
                               blank=True, null=True)



