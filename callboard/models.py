from django.db import models

from config import settings


class Ad(models.Model):
    """Модель объявления"""
    title = models.CharField(max_length=150, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    description = models.CharField(max_length=1000, verbose_name='Описание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-created_at',)


class Review(models.Model):
    """Модель отзыва"""
    text = models.CharField(max_length=300, verbose_name='Текст')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
