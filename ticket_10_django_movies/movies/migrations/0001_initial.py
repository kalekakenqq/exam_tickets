from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название')),
                ('director', models.CharField(max_length=100, verbose_name='режиссёр')),
                ('year', models.IntegerField(verbose_name='год')),
                ('rating', models.FloatField(verbose_name='рейтинг')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'фильм',
                'verbose_name_plural': 'фильмы',
                'ordering': ['-rating'],
            },
        ),
    ]
