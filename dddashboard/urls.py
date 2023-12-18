from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.industry, name="industry"),
    # path('user/', views.userPage, name="user-page"),

    # path('account/', views.accountSettings, name="account"),

    # path('products/', views.products, name='products'),
    # path('customer/<str:pk_test>/', views.customer, name="customer"),

    # path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    # path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    # path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('industry/', views.industry, name='industry'),
    path('small_industry/', views.small_industry, name='small_industry'),
    path('large_industry/', views.large_industry, name='large_industry'),
    path('company/', views.company, name='company'),
    path('historical_data/', views.historicalData, name='historicaldata'),
    
    path('demographic_variables/aboriginal.html', views.demographicAboriginal, name='demographic_aboriginal'),
    path('demographic_variables/persons_with_disabilities.html', views.demographicDisability, name='demographic_disability'),
    path('demographic_variables/sex.html', views.demographicSex, name='demographic_sex'),
    path('demographic_variables/visible_minority.html', views.demographicMinority, name='demographic_minority'),

    path('demographic_variables/small_aboriginal.html', views.small_demographicAboriginal, name='small_demographic_aboriginal'),
    path('demographic_variables/small_persons_with_disabilities.html', views.small_demographicDisability, name='small_demographic_disability'),
    path('demographic_variables/small_sex.html', views.small_demographicSex, name='small_demographic_sex'),
    path('demographic_variables/small_visible_minority.html', views.small_demographicMinority, name='small_demographic_minority'),

    path('demographic_variables/large_aboriginal.html', views.large_demographicAboriginal, name='large_demographic_aboriginal'),
    path('demographic_variables/large_persons_with_disabilities.html', views.large_demographicDisability, name='large_demographic_disability'),
    path('demographic_variables/large_sex.html', views.large_demographicSex, name='large_demographic_sex'),
    path('demographic_variables/large_visible_minority.html', views.large_demographicMinority, name='large_demographic_minority'),

    path('contact/', views.contact, name='contact'),


    path('upload/', views.uploadFile, name='upload'),
    path('new_company_creation/', views.create_company, name='new_company'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard_navbar_footer/', views.navbarfooter, name='dashboard_navbar_footer'),


    path('test/', views.test, name='test'),


   



]