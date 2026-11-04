# Generated migration to remove SMS status fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farming', '0006_order_sms_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sms_status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='sms_error',
        ),
    ]
