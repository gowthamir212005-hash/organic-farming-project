# Generated migration for SMS status fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farming', '0005_product_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sms_status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('failed', 'Failed')],
                default='pending',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='sms_error',
            field=models.TextField(blank=True, default=''),
        ),
    ]
