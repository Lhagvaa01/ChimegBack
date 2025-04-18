
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from invoice import views
from invoice.views import *


router = DefaultRouter()
router.register(r'info-products', InfoProductNewViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('get_products/<int:id>', get_product_detail.as_view(), name='get_product_detail'),

    path('get_InvoiceNumber/<str:userId>/<str:isNeh>/', get_InvoiceNumberView.as_view(), name='get_InvoiceNumber'),

    path('get_SiteProductNew/<str:itemCode>/', get_SiteProductNew.as_view(), name='get_SiteProductNew'),

    path('get_GroupHDR/', get_GroupHDR.as_view(), name='get_GroupHDR'),

    path('get_locations/', LocationListView.as_view(), name='LocationListView'),

    path('get_User/<int:pk>/', SiteUserView.as_view(), name='SiteUserView'),

    path('post_CreateUser/', CreateUserView.as_view(), name='CreateUserView'),

    path('put_EditUser/<int:pk>/', EditUserAPIView.as_view(), name='EditUserAPIView'),

    path('get_UserAddress/<int:pk>/', UserAddressListView.as_view(), name='UserAddressListView'),

    path('post_UserAddress/', CreateUserAddressAPIView.as_view(), name='CreateUserAddressAPIView'),

    path('put_UserAddress/<int:pk>/', EditUserAddressAPIView.as_view(), name='EditUserAddressAPIView'),

    path('post_DelUserAddress/<int:pk>/', DeleteUserAddressAPIView.as_view(), name='DeleteUserAddressAPIView'),

    path('get_UserHistory/<int:pk>/', UserOrderHistoryListView.as_view(), name='UserOrderHistoryListView'),

    path('post_UserHistory/', CreateUserOrderHistoryAPIView.as_view(), name='CreateUserOrderHistoryAPIView'),

    path('put_UserHistory/<int:pk>/', EditUserOrderHistoryAPIView.as_view(), name='EditUserOrderHistoryAPIView'),

    path('post_LoginUser/', SiteLoginUserAPIView.as_view(), name='SiteLoginUserAPIVie w'),

    path('get_ProductDownloads/<int:itemCode>/', get_ProductDownloads.as_view(), name='get_ProductDownloads'),

    path('get_SiteSliderImg/', SiteSliderListView.as_view(), name='SiteSliderListView'),

    path('get_DiscountProducts/', DiscountProductsListView.as_view(), name='DiscountProductsListView'),

    path('api/transaction/', transaction_view, name='TransactionAPIView'),

    path('api/CheckOrder/', CheckOrderView.as_view(), name='CheckOrderView'),

    path('brands/', BrandListView.as_view(), name='brand-list'),

    path('getAd/', AdvertisementView.as_view(), name='AdvertisementView'),

    path('partners/', PartnerListView.as_view(), name='partner-list'),

    path('program-info/', ProgramInfoAPIView.as_view(), name='program-info'),





]
