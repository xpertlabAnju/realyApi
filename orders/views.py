from django.shortcuts import render
from django.core import serializers
import json
from  orders.models import Orders,Orderdetails
from customers.models import customers
from chats.models import chat
from chatDetails.models import chatDetails
from django.http import JsonResponse
import hashlib
import datetime
import math
import random
import os
import dateutil.parser
from wallet.models import walletHistory

# order request
def order_request(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":

            data = json.loads(request.body.decode("utf-8"))

            userId = data.get('userid')
            fromlocation = data.get('fromlocation')
            to = data.get('to')
            fromlatitude = data.get('fromLatitude')
            fromLongitude = data.get('fromLongitude')
            toLatitude = data.get('toLatitude')
            toLongitude = data.get('toLongitude')
            msg = json.loads(data.get('msg'))
          
            time = data.get('time')

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            elif to == '':
                order = {
                    "status": "400",
                    "message": "To is Requried",
                }
                return JsonResponse(order, safe=False)
            elif fromlatitude == '':
                order = {
                    "status": "400",
                    "message": "fromlatitude is Requried",
                }
                return JsonResponse(order, safe=False)
            elif fromLongitude == '':
                order = {
                    "status": "400",
                    "message": "FromLongitude is Requried",
                }
                return JsonResponse(order, safe=False)
            elif toLatitude == '':
                order = {
                    "status": "400",
                    "message": "ToLatitude is Requried",
                }
                return JsonResponse(order, safe=False)
            elif toLongitude == '':
                order = {
                    "status": "400",
                    "message": "ToLongitude is Requried",
                }
                return JsonResponse(order, safe=False)
            elif msg == '':
                order = {
                    "status": "400",
                    "message": "Message is Requried",
                }
                return JsonResponse(order, safe=False)
            elif fromlocation == '':
                order = {
                    "status": "400",
                    "message": "From Location is Requried",
                }
                return JsonResponse(order, safe=False)
            elif time == '':
                order = {
                    "status": "400",
                    "message": "Time is Requried",
                }
                return JsonResponse(order, safe=False)

            else:
                try:
                    userObject = customers.objects.filter(delete='0', id=userId, status='0').count()
               
                    if userObject is not None:
                        checkOrder = Orders.objects.filter(fromcity=fromlocation,
                                            tocity=to,
                                            fromlatitude=fromlatitude,
                                            fromlongitude=fromLongitude,
                                            tolatitude=toLatitude,
                                            tolongitude=toLongitude,
                                            delete='0',
                                            userId=userId, 
                                            statusFromUser=0
                                            ).count()
                        if checkOrder !=0:
                       
                            order=Orders.objects.filter(fromcity=fromlocation,
                                                tocity=to,
                                                fromlatitude=fromlatitude,
                                                fromlongitude=fromLongitude,
                                                tolatitude=toLatitude,
                                                tolongitude=toLongitude,
                                                delete='0', userId=userId)
                            filter=json.loads(serializers.serialize( "json",order))
                           


                                # print(key)
                            for j in filter:
                                orderId=(json.dumps(j['pk']))                                
                                for key in (msg):
                                    # print(key)  
            
                                    # try:
                                        orderDetailInsert=Orderdetails(orderid=orderId,userId=userId,message=(json.dumps(key["message"])),messagetime=(json.dumps(key["time"])))
                                        orderDetailInsert.save()
                                    # except:
                                    #     order = {
                                    #         "status": "400",
                                    #         "message": "failed"
                                    #     }
                                    #     return JsonResponse(order, safe=False)  


                        
                        else:                                    
                            insertOrderDetail = Orders(
                            fromcity=fromlocation,
                            tocity=to,
                            userId=userId,
                            fromlatitude=fromlatitude,
                            fromlongitude=fromLongitude,
                            tolatitude=toLatitude,
                            tolongitude=toLongitude)
                            insertOrderDetail.save()


                            lastOrder=insertOrderDetail.id  # last inserted id
    
                            for key in (msg):
                                    try:
                                        orderDetailInsert=Orderdetails(orderid=lastOrder,userId=userId,message=key["message"],messagetime=key["time"])
                                        orderDetailInsert.save()
                                    except:
                                        order = {
                                            "status": "400",
                                            "message": "failed1",
                                        }
                                        return JsonResponse(order, safe=False)  






                            # insertOrderDetail = Orders(
                            #     fromcity=fromlocation,
                            #     tocity=to,
                            #     userId=userId,
                            #     fromlatitude=fromlatitude,
                            #     fromlongitude=fromLongitude,
                            #     tolatitude=toLatitude,
                            #     tolongitude=toLongitude)
                            # insertOrderDetail.save()

                        # print(insertOrderDetail.id)  # last inserted id
                        # userProfile=Orders.objects.filter(delete='0',id=userId,status=0).update(document=fromLongitude,type=1)

                        order = {
                            "status": "200",
                            "message": "Order Request Sent Successfully",
                            "userId": userId
                        }
                        return JsonResponse(order, safe=False)
                    else:
                       
                        order = {
                            "status": "400",
                            "message": "User not found"
                        }
                        return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Uer Not found",
                    }
                    return JsonResponse(order, safe=False)

        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False)


