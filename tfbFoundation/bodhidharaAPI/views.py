from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .utilities.news_insert import news_insert
from . import serializers
from .models import BodhidharaNews, BodhidharaNewsComment, BodhidharaNewsCommentReply1, BodhidharaNewsCommentReply2
from libs.get_client_ip import get_client_ip
from rest_framework.permissions import IsAuthenticated

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

#---------- BODHIDHARA SINGLE NEWS VIEW START ----------
class NewsSingleView(APIView):
    serializer_class = serializers.BodhadharaNewsSerializers
    def get(self, request, id):
        single_news = BodhidharaNews.objects.get(id=id)
        serializer = self.serializer_class(single_news, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
#---------- BODHIDHARA SINGLE NEWS VIEW END ----------
        

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



#---------- NEWS COMMENT START ----------
class NewsCommentView(APIView):
    serializer_class = serializers.BodhidharaNewsCommentSerializers
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        data = request.data

        user = request.user
        news = BodhidharaNews.objects.get(id=id)
        data['user'] = user.id
        data['news'] = news.id
        print(data)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('success to comment', status=status.HTTP_201_CREATED)
        else:
            return Response('failed to comment submit', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#---------- NEWS COMMENT END ----------


#---------- NEWS COMMENT ALL RETRIEVE START ----------
class NewsCommentsView(APIView):
    serializer_class = serializers.BodhidharaNewsCommentSerializers
    def get(self, request, id):
        comments = BodhidharaNewsComment.objects.filter(news=id).order_by('-id')
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#---------- NEWS COMMENTA ALL RETRIEVE END ----------

#---------- NEWS COMMENT REPLY 1 START ----------
class NewsCommentReply1View(APIView):
    serializer_class = serializers.BodhidharaNewsCommentReply1Serializers
    permission_classes = [IsAuthenticated]
    def post(self,request,comment_id):
        data = request.data
        data['user'] = request.user.id 
        data['comment'] = comment_id 
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('success to reply 1', status=status.HTTP_201_CREATED)
        else:
            return Response('failed to reply 1 submit', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#---------- NEWS COMMENT REPLY 1 END ----------


#---------- NEWS COMMENT REPLIES 1 START----------
class NewsCommentReplies1View(APIView):
    serializer_class = serializers.BodhidharaNewsCommentReply1Serializers
    def get(self, request, comment_id):
        replies = BodhidharaNewsCommentReply1.objects.filter(comment=comment_id).order_by('-id')
        serializer = self.serializer_class(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#---------- NEWS COMMENT REPLIES 1 END----------

#---------- NEWS REPLY1 REPLY2 START----------
class NewsReply1Reply2View(APIView):
    serializer_class = serializers.BodhidharaNewsCommentReply2Serializers
    permission_classes = [IsAuthenticated]
    def post(self, request, reply1_id):
        data = request.data
        data['user'] = request.user.id
        data['reply1'] = reply1_id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('success to reply 2', status=status.HTTP_201_CREATED)
        else:
            return Response('failed to reply 2 submit', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#---------- NEWS REPLY1 REPLY2 END----------

#---------- NEWS REPLY1 REPLIES2 VIEWS START----------
class NewsReply1Replies2View(APIView):
    serializer_class = serializers.BodhidharaNewsCommentReply2Serializers
    def get(self, request, reply1_id):
        replies = BodhidharaNewsCommentReply2.objects.filter(reply1=reply1_id).order_by('-id')
        serializer = self.serializer_class(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#---------- NEWS REPLY1 REPLIES2 VIEWS END----------