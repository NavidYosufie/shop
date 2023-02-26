# Generated by Django 4.1.3 on 2023-02-26 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_reviewsuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewsuser',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='reviewsuser',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='reviewsuser',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='reviewsuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reviewsuser',
            name='text',
            field=models.TextField(null=True),
        ),
    ]