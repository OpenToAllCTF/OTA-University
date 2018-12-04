from django.http import HttpResponse
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from ..models import UserProfile, Challenge, Category, Writeup
from ..forms import *
