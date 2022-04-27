from ast import Delete
from asyncio import transports
from django.shortcuts import render
from django.core import serializers
import json

from wallet.models import walletHistory
from chats.models import chat
from chatDetails.models import chatDetails
from django.http import JsonResponse
import dateutil.parser


from datetime import datetime

#show wallwthistory 
def wallet_history(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # get parameter values
            userdata = json.loads(request.body.decode("utf-8"))
            userid = userdata.get('userid')

            data=[]
          
             # all parameters requried conditions
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"UserId is Requried",
                }
                return JsonResponse(customer,safe=False)
           
            else: 
                try:
                    walletData = walletHistory.objects.filter(delete='0',userId=userid).count() #check wallet history exist or not 
                    if walletData > 0 :
                        walletDetail = walletHistory.objects.filter(delete='0',userId=userid) #get wallet data
                        json_data = json.loads(serializers.serialize( "json",walletDetail))

                        for j in json_data:
                            data.append(json.loads(json.dumps(j["fields"])))
                           
                        # response
                        customer ={
                            "status":"200",
                            "userid":userid,    
                            "data":data     }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                            "status":"400",
                            "userid":userid,  
                            "message":"User not found",  
                            "data":data     }
                        return JsonResponse(customer,safe=False)

                except:
                    customer ={
                    "status":"400",
                    "message":"Somthing went wrong",
                    
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

