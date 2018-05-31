from django.contrib.auth.models import User
from django.db import models


class Analise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name="Имя анализа", unique=True)
    WS = models.CharField(max_length=20, verbose_name='Сигнал скорости ветра')
    WD = models.CharField(max_length=20, verbose_name='Сигнал направления ветра')
    WD_Step = models.FloatField(default=0, verbose_name="Шаг группировки направления")
    WD_Start = models.FloatField(default=0, verbose_name="Начало сектора направления")
    WD_Stop = models.FloatField(default=0, verbose_name="Конец сектора направления")
    WS_Start = models.FloatField(default=0, verbose_name="Начало диапазона скорости")
    WS_Stop = models.FloatField(default=0, verbose_name="Конец диапазона скорости")
    Date_Create = models.DateField(auto_now_add=True)
    Date_Modified = models.DateField(auto_now=True)
    File_Data = models.FileField(upload_to="upload_data",default="")
    File_Zip = models.FileField(upload_to="downloads", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Анализ"
        ordering = ["Date_Modified"]

    def delete(self, using=None, keep_parents=False):
        try:
            self.File_Data.delete()
            self.File_Zip.delete()
        except Exception:
            pass
        super(Analise, self).delete(using, keep_parents)
