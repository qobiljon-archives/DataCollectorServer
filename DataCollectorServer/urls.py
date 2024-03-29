"""DataCollectorServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api_submit_location_data/', views.api_submit_location_data),
	path('api_submit_bt_scan_data/', views.api_submit_bt_scan_data),
	path('api_battery_level_data/', views.api_battery_level_data),
	path('api_get_data_submission_progress/', views.api_get_data_submission_progress),
	path('api_get_lof_calculation_progress/', views.api_get_lof_calculation_progress),
]
