from itertools import count
from django.shortcuts import render
from django.core import serializers
from .models import content 
from django.http import JsonResponse
import json

def terms_and_condition(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data = json.loads(request.body.decode("utf-8"))
            title=data.get('title')
            
            if title == '':
                customer ={
                    "status":"400",
                    "message":"Title is Requried",
                }
                return JsonResponse(customer,safe=False)
            else: 
                try:
                    data=[]
                    contentData = content.objects.filter(key=title).count()

                    if contentData > 0 :
                            contentData = content.objects.filter(key=title)
                            json_data = json.loads(serializers.serialize( "json",contentData))

                            for j in json_data:
                                data.append(json.loads(json.dumps(j["fields"])))
                        
                            customer ={
                                "status":"200",
                                "message":"Successfully",
                                "data":data   
                                
                                }
                            return JsonResponse(customer,safe=False)
                    else :
                        customer ={
                            "status":"400",
                            "message":"Somthing went wrong..",
                            }
                        return JsonResponse(customer,safe=False)
                except:
                    customer ={
                    "status":"400",
                    "message":"Somthing went wrong..",
                    }
                    return JsonResponse(customer,safe=False)
        else: 
            customer ={
                "status":"400",
                "message":"Authentication failed!!",
            }
            return JsonResponse(customer,safe=False)
    else: 
        customer ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(customer,safe=False)
        
        
def admin_commision(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
           # get parameter values 
            data = json.loads(request.body.decode("utf-8"))
            title=data.get('title')
            # all parameters requried conditions
            if title == '':
                customer ={
                    "status":"400",
                    "message":"Title is Requried",
                }
                return JsonResponse(customer,safe=False)
            else: 
                try:
                    data=[]
                    contentData = content.objects.filter(key=title).count() #check this title are exists or not

                    if contentData > 0 :
                            # get content data
                            contentData = content.objects.filter(key=title)
                            json_data = json.loads(serializers.serialize( "json",contentData))

                            for j in json_data:
                                data.append(json.loads(json.dumps(j["fields"])))
                        
                            customer ={
                                "status":"200",
                                "message":"Successfully",
                                "data":data   
                                
                                }
                            return JsonResponse(customer,safe=False)
                    else :
                        customer ={
                            "status":"400",
                            "message":"Somthing went wrong..",
                            }
                        return JsonResponse(customer,safe=False)
                except:
                    customer ={
                    "status":"400",
                    "message":"Somthing went wrong..",
                    }
                    return JsonResponse(customer,safe=False)
        else: 
            customer ={
                "status":"400",
                "message":"Authentication failed!!",
            }
            return JsonResponse(customer,safe=False)
    else: 
        customer ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(customer,safe=False)
        