from django.contrib.auth.models import User
from django.db import models


class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name="Имя анализа", unique=True)
    ws = models.CharField(max_length=20, verbose_name='Сигнал скорости ветра')
    wd = models.CharField(max_length=20, verbose_name='Сигнал направления ветра')
    wd_step = models.FloatField(default=0, verbose_name="Шаг группировки направления")
    wd_start = models.FloatField(default=0, verbose_name="Начало сектора направления")
    wd_stop = models.FloatField(default=0, verbose_name="Конец сектора направления")
    ws_start = models.FloatField(default=0, verbose_name="Начало диапазона скорости")
    ws_stop = models.FloatField(default=0, verbose_name="Конец диапазона скорости")
    date_create = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    file_data = models.FileField(upload_to="upload_data", default="")
    file_zip = models.FileField(upload_to="downloads", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Анализ"
        verbose_name_plural = "Анализы"
        ordering = ["date_modified"]

    def delete(self, using=None, keep_parents=False):
        try:
            self.file_data.delete()
            self.file_zip.delete()
        except Exception:
            pass
        super(Analysis, self).delete(using, keep_parents)
