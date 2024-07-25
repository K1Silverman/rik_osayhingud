# Generated by Django 5.0.7 on 2024-07-25 12:56

import datetime
import django.core.validators
from django.db import migrations, models
from ..models.dummyfie import DummyFie
from django.db import transaction

def seed_data(apps, schema_editor):
    
    dummies = [
        {'name': 'Aabi Ausmaa', 'registry_code': '11780308'},
        {'name': 'Aare Mägi FLORES', 'registry_code': '10125795'},
        {'name': 'Baarimees Hanno Torgla', 'registry_code': '14999450'},
        {'name': 'Caius Kull', 'registry_code': '11747328'},
        {'name': 'Çetin Kaltar', 'registry_code': '16491106'},
        {'name': 'Daemon Elson', 'registry_code': '16924516'},
        {'name': 'Ea Annuk', 'registry_code': '16874244'},
        {'name': 'Fabrisio-Fouad Ahwazian', 'registry_code': '16641586'},
        {'name': 'Gabriel Alberto Ceballos Rodriguez', 'registry_code': '14997630'},
        {'name': 'HAAMERI talu', 'registry_code': '10183958'},
        {'name': 'Iago Renan Flauzino Bresciani', 'registry_code': '17023726'},
        {'name': 'Jaagu Annemäe Talu', 'registry_code': '11735176'},
        {'name': 'Kaabrieli - Jerreski talu', 'registry_code': '10579082'},
        {'name': 'Laanegu talu', 'registry_code': '10372079'},
        {'name': 'Maage talu', 'registry_code': '10444985'},
        {'name': 'Naaja Kuningas', 'registry_code': '11819758'},
        {'name': 'Oandu-Möldri talu', 'registry_code': '10580168'},
        {'name': 'Paala talu', 'registry_code': '10131619'},
        {'name': 'Qasim Parvez', 'registry_code': '16976128'},
        {'name': 'Rabakivi Talu', 'registry_code': '10376597'},
        {'name': 'Saade Kirsimägi', 'registry_code': '11648425'},
        {'name': 'ŠUKUFA KERIMOVA', 'registry_code': '11708268'},
        {'name': 'Zabar Vishnyakov', 'registry_code': '17010563'},
        {'name': 'Žanna Anatskaja', 'registry_code': '16199452'},
        {'name': 'Taago Daniel', 'registry_code': '11812020'},
        {'name': 'Ubaid Ali Mughal', 'registry_code': '16858759'},
        {'name': 'Vaade talu', 'registry_code': '10045191'},
        {'name': 'Waldemar Mieczyslaw Sekrecki', 'registry_code': '14115333'},
        {'name': 'Õie Arusoo', 'registry_code': '11807668'},
        {'name': 'Äriküla-Ennu talu', 'registry_code': '10185271'},
        {'name': 'Öko-Mihkli talu', 'registry_code': '16203018'},
        {'name': 'ÜISTE TALU', 'registry_code': '11685811'},
        {'name': 'Xavier Roger Pierre Sauvestre', 'registry_code': '16567588'},
        {'name': 'Yagub Sadygov', 'registry_code': '14716446'}
        ]
    try:
        with transaction.atomic():
            for dummy in dummies:
                DummyFie.objects.create(name=dummy['name'], registry_code=dummy['registry_code'])
        print("DummyFie seeded")
    except Exception as e:
        print(f"Error in migration: {e}")
        raise


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enterprise',
            name='fie',
        ),
        migrations.RemoveField(
            model_name='enterprise',
            name='proprietor_first_entry_date',
        ),
        migrations.AddField(
            model_name='enterprise',
            name='first_entry_date',
            field=models.DateField(default=datetime.date(2024, 7, 25), validators=[django.core.validators.MinValueValidator(datetime.date(2024, 7, 25))]),
        ),
        migrations.CreateModel(
            name='DummyFie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('registry_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.RunPython(seed_data)
    ]

