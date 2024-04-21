from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('request_for_all/<int:id>', views.request_for_all, name='request_for_all'),
    path('request_for_Pc/<int:id>', views.request_for_Pc, name='request_for_Pc'),
    path('request_for_Electronics/<int:id>', views.request_for_Electronics, name='request_for_Electronics'),
    path('request_for_Book/<int:id>', views.request_for_Book, name='request_for_Book'),
    path('request_for_available/<int:id>', views.request_for_available, name='request_for_available'),
    path('search_by_typing/', views.search_by_typing, name='search_by_typing'),
    path('cancel_request/<int:id>', views.cancel_request, name='cancel_request'),

    path('request_again/<int:id>', views.request_again, name='request_again'),

    
    path('historical_bookings/', views.historical_bookings, name='historical_bookings'),
    path('filter_equipments/<str:keyword>', views.filter_equipments, name='filter_equipments'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('success_page/', views.success_page, name='success_page'),
    path('users_reservations/', views.users_reservations, name='users_reservations')
    
]