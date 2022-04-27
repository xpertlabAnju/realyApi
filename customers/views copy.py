from itertools import count
from pickle import NONE
from string import digits
from urllib import response
from django.shortcuts import render
from django.http import  Http404
from django.core import serializers
import json
from .models import customers 
from rest_framework import generics
from .serializers import CustomerSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
import hashlib
import datetime
import math, random
from django.db.models import Q

current_datetime = datetime.datetime.now()  

# Create your views here.
class CustomerDetail(generics.RetrieveAPIView):
    # API endpoint that returns a single customer by pk.
    queryset = customers.objects.all()
    serializer_class = CustomerSerializer

#otp generate function
def generateOTP() :
     digits = "123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

# all customer dispaly
def customer(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
          
            data=[]
       
            try:
                userObject = customers.objects.filter(delete='0',status= 0)
                json_data = json.loads(serializers.serialize( "json",userObject))

                for j in json_data:
                    data.append(json.loads(json.dumps(j["fields"])))
                customer ={
                    "status":"200",
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

# LogIn Customer 
def customer_signin(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data = json.loads(request.body.decode("utf-8"))
            email = data.get('email')
            password = data.get('password')

            if email == '':
                customer ={
                    "status":"400",
                    "message":"Email is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif password == '':
                customer ={
                    "status":"400",
                    "message":"Password is Requried",
                }
                return JsonResponse(customer,safe=False)

            else: 
                try:
                    h = hashlib.md5(password.encode()).hexdigest()
                    # userCounts = customers.objects.filter(type=0, delete=0,email=email,password=h).count()
                    userObject = customers.objects.get(delete=0,email=email,status=0)
                    id=userObject.id
                    if userObject.password == h:
                        customer ={
                        "status":"200",
                        "message":"Login Successful",
                        "userid":id,
                        "fullname":userObject.firstname
                        }
                        return JsonResponse(customer,safe=False)
                    else:
                        
                        customer ={
                            "status":"200",
                            "message":"Password is Wrong!"  
                            }
                        return JsonResponse(customer,safe=False)
                except:
                    customer ={
                    "status":"400",
                    "message":"User not found",
                    }
                    return JsonResponse(customer,safe=False)
        else: 
            customer ={
                "status":"200",
                "message":"Authentication failed!!",
            }
            return JsonResponse(customer,safe=False)
    else: 
        customer ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(customer,safe=False)

# Customer SignUp
def customer_signup(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data = json.loads(request.body.decode("utf-8"))
            fullname=data.get('fullname')
            email = data.get('email')
            password = data.get('password')
            confirmpassword=data.get('confirmpassword')
            passwordCompare=(password == confirmpassword)
            # otp=generateOTP()
            # print(otp)
           
            if fullname == '':
                customer ={
                    "status":"400",
                    "message":"Fullname is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif email == '':
                customer ={
                    "status":"400",
                    "message":"Email is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif password == '':
                customer ={
                    "status":"400",
                    "message":"Password is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif confirmpassword == '':
                customer ={
                    "status":"400",
                    "message":"Confirm Password Required",
                }
                return JsonResponse(customer,safe=False)
            elif passwordCompare != True :
               
                customer ={
                    "status":"400",
                    "message":"Password not match...",
                }
                return JsonResponse(customer,safe=False)
            else: 
                try:
                    # print(current_datetime)
                    h = hashlib.md5(password.encode()).hexdigest() #password convert md5
                    userCounts = customers.objects.filter(delete=0,email=email,status=0).count() #count customer data
                   
                    if userCounts > 0 :
                        customer ={
                        "status":"400",
                        "message":"Email is alreay Exits"
                        }
                        return JsonResponse(customer,safe=False)
                    else:

                        try:
                            insertQuery = customers(lastname=fullname,firstname=fullname,email=email,password=h,profilepic="images.jpg")
                            insertQuery.save() #Inasertquery save
                            
                            customer ={
                                    "status":"200",
                                    "message":"Registration Successful"  
                                    }
                            return JsonResponse(customer,safe=False)
                        except:
                           
                            customer ={
                                "status":"400",
                                "message":"Somthing went wrong.."  
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
                "status":"200",
                "message":"Authentication failed!!",
            }
            return JsonResponse(customer,safe=False)
    else: 
        customer ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(customer,safe=False)

# forgot password
def forgotpassword(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data = json.loads(request.body.decode("utf-8"))
            email = data.get('email')
            
            if email == '':
                customer ={
                    "status":"400",
                    "message":"Email is Requried",
                }
                return JsonResponse(customer,safe=False)
           
            else: 
                try:
                    # otp generate function call
                    userOtp=generateOTP()
                    userData = customers.objects.filter(delete=0,email=email,status=0)
                    json_data =json.loads(serializers.serialize( "json",userData))
                    # print(json.dumps(json_data['pk']))
                    for j in json_data:
                        userId=json.loads(json.dumps(j['pk']))
                    
                    if id != None:
                        customers.objects.filter(id=userId).update(otp=userOtp)
                        customer ={
                        "status":"400",
                        "message":"Otp Genearte successfully",
                        "userid":userId,
                        "otp":userOtp
                        }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                                "status":"400",
                                "message":"This user does not exist"  
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
                "status":"200",
                "message":"Authentication failed!!",
            }
            return JsonResponse(customer,safe=False)
    else: 
        customer ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(customer,safe=False)

#verify_otp
def verify_otp(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data = json.loads(request.body.decode("utf-8"))
            userid = data.get('userid')
            otp = data.get('otp')
            
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"CustomerId is Requried",
                }
                return JsonResponse(customer,safe=False)
           
            else: 
                try:
                    # otp generate function call
                    userOtp=generateOTP()
                    userData = customers.objects.filter(delete=0,id=userid,status=0,otp=otp)
                    json_data =json.loads(serializers.serialize( "json",userData))
                    # print(json.dumps(json_data['pk']))
                    for j in json_data:
                        userId=json.loads(json.dumps(j['pk']))
                    
                    if id != None:
                        customers.objects.filter(id=userId).update(otp=userOtp)
                        customer ={
                        "status":"400",
                        "message":"Otp is Verify Successfully",
                        
                        }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                                "status":"400",
                                "message":"OTP Incorrect"  
                                }
                        return JsonResponse(customer,safe=False)
                except:
                    customer ={
                    "status":"400",
                    "message":"UserId and Otp are wrong",
                    }
                    return JsonResponse(customer,safe=False)
        else: 
            customer ={
                "status":"200",
                "message":"Authentication failed!!",
            }
            return JsonResponse(customer,safe=False)
    else: 
        customer ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(customer,safe=False)

#reset Password
def reset_password(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data = json.loads(request.body.decode("utf-8"))
            userid=data.get('userid')
            password = data.get('password')
            confirmpassword=data.get('confirmpassword')
            passwordCompare=(password == confirmpassword)
            if password == '':
                customer ={
                    "status":"400",
                    "message":"Password is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif confirmpassword == '':
                customer ={
                    "status":"400",
                    "message":"Confirm Password Required",
                }
                return JsonResponse(customer,safe=False)
            elif passwordCompare != True :
               
                customer ={
                    "status":"400",
                    "message":"Password not match...",
                }
                return JsonResponse(customer,safe=False)
            else: 
                try:
                    h = hashlib.md5(password.encode()).hexdigest() #password convert md5

                    userData = customers.objects.filter(delete=0,id=userid,status=0).count()
                    
                    if userData > 0:

                        customers.objects.filter(id=userid).update(password=h)
                        customer ={
                        "status":"400",
                        "message":"Password  set Successfully",
                        
                        }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                                "status":"400",
                                "message":"This user does not exist"  
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
                "status":"200",
                "message":"Authentication failed!!",
            }
            return JsonResponse(customer,safe=False)
    else: 
        customer ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(customer,safe=False)

#show profile data
def view_profile(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
          
            userdata = json.loads(request.body.decode("utf-8"))
            userid = userdata.get('userid')
            data=[]
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"UserId is Requried",
                }
                return JsonResponse(customer,safe=False)
           
            else: 
                try:
                    userObject = customers.objects.filter(delete='0',id=userid,status=0).count()
                    if userObject > 0 :
                        userObject1 = customers.objects.filter(delete='0',id=userid,status=0)
                        json_data = json.loads(serializers.serialize( "json",userObject1))

                        for j in json_data:
                            data.append(json.loads(json.dumps(j["fields"])))
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

#update Profile
def edit_profile(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
          
            data = json.loads(request.body.decode("utf-8"))
            userid = data.get('userid')
            fullname=data.get('fullname')
            email = data.get('email')
            dob = data.get('dob')

            customerdata=[]

            if userid == '':
                customer ={
                    "status":"400",
                    "message":"UserId is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif fullname == '':
                customer ={
                    "status":"400",
                    "message":"Fullname is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif dob == '':
                customer ={
                    "status":"400",
                    "message":"Date of Birth is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif email == '':
                customer ={
                    "status":"400",
                    "message":"Email is Requried",
                }
                return JsonResponse(customer,safe=False)
            else: 
                try:
                    userObject = customers.objects.filter(delete='0',id=userid,status='0').count()
                    # print(userObject)
                    if userObject > 0 :
                        
                        # userEmail=customers.objects.raw('SELECT * FROM customers_customers WHERE  "delete"=0  AND "status"= 0 AND "id" != "'+userid+'" AND "email"="'+email+'"')
                        # print(userEmail)

                        userProfile=customers.objects.filter(delete='0',id=userid,status=0).update(firstname=fullname,dob=dob,email=email)

                        # userProfile=customers.objects.filter(delete='0',(~Q(id=3)),status=0)

                        customer ={
                            "status":"200",
                            "userid":userid,  
                            "message":"Profile Update Successfully" , 
                                 }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                            "status":"400",
                            "userid":userid,  
                            "message":"User not found"  
                              }
                        return JsonResponse(customer,safe=False)

                except:
                    customer ={
                    "status":"400",
                    "message":"Email is alreay Exits",
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
#become driver
def become_driver(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
          
            data = json.loads(request.body.decode("utf-8"))
            userid = data.get('userid')
            document=data.get('document')
          
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"UserId is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif document == '':
                customer ={
                    "status":"400",
                    "message":"Documentis Requried",
                }
                return JsonResponse(customer,safe=False)
           
            else: 
                try:
                    userObject = customers.objects.filter(delete='0',id=userid,status='0').count()
                   
                    if userObject > 0 :
                        
                        userProfile=customers.objects.filter(delete='0',id=userid,status=0).update(document=fullname,type=1)

                        customer ={
                            "status":"200",
                            "message":"Uploadid Update Successfully" , 
                                 }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                            "status":"400",
                            "message":"User not found"  
                              }
                        return JsonResponse(customer,safe=False)

                except:
                    customer ={
                    "status":"400",
                    "message":"Uer Not found",
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

