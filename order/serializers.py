from rest_framework import serializers
from .models import Purchase, Session

class PurchaseSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all())

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'session', 'quantity', 'showdata', 'timestamp', 'paid', 'total']
        read_only_fields = ['id', 'timestamp', 'total']