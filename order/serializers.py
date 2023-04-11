"""Serializer for order app"""

from rest_framework import serializers

from order.models import Purchase

from kinohall.models import Session


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for the Purchase model"""

    session = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all())
    total = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'session', 'quantity', 'showdata', 'timestamp', 'paid', 'total']
        read_only_fields = ['id', 'timestamp', 'total']

    def get_total(self, obj):
        return obj.get_sum()
