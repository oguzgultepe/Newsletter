from django.shortcuts import render
from django.http import HttpResponse

def submit(request):
    return HttpResponse("You are at the submissions page.")

def display(request):
    return HttpResponse("You are at the display page")

def user(request):
    return HttpResponse("You are at the user page")

def send(request):
    return HttpResponse("You are at the send page")

def edit(request):
    return HttpResponse("You are at the edit page")
