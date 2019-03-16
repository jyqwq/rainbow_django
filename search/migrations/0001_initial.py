# Generated by Django 2.1.7 on 2019-03-16 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('brand', models.CharField(max_length=50)),
                ('component', models.CharField(max_length=255)),
                ('Effect', models.CharField(max_length=255)),
                ('capacity', models.CharField(max_length=50)),
                ('security', models.IntegerField()),
                ('overdue', models.CharField(max_length=50)),
                ('date', models.CharField(max_length=255)),
                ('click', models.IntegerField(default=0)),
                ('fbs', models.IntegerField(default=0)),
                ('cols', models.IntegerField(default=0)),
                ('com', models.IntegerField(default=0)),
                ('adaptability', models.ManyToManyField(to='user.Skin')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Category')),
            ],
        ),
        migrations.CreateModel(
            name='CommodityCol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=255)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Commodity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='CommodityCom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=255)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Commodity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='CommodityFbs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=255)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Commodity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='CommodityImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('size', models.CharField(max_length=50, null=True)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Commodity')),
            ],
        ),
        migrations.CreateModel(
            name='SearchKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=255)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]
