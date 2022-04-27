
from django.core import serializers
import json
from .models import customers 
# from rest_framework import generics
# from .serializers import CustomerSerializer
from django.http import JsonResponse
import hashlib
import datetime
import math, random
from django.core.files.storage import FileSystemStorage
import os
import datetime


#mail lib


import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




current_datetime = datetime.datetime.now()  


# mail function
def SendEmail(request, SenderEmail,OTP):
    
	sender_email =  'xpertlab.uday@gmail.com'
	receiver_email =SenderEmail
	password = 'P(13xpertu'
	msg = MIMEMultipart("alternative")
	msg["Subject"] = "OTP for Relay Admin Penal"
	msg["From"] = sender_email
	msg["To"] = receiver_email
	html =''' <!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title></title>
       
    </head>
    <body>
        <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
            <div style="margin:50px auto;width:70%;padding:20px 0">
              <div style="border-bottom:1px solid #eee">
                <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Relay</a>
              </div>
              <p style="font-size:1.1em">Hi,</p>
              <p>Use the following OTP to Reset Password</p>
              <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">'''+str(OTP)+'''</h2>
              <p style="font-size:0.9em;">Regards,<br />Relay</p>
              <hr style="border:none;border-top:1px solid #eee" />
            </div>
          </div>
    </body>
</html>'''
 
 

 
 
 
	part = MIMEText(html, "html")
	msg.attach(part)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		try:
			server.sendmail(
				sender_email, receiver_email, msg.as_string()
			)
			return ("Successfully sent email")
		except:
			return ("failed")


