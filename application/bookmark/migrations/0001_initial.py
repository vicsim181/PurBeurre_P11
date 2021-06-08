# Generated by Django 3.2 on 2021-06-08 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('replaced_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replaced_product', to='main.product')),
                ('replacing_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replacing_product', to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bookmark_substitution',
            },
        ),
        migrations.AddConstraint(
            model_name='substitution',
            constraint=models.UniqueConstraint(fields=('replacing_product', 'replaced_product', 'user_id'), name='unique_substitution_user'),
        ),
    ]
