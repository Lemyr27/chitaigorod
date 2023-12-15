from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    authors = models.ManyToManyField('Author', related_name='books', verbose_name='Авторы')
    description = models.TextField(verbose_name='Описание')
    publisher = models.ForeignKey('Publisher', related_name='books', on_delete=models.PROTECT, verbose_name='Издатель')
    year_published = models.IntegerField(verbose_name='Год публикации')
    genre = models.ForeignKey('Genre', related_name='books', on_delete=models.PROTECT, verbose_name='Жанр')
    languages = models.ManyToManyField('Language', related_name='books', verbose_name='Языки')
    isbn = models.CharField(max_length=30, verbose_name='ISBN')
    downloads_count = models.IntegerField(default=0, verbose_name='Количество скачиваний')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='ФИО автора')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    date_of_death = models.DateField(blank=True, null=True, default=None, verbose_name='Дата смерти')
    description = models.TextField(verbose_name='Биография')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Language(models.Model):
    name = models.CharField(max_length=255, verbose_name='Язык')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class Publisher(models.Model):
    name = models.CharField(max_length=255, verbose_name='Издатель')
    city = models.CharField(max_length=255, verbose_name='Город')
    date_foundation = models.DateField(verbose_name='Дата основания')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Жанр')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    favorite_books = models.ManyToManyField('Book', related_name='favorite_users', blank=True)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

