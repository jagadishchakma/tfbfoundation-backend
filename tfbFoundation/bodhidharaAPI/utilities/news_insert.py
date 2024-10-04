from rest_framework.response import Response
import requests
from rest_framework import status
import json
from django.conf import settings

def news_insert(request):
    access_token = settings.PAGE_ACCESS_TOKEN
    page_id = settings.PAGE_ID
    message = request.data.get('message')
    images = request.FILES.getlist('image')  # Get multiple images
    videos = request.FILES.getlist('video')  # Get multiple videos
    videos_details =  json.loads(request.data.get('video_details')) # Get multiple video details
    # print("details: ",videos_details)
    # print("videos: ", videos)
    # print("images: ",images)
    # print("title: ", title)
    # print("message: ", message)
  
    if not message:
        return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not images and not videos:
        return Response({'error': 'At least one image or video is required'}, status=status.HTTP_400_BAD_REQUEST)


    # Upload images if provided
    image_url = f'https://graph.facebook.com/v20.0/{page_id}/photos'
    image_ids = []
    for image in images:
        image_data = image.read()
        params = {
            'access_token': access_token,
            'published': 'false',  # Don't publish yet
        }
        files = {
            'source': (image.name, image_data, image.content_type),
        }

        try:
            print("image uploade...")
            response = requests.post(image_url, params=params, files=files)
            response_data = response.json()
            if response.status_code == 200:
                # Collect the photo ID from the response
                image_ids.append(response_data['id'])
            else:
                return Response({'error': response_data}, status=response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   





    # Upload videos if provided
    video_url = f'https://graph-video.facebook.com/v20.0/{page_id}/videos'
    video_ids = []
    for index,video in enumerate(videos):
        video_data = video.read()
        video_params = {
            'access_token': access_token,
            'title': videos_details[index]['video_title'],
            'description': videos_details[index]['video_description'],
            'published': 'true',  # publish yet
        }
       
        video_files = {
            'source': (video.name, video_data, video.content_type),
        }

        try:
            print("uploading video....")
            video_response = requests.post(video_url, params=video_params, files=video_files)
            video_response_data = video_response.json()
            
            if video_response.status_code == 200:
                print("upload complete..")
                # Get the video ID from the response
                video_id = video_response_data['id']
                video_ids.append(video_id)
            else:
                print("uploading error")
                return Response({'error': video_response_data}, status=video_response.status_code)
        except Exception as e:
            print("error:", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    # post on timeline
    post_url = f'https://graph.facebook.com/v20.0/{page_id}/feed'
    attached_media = []
    if image_ids:
        attached_media = [{'media_fbid': image_id} for image_id in image_ids]

   

    post_params = {
        'access_token': access_token,
        'message': message,
        'attached_media': json.dumps(attached_media),
    }

    try:
        print("posting on timeline....")
        post_response = requests.post(post_url, params=post_params)
        post_data = post_response.json()
        if post_response.status_code == 200:
            print('posting on timeline success...')
            return {'fb_post_id':post_data.get('id'), 'fb_photo_ids': image_ids, 'fb_video_ids': video_ids}
        else:
            return Response({'error': post_data}, status=post_response.status_code)
    except Exception as e:
        print('posting on timeline failed....')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
