# Generated by Django 3.1.4 on 2020-12-05 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=128, verbose_name='课程名')),
                ('course_id', models.CharField(blank=True, max_length=128, null=True, unique=True, verbose_name='课程号')),
                ('credit', models.IntegerField(verbose_name='学分')),
                ('hour', models.IntegerField(verbose_name='学时')),
                ('pre_course', models.CharField(blank=True, max_length=128, null=True, verbose_name='先修要求')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.department', verbose_name='开课院系')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school', verbose_name='学校')),
            ],
            options={
                'verbose_name': '课程表',
                'verbose_name_plural': '课程表',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='CourseTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course', verbose_name='课程')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher', verbose_name='教师')),
            ],
            options={
                'verbose_name': '课程教师中间表',
                'verbose_name_plural': '课程教师中间表',
                'ordering': ['-c_time'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(related_name='courses', through='course.CourseTeacher', to='school.Teacher', verbose_name='开课教师'),
        ),
    ]