#All new request order for drivers

def pending_orders_for_customer(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            # print(userId)
      

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                try: 

                    userData = customers.objects.filter(delete=0,id=userId,status=0).count()
                    if userData > 0:
                        mainData=[]
                       
                        userData = customers.objects.filter(delete=0,id=userId,status=0)
                        json_data =json.loads(serializers.serialize( "json",userData))
                       
                        for j in json_data:

                            orderCount=Orders.objects.filter(statusFromUser=0,userId=userId,OrderStatus=0,transporterId=0).count()
                           
                            if orderCount > 0 :
                                
                               
                                   
                        
                                order=Orders.objects.filter(statusFromUser=0,userId=userId,OrderStatus=0,transporterId=0)
                                filter=json.loads(serializers.serialize( "json",order))
                            
                                for k in filter:
                                    
                                    orderDetails=Orderdetails.objects.filter(userId=userId,orderid=k["pk"])[:1]
                                    filter=json.loads(serializers.serialize( "json",orderDetails))
                                  
                                    for o in filter:
                                        json.loads(json.dumps(o["fields"]))
                                        # print((dateutil.parser.isoparse(o["fields"]["created"])).strftime("%m/%d/%Y"))
                                        
                                    k["fields"]["firstname"]=(json.loads(json.dumps(j["fields"]["firstname"])))
                                    o["fields"]["messagetime"]=(dateutil.parser.isoparse(o["fields"]["created"])).strftime("%d/%m/%Y")
                                    k["fields"].update(json.loads(json.dumps(o["fields"])))
                                    mainData.append(json.loads(json.dumps(k["fields"])))
                                    
                        
                                order ={
                                    "status":"200",
                                    "message":"successfully",
                                    "data":mainData
                        
                                    }
                                return JsonResponse(order, safe=False)
                            
                            else:
                                order ={
                                    "status":"400",
                                    "message":"No order Found"
                                    
                                    }
                                return JsonResponse(order, safe=False)
                    else :
                        order = {
                        "status": "400",
                        "message": "User not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False)
            
#All Inprogress order for customer

def progress_orders_for_customer(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            # print(userId)
      

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                try: 

                    userData = customers.objects.filter(delete=0,id=userId,status=0,type=0).count()
                    if userData > 0:
                        mainData=[]
                       
                        userData = customers.objects.filter(delete=0,id=userId,status=0,type=0)
                        json_data =json.loads(serializers.serialize( "json",userData))
                       
                        for j in json_data:

                            orderCount=Orders.objects.filter(statusFromUser=1,userId=userId,OrderStatus=1).count()
                            if orderCount > 0 :
                                
                                order=Orders.objects.filter(statusFromUser=1,userId=userId,OrderStatus=1)
                                filter=json.loads(serializers.serialize( "json",order))
                            
                                for k in filter:
                                    
                                    orderDetails=Orderdetails.objects.filter(userId=userId,orderid=k["pk"])[:1]
                                    filter=json.loads(serializers.serialize( "json",orderDetails))
                                    
                                    for o in filter:
                                        json.loads(json.dumps(o["fields"]))
                                        
                                        k["fields"]["firstname"]=(json.loads(json.dumps(j["fields"]["firstname"])))
                                        o["fields"]["messagetime"]=(dateutil.parser.isoparse(o["fields"]["created"])).strftime("%d/%m/%Y")
                                        k["fields"].update(json.loads(json.dumps(o["fields"])))
                                        mainData.append(json.loads(json.dumps(k["fields"])))
                                
                        
                                order ={
                                    "status":"200",
                                    "message":"successfully",
                                    "data":mainData
                        
                                    }
                                return JsonResponse(order, safe=False)
                            
                            else:
                                order ={
                                    "status":"400",
                                    "message":"No chat Found"
                                    
                                    }
                                return JsonResponse(order, safe=False)
                    else :
                        order = {
                        "status": "400",
                        "message": "User not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False)   

#All Finished order for customer

def finished_orders_for_customer(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            # print(userId)
      

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                try: 

                    userData = customers.objects.filter(delete=0,id=userId,status=0,type=0).count()
                    if userData > 0:
                        mainData=[]
                       
                        userData = customers.objects.filter(delete=0,id=userId,status=0,type=0)
                        json_data =json.loads(serializers.serialize( "json",userData))
                       
                        for j in json_data:

                            orderCount=Orders.objects.filter(statusFromUser=1,userId=userId,OrderStatus=4).count()
                            if orderCount > 0 :
                                
                                orderDetails=Orderdetails.objects.filter(userId=userId)[:1]
                                filter=json.loads(serializers.serialize( "json",orderDetails))
                                for o in filter:
                                    json.loads(json.dumps(o["fields"]))
                               
                        
                                order=Orders.objects.filter(statusFromUser=1,userId=userId,OrderStatus=4)
                                filter=json.loads(serializers.serialize( "json",order))
                            
                                for k in filter:
                                    k["fields"]["firstname"]=(json.loads(json.dumps(j["fields"]["firstname"])))
                                    o["fields"]["messagetime"]=(dateutil.parser.isoparse(o["fields"]["created"])).strftime("%d/%m/%Y")
                                    k["fields"].update(json.loads(json.dumps(o["fields"])))
                                    mainData.append(json.loads(json.dumps(k["fields"])))
                                
                        
                                order ={
                                    "status":"200",
                                    "message":"successfully",
                                    "data":mainData
                        
                                    }
                                return JsonResponse(order, safe=False)
                            
                            else:
                                order ={
                                    "status":"400",
                                    "message":"No chat Found"
                                    
                                    }
                                return JsonResponse(order, safe=False)
                    else :
                        order = {
                        "status": "400",
                        "message": "User not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False)           

# count all orders for customer
def count_orders_for_customer(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            # print(userId)
      

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                try: 

                    userData = customers.objects.filter(delete=0,id=userId,status=0).count()
                    if userData > 0:
                                              
                        newRequestorderCount=Orders.objects.filter(statusFromUser=0,userId=userId,OrderStatus=0).count()
                        inProgressOrderCount=Orders.objects.filter(statusFromUser=1,userId=userId,OrderStatus=1).count()
                        finishedOrderCount=Orders.objects.filter(statusFromUser=1,userId=userId,OrderStatus=4).count()      
                        order ={
                            "status":"200",
                            "message":"successfully",
                            "newRequestOrder":newRequestorderCount,
                            "inProgressOrder":inProgressOrderCount,
                            "finishedOrder":finishedOrderCount
                
                            }
                        return JsonResponse(order, safe=False)
                    
                       
                    else :
                        order = {
                        "status": "400",
                        "message": "User not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False) 

#All new request order for drivers

def pending_orders_for_drivers(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            # print(userId)
      

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                # try: 

                #     userData = customers.objects.filter(delete=0,id=userId,status=0,type=1).count()
                #     if userData > 0:
                #         mainData=[]

                #         userData = customers.objects.filter(delete=0,id=userId,status=0,type=1)
                #         json_data =json.loads(serializers.serialize( "json",userData))
                       
                #         for udata in json_data:
                       

                #             orderCount=Orders.objects.filter(statusFromUser=0,OrderStatus=0,transporterId=0).count()
                #             if orderCount > 0 :
                #                 order=Orders.objects.filter(statusFromUser=0,OrderStatus=0,transporterId=0).exclude(userId=userId)
                #                 filter=json.loads(serializers.serialize( "json",order))
                                
                #                 for odata in filter:
                #                     orderId=json.loads(json.dumps(odata["pk"]))
                                    
                            
                #                     for j in filter:
                                        
                #                         orderDetails=Orderdetails.objects.filter(delete=0,orderid=orderId).exclude(userId=userId)[:1]
                #                         filterOrder=json.loads(serializers.serialize( "json",orderDetails))
                                    
                            
                #                     for o in filterOrder:
                #                         json.loads(json.dumps(o["fields"]))
                #                         # print(o["fields"])
                                    
                #                         # user_id=json.loads(json.dumps(j["fields"]["userId"]))
                #                         # userData1 = customers.objects.filter(delete=0,id=user_id,status=0,type=0)
                #                         # json_data1 =json.loads(serializers.serialize( "json",userData1))
                #                         # for udata in json_data1:
                                    
                                    
                #                     j["fields"]["firstname"]=(json.loads(json.dumps(udata["fields"]["firstname"])))
                #                     o["fields"]["messagetime"]=(dateutil.parser.isoparse(o["fields"]["created"])).strftime("%d/%m/%Y")
                #                     j["fields"].update(json.loads(json.dumps(o["fields"])))
                #                     mainData.append(json.loads(json.dumps(j["fields"])))
                                           
                #                 order ={
                #                     "status":"200",
                #                     "message":"successfully",
                #                     "data":mainData
                        
                #                     }
                #                 return JsonResponse(order, safe=False)
                                
                #             else:
                #                 order ={
                #                     "status":"400",
                #                     "message":"No chat Found"
                                    
                #                     }
                #                 return JsonResponse(order, safe=False)
                #     else :
                #         order = {
                #         "status": "400",
                #         "message": "user not Found",
                #         }
                #         return JsonResponse(order, safe=False)
                try:
                    userData = customers.objects.filter(delete=0,id=userId,status=0,type=1).count()
                    if userData > 0:
                        mainData=[]
                       
                        userData = customers.objects.filter(delete=0,id=userId,status=0,type=1)
                        json_data =json.loads(serializers.serialize( "json",userData))
                       
                        for j in json_data:
    
                            orderCount=Orders.objects.filter(statusFromUser=0,OrderStatus=0,transporterId=0).count()
                            if orderCount > 0 :
                                
                                order=Orders.objects.filter(statusFromUser=0,OrderStatus=0,transporterId=0).exclude(userId=userId)
                                filter=json.loads(serializers.serialize( "json",order))
                            
                                for k in filter:
                                    
                                    orderDetails=Orderdetails.objects.filter(delete=0,orderid=k["pk"]).exclude(userId=userId)[:1]
                                    filter=json.loads(serializers.serialize( "json",orderDetails))
                                  
                                    for o in filter:
                                        json.loads(json.dumps(o["fields"]))
                                        # user name get
                                        user_id=json.loads(json.dumps(o["fields"]["userId"]))
                                        userData1 = customers.objects.filter(delete=0,id=user_id,status=0,type=0)
                                        json_data1 =json.loads(serializers.serialize( "json",userData1))
                                        for udata in json_data1:
                                   
                                 
                                            j["fields"]["firstname"]=(json.loads(json.dumps(udata["fields"]["firstname"])))
                                        
                                    k["fields"]["firstname"]=(json.loads(json.dumps(j["fields"]["firstname"])))
                                    o["fields"]["messagetime"]=(dateutil.parser.isoparse(o["fields"]["created"])).strftime("%d/%m/%Y")
                                    k["fields"].update(json.loads(json.dumps(o["fields"])))
                                    mainData.append(json.loads(json.dumps(k["fields"])))
                                    
                        
                                order ={
                                    "status":"200",
                                    "message":"successfully",
                                    "data":mainData
                        
                                    }
                                return JsonResponse(order, safe=False)
                            
                            else:
                                order ={
                                    "status":"400",
                                    "message":"No chat Found"
                                    
                                    }
                                return JsonResponse(order, safe=False)
                    else :
                        order = {
                        "status": "400",
                        "message": "User not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False)
#All Inprogress order for Driver

def progress_orders_for_driver(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            
            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                try: 

                    userData = customers.objects.filter(delete=0,id=userId,status=0,type=1).count()
                    if userData > 0:
                        mainData=[]
                       
                        userData = customers.objects.filter(delete=0,id=userId,status=0,type=1)
                        json_data =json.loads(serializers.serialize( "json",userData))
                       
                        for j in json_data:

                            orderCount=Orders.objects.filter(statusFromUser=1,transporterId=userId,OrderStatus=1).count()
                            if orderCount > 0 :
                                
                                
                                order=Orders.objects.filter(statusFromUser=1,transporterId=userId,OrderStatus=1)
                                filter=json.loads(serializers.serialize( "json",order))
                            
                                for k in filter:
                                    
                                    orderDetails=Orderdetails.objects.filter(transporterid=userId,orderid=k["pk"])[:1]
                                    filter=json.loads(serializers.serialize( "json",orderDetails))
                                    for o in filter:
                                        json.loads(json.dumps(o["fields"]))
                                        
                                        # user name get
                                        user_id=json.loads(json.dumps(o["fields"]["userId"]))
                                        userData1 = customers.objects.filter(delete=0,id=user_id,status=0,type=0)
                                        json_data1 =json.loads(serializers.serialize( "json",userData1))
                                        for udata in json_data1:
                                            j["fields"]["firstname"]=(json.loads(json.dumps(udata["fields"]["firstname"])))
                                    
                                        k["fields"]["firstname"]=(json.loads(json.dumps(j["fields"]["firstname"])))
                                        o["fields"]["messagetime"]=(dateutil.parser.isoparse(o["fields"]["created"])).strftime("%d/%m/%Y")
                                        k["fields"].update(json.loads(json.dumps(o["fields"])))
                                        mainData.append(json.loads(json.dumps(k["fields"])))
                                
                        
                                order ={
                                    "status":"200",
                                    "message":"successfully",
                                    "data":mainData
                        
                                    }
                                return JsonResponse(order, safe=False)
                            
                            else:
                                order ={
                                    "status":"400",
                                    "message":"No chat Found"
                                    
                                    }
                                return JsonResponse(order, safe=False)
                    else :
                        order = {
                        "status": "400",
                        "message": "Driver not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False)   

#All Finished order for driver

def finished_orders_for_driver(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            # print(userId)
      

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                try: 

                    userData = customers.objects.filter(delete=0,id=userId,status=0,type=1).count()
                    if userData > 0:
                        mainData=[]
                       
                        userData = customers.objects.filter(delete=0,id=userId,status=0,type=1)
                        json_data =json.loads(serializers.serialize( "json",userData))
                       
                        for j in json_data:

                            orderCount=Orders.objects.filter(statusFromUser=1,transporterId=userId,OrderStatus=4).count()
                            if orderCount > 0 :
                                
                                orderDetails=Orderdetails.objects.filter(transporterid=userId)[:1]
                                filter=json.loads(serializers.serialize( "json",orderDetails))
                                for o in filter:
                                    json.loads(json.dumps(o["fields"]))
                                    
                                # user name get
                                user_id=json.loads(json.dumps(o["fields"]["userId"]))
                                userData1 = customers.objects.filter(delete=0,id=user_id,status=0,type=0)
                                json_data1 =json.loads(serializers.serialize( "json",userData1))
                                for udata in json_data1:
                                    j["fields"]["firstname"]=(json.loads(json.dumps(udata["fields"]["firstname"])))
                               
                        
                                order=Orders.objects.filter(statusFromUser=1,transporterId=userId,OrderStatus=4)
                                filter=json.loads(serializers.serialize( "json",order))
                            
                                for k in filter:
                                    k["fields"]["firstname"]=(json.loads(json.dumps(j["fields"]["firstname"])))
                                    o["fields"]["messagetime"]=(dateutil.parser.isoparse(o["fields"]["created"])).strftime("%d/%m/%Y")
                                    k["fields"].update(json.loads(json.dumps(o["fields"])))
                                    mainData.append(json.loads(json.dumps(k["fields"])))
                                
                        
                                order ={
                                    "status":"200",
                                    "message":"successfully",
                                    "data":mainData
                        
                                    }
                                return JsonResponse(order, safe=False)
                            
                            else:
                                order ={
                                    "status":"400",
                                    "message":"No chat Found"
                                    
                                    }
                                return JsonResponse(order, safe=False)
                    else :
                        order = {
                        "status": "400",
                        "message": "Driver not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False)        

# count all orders for Driver
def count_orders_for_driver(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            # print(userId)
      

            if userId == '':
                order = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(order, safe=False)
            else:
                     
                try: 

                    userData = customers.objects.filter(delete=0,id=userId,status=0,type=1).count()
                    if userData > 0:
                                              
                        newRequestorderCount=Orders.objects.filter(statusFromUser=0,OrderStatus=0,transporterId=0).exclude(userId=userId).count()
                        inProgressOrderCount=Orders.objects.filter(statusFromUser=1,OrderStatus=1).exclude(userId=userId).count()
                        finishedOrderCount=Orders.objects.filter(statusFromUser=1,OrderStatus=4).exclude(userId=userId).count()     
                        order ={
                            "status":"200",
                            "message":"successfully",
                            "newRequestOrder":newRequestorderCount,
                            "inProgressOrder":inProgressOrderCount,
                            "finishedOrder":finishedOrderCount
                
                            }
                        return JsonResponse(order, safe=False)
                    
                       
                    else :
                        order = {
                        "status": "400",
                        "message": "Driver not Found",
                    }
                    return JsonResponse(order, safe=False)

                except:
                    order = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(order, safe=False)
        else:
            order = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(order, safe=False)
    else:
        order = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(order, safe=False) 

        
# user order accepted all driver
def user_order_accepted(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            # userId = data.get('userid')
            orderId = data.get('orderid')
            # print(userId)
            orderResponse={}

            if orderId == '':
                orderResponse = {
                    "status": "400",
                    "message": "orderId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            else:
                     
                try: 
   
                    chatDatacount=chat.objects.filter(orderId=orderId,delete=0,driverstatus=1).count()
                    mainData=[]
                    if chatDatacount > 0 :
                        chatData=chat.objects.all().filter(orderId=orderId,delete=0,driverstatus=1)
                        filter=json.loads(serializers.serialize("json",chatData))
                        # print(filter)
                        for cdetail in filter:
                            driverId=json.loads(json.dumps(cdetail["fields"]["transporterId"]))
                            chatId= json.loads(json.dumps(cdetail["pk"]))
                            
                            #order data get
                            orderData=Orders.objects.filter(id=orderId,delete=0)
                            orderfilter=json.loads(serializers.serialize("json",orderData))
                            for orderdetail in orderfilter:
                                json.loads(json.dumps(orderdetail["fields"]))

                            userData = customers.objects.filter(delete=0,id=driverId,status=0,type=1)
                            filter=json.loads(serializers.serialize( "json",userData))
                            for ud in filter:
                                # print(json.loads(json.dumps(ud["fields"])))

                                chatDetail=chatDetails.objects.filter(chatId=chatId)[:1]
                                filter=json.loads(serializers.serialize( "json",chatDetail))
                                for o in filter:
                                    json.loads(json.dumps(o["fields"]))
                                    o["fields"]["fromcity"]=(json.loads(json.dumps(orderdetail["fields"]["fromcity"])))
                                    o["fields"]["tocity"]=(json.loads(json.dumps(orderdetail["fields"]["tocity"])))
                                    o["fields"]["firstname"]=(json.loads(json.dumps(ud["fields"]["firstname"])))
                                    o["fields"]["profile"]=(json.loads(json.dumps(ud["fields"]["profilepic"])))
                                    o["fields"]["time"]= (dateutil.parser.isoparse(o["fields"]["created"])).strftime("%H:%M %p %b %d")
            
                                    o["fields"].update(json.loads(json.dumps(o["fields"])))
                                    mainData.append(json.loads(json.dumps(o["fields"])))
                            
                            orderResponse ={
                                "status":"200",
                                "message":"successfully",
                                "data":mainData
                    
                                }
                            
                        return JsonResponse(orderResponse, safe=False)
                    
                    else:
                        orderResponse ={
                            "status":"400",
                            "message":"Chat not Found"
                            
                            }
                        return JsonResponse(orderResponse, safe=False)
            

                except:
                    orderResponse = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(orderResponse, safe=False)
        else:
            orderResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(orderResponse, safe=False)
    else:
        orderResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(orderResponse, safe=False)
        

# accepte Order
def accepte_order(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            userId = data.get('userid')
            orderId=data.get('orderid')
            driverId= data.get('driverid')
            paymentType= data.get('paymentType')
            price= data.get('price')
            commission= data.get('commission')
            finalprice= data.get('finalprice')
            chatId=data.get('chatid')
            chatdetailId=data.get('chatdetailid')
         
            orderResponse={}

            if userId == '':
                orderResponse = {
                    "status": "400",
                    "message": "userId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif driverId == '':
                orderResponse = {
                    "status": "400",
                    "message": "driverId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif orderId == '':
                orderResponse = {
                    "status": "400",
                    "message": "orderId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif paymentType == '':
                orderResponse = {
                    "status": "400",
                    "message": "paymentType is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif price == '':
                orderResponse = {
                    "status": "400",
                    "message": "price is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif commission == '':
                orderResponse = {
                    "status": "400",
                    "message": "commission is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif finalprice == '':
                orderResponse = {
                    "status": "400",
                    "message": "finalprice is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif chatId == '':
                orderResponse = {
                    "status": "400",
                    "message": "chatDetailId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif chatdetailId == '':
                orderResponse = {
                    "status": "400",
                    "message": "chatdetailId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            else:
                     
                try: 
                    # order is exists or not
                    orderDataCount=Orders.objects.filter(id=orderId,delete=0).count()
                   
                    
                    if orderDataCount > 0 :
                        orderData=Orders.objects.filter(id=orderId,delete=0).update(transporterId=driverId,statusFromUser=1,OrderStatus=1,paymentType=paymentType,amount=price,commision=commission,finalprice=finalprice) #update order data

                       
                        # orderdetail update
                        orderDetailData=Orderdetails.objects.filter(orderid=orderId,delete=0).update(transporterid=driverId,senderType="User",receiverType="TRANSPORTER")

                        #chatdetail update
                        chatDetail=chatDetails.objects.filter(id=chatdetailId,delete=0).update(chatOrderStatus=4)
                        
                        #chatupdate
                        chatdata=chat.objects.filter(id=chatId,delete=0).update(driverstatus=2)
                       
                        orderResponse ={
                            "status":"200",
                            "message":"Order Accepted",
                            "orderId":orderId
                            }
                            
                        return JsonResponse(orderResponse, safe=False)
                    
                    else:
                        orderResponse ={
                            "status":"400",
                            "message":"Order not Found"
                            
                            }
                        return JsonResponse(orderResponse, safe=False)
            

                except:
                    orderResponse = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(orderResponse, safe=False)
        else:
            orderResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(orderResponse, safe=False)
    else:
        orderResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(orderResponse, safe=False)


        

#order_status display
def order_status(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
          
            data = json.loads(request.body)
            orderId = data.get('orderid')
           
            # print(userId)
            orderResponse={}

            if orderId == '':
                orderResponse = {
                    "status": "400",
                    "message": "orderId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
           
            else:
                     
                try: 
                    # order is exists or not
                    orderDataCount=Orders.objects.filter(id=orderId,delete=0).count()
                    # print(orderDataCount)
                    
                    if orderDataCount > 0 :
                        orderData=Orders.objects.filter(id=orderId,delete=0)
                      
                        filter=json.loads(serializers.serialize("json",orderData))
                        for odata in filter:
                            json.loads(json.dumps(odata["fields"]))
                            Orderstatus=json.loads(json.dumps(odata["fields"]["OrderStatus"]))
                            if(Orderstatus == 0):
                                status="Pending"
                            elif(Orderstatus == 1):
                                status="Running"
                            elif(Orderstatus == 2):
                                status="Delivered"
                            else:
                                status="Rejected"
  

                        orderResponse ={
                            "status":"200",
                            "message":"successfully",
                            "orderStatus":status,
                            "orderId":orderId
                            }
                            
                        return JsonResponse(orderResponse, safe=False)
                    
                    else:
                        orderResponse ={
                            "status":"400",
                            "message":"Order not Found"
                            
                            }
                        return JsonResponse(orderResponse, safe=False)
            

                except:
                    orderResponse = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(orderResponse, safe=False)
        else:
            orderResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(orderResponse, safe=False)
    else:
        orderResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(orderResponse, safe=False)

#complete Order
def complete_order(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
          
            data = json.loads(request.body)
            userId = data.get('userid')
            transporterId = data.get('transporterid')
            orderId = data.get('orderid')
            chatId=data.get('chatid')
            balance=data.get('balance') #minus commision
           
            orderResponse={}

            if userId == '':
                orderResponse = {
                    "status": "400",
                    "message": "UserId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif transporterId == '':
                orderResponse = {
                    "status": "400",
                    "message": "TransporterId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif orderId == '':
                orderResponse = {
                    "status": "400",
                    "message": "OrderId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif chatId == '':
                orderResponse = {
                    "status": "400",
                    "message": "ChatId is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            elif balance == '':
                orderResponse = {
                    "status": "400",
                    "message": "balance is Requried",
                }
                return JsonResponse(orderResponse, safe=False)
            
        
            else:
                     
                try: 
                    # order is exists or not
                    orderDataCount=Orders.objects.filter(id=orderId,delete=0).count()
                   
                    
                    if orderDataCount > 0 :
                        #update order data
                        orderData=Orders.objects.filter(id=orderId,delete=0).update(OrderStatus=4) 

                        # orderdisplay=orders.objects.filter(id=orderId,delete=0)
                        # filter=json.loads(serializers.serialize("json",orderdisplay))
                  
                        # for cdetail in filter:
                        #     cdetail["fields"]["userId"]   
                              
                        #update chat in order status
                         
                        chatDetail=chat.objects.filter(id=chatId,delete=0).update(driverstatus=3)
                        #wallet history insert data
                        walletHistoryInsert=walletHistory(transporterId=transporterId,userId=userId,orderId=orderId,amount=balance,action="CREDIT",msg="order payment")
                        walletHistoryInsert.save()   
                        #insert balance
                        customerData=customers.objects.filter(id=transporterId,delete=0)
                        customerDatafilter=json.loads(serializers.serialize("json",customerData))
                        for cdetail in customerDatafilter:
                            cdetail["fields"]["walletamount"]
                        # print(cdetail["fields"]["walletamount"]+float(balance))

                            customerData=customers.objects.filter(id=transporterId,delete=0).update(walletamount=cdetail["fields"]["walletamount"]+float(balance)) 

                        orderResponse ={
                            "status":"200",
                            "message":"Order Completed",
                            "orderId":orderId,
                            "userId":userId
                            }
                            
                        return JsonResponse(orderResponse, safe=False)
                    
                    else:
                        orderResponse ={
                            "status":"400",
                            "message":"Order not Found"
                            
                            }
                        return JsonResponse(orderResponse, safe=False)
            

                except:
                    orderResponse = {
                        "status": "400",
                        "message": "Somithing Went wrong!!",
                    }
                    return JsonResponse(orderResponse, safe=False)
        else:
            orderResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(orderResponse, safe=False)
    else:
        orderResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(orderResponse, safe=False)   
        
        