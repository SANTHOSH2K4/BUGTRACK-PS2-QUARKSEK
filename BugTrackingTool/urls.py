"""
URL configuration for BugTrackingTool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('user/',views.user,name='user'),
    path('manager_home/',views.manager_home,name='manager_home'),
    path('customer_requests/',views.customer_requests,name='customer_requests'),
    path('clog/',views.clog,name='clog'),
    path('tlog/',views.tlog,name='tlog'),
    path('plog/',views.plog,name='plog'), 
    path('creg/',views.creg,name='creg'),
    path('treg/',views.treg,name='treg'),
    path('treg/',views.treg,name='treg'),
    path('bug_testst_cmt/',views.bug_testst_cmt,name='bug_testst_cmt'),
    path('bug_comments_tester/',views.bug_comments_tester,name='bug_comments_tester'),
    path('newTester/',views.newTester,name='newTester'),
    path('bugs/',views.bugs,name='bugs'),
    path('bugraise/',views.bugraise,name='bugraise'),
    path('manager_comment/',views.manager_comment,name='manager_comment'),
    path('bug_st_cmt/',views.bug_st_cmt,name="bug_st_cmt"),
    path('avail_testers/',views.avail_testers,name='avail_testers'),
    path('bug_comments/',views.bug_comments,name='bug_comments'),
    path('reqstatusupdatefunc/',views.reqstatusupdatefunc,name='reqstatusupdatefunc'),
    path('assigntotester/',views.assigntotester,name='assigntotester'),
    path('bug_info/',views.bug_info,name='bug_info'),
    path('customer_login/',views.customer_login,name='customer_login'),
    path('tester_login/',views.tester_login,name='tester_login'),
    path('project_manager_login/',views.project_manager_login,name='project_manager_login'),
    path('user_home/',views.user_home,name='user_home'),
    path('testing-requests/', views.testing_requests, name='testing_requests'),
    path('assigned-requests/', views.assigned_requests, name='assigned_requests'),  # New URL for assigned requests
    path('assign-tester/<int:request_id>/', views.assign_tester, name='assign_tester'),
    path('admin/', admin.site.urls),
    path('projectmanagerpage/', views.testing_requests),  # Default view
    path('submit_url/',views.submit_url,name='submit_url')
]
