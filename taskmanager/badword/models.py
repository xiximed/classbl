from django.db import models


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TextModel(models.Model):
    title = models.TextField('Название')

    class Meta:
        managed = True
        verbose_name = 'texts'
       # db_table = 'texts_klass'

    def __str__(self):
        return str(self.title)
