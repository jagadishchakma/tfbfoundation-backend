from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .utilities.news_insert import news_insert
from . import serializers
from .models import BodhidharaNews

# bodhidhara news insert view
class NewsInsertView(APIView):
    serializer_class  = serializers.BodhadharaNewsSerializers

    def post(self,request):
        title = request.data['title']
        category = request.data['category']

        response = news_insert(request)
        if response.get('fb_post_id'):
            data = {
                'fb_post_id': response.get('fb_post_id'),
                'title': title,
                'category': category,
                'fb_video_ids': response.get('fb_video_ids'),
                'fb_photo_ids': response.get('fb_photo_ids'),
            }
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'response':'successfully video post created'}, status=status.HTTP_201_CREATED)
            print("invalid")
            return Response({'response':'FB video post created but database not post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        return response



# bodhidhara news view
class NewsView(ListAPIView):
    serializer_class = serializers.BodhadharaNewsSerializers

    def get_queryset(self):
        return BodhidharaNews.objects.filter().order_by('-id')
        
