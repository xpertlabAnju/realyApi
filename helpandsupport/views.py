from django.core import serializers
import json
from .models import helpandsupport
from customers.models import customers
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
import datetime

# current date time dispaly
current_datetime = datetime.datetime.now()  

# help_and_support
def help_and_support(request):
    if request.method == 'POST':
        if request.headers["Apitoken"] == "391a7704a49d9dc3209ced10c55c8dc6":
            
            # data = json.loads(request.body.decode("utf-8"))
            filename= request.FILES.get('filename')
            subject = request.POST.get('subject')
            description = request.POST.get('description')
            userid= request.POST.get('userid')
            
            if filename == '':
                helpdata ={
                    "status":"400",
                    "message":"Filename is Requried",
                }
                return JsonResponse(helpdata,safe=False)
            elif subject == '':
                helpdata ={
                    "status":"400",
                    "message":"Subject is Requried",
                }
                return JsonResponse(helpdata,safe=False)
            elif description == '':
                helpdata ={
                    "status":"400",
                    "message":"Description is Requried",
                }
                return JsonResponse(helpdata,safe=False)
            elif userid == '':
                helpdata ={
                    "status":"400",
                    "message":"Userid is Requried",
                }
                return JsonResponse(helpdata,safe=False)
           
            else: 
               
                try:
                    userCounts = customers.objects.filter(delete=0,id=userid,status=0).count() #count customer data
                   
                    if userCounts > 0 :
                        try:
                            fs = FileSystemStorage(location="static/media/")
                            file = fs.save(filename.name, filename)

                            ext="."+(file).split(".")[-1]
                            # filenm=(file).split(".")[0]
                            date=datetime.datetime.now().strftime("%I%M%p%B%d%Y")
                            temp="help"+date+ext

                            os.rename("static/media/"+file ,"static/media/"+temp)
                            insertQuery = helpandsupport(subject=subject,description=description,customerId=userid,fileName="http://216.10.247.209:8083/static/media/"+temp,created=current_datetime,updated=current_datetime)
                            insertQuery.save() 
                            
                            helpdata ={
                                "status":"200",
                                "message":"Help And Support Inserted Successfully",
                            }
                            return JsonResponse(helpdata,safe=False)
                        except:
                            helpdata ={
                                "status":"400",
                                "message":"Help And Support not Inserted", 
                            }
                            return JsonResponse(helpdata,safe=False)
                    else:

                        helpdata ={
                            "status":"400",
                            "message":"User not found",
                        }
                        return JsonResponse(helpdata,safe=False)
                except:
                    helpdata ={
                        "status":"400",
                        "message":"Somthing went wrong",
                    }
                    return JsonResponse(helpdata,safe=False)
        else: 
            helpdata ={
                "status":"400",
                "message":"Authentication failed!!",
            }
            return JsonResponse(helpdata,safe=False)
    else: 
        helpdata ={
            "status":"400",
            "message":"Somthing went wrong",
            }
        return JsonResponse(helpdata,safe=False)