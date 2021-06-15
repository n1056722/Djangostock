from rest_framework import serializers

from item.models import Item


# 如果序列化是數據庫的表盡量用ModelSerializer
class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name',)

    def to_representation(self, item):
        return {'items_id': item.id, 'items_name': item.name}


class ItemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'value',)

    def to_representation(self, item):
        return {'items_id': item.id, 'items_name': item.name, 'items_value': str(item.value)}
