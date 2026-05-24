import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.IntegerField(default=0)),
                ('car_name', models.CharField(default='', max_length=30)),
                ('car_desc', models.CharField(default='', max_length=300)),
                ('price', models.IntegerField(default=0)),
                ('image', models.ImageField(default='', upload_to='car/images')),
                ('category', models.CharField(choices=[('sedan', 'Sedan'), ('suv', 'SUV'), ('luxury', 'Luxury'), ('pickup', 'Pickup'), ('hatchback', 'Hatchback')], default='sedan', max_length=20)),
                ('is_available', models.BooleanField(default=True)),
                ('seating_capacity', models.IntegerField(default=5)),
                ('fuel_type', models.CharField(default='Petrol', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=150)),
                ('email', models.CharField(default='', max_length=150)),
                ('phone_number', models.CharField(default='', max_length=15)),
                ('message', models.TextField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=90)),
                ('email', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=20)),
                ('address', models.CharField(default='', max_length=500)),
                ('city', models.CharField(default='', max_length=50)),
                ('car_name', models.CharField(default='', max_length=50)),
                ('days_for_rent', models.IntegerField(default=0)),
                ('price_per_day', models.IntegerField(default=0)),
                ('total_price', models.IntegerField(default=0)),
                ('date', models.CharField(default='', max_length=50)),
                ('loc_from', models.CharField(default='', max_length=50)),
                ('loc_to', models.CharField(default='', max_length=50)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='confirmed', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MyApp.car')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(default='', max_length=15)),
                ('address', models.CharField(default='', max_length=500)),
                ('city', models.CharField(default='', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
