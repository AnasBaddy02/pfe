# Generated by Django 4.2.1 on 2023-06-10 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plearn', '0006_discussion_learner_reply_editor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='video',
            field=models.FileField(null=True, upload_to='videos/', verbose_name=''),
        ),
    ]
