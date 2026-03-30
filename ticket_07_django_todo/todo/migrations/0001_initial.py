from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('completed', models.BooleanField(default=False, verbose_name='выполнено')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'задача',
                'verbose_name_plural': 'задачи',
                'ordering': ['-created_at'],
            },
        ),
    ]
