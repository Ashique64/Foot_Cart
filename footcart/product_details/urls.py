from django.urls import path
from product_details import views

urlpatterns = [
    path('Product_details/<int:product_id>', views.Product_details,name='Product_details'),
    path('My_cart', views.My_cart,name='My_cart'),
    path('Add_cart/<int:product_id>/', views.Add_cart, name='Add_cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity_endpoint'),
    path('Remove_cart_item/<int:cart_item_id>/', views.Remove_cart_item, name='Remove_cart_item'),
    path('Shipping_details/<int:cart_id>', views.Shipping_details, name='Shipping_details'),
    path('Payment_details/<int:cart_id>', views.Payment_details,name='Payment_details'),
    path('Order_summary', views.Order_summary,name='Order_summary'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('razorpay/<int:cart_id>', views.razorpay,name='razorpay'),

    
]
