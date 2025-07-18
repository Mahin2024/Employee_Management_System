from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import loginViewset, employeeViewset,changePassword,forgotPassword,resetPassword,logout,leaveViewset,leaveStatusViewset,paidLeaveViewset

router = DefaultRouter()

router.register(r'login',loginViewset,basename='login')
router.register(r'employeeinfo',employeeViewset,basename='employeeinfo')
router.register(r'leaves',leaveViewset,basename='leave')
router.register(r'leavestatus',leaveStatusViewset,basename='leavestatus')
# router.register(r'paidleave',paidLeaveViewset,basename='paidleave')
urlpatterns = [
    path('',include(router.urls)),
    path('updatepassword/', changePassword.as_view(), name='updatepassword'),
    path('forgotpassword/', forgotPassword.as_view(), name='forgotpassword'),
    path('resetpassword/', resetPassword.as_view(), name='resetpassword'),
    path('logout/',logout.as_view(),name='logout'),
    path('paidleave/',paidLeaveViewset.as_view(),name='paidleave'),

]