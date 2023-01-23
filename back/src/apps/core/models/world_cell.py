from django.db import models


class WorldCell(models.Model):
    world = models.ForeignKey(
        to='core.World',
        on_delete=models.CASCADE,
        related_name='world_cells',
        related_query_name='world_cells',
    )
    cell = models.ForeignKey(
        to='core.Cell',
        on_delete=models.CASCADE,
        related_name='world_cells',
        related_query_name='world_cells',
    )
    alive = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (('cell', 'world'),)
        ordering = ('cell__x', 'cell__y')
