from django.db import models


class Categories(models.Model):
    '''Категории (типы) произведений'''
    name = models.CharField(max_length=256, verbose_name='Hазвание категории')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='slug категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    '''Категории жанров'''
    name = models.CharField(max_length=256, verbose_name='Hазвание жанра')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='slug жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    '''Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка)'''
    name = models.CharField(max_length=256,
                            verbose_name='Hазвание прозведения')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genres, related_name='titles',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
