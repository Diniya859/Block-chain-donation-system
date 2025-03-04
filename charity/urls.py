from django.urls import path
from charity import views
urlpatterns = [
    path('', views.index),
    path('home',views.home),
    path('login_post',views.login_post),
    path('register',views.register),
    path('admin_functions', views.admin_functions),
    path('user_functions', views.user_functions),
    path('reply_post/<int:id>/', views.reply_post, name='reply_post'),
    path('user_feedback', views.user_feedback,name='user_feedback'),
    path('user_complaint',views.user_complaint),
    path('add',views.add),
    path('donates',views.donate),
    path("make-payment/", views.save_transaction, name="save_transaction"),
    path('save-transaction/', views.save_transaction, name="save_transaction"),
    path("donate/<int:charity_id>/", views.donate_page, name="donate"),
    path('delete-charity/<int:id>/', views.delete_charity, name='delete_charity'),
    path('reply',views.reply),
]
