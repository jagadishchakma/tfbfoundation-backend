from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .utilities.news_insert import news_insert
from . import serializers
from .models import BodhidharaNews
from libs.get_client_ip import get_client_ip

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
        

#---------- NEWS VIEWS COUNT START ----------
class NewsViewCount(APIView):
    def put(self, request):

        news_id = request.data.get('news_id')
        news = BodhidharaNews.objects.get(id=news_id)
        
        if request.user.is_authenticated:
            visitor_id = request.user.id
        else:
            ip = get_client_ip(request)
            visitor_id = ip
            print('views count based on ip: ', ip)
        
        current_views = news.views or [] # Default to empty list if view is None
        if visitor_id not in current_views:
            current_views.append(visitor_id)
            news.views = current_views
            news.save()

            return Response({'success':'News views success'}, status=status.HTTP_202_ACCEPTED)
        return Response({'warning':'already this users views count'}, status=status.HTTP_226_IM_USED)
#---------- NEWS VIEWS COUNT END ----------