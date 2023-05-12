import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title, User

FILE_HANDLE = (  # не менять порядок
    ('category.csv', Category, {}),
    ('genre.csv', Genre, {}),
    ('users.csv', User, {}),
    ('titles.csv', Title, {'category': 'category_id'}),
    ('genre_title.csv', Title.genre.through, {}),
    ('review.csv', Review, {'author': 'author_id'}),
    ('comments.csv', Comment, {'author': 'author_id'}),
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for file_name, model, column_name in FILE_HANDLE:
            file_path = f'{settings.BASE_DIR}/static/data/{file_name}'
            with open(file_path, mode='r', encoding='utf8') as csf_file:
                reader = csv.DictReader(csf_file)
                objects = []
                for line in reader:
                    data = dict(**line)
                    if column_name:
                        for old_column, new_column in column_name.items():
                            data[new_column] = data.pop(old_column)
                    try:
                        objects.append(model(**data))
                    except TypeError:
                        self.stderr.write('Неверный заголовок в csv-файле')
                        break
                try:
                    model.objects.bulk_create(objects, ignore_conflicts=True)
                    self.stdout.write(f'{file_name} объектов {len(objects)}')
                except ValueError:
                    self.stderr.write('Ошибка заполнения csv. Импорт отменен')
                except IntegrityError as error:
                    self.stderr.write(f'{file_name} ошибка: {error}, {line}')
