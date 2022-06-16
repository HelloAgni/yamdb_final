import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

Models = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def handle(self, *args, **options):
        answer = input('Очистить базу перед импортом? [Y/N]: ')
        yes = ['Y', 'y']
        no = ['N', 'n']
        if answer in yes:
            for model, csv_files in Models.items():
                model.objects.all().delete()
        elif answer in no:
            return ('Лучше воспользоваться admin панелью')
        elif answer not in yes or no:
            return ('Incorrect answer')

        for model, csv_files in Models.items():
            with open(
                f'{settings.STATIC_ROOT}/data/{csv_files}',
                # f'{settings.STATICFILES_DIRS[0]}/data/{csv_files}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader
                )
            self.stdout.write(
                f'Данные для таблицы {model.__name__} успешно загружены')
        return('База данных успешно загружена.')
