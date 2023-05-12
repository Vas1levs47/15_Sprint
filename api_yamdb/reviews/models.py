import datetime as dt
import time
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models import Avg

from users.models import User

FIRST_MOVIE = 1895
RETRY_PERIOD = 86400
SCHET = []

def CheckValid():
    result = dt.datetime.now().year
    while True:
        if len(SCHET) <1:
            SCHET.append('1')
            #print(len(SCHET))
            return result
        else:
            result = dt.datetime.now().year
            time.sleep(RETRY_PERIOD)
            return result

SLUGVALIDATORSET = RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')


class BaseCategoryTitle(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True,)  # validators=[SLUGVALIDATORSET]

#    class Meta:
#        ordering = ('pk',)


class Category(BaseCategoryTitle):
    #name = models.CharField(max_length=256)
    #slug = models.SlugField(max_length=50, unique=True,)  # validators=[SLUGVALIDATORSET]

    
    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(BaseCategoryTitle):
    #name = models.CharField(max_length=256)
    #slug = models.SlugField(max_length=50, unique=True,)  # validators=[SLUGVALIDATORSET]

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(FIRST_MOVIE),
                    MaxValueValidator(CheckValid())])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre,)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='titles')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        avg_score = self.reviews.aggregate(rating=Avg('score'))
        return avg_score['rating']


"""class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'),
        ]"""


class BaseRevCom(models.Model):
    #text = models.TextField()
    #pub_date = models.DateTimeField(auto_now_add=True)
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title'),
        ]

    def __str__(self):
        return f'{self.title} {self.score}'


class Comment(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.review} {self.author}'
