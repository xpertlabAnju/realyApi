from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from orders.models import Orders
from .models import rateData
import json

# order_rate
def order_rate(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
          
            data = json.loads(request.body)
            orderId = data.get('orderid')
            driverId=data.get('driverid')
            userId=data.get('userid')
            rate=data.get('rate')
            msg=data.get('msg')

            rateResponse={}

            if orderId == '':
                rateResponse = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(rateResponse, safe=False)
            elif driverId == '':
                rateResponse = {
                    "status": "400",
                    "message": "driverId is Requried",
                }
                return JsonResponse(rateResponse, safe=False)
            elif userId == '':
                rateResponse = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(rateResponse, safe=False)
            elif rate == '':
                rateResponse = {
                    "status": "400",
                    "message": "rate is Requried",
                }
                return JsonResponse(rateResponse, safe=False)
           
            else:
                     
                try: 
                    # order is exists or not
                    orderDataCount=Orders.objects.filter(id=orderId,delete=0).count()
                    
                    if orderDataCount > 0 :
                        #check rateing 
                        rateCount=rateData.objects.filter(orderId=orderId,userId=userId,deriverId=driverId,delete=0).count()

                        if rateCount > 0 :

                            rateResponse ={
                                "status":"400",
                                "message":"Alraedy Rated"
                            
                                }
                            return JsonResponse(rateResponse, safe=False)
                        else:

                            #insert rate
                            rateInsert=rateData(orderId=orderId,userId=userId,deriverId=driverId,rate=rate,message=msg)
                            rateInsert.save()

                        
                            rateResponse ={
                                "status":"200",
                                "message":"Rating Successful"
                            
                                }
                            return JsonResponse(rateResponse, safe=False)
                    
                    else:
                        rateResponse ={
                            "status":"400",
                            "message":"Order not Found"
                            
                            }
                        return JsonResponse(rateResponse, safe=False)
            

                except:
                    rateResponse = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(rateResponse, safe=False)
        else:
            rateResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(rateResponse, safe=False)
    else:
        rateResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(rateResponse, safe=False)