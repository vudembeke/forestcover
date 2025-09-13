

from django.db import models

class Forest(models.Model):
    forest_name = models.CharField(max_length=255)

    def __str__(self):
        return self.forest_name
    class Meta:
        app_label = 'mainapp'


class ForestData(models.Model):
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, related_name='data')
    ndvi = models.FloatField()
    area = models.FloatField()
    density = models.FloatField()
    change = models.FloatField()
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = ('forest', 'year')  # Ensures unique year per forest
        app_label = 'mainapp'

    def __str__(self):
        return f"{self.forest.forest_name} - {self.year}"



