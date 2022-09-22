from cProfile import label
from http.client import HTTPResponse
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import re
from django.shortcuts import render
from django import forms
from datetime import datetime,date
from phone_field import PhoneField
from phonenumber_field.formfields import PhoneNumberField
from django.forms import widgets

province_list=((1,"Alberta"),(2,"British Columbia"),(3,"Manitoba"),(4,"New Brunswick"),(5,"Newfoundland and Labrador"),(6,"Nova Scotia"),(7,"Ontario"),(8,"Prince Edward Island"),(9,"Quebec"),(10,"Saskatchewan"),(11,"Northwest Territories"),(12,"Nunavut"),(13,"Yukon"))
class NewAppForm(forms.Form):
    fname=forms.CharField(label="First Name")
    mname=forms.CharField(label="Middle Name",required=False)
    lname=forms.CharField(label="Last Name",required=False)#show dialog box if blank
    date=forms.DateField(label="Date",widget=widgets.SelectDateWidget())
    addr1=forms.CharField(label="Address Line 1")
    addr2=forms.CharField(label="Address Line 2",required=False)
    city=forms.CharField(label="City")
    province=forms.CharField(label="Province/Territory",widget=widgets.Select(attrs={'size': 1},choices=province_list))
    postal=forms.CharField(label="Postal code")#validate format
    tel=forms.CharField(label="Telephone #")
    tel2=forms.CharField(label="Other Telephone #",required=False)
    email=forms.EmailField(label="E-mail")#check if valid address
    reffered=forms.CharField(label="Reffered by",required=False)
    #phone=PhoneNumberField(required=True)

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
            request.session["data"][7]=province_list[int(request.session["data"][7][0])-1][1] #get for province string that corresponds with the field output
            return HttpResponseRedirect(reverse("form:completed"))
        else: #if form is data is not valid, the form is reloaded with the data the use rput in it
            return render(request,"form/index.html",{
                "appform":appform
            })
    return render(request,"form/index.html",{
        "appform":NewAppForm()
    })


def completed(request):
    if "data" not in request.session: #might be redundant
        request.session["data"]=[]
    return render(request,"form/completed.html",{
        "data":request.session["data"],
        "fname":request.session["data"][0],
        "mname":request.session["data"][1],
        "lname":request.session["data"][2],
        "date":request.session["data"][3],
        "addr1":request.session["data"][4],
        "addr2":request.session["data"][5],
        "city":request.session["data"][6],
        "province":request.session["data"][7],
        "postal":request.session["data"][8],
        "tel":request.session["data"][9],
        "tel2":request.session["data"][10],
        "email":request.session["data"][11],
        "reffered":request.session["data"][12]
    })