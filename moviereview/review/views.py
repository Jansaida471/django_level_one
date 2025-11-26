from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from review.models import Movie_details
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def basic(request):
    return HttpResponse("hello world")

def movie_info(request):
    movie=request.GET.get("movie")
    date=request.GET.get("date")
    return JsonResponse({"status":"success","result":{"movie_name":movie,"release_date":date}},status=200)

# @csrf_exempt
# def movies(request):
#     if request.method=="POST":
    
#         data=json.loads(request.body)
#         print(data.get("movie_name"),"hello")
#         movie=Movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
#         return JsonResponse({"status":"success","id":"movie.id","message":"movie record inserted successfully","data":movie.id},status=200)
#     return JsonResponse({"error":"error occured"},status=400)
@csrf_exempt
def movie(request):
    if request.method=="GET":
        movie_info=Movie_details.objects.all()
        movie_list=[]
        rating_filter=request.GET.get("rating")
        min_bud_filter=request.GET.get("min_budget")
        max_bud_filter=request.GET.get("max_budget")
        if rating_filter:
            movie_info=movie_info.filter(rating__gte=float(rating_filter))
        

        for movie in movie_info:
            if min_bud_filter or max_bud_filter:
                budget_str=movie.budget.lower().replace("cr","")
                budget_value=float(budget_str)
                if min_bud_filter and budget_value<=float(min_bud_filter):
                    continue
                if max_bud_filter and budget_value>=float(max_bud_filter):
                    continue



            movie_list.append({
                "movie_name":movie.movie_name,
                "release_date":movie.release_date,
                "budget":movie.budget,
                "rating":movie.rating
            })
        if len(movie_list)==0:
            return JsonResponse({"status":"success","message":"no movies found matching the criteria"},status=200)


        return JsonResponse({"status":"success","data":movie_list},status=200)
    elif request.method=="PUT":
        data=json.loads(request.body)
        print("PUT data:",data)
        ref_id=data.get("id")
        print(ref_id)
        existing_movie=Movie_details.objects.get(id=ref_id)
        print("Existing movie:",existing_movie)
        if data.get("movie_name"):
            new_movie_name=data.get("movie_name")
            existing_movie.movie_name=new_movie_name
            existing_movie.save()
        elif data.get("release_date"):
            new_release_date=data.get("release_date")
            existing_movie.release_date=new_release_date
            existing_movie.save()

        elif data.get("budget"):
            new_budget=data.get("budget")
            existing_movie.budget=new_budget
            existing_movie.save()
            
        elif data.get("rating"):
            new_rating=data.get("rating")
            existing_movie.rating=new_rating
            existing_movie.save()
        return JsonResponse({"status":"success","message":"movue record updated successfully","date":data},status=200)
    
    elif  request.method=="DELETE":
        data=request.GET.get("id")
        ref_id =int(data)
        existing_movie=Movie_details.objects.get(id=ref_id)
        existing_movie.delete()
        return JsonResponse({"status":"success","message":"movie record deleted successfully "},status=200)

    elif request.method=="POST":
        # data=json.loads(request.body)
        data=request.POST
        # convert stars to number
        rating_value=int(data.get("rating",0))
        rating_stars="*" * rating_value
        movie=Movie_details.objects.create(
            movie_name=data.get('movie_name'),
            release_date = data.get('release_date'),
            budget=data.get('budget'),
            rating=rating_value
        )
        return JsonResponse({
            "status": "success",
            "id": movie.id,
            "movie_name": movie.movie_name,
            "rating_number": rating_value,
            "rating_stars": rating_stars
        }, status=200)
    # elif request.method == 'GET':
    #     movie_id = request.GET.get("id")     # example: /movie/?id=5
    #     if movie_id:
    #         try:
    #             m = Movie_details.objects.get(id=movie_id)
    #         except Movie_details.DoesNotExist:
    #             return JsonResponse({"error": "Movie not found"}, status=404)

    #         data = {
    #             "id": m.id,
    #             "movie_name": m.movie_name,
    #             "release_date": str(m.release_date),
    #             "budget": m.budget,
    #             "rating": m.rating,
    #             "rating_stars": "*" * m.rating
    #         }
    #         return JsonResponse(data, status=200)

        
    #     all_movies = Movie_details.objects.all()
    #     output = []
    #     for m in all_movies:
    #         output.append({
    #             "id": m.id,
    #             "movie_name": m.movie_name,
    #             "release_date": str(m.release_date),
    #             "budget": m.budget,
    #             "rating": m.rating,
    #             "rating_stars": "*" * int(m.rating)
    #         })

    #     return JsonResponse({"movies": output}, status=200)
    # elif request.method == "PUT":
    # # Check for body
    #     if not request.body:
    #         return JsonResponse({"error": "Empty request body"}, status=400)

    #     try:
    #         data = json.loads(request.body)
    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON"}, status=400)

    #     movie_id = data.get("id")
    #     if not movie_id:
    #         return JsonResponse({"error": "Movie ID required"}, status=400)

    #     # Fetch movie
    #     try:
    #         movie =Movie_details.objects.get(id=movie_id)
    #     except Movie_details.DoesNotExist:
    #         return JsonResponse({"error": "Movie not found"}, status=404)

    #     # Update fields
    #     movie.movie_name = data.get("movie_name", movie.movie_name)
    #     movie.release_date = data.get("release_date", movie.release_date)
    #     movie.budget = data.get("budget", movie.budget)

    #     if "rating" in data:
    #         movie.rating = int(data["rating"])

    #     movie.save()

    #     return JsonResponse({
    #         "status": "updated",
    #         "id": movie.id,
    #         "movie_name": movie.movie_name,
    #         "rating": movie.rating,
    #         "rating_stars": "*" *int( movie.rating)
    #     }, status=200)
    # elif request.method == "DELETE":
    # # Validate body
    #     if not request.body:
    #         return JsonResponse({"error": "Empty request body"}, status=400)

    #     try:
    #         data = json.loads(request.body)
    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON"}, status=400)

    #     movie_id = data.get("id")
    #     if not movie_id:
    #         return JsonResponse({"error": "Movie ID is required"}, status=400)

    #     # Check if movie exists
    #     try:
    #         movie = Movie_details.objects.get(id=movie_id)
    #     except Movie_details.DoesNotExist:
    #         return JsonResponse({"error": "Movie not found"}, status=404)

    #     # Store deleted data to return in response
    #     deleted_data = {
    #         "id": movie.id,
    #         "movie_name": movie.movie_name,
    #         "release_date": str(movie.release_date),
    #         "budget": movie.budget,
    #         "rating": movie.rating,
    #         "rating_stars": "*" * int(movie.rating)
    #     }

    #     # Delete movie
    #     movie.delete()

    #     return JsonResponse({
    #         "status": "success",
    #         "message": "Movie deleted successfully",
    #         "deleted_data": deleted_data
    #     }, status=200)
