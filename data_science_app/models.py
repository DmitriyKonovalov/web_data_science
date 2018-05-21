from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Analise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20, verbose_name="Имя анализа", unique=True)
    WS = models.CharField(max_length=20, verbose_name='Сигнал скорости ветра')
    WD = models.CharField(max_length=20, verbose_name='Сигнал направления ветра')
    WD_Step = models.FloatField(default=0, verbose_name="Шаг группировки направления")
    WD_Start = models.FloatField(default=0, verbose_name="Начало сектора направления")
    WD_Stop = models.FloatField(default=0, verbose_name="Конец сектора направления")
    WS_Start = models.FloatField(default=0, verbose_name="Начало диапазона скорости")
    WS_Stop = models.FloatField(default=0, verbose_name="Конец диапазона скорости")
    Date_Create = models.DateField(default=now)
    Date_Modified = models.DateField(default=now)
    File_Data = models.FileField(upload_to="upload_data")

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "Анализ"
        ordering = ["Date_Modified"]


class Output(models.Model):
    data_avg = models.FileField(upload_to="data_avg/")
    data_filtered = models.FileField(upload_to="data_filtered/")
    ws_wd_graph = models.ImageField(upload_to="ws_wd_graph/")
    hist_graph = models.ImageField(upload_to="hist_graph/")
    time_graph = models.ImageField(upload_to="time_graph/")
    rose_graph = models.ImageField(upload_to="rose_graph/")

    class Meta:
        verbose_name = "Вывод"