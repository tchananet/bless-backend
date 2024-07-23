from rest_framework.response import Response
from rest_framework.decorators import api_view  
from django.views.decorators.csrf import csrf_exempt
# from .models import Data
from ..models.models import Data 
from ..serializers.serializers import DataSerializer 

from django.http import HttpResponse
import requests


@csrf_exempt
def url_repeater(request):
    # Get the target URL from the request parameters
    target_url = request.GET.get('target_url')

    # Check if the target URL is provided
    if not target_url:
        return HttpResponse("Please provide a target URL parameter.", status=400)

    try: 
        # Get the headers from the request
        headers = dict(request.headers)

        # Get the bearer token from the Authorization header
        auth = request.headers.get('Authorization')
        bearer_token =  ''
        content_type = ''
        if auth!=None:
            bearer_token = headers.get('Authorization', '')
            print(bearer_token)
            if 'null' in bearer_token:
                bearer_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MTk1MDExMDgsImV4cCI6MTcyMzEwMTEwOCwicm9sZXMiOltdLCJpZCI6ImUwNmMxNDYwLTM0OTYtMTFlZi04NzRjLTRkNmRjMWFjNDFmZiIsInVzZXJuYW1lIjoidXNlcjIwMjRAZ21haWwuY29tIn0.elCywVZtDQ2FjkDTQVZFD8k1mwcWSyzFbrVBaRNC4n2eYCdoSkAe5u-NJn0_UJFMIteixv_m9bK1RDUpWlqVcOH3E1llkZq73zOdnZy2EObwXAw52dePMObjfUc7aQYg2U9OZ-tS5Ry35SeTDniw9efJsu8rdoVcj75eRIKNUseQcNMHZ8isw-WHFEtpE25kVhoOROt9EySdxDxamJMxB1ITym1ivdON_yRu9SUXEACPDVI5tEy_trrHJmKsHlETkHk0mQT6nsZQAmjnNG8c9wU40nH1mj-1mhSwXLe7LCQbsg3n3a8rF3TMXxE0BhNtib5vngZHWvN3rYJbnKx3RQ'
            content_type = headers.get('Content-Type', '')
            # print('bearer token: ', end='')
            # print(request.headers.get('Authorization', ''))
            print(headers)
        # bearer_token = headers.get('Authorization', '').split()[1]

        # Get the data from the request body
        data = request.body
        print(data)
        # 'Authorization': 'Bearer {}'.format(access_token)


        # Forward the request to the target URL
        response = requests.request(
            request.method, target_url, 
            data=data, 
            headers=
{ 'Content-Type': content_type,  'Accept': 'application/json', 'Sec-Ch-Ua-Mobile': '?1', 'Authorization': bearer_token,  }
            # headers={'Content-Type': content_type, 'Accept': 'application/json, text/plain, */*', 'Authorization': 'None', 'Request-Start-Time': '1720693914292', 'User-Agent': 'axios/1.6.8', 'Accept-Encoding': 'gzip, compress, deflate, br', 'Host': '127.0.0.1:8000', 'Connection': 'close'} 
        ) 
        headersw={'Content-Type': content_type, 'Accept': 'application/json, text/plain, */*' ,'Request-Start-Time': '1720693914292', 'User-Agent': 'axios/1.6.8', 'Accept-Encoding': 'gzip, compress, deflate, br', 'Host': '127.0.0.1:8000', 'Connection': 'close'} 

        # Return the response to the client
        # return HttpResponse(f'{headers} {headersw}', status=response.status_code)
        print(data)
        return HttpResponse(response.content, status=response.status_code)

    except Exception as e:
        # Handle request errors
        print(request)
        print(target_url)
        print(request.headers)
        return HttpResponse(f"Error forwarding request: {e}. The full request is {request}", status=500)
    

# Create your views here.
@api_view(['GET'])
def getDate(request):
    app = Data.objects.all()
    serializer = DataSerializer(app, many=True)
    return Response(serializer.data)

# Create your views here.
@api_view(['POST'])
def postData(request):
    serialiser = DataSerializer(data=request.data)
    if serialiser.is_valid():
        serialiser.save()
        return Response(serialiser.data)
    return Response()


    # def post(self, request, format=None):
    #     serializer =ServiceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)