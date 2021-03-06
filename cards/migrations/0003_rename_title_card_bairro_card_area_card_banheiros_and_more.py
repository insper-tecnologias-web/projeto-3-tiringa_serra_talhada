# Generated by Django 4.0.3 on 2022-05-31 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_remove_card_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='title',
            new_name='bairro',
        ),
        migrations.AddField(
            model_name='card',
            name='area',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='banheiros',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='preco',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='quartos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='rua',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='vagas',
            field=models.IntegerField(default=0),
        ),
    ]
