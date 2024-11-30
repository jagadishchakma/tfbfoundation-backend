from rest_framework import serializers
from .models import BodhidharaNews, BodhidharaNewsComment, BodhidharaNewsCommentReply1, BodhidharaNewsCommentReply2
#BodhidharaNews Serializers
class BodhadharaNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = BodhidharaNews
        fields = '__all__'

#Comment Serializer
class BodhidharaNewsCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = BodhidharaNewsComment 
        fields = '__all__'

#Reply1 Serializer
class BodhidharaNewsCommentReply1Serializers(serializers.ModelSerializer):
    class Meta:
        model = BodhidharaNewsCommentReply1
        fields = '__all__'

#Reply2 Serializer
class BodhidharaNewsCommentReply2Serializers(serializers.ModelSerializer):
    class Meta:
        model = BodhidharaNewsCommentReply2 
        fields = '__all__'
        