from django.db import models


class Cell(models.Model):
    x = models.IntegerField(
        verbose_name='X координата'
    )
    y = models.IntegerField(
        verbose_name='Y координата'
    )

    def __str__(self):
        return f"({self.x}, {self.y})"

    class Meta:
        indexes = [models.Index(fields=['x', 'y'])]
        unique_together = (('x', 'y'), )
        ordering = ('x', 'y')
