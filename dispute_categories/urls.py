from django.urls import path
from dispute_categories.views import *

app_name = "categories"

urlpatterns = [
    path("", category_list, name="list"),
    path("<slug:slug>/", category_detail, name="detail"),
    path("<slug:slug>/eligibility/", eligibility_screen, name="eligibility"),
]
