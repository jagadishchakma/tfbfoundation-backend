from rest_framework import serializers
from .models import BodhidharaNews, Comment, Reply1, Reply2
#BodhidharaNews Serializers
class BodhadharaNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = BodhidharaNews
        fields = '__all__'

#Comment Serializer
class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = '__all__'

#Reply1 Serializer
class Reply1Serializers(serializers.ModelSerializer):
    class Meta:
        model = Reply1
        fields = '__all__'

#Reply2 Serializer
class Reply2Serializers(serializers.ModelSerializer):
    class Meta:
        model = Reply2 
        fields = '__all__'
        