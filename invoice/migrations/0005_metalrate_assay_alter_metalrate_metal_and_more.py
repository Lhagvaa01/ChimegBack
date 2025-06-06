# Generated by Django 5.0.4 on 2025-04-21 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_metalrate_alter_infoproduct_tcisview'),
    ]

    operations = [
        migrations.AddField(
            model_name='metalrate',
            name='assay',
            field=models.IntegerField(default=1, help_text='Сорьц'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='metalrate',
            name='metal',
            field=models.CharField(help_text='Металын нэр', max_length=20),
        ),
        migrations.AlterField(
            model_name='metalrate',
            name='rate',
            field=models.DecimalField(decimal_places=2, help_text='1 граммын үнэ', max_digits=10),
        ),
    ]
