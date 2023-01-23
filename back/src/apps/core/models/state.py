from django.db import models


class State(models.Model):
    generation_num = models.IntegerField(
        verbose_name='Номер генерации'
    )
    state_hash = models.CharField(
        verbose_name='Хэш состояния',
        max_length=64
    )
    world = models.ForeignKey(
        to='core.World',
        related_name='states',
        related_query_name='states',
        on_delete=models.CASCADE
    )
