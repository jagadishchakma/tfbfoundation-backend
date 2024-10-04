from rest_framework import serializers
from .models import BodhidharaNews
#BodhidharaNews Serializers
class BodhadharaNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = BodhidharaNews
        fields = '__all__'