#otp generate function
def generateOTP() :
     digits = "123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


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

                        # try:
                            insertQuery = customers(lastname=fullname,firstname=fullname,email=email,password=h,profilepic="http://216.10.247.209:8083/static/media/default.jpg")
                            insertQuery.save() #Inasertquery save
                            
                            customer ={
                                    "status":"200",
                                    "message":"Registration Successful"  
                                    }
                            return JsonResponse(customer,safe=False)
                        # except:
                           
                        #     customer ={
                        #         "status":"400",
                        #         "message":"Somthing went wrong.."  
                        #         }
                        #     return JsonResponse(customer,safe=False)
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
            # get parameter values
            data = json.loads(request.body.decode("utf-8"))
            email = data.get('email')
            # all parameters requried conditions
            if email == '':
                customer ={
                    "status":"400",
                    "message":"Email is Requried",
                }
                return JsonResponse(customer,safe=False)
           
            else: 
                try:
                    # otp generate function call
                    userOtp = random.randint(1111,9999)
                    # select customer data
                    userData = customers.objects.filter(delete=0,email=email,status=0)
                    json_data =json.loads(serializers.serialize( "json",userData))
                    
                    for j in json_data:
                        userId=json.loads(json.dumps(j['pk']))
                    # update customer data
                        if id != None:
                            customers.objects.filter(id=userId).update(otp=userOtp)

                            # email function call
                            EmailStatus = SendEmail(request, email,userOtp)

                            customer ={
                                "status":"200",
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
                        userObject = customers.objects.filter(delete='0',id=userid,status=0)
                        json_data = json.loads(serializers.serialize( "json",userObject))
        
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
            # get parameter values
            data = json.loads(request.body.decode("utf-8"))
            userid = data.get('userid')
            fullname=data.get('fullname')
            email = data.get('email')
            dob = data.get('dob')

            customerdata=[]
            # all parameters requried conditions
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
                    if userObject == 1 :
                      
                        # update Query
                        userProfile=customers.objects.filter(delete='0',id=userid,status=0).update(firstname=fullname,dob=dob,email=email)
                        
                        userObject = customers.objects.filter(delete='0',id=userid,status=0) #get customer data
                        json_data = json.loads(serializers.serialize( "json",userObject))

                        for j in json_data:
                            j["fields"]["type"]
                        #return response
                        customer ={
                            "status":"200",
                            "userid":userid,  
                            "type":j["fields"]["type"],
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


        

#change Password
def changepassword(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            data = json.loads(request.body.decode("utf-8"))
            userid=data.get('userid')
            oldpassword = data.get('oldpassword')
            newpassword=data.get('newpassword')
            confirmpassword=data.get('confirmpassword')
            passwordCompare=(newpassword == confirmpassword)
            if newpassword == '':
                customer ={
                    "status":"400",
                    "message":"New Password is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif confirmpassword == '':
                customer ={
                    "status":"400",
                    "message":"Re-type Password Required",
                }
                return JsonResponse(customer,safe=False)
            elif oldpassword == '':
                customer ={
                    "status":"400",
                    "message":"Old Password Required",
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
                    h = hashlib.md5(newpassword.encode()).hexdigest() #password convert md5
                    oldpasswordmd5 = hashlib.md5(oldpassword.encode()).hexdigest() #password convert md5
                    userData = customers.objects.filter(delete=0,id=userid,status=0,password=oldpasswordmd5).count()
                    
                    if userData > 0:

                        customers.objects.filter(id=userid).update(password=h)
                        customer ={
                        "status":"200",
                        "message":"Password changed Successfully",
                        
                        }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                                "status":"400",
                                "message":"Old password not match .."  
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

# become dirver
def become_driver(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            userid=request.POST.get('userid')
            filename = request.FILES.get('filename')
            
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"Userid is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif filename == '':
                customer ={
                    "status":"400",
                    "message":"Uploadid is Required",
                }
                return JsonResponse(customer,safe=False)
            
            else: 
                
                    
                    userData = customers.objects.filter(delete=0,id=userid,status=0).count()
                   
                    if userData > 0:
                        try:
                            fs = FileSystemStorage(location="static/media/")
                            file = fs.save(filename.name, filename)

                            ext="."+(file).split(".")[-1]
                            # filenm=(file).split(".")[0]
                            date=datetime.datetime.now().strftime("%I%M%p%B%d%Y")
                            temp="document"+date+ext

                            os.rename("static/media/"+file ,"static/media/"+temp)

                            customers.objects.filter(id=userid).update(isrequested=1,document="http://216.10.247.209:8083/static/media/"+temp,updated=current_datetime)
                            customer ={
                            "status":"200",
                            "message":"Driver created Successfully",
                            
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
                                "message":"User not Found.."  
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




# check customer or driver
def check_customer_or_not(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":

            userdata = json.loads(request.body.decode("utf-8"))
            userid=userdata.get('userid')
            # data=[]           
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"Userid is Requried",
                }
                return JsonResponse(customer,safe=False)
                      
            else: 
                try:
                    userData = customers.objects.filter(delete=0,id=userid,status=0).count()
                    # print(userid)
                    if userData > 0:
                        userObject = customers.objects.filter(delete='0',id=userid,status=0)
                        json_data = json.loads(serializers.serialize( "json",userObject))

                        for j in json_data:
                            data=(json.loads(json.dumps(j["fields"]["type"])))
                        if data == 0 :
                            type="Customer"
                        else :
                            type="Driver"
                        customer ={
                            "status":"200",
                            "message":"Successfull",
                            "type":type,
                            
                        }
                        return JsonResponse(customer,safe=False)
                    else:
                        customer ={
                                "status":"400",
                                "message":"User not Found.."  
                                }
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

# Edit Image 
def edit_image(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # get parameter values
            userid=request.POST.get('userid')
            filename = request.FILES.get('filename')
            # all parameters requried conditions
            if userid == '':
                customer ={
                    "status":"400",
                    "message":"Userid is Requried",
                }
                return JsonResponse(customer,safe=False)
            elif filename == '':
                customer ={
                    "status":"400",
                    "message":"Profile Image is Required",
                }
                return JsonResponse(customer,safe=False)
            
            else: 
                
                    
                    userData = customers.objects.filter(delete=0,id=userid,status=0).count()#check user exists or not 
                   
                    if userData > 0:
                        try:
                            fs = FileSystemStorage(location="static/media/")
                            file = fs.save(filename.name, filename) #image save to directory

                            ext="."+(file).split(".")[-1] #split image extension
                            date=datetime.datetime.now().strftime("%I%M%p%B%d%Y") #image unique name generate
                            temp="profile"+date+ext 

                            os.rename("static/media/"+file ,"static/media/"+temp) #rename image
                            #update customer Query
                            customers.objects.filter(id=userid).update(profilepic="http://216.10.247.209:8083/static/media/"+temp)

                            customer ={
                            "status":"200",
                            "message":"Profile Image Change Successfully",
                            "profileImage":temp,
                            
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
                                "message":"User not Found.."  
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

#All Driver List
def all_driver(request):
        
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            # data = json.loads(request.body.decode("utf-8"))
                       
                try: 

                    userData = customers.objects.filter(delete=0,status=0,type=1).count()
                    
                    if userData > 0:
                        mainData=[]
                        
                        userData = customers.objects.filter(delete=0,status=0,type=1)
                        json_data =json.loads(serializers.serialize( "json",userData))
                        # print(userData)
                      
                        for j in json_data:
                            driver={}
                           
                            driver["firstname"]=(json.loads(json.dumps(j["fields"]["firstname"])))
                            driver["userid"]=j["pk"]
                            
                            mainData.append(driver)
                            # print(driver["firstname"])
                    
                        order ={
                            "status":"200",
                            "message":"successfully",
                            "data":mainData
                
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
