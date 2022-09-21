from cProfile import label
from http.client import HTTPResponse
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import re
from django.shortcuts import render
from django import forms
from datetime import datetime,date

province_list=((1,"Alberta"),(2,"British Columbia"),(3,"Manitoba"),(4,"New Brunswick"),(5,"Newfoundland and Labrador"),(6,"Nova Scotia"),(7,"Ontario"),(8,"Prince Edward Island"),(9,"Quebec"),(10,"Saskatchewan"),(11,"Northwest Territories"),(12,"Nunavut"),(13,"Yukon"))
class NewAppForm(forms.Form):
    fname=forms.CharField(label="First Name")
    mname=forms.CharField(label="Middle Name")#, blank=True)
    lname=forms.CharField(label="Last Name")#, blank=True)#show dialog box if blank
    date=forms.DateField(label="Date")
    addr1=forms.CharField(label="Address Line 1")
    addr2=forms.CharField(label="Address Line 2")#,blank=True)
    city=forms.CharField(label="City")
    province=forms.MultipleChoiceField(label="Province/Territory",choices=province_list)
    postal=forms.CharField(label="Postal code")#validate format
    tel=forms.CharField(label="Telephone #")
    tel2=forms.CharField(label="Other Telephone #")#,blank=True)
    email=forms.CharField(label="E-mail")#check if valid address
    reffered=forms.CharField(label="Reffered by")

def index(request): 
    if request.method=="POST":
        if "data" not in request.session:
            request.session["data"]=[]
        appform=NewAppForm(request.POST)
        if appform.is_valid(): #serverside verification
            request.session["data"]=[] #clear previous form data
            for f in appform.cleaned_data:
                if isinstance(appform.cleaned_data[f],date):
                    appform.cleaned_data[f] = appform.cleaned_data[f].strftime("%m/%d/%Y")
                #if isinstance(appform.cleaned_data[f],int):
                #appform.cleaned_data["province"]=province_list[appform.cleaned_data["province"]]
                request.session["data"]+=[appform.cleaned_data[f]]
            request.session["data"][7]=province_list[int(request.session["data"][7][0])-1][1]
            return HttpResponseRedirect(reverse("form:completed"))
        else: #if form is data is not valid, the form is reloaded with the data the use rput in it
            return render(request,"form/index.html",{
                "appform":appform
            })
    return render(request,"form/index.html",{
        "appform":NewAppForm()
    })


def completed(request):
    if "data" not in request.session:
        request.session["data"]=[]
    return render(request,"form/completed.html",{
        "data":request.session["data"]
    })