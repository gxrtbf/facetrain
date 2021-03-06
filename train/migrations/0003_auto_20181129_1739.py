# Generated by Django 2.1.3 on 2018-11-29 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('train', '0002_auto_20181119_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageVertor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vecjson', models.TextField(blank=True, null=True, verbose_name='json')),
                ('vectype', models.CharField(max_length=20, verbose_name='function')),
                ('veccode', models.CharField(max_length=20, verbose_name='code')),
                ('createDateTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'imagevertor',
                'ordering': ('createDateTime',),
            },
        ),
        migrations.AddField(
            model_name='uploadrecord',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagevertor',
            name='uuid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train.UploadRecord'),
        ),
    ]
