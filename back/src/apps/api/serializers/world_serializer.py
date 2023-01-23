from rest_framework import serializers

from src.apps.core.models import World, WorldCell


class WorldCellSerializer(serializers.ModelSerializer):
    x = serializers.IntegerField(
        source='cell.x',
        read_only=True
    )
    y = serializers.IntegerField(
        source='cell.y',
        read_only=True
    )

    class Meta:
        model = WorldCell
        fields = ('id', 'x', 'y', 'alive')


class WorldSerializer(serializers.ModelSerializer):
    alive_cells = WorldCellSerializer(
        many=True,
        read_only=True
    )

    def to_representation(self, instance):
        instance.alive_cells = instance.world_cells.filter(alive=True)
        representation = super().to_representation(instance=instance)
        return representation

    class Meta:
        model = World
        fields = ('id', 'name', 'width', 'height', 'alive_cells')
