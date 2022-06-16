from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import validate_year

CATEGORY_NAME = 'Категория'


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=16,
        choices=USER_ROLE,
        default=USER,
        db_index=True,
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='Использовать имя \'me\' в качестве username запрещено'
            )
        ]


class Category(models.Model):
    name = models.CharField(
        CATEGORY_NAME,
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        'Ключ категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = CATEGORY_NAME
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        'Ключ жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=150,
        db_index=True,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[validate_year],
    )
    category = models.ForeignKey(
        Category,
        verbose_name=CATEGORY_NAME,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите отзыв на произведение'
    )
    score = models.IntegerField(
        'Оценка',
        help_text='Поставьте оценку',
        validators=[
            MinValueValidator(1, 'От 1 до 10'),
            MaxValueValidator(10, 'От 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        'Комментарий',
        help_text='Введите коментарий на отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
