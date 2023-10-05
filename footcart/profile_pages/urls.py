from django.urls import path
from profile_pages import views

urlpatterns = [
    path('User_profile', views.User_profile,name='User_profile'),
    path('User_address', views.User_address,name='User_address'),
    path('Add_address', views.Add_address,name='Add_address'),
    path('Edit_address/<int:addr_id>', views.Edit_address,name='Edit_address'),
    path('Delete_address/<int:addr_id>', views.Delete_address,name='Delete_address'),
    path('Logout', views.Logout, name='Logout'),
    path('User_orders', views.User_orders,name='User_orders'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order_items_invoice/<int:order_id>/', views.order_items_invoice, name='order_items_invoice'),
    path('wallet', views.wallet,name='wallet'),
    path('wishlist', views.wishlist,name='wishlist'),
    path('add_wishlist/<int:product_id>', views.add_wishlist,name='add_wishlist'),
    path('remove_from_wishliste/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('track_order/<int:order_id>/', views.track_order, name='track_order'),
    
]