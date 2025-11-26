from django.http import JsonResponse
from django.http import HttpResponse
class MovieReviewMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request ):
        if request.path=="/movie/" and request.method=="POST":
            # print("movie api called")
            incoming_data=request.POST
            print(incoming_data)
            if not incoming_data.get("rating"):
                return JsonResponse({"error":"rating is required"},status=400)
            elif float(incoming_data.get("rating"))<0 or float(incoming_data.get("rating"))>5:
                return JsonResponse({"error":"rating should be between 0 to 10"},status=400)
            elif not ( incoming_data.get("budget"))<=0:
                return JsonResponse({"error ":"budget is required"},status=400)
            elif not (incoming_data.get("movie_name")):
                return JsonResponse({"error":"movie_name is required"},status=400)
            
        return self.get_response(request)
        
