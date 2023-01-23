from django.db import models, transaction

from src.apps.core.service import GameOfLife


class World(models.Model):
    DEFAULT_WIDTH = 50
    DEFAULT_HEIGHT = 50

    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        default='Test'
    )
    cells = models.ManyToManyField(
        to='core.Cell',
        related_name='worlds',
        related_query_name='worlds',
        through='core.WorldCell'
    )

    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @transaction.atomic
    def save(self, **kwargs):
        is_create = not self.pk
        super(World, self).save(**kwargs)
        if is_create:
            GameOfLife(world=self).init_world()
