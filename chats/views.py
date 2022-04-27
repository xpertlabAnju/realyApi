from asyncio import transports
from django.shortcuts import render
from django.core import serializers
import json

from .models import chat
from customers.models import customers
from orders.models import Orders
from orders.models import Orderdetails
from chatDetails.models import chatDetails
from django.http import JsonResponse
import dateutil.parser

# order Accept with chat
def order_request_chat(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
             # get parameter values
            # data = json.loads(request.body.decode("utf-8"))
            # print(request.body)
            chatResponse={}
            data=json.loads(request.body)
            
            userId = data.get('userid')
            orderId = data.get('orderid')
            driverId = data.get('driverid')
            msg = data.get('msg')   
            # time = data.get('time')
             # all parameters Required conditions
            if userId == '':
                chatResponse = {
                    "status": "400",
                    "message": "userId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif orderId == '':
                chatResponse = {
                    "status": "400",
                    "message": "orderId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif driverId == '':
                chatResponse = {
                    "status": "400",
                    "message": "driverId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif msg == '':
                chatResponse = {
                    "status": "400",
                    "message": "Message is Required",
                }
                return JsonResponse(chatResponse, safe=False)
           
            else:
                try:
                    userObject = customers.objects.filter(delete='0', id=userId, status='0', type=0).count()
                
                    if userObject > 0:
                        # check order are exits or not 
                        checkOrder = Orders.objects.filter(id=orderId,delete='0',userId=userId, statusFromUser=0,OrderStatus=0).count()
                        # print(checkOrder)
                        if checkOrder != 0:
                            # check chat
                            checkChat = chat.objects.filter(orderId=orderId, userId=userId,transporterId=driverId,delete='0').count()
                            # print(checkChat)
                            if checkChat !=0:
                                #get order data
                                chatData=chat.objects.filter(orderId=orderId,
                                                    userId=userId,
                                                    transporterId=driverId,
                                                    delete='0')
                                filter=json.loads(serializers.serialize( "json",chatData))
                               
                            #insert chat detail
                                for j in filter:
                                    chatId=json.loads(json.dumps(j['pk']))                                
                                   
                                    chatDetailInsert=chatDetails(chatId=chatId,senderId=driverId,receiverId=userId,senderType="TRANSPORTER",receiverType="USER",message=msg)
                                    chatDetailInsert.save()

                                    chatResponse = {
                                    "status": "200",
                                    "message": "Chat is inserted Successful",
                                    "chatId":chatId
                                    }
                                    return JsonResponse(chatResponse, safe=False)

                        
                            else:                                    
                                chatInsert = chat(
                                    orderId=orderId,
                                    transporterId=driverId,
                                    userId=userId
                                    )
                                chatInsert.save()


                                lastChat=chatInsert.id  # last inserted id

                                for key in msg:
                                    # print(key)
                                    chatDetailInsert=chatDetails(chatId=lastChat,senderId=driverId,receiverId=userId,senderType="TRANSPORTER",receiverType="USER",message=key["message"])
                                    chatDetailInsert.save()

                                chatResponse = {
                                    "status": "200",
                                    "message": "Chat is inserted Successful",
                                    "chatId":lastChat
                                    }
                                return JsonResponse(chatResponse, safe=False)
                        else:


                            chatResponse = {
                                "status": "400",
                                "message": "Order is not exits"
                            }
                            return JsonResponse(chatResponse, safe=False)
                    else:
                       
                        chatResponse = {
                            "status": "400",
                            "message": "User not found"
                        }
                        return JsonResponse(chatResponse, safe=False)

                except:
                    chatResponse = {
                        "status": "400",
                        "message": "Somthing went wrong",
                    }
                    return JsonResponse(chatResponse, safe=False)

        else:
            chatResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(chatResponse, safe=False)
    else:
        chatResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(chatResponse, safe=False)

# show chat

def show_chat(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # get parameter values
            data=json.loads(request.body)
            
            orderId = data.get('orderid')
            driverId = data.get('driverid')
            
            
             # all parameters Required conditions
            if orderId == '':
                chatResponse = {
                    "status": "400",
                    "message": "orderId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif driverId == '':
                chatResponse = {
                    "status": "400",
                    "message": "driverId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            else:
                try:
                    dataArr=[]
                    orderArr=[]
                    #chat are exists or not
                    checkChat = chat.objects.filter(orderId=orderId,transporterId=driverId,delete='0').count()
                
                    if checkChat > 0:

                        #get order data
                        orderDetail = Orderdetails.objects.filter(orderid=orderId,delete='0').order_by("created")
                        orderJs=json.loads((serializers.serialize("json", orderDetail)))
                        for odata in orderJs:

                            # odata["fields"]["messagetime"]=(dateutil.parser.isoparse(odata["fields"]["messagetime"])).strftime("%b %d %H:%M %p")
                           
                            orderArr.append(odata["fields"])
                           
                            userObject = customers.objects.filter(delete='0',id=odata["fields"]["userId"],status=0,type=0) #get user name
                            json_data = json.loads(serializers.serialize( "json",userObject))

                            for userd in json_data:
                                odata["fields"]["firstname"]=json.loads(json.dumps(userd["fields"]["firstname"]))
                               
                        #getchat data
                        chatData = chat.objects.filter(orderId=orderId,transporterId=driverId,delete='0')
                        orderserializeJs=json.loads((serializers.serialize("json",chatData)))
                       
                        for chatarr in orderserializeJs:
                           
                            chatId=chatarr["pk"]
                            driverstatus=json.loads(json.dumps(chatarr["fields"]["driverstatus"]))
                           
                            # print(chatarr["fields"]["driverstatus"])
                          
                            chatDetail = chatDetails.objects.filter(chatId=chatId,delete='0').order_by("created")
                            serializeJs=json.loads((serializers.serialize("json", chatDetail)))
                            for j in serializeJs:
                                
                                userObject = customers.objects.filter(delete='0',id=j["fields"]["senderId"],status=0) #get customer data
                                json_data = json.loads(serializers.serialize( "json",userObject))

                                for ud in json_data:
                                    json.loads(json.dumps(ud["fields"]))
                                
                                j["fields"]["time"]= (dateutil.parser.isoparse(j["fields"]["created"])).strftime("%b %d %H:%M %p")
                                j["fields"]["firstname"]=ud["fields"]["firstname"]
                                j["fields"]["chatDetailID"]=j["pk"]
                                dataArr.append(j["fields"])
                               
                            chatResponse = {
                            "status": "200",
                            "message": "successfully",
                            "driverStatus":chatarr["fields"]["driverstatus"],
                            "data":dataArr,
                            "orderArr":orderArr

                            }
                            return JsonResponse(chatResponse, safe=False)
                       
                    else:
                       #check order are exists or not
                        checkOrder = Orders.objects.filter(id=orderId,delete='0').count()
                       
                        if checkOrder > 0:
                        #get order detail
                            orderDetail = Orderdetails.objects.filter(orderid=orderId,delete='0').order_by("created")
                            serializeJs=json.loads((serializers.serialize("json", orderDetail)))

                            for j in serializeJs:

                                # j["fields"]["messagetime"]=(dateutil.parser.isoparse(j["fields"]["messagetime"])).strftime("%b %d %H:%M %p")
                            
                                orderArr.append(j["fields"])
                                # print(orderArr)
                                #get user name
                                userObject = customers.objects.filter(delete='0',id=j["fields"]["userId"],status=0,type=0) 
                                json_data = json.loads(serializers.serialize( "json",userObject))

                                for ud in json_data:
                                    j["fields"]["firstname"]=json.loads(json.dumps(ud["fields"]["firstname"]))
                                   
                                
                            chatResponse = {
                                "status": "200",
                                "message": "successfully",
                                "driverStatus":"0",
                                "orderArr":orderArr
                            }
                            return JsonResponse(chatResponse, safe=False)  
                        else:
                            chatResponse = {
                                "status": "400",
                                "message": "Order  Not found",
                            }
                            return JsonResponse(chatResponse, safe=False)   
                        
                except:
                    chatResponse = {
                        "status": "400",
                        "message": "Somthing went wrong",
                    }
                    return JsonResponse(chatResponse, safe=False)

        else:
            chatResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(chatResponse, safe=False)
    else:
        chatResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(chatResponse, safe=False)   

        
        
def order_request_chat_final(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
             # get parameter values
            # data = json.loads(request.body.decode("utf-8"))
            # print(request.body)
            chatResponse={}
            data=json.loads(request.body)
            
            userId = data.get('userid')
            orderId = data.get('orderid')
            driverId = data.get('driverid')
            senderType=data.get('sendertype')
            receiverType=data.get('receivertype')
            msg = data.get('msg')   
            # time = data.get('time')
             # all parameters Required conditions
            if userId == '':
                chatResponse = {
                    "status": "400",
                    "message": "userId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif orderId == '':
                chatResponse = {
                    "status": "400",
                    "message": "orderId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif driverId == '':
                chatResponse = {
                    "status": "400",
                    "message": "driverId is Required",
                }
                return JsonResponse(chatResponse, safe=False)

            elif senderType == '':
                chatResponse = {
                    "status": "400",
                    "message": "senderType is Required",
                }
                return JsonResponse(chatResponse, safe=False)

            elif receiverType == '':
                chatResponse = {
                    "status": "400",
                    "message": "ReceiverType is Required",
                }
                return JsonResponse(chatResponse, safe=False)

            elif msg == '':
                chatResponse = {
                    "status": "400",
                    "message": "Message is Required",
                }
                return JsonResponse(chatResponse, safe=False)
           
            else:
                try:
                    userObject = customers.objects.filter(delete='0', id=userId, status='0', type=0).count()
                
                    if userObject > 0:
                        # check order are exits or not 
                        checkOrder = Orders.objects.filter(id=orderId,delete='0',userId=userId, statusFromUser=0,OrderStatus=0).count()
                        # print(checkOrder)
                        if checkOrder != 0:
                            # check chat
                            checkChat = chat.objects.filter(orderId=orderId, userId=userId,transporterId=driverId,delete='0').count()
                            # print(checkChat)
                            if checkChat !=0:
                                #get order data
                                chatData=chat.objects.filter(orderId=orderId,
                                                    userId=userId,
                                                    transporterId=driverId,
                                                    delete='0')
                                filter=json.loads(serializers.serialize( "json",chatData))
                               
                            #insert chat detail
                                for j in filter:
                                    chatId=json.loads(json.dumps(j['pk']))                                
                                   
                                    if senderType == "USER":
                                        senderId=userId
                                        receiverId=driverId
                                    else:
                                        senderId=driverId
                                        receiverId=userId

                                    chatDetailInsert=chatDetails(chatId=chatId,senderId=senderId,receiverId=receiverId,senderType=senderType,receiverType=receiverType,message=msg)
                                    chatDetailInsert.save()

                                    chatResponse = {
                                    "status": "200",
                                    "message": "Chat is inserted Successful",
                                    "chatId":chatId
                                    }
                                    return JsonResponse(chatResponse, safe=False)

                        
                            else:                                    
                                chatInsert = chat(
                                    orderId=orderId,
                                    transporterId=driverId,
                                    userId=userId
                                    )
                                chatInsert.save()


                                lastChat=chatInsert.id  # last inserted id

                                for key in msg:
                                    # print(key)
                                    chatDetailInsert=chatDetails(chatId=lastChat,senderId=driverId,receiverId=userId,senderType=senderType,receiverType=receiverType,message=msg)
                                    chatDetailInsert.save()

                                chatResponse = {
                                    "status": "200",
                                    "message": "Chat is inserted Successful",
                                    "chatId":lastChat
                                    }
                                return JsonResponse(chatResponse, safe=False)
                        else:


                            chatResponse = {
                                "status": "400",
                                "message": "Order is not exits"
                            }
                            return JsonResponse(chatResponse, safe=False)
                    else:
                       
                        chatResponse = {
                            "status": "400",
                            "message": "User not found"
                        }
                        return JsonResponse(chatResponse, safe=False)

                except:
                    chatResponse = {
                        "status": "400",
                        "message": "Somthing went wrong",
                    }
                    return JsonResponse(chatResponse, safe=False)

        else:
            chatResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(chatResponse, safe=False)
    else:
        chatResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(chatResponse, safe=False)
        
        
#confirm Price
def confirm_price(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data=json.loads(request.body)
            chatResponse={}

            orderId = data.get('orderid')
            driverId = data.get('driverid')
            price=data.get('price')
             # all parameters Required conditions
            if orderId == '':
                chatResponse = {
                    "status": "400",
                    "message": "orderId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif driverId == '':
                chatResponse = {
                    "status": "400",
                    "message": "driverId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif price == '':
                chatResponse = {
                    "status": "400",
                    "message": "Price is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            else:
                try:
                   
                    checkChat = chat.objects.filter(orderId=orderId,transporterId=driverId,delete='0').count()
                
                    if checkChat > 0:
                        chatData = chat.objects.filter(orderId=orderId,transporterId=driverId,delete='0').update(amount=price)

                        chattableDqata = chat.objects.filter(orderId=orderId,transporterId=driverId,delete='0')
                        json_data = json.loads(serializers.serialize( "json",chattableDqata))

                        for j in json_data:
                            userId=json.loads(json.dumps(j["fields"]['userId']))
                            chatId=json.loads(json.dumps(j["pk"]))

                        chatDetailInsert=chatDetails(chatId=chatId,senderId=driverId,receiverId=userId,senderType="TRANSPORTER",receiverType="USER",message=price,messagetype="price")
                        chatDetailInsert.save()

                        chatResponse = {
                            "status": "200",
                            "message": "successfully"
                            
                            }
                        return JsonResponse(chatResponse, safe=False)
                       
                    else:
                       
                        chatResponse = {
                            "status": "400",
                            "message": "Chat  Not found",
                        }
                        return JsonResponse(chatResponse, safe=False)   
                except:
                    chatResponse = {
                        "status": "400",
                        "message": "Somthing went wrong",
                    }
                    return JsonResponse(chatResponse, safe=False)

        else:
            chatResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(chatResponse, safe=False)
    else:
        chatResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(chatResponse, safe=False)   
        


#start chat 
def start_chat(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # get parameter values
       
            chatResponse={}
            data=json.loads(request.body)
            
            userId = data.get('userid')
            orderId = data.get('orderid')
            driverId = data.get('driverid')
           
            # all parameters Required conditions
            if userId == '':
                chatResponse = {
                    "status": "400",
                    "message": "userId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif orderId == '':
                chatResponse = {
                    "status": "400",
                    "message": "orderId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            elif driverId == '':
                chatResponse = {
                    "status": "400",
                    "message": "driverId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
          
            else:
                try:
                    #user sra exists or not
                    userObject = customers.objects.filter(delete='0', id=userId, status='0', type=0).count()
                
                    if userObject > 0:
                        # check order are exits or not 
                        checkOrder = Orders.objects.filter(id=orderId,delete='0',userId=userId, statusFromUser=0,OrderStatus=0).count()
                      
                        if checkOrder != 0:
                        
                            try:
                                # check order are exits or not 
                                checkChat= chat.objects.filter(orderId=orderId,
                                                    transporterId=driverId,
                                                    userId=userId,
                                                    driverstatus=1).count()
                               
                                if checkChat == 0:

                                    chatInsert = chat(
                                                        orderId=orderId,
                                                        transporterId=driverId,
                                                        userId=userId,
                                                        driverstatus=1
                                                        )
                                    chatInsert.save()
                                    chatResponse = {
                                        "status": "200",
                                        "message": "Order Request Accepted",
                                
                                    }
                                    return JsonResponse(chatResponse, safe=False)

                                else:
                                    chatResponse = {
                                        "status": "400",
                                        "message": "chat already exists",
                                
                                    }
                                    return JsonResponse(chatResponse, safe=False)
                            except:
                                chatResponse = {
                                    "status": "400",
                                    "message": "Order req failed",
                                }
                                return JsonResponse(chatResponse, safe=False)    
                           
                        else:


                            chatResponse = {
                                "status": "400",
                                "message": "Order is not exits"
                            }
                            return JsonResponse(chatResponse, safe=False)
                    else:
                       
                        chatResponse = {
                            "status": "400",
                            "message": "User not found"
                        }
                        return JsonResponse(chatResponse, safe=False)

                except:
                    chatResponse = {
                        "status": "400",
                        "message": "Somthing went wrong",
                    }
                    return JsonResponse(chatResponse, safe=False)

        else:
            chatResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(chatResponse, safe=False)
    else:
        chatResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(chatResponse, safe=False)

#withdraw_order
def withdraw_order(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data=json.loads(request.body)
            chatResponse={}

            chatDetailId = data.get('chatdetailid')
          
            # all parameters Required conditions
            if chatDetailId == '':
                chatResponse = {
                    "status": "400",
                    "message": "chatDetailId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            
            else:
                try:
                   
                    checkChat = chatDetails.objects.filter(id=chatDetailId,delete='0',chatOrderStatus=0).count()
                
                    if checkChat > 0:
                        # print(checkChat)
                        chatData = chatDetails.objects.filter(id=chatDetailId,delete='0',chatOrderStatus=0).update(chatOrderStatus=1)

                        chatResponse = {
                            "status": "200",
                            "message": "Order withdraw successfully"
                            
                            }
                        return JsonResponse(chatResponse, safe=False)
                       
                    else:
                       
                        chatResponse = {
                            "status": "400",
                            "message": "Chat  Not found",
                        }
                        return JsonResponse(chatResponse, safe=False)   
                except:
                    chatResponse = {
                        "status": "400",
                        "message": "Somthing went wrong",
                    }
                    return JsonResponse(chatResponse, safe=False)

        else:
            chatResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(chatResponse, safe=False)
    else:
        chatResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(chatResponse, safe=False)   
        
#decline_order
def decline_order(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data=json.loads(request.body)
            chatResponse={}

            chatDetailId = data.get('chatdetailid')
          
            # all parameters Required conditions
            if chatDetailId == '':
                chatResponse = {
                    "status": "400",
                    "message": "chatDetailId is Required",
                }
                return JsonResponse(chatResponse, safe=False)
            
            else:
                try:
                   
                    checkChat = chatDetails.objects.filter(id=chatDetailId,delete='0',chatOrderStatus=0).count()
                
                    if checkChat > 0:
                        # print(checkChat)
                        chatData = chatDetails.objects.filter(id=chatDetailId,delete='0',chatOrderStatus=0).update(chatOrderStatus=3)

                        chatResponse = {
                            "status": "200",
                            "message": "Order decline successfully"
                            
                            }
                        return JsonResponse(chatResponse, safe=False)
                       
                    else:
                       
                        chatResponse = {
                            "status": "400",
                            "message": "Chat  Not found",
                        }
                        return JsonResponse(chatResponse, safe=False)   
                except:
                    chatResponse = {
                        "status": "400",
                        "message": "Somthing went wrong",
                    }
                    return JsonResponse(chatResponse, safe=False)

        else:
            chatResponse = {
                "status": "400",
                "message": "Authentication failed!!",
            }
            return JsonResponse(chatResponse, safe=False)
    else:
        chatResponse = {
            "status": "400",
            "message": "Somthing went wrong",
        }
        return JsonResponse(chatResponse, safe=False)   

