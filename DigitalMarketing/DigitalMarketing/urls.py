"""template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DigitalMarketing import views


urlpatterns = [
    path("admin/", admin.site.urls), 
    path("uploaderdashboard/<str:id>", views.uploaderdashboard),
    path("filterpage/<str:id>/<str:id1>/<str:id2>", views.filterpage),
    path("myvideos/<str:id>", views.myvideos),
    path("createrupload/<str:id>", views.creater_upload),
    path("UserIndexpage", views.user_indexpage),
    path("approver/<str:id>", views.approver),
    path("approverview/<str:id>/<str:uid>", views.approver_view),
    # path("status/<str:id1>", views.status),
    path("statusview/<str:id1>/<str:uid>", views.status_view),
    path("Download/<str:id>", views.download),
    path("Downloadvideo/<str:id>", views.download_video),
    path("DeleteVideo/<str:id>/<str:id1>", views.delete_video),
    path("uploadagain/<str:id>/<str:id1>", views.upload_again), 
    path("updateview/<str:id>/<str:id1>", views.update_view), 
    path("update/<str:id>/<str:id1>", views.creater_update_video), 
    path("detailedview/<str:id>", views.detailed_view), 
    path("approverdetail_view/<str:id>", views.approverdetail_view), 
    path("superadmin/<str:id>", views.admin), 
    path("superadmindetail_view/<str:id>", views.superadmindetail_view), 
    path("superadmindetail_downloader_view/<str:id>", views.superadmindetail_downloader_view), 
    path('Activation',views.activate),
    

     

    # Login
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view,  name="logout") 
]

