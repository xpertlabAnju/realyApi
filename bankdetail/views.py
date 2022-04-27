from ast import Delete
from asyncio import transports
from django.shortcuts import render
from django.core import serializers
import json

from .models import bankdetail
from django.http import JsonResponse
import dateutil.parser


from datetime import datetime
#add bank detail
def add_bank_detail(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # get parameter values
            userdata = json.loads(request.body.decode("utf-8"))
            userid = userdata.get('userid')
            bankname = userdata.get('bankname')
            accountname = userdata.get('accountname')
            accountnumber = userdata.get('accountnumber')
            ifsccode=userdata.get('ifsccode')

            data=[]
          
             # all parameters requried conditions
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"UserId is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif bankname == '':
                customer ={
                    "status":"400",
                    "message":"Bankname Requried",
                }
                return JsonResponse(customer,safe=False)
            elif accountname == '':
                customer ={
                    "status":"400",
                    "message":"Accountname Requried",
                }
                return JsonResponse(customer,safe=False)
            elif accountnumber == '':
                customer ={
                    "status":"400",
                    "message":"Accountnumber Requried",
                }
                return JsonResponse(customer,safe=False)
            elif ifsccode == '':
                customer ={
                    "status":"400",
                    "message":"ifsccode Requried",
                }
                return JsonResponse(customer,safe=False)
            
            else: 
                try:
                    bankdetailCount=bankdetail.objects.filter(userId=userid,delete=0).count()

                    if bankdetailCount == 0 :

                        # insert bank detail data
                        insertQuery = bankdetail(userId=userid,bankname=bankname,accountname=accountname,accountnumber=accountnumber,ifccode=ifsccode)
                        insertQuery.save() #Inasertquery save
                        
                        customer ={
                                "status":"200",
                                "message":"Bank Detail insert Successfully"  
                                }
                        return JsonResponse(customer,safe=False)
                    else :
                        updateQuery=bankdetail.objects.filter(userId=userid,delete=0).update(bankname=bankname,accountname=accountname,accountnumber=accountnumber,ifccode=ifsccode) #update bank detail data
                        customer ={
                                "status":"200",
                                "message":"Bank Detail insert Successfully"  
                                }
                        return JsonResponse(customer,safe=False)
                except:
                    
                    customer ={
                        "status":"400",
                        "message":"not Insert bank detail"  
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

#show bank detail

def show_bank_detail(request):
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
                    bankDetailData = bankdetail.objects.filter(delete='0',userId=userid).count() #check that user bank detail exist or not 
                    if bankDetailData > 0 :
                        bankdata = bankdetail.objects.filter(delete='0',userId=userid) #get bank data
                        json_data = json.loads(serializers.serialize( "json",bankdata))

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
                            "message":"Bankdetail not found",  
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


