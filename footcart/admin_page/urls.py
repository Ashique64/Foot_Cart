from django.urls import path
from admin_page import views

urlpatterns = [
    path('Admn', views.Dashboard, name='Admn'),
    path('Admn_login', views.Admin_login, name='Admn_login'),
    path('Admn_logout', views.Admin_logout, name='Admn_logout'),


    path('Admn_user', views.Admin_user, name='Admn_user'),
    path('block_user/<int:id>', views.Admin_block_user, name='block_user'),
    path('unblock_user/<int:id>', views.Admin_unblock_user, name='unblock_user'),


    path('Admn_product', views.Admin_product, name='Admn_product'),
    path('Admn_add_product', views.Admin_add_product, name='Admn_add_product'),
    path('Admn_edit_product/<int:product_id>',
         views.Admin_edit_product, name='Admn_edit_product'),
    path('Admn_delete_product/<int:product_id>',
         views.Admin_delete_product, name='Admn_delete_product'),
    
    path('Variant/<int:product_id>', views.Variant, name='Variant'),
    path('Add_variant/<int:product_id>', views.Add_variant, name='Add_variant'),
    path('Edit_variant/<int:variant_id>', views.Edit_variant, name='Edit_variant'),
    path('Delete_variant/<int:variant_id>', views.Delete_variant, name='Delete_variant'),


    path('Admn_categories', views.Admin_categories, name='Admn_categories'),
    path('Admn_edit_categories/<int:id>',
         views.Admin_edit_categories, name='Admn_edit_categories'),
    path('Admn_delete_categories/<int:id>',
         views.Admin_delete_categories, name='Admn_delete_categories'),
    path('Admn_add_categories', views.Admin_add_categories,
         name='Admn_add_categories'),
    
    
    path('Admn_orders', views.Admn_orders, name='Admn_orders'),
    path('Admin_order_items/<int:order_id>/', views.Admin_order_items, name='Admin_order_items'),
    path('Admin_update_order_status/<int:order_id>/', views.Admin_update_order_status, name='Admin_update_order_status'),
    
    path('Admn_coupons', views.Admn_coupons, name='Admn_coupons'),
    path('Admn_add_coupons', views.Admn_add_coupons, name='Admn_add_coupons'),
    path('Admn_edit_coupons/<int:coupon_id>', views.Admn_edit_coupons, name='Admn_edit_coupons'),
    path('Admn_delete_coupons/<int:coupon_id>', views.Admn_delete_coupons, name='Admn_delete_coupons'),
    
    
    path('sales_report', views.sales_report, name='sales_report'),
]
