
from .models import Stockdeatils

from rest_framework.serializers import ModelSerializer


class StockSerializer(ModelSerializer):

    class Meta:
        model = Stockdeatils
        fields = "__all__"
