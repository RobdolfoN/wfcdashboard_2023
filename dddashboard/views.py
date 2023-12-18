from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.mail import send_mail
from .models import *
import datetime
from .forms import CreateUserForm, CustomerForm, DataForm, CompanyForm
# from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from .dataManagement import  (
	handle_uploaded_file, sex_donut_industrychart,
	minority_donut_industrychart, aboriginal_donut_industrychart, 
	disability_donut_industrychart, 
	Companydata_sex_donut_industrychart, sex_barchart_industrychart,
	minority_barchart_industrychart, 
	aboriginal_barchart_industrychart, 
	disability_barchart_industrychart, c_sex_barchart_industrychart,
	c_minority_barchart_industrychart, c_aboriginal_barchart_industrychart,
	c_disability_barchart_industrychart, 
	Companydata_create_donut_chart,
	size_sex_donut_industrychart, size_create_donut_chart,
	sex_donut_industrychart, size_sex_barchart_industrychart,
	size_minority_barchart_industrychart, size_aboriginal_barchart_industrychart,
	size_disability_barchart_industrychart, sex_donut_second_mostrecent_industrychart,
	Companydata_sex_donut_second_mostrecent_industrychart, create_second_mostrecent_donut_chart,
	minority_second_mostrecent_donut_industrychart, aboriginal_second_mostrecent_donut_industrychart,
	disability_second_mostrecent_donut_industrychart,
	Companydata_create_donut_second_mostrecent_chart, contextCreator, companyContextCreator, contextCreatorSmallindustry,
	contextCreatorLargeindustry,

)
from .jsonTest import jcontextCreator
import pathlib
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import concurrent
import json
import plotly.graph_objs as go
import plotly.io as pio






# Create your views here.

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Dashboard_user.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	#return render(request, 'accounts/register.html', context)
	return render(request, context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('industry')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'dddashboard/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')





@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def industry(request):
# 	dashboarduser = request.user
	
# 	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
# 	dashboardusercompany = dashboarduserinfo.company_name
# 	dashboardusercompany_ID = dashboarduserinfo.company_name_id
	
# 	chart_key_1 = 'queryset1'
# 	cached_queryset1 = cache.get(chart_key_1)
# 	if not cached_queryset1:

# 		queryset1 = CompanyData.objects.all().select_related('name')
# 		cache.set(chart_key_1, queryset1, 3600)
# 		cached_queryset1 = cache.get(chart_key_1)

# 	chart_key_2 = f'queryset2_{dashboardusercompany_ID}'
# 	cached_queryset2 = cache.get(chart_key_2)
# 	if not cached_queryset2:

# 		queryset2 = CompanyData.objects.filter(name_id=dashboardusercompany_ID).select_related('name')
# 		cache.set(chart_key_2, queryset2, 3600)
# 		cached_queryset2 = cache.get(chart_key_2)



# 	context = contextCreator(dashboardusercompany_ID, dashboardusercompany, cached_queryset1, cached_queryset2)




# 	return render(request, 'dddashboard/industry.html', context)

@login_required(login_url='login')
def industry(request):
    dashboarduser = request.user

    dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
    dashboardusercompany = dashboarduserinfo.company_name
    dashboardusercompany_ID = dashboarduserinfo.company_name_id

    # Instead of getting the queryset from the cache, 
    # we directly retrieve it from the database every time
    queryset1 = CompanyData.objects.all().select_related('name')

    # Do the same for the second queryset
    queryset2 = CompanyData.objects.filter(name_id=dashboardusercompany_ID).select_related('name')

    # Create context using the fresh querysets
    context = contextCreator(dashboardusercompany_ID, dashboardusercompany, queryset1, queryset2)

    return render(request, 'dddashboard/industry.html', context)




# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def company(request):
	dashboarduser = request.user
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	dashboardusercompany = dashboarduserinfo.company_name
	dashboardusercompany_ID = dashboarduserinfo.company_name_id
	
	chart_key_1 = 'queryset1'
	cached_queryset1 = cache.get(chart_key_1)
	if not cached_queryset1:

		queryset1 = CompanyData.objects.all().select_related('name')
		cache.set(chart_key_1, queryset1, 3600)
		cached_queryset1 = cache.get(chart_key_1)

	chart_key_2 = f'queryset2_{dashboardusercompany_ID}'
	cached_queryset2 = cache.get(chart_key_2)
	if not cached_queryset2:

		queryset2 = CompanyData.objects.filter(name_id=dashboardusercompany_ID).select_related('name')
		cache.set(chart_key_2, queryset2, 3600)
		cached_queryset2 = cache.get(chart_key_2)

	context = companyContextCreator(dashboardusercompany_ID, dashboardusercompany, cached_queryset1, cached_queryset2)

	return render(request, 'dddashboard/company.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def historicalData(request):
	dashboarduser = request.user
	print(dashboarduser)
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	print(dashboarduserinfo)
	dashboardusercompany = dashboarduserinfo.company_name
	print(dashboardusercompany)

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive')
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader')
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent')
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson')
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor')

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive')
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader')
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent')
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson')
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor')

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive')
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader')
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent')
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson')
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor')

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive')
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader')
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent')
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson')
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor')

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}
	# context = {}
	return render(request, 'dddashboard/historical_data.html', context)


##### industry filtered by size #######

def small_industry(request):
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	dashboardusercompany = dashboarduserinfo.company_name
	dashboardusercompany_ID = dashboarduserinfo.company_name_id

	chart_key_1 = 'queryset1'
	cached_queryset1 = cache.get(chart_key_1)
	if not cached_queryset1:

		queryset1 = CompanyData.objects.all().select_related('name')
		cache.set(chart_key_1, queryset1, 3600)
		cached_queryset1 = cache.get(chart_key_1)

	chart_key_2 = f'queryset2_{dashboardusercompany_ID}'
	cached_queryset2 = cache.get(chart_key_2)
	if not cached_queryset2:

		queryset2 = CompanyData.objects.filter(name_id=dashboardusercompany_ID).select_related('name')
		cache.set(chart_key_2, queryset2, 3600)
		cached_queryset2 = cache.get(chart_key_2)



	context = contextCreatorSmallindustry(dashboardusercompany_ID, dashboardusercompany, cached_queryset1, cached_queryset2)



	return render(request, 'dddashboard/small_industry.html', context)

def large_industry(request):
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	dashboardusercompany = dashboarduserinfo.company_name
	dashboardusercompany_ID = dashboarduserinfo.company_name_id

	chart_key_1 = 'queryset1'
	cached_queryset1 = cache.get(chart_key_1)
	if not cached_queryset1:

		queryset1 = CompanyData.objects.all().select_related('name')
		cache.set(chart_key_1, queryset1, 3600)
		cached_queryset1 = cache.get(chart_key_1)

	chart_key_2 = f'queryset2_{dashboardusercompany_ID}'
	cached_queryset2 = cache.get(chart_key_2)
	if not cached_queryset2:

		queryset2 = CompanyData.objects.filter(name_id=dashboardusercompany_ID).select_related('name')
		cache.set(chart_key_2, queryset2, 3600)
		cached_queryset2 = cache.get(chart_key_2)

	context = contextCreatorLargeindustry(dashboardusercompany_ID, dashboardusercompany, cached_queryset1, cached_queryset2)


	return render(request, 'dddashboard/large_industry.html', context)



#######################





def uploadFile(request):
	if request.method == 'POST':
		form = DataForm(request.POST, request.FILES)
		if form.is_valid():
			#company_name from forms is store in "form.cleaned_data['company_name']"
			#file uploaded from form is stored in "request.FILES" se puede consultar el nombre asi: print(request.FILES['file'])
			#se guarda nombre de compañia en variable
			name_of_company = form.cleaned_data['company_name'].lower()
			#borrar informacion de la tabla que contenga el nombre guardado en name_of_company
			#esto se hace para borrar la informacion del modelo CompanyData que esta relacionado con el nombre de la compañia que se acaba de crear
			CompanyName.objects.filter(name=name_of_company).delete()
			#se crea de nuevo una instancia en la tabla de los nombres.
			n, created = CompanyName.objects.get_or_create(name=name_of_company)

			uploaded_data = handle_uploaded_file(request.FILES['file'])

			for index, row in uploaded_data.iterrows():
				company_data = CompanyData.objects.create(
					name=n,
					gender_code=row["gender code"],
					aboriginal_peoples=row["aboriginal peoples"],
					visible_minorities=row["visible minorities"],
					person_with_disabilities=row["person with disabilities"],
					position_category=row["position/role category"],
					)
			return HttpResponse("The name of the uploaded file is " + form.cleaned_data['company_name'].lower())
	
	else:
		
		form = DataForm()

	return render(request, 'dddashboard/upload.html', {'form': form})

def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created/updated successfully!')
            return redirect('new_company')
    else:
        form = CompanyForm()
    return render(request, 'admin/new_company_creation.html', {'form': form})



@admin_only
def admin_dashboard(request):
	if request.method == 'POST':
		form = DataForm(request.POST, request.FILES)
		if form.is_valid():
			#company_name from forms is store in "form.cleaned_data['company_name']"
			#file uploaded from form is stored in "request.FILES" se puede consultar el nombre asi: print(request.FILES['file'])
			#se guarda nombre de compañia en variable
			name_of_company = form.cleaned_data['company_name']
			size_of_company = form.cleaned_data['company_size']
			# size_of_company = name_of_company.size
			data_year = form.cleaned_data['year_collected']
			year_data_collection = data_year.year if isinstance(data_year, datetime.date) else data_year
			#borrar informacion de la tabla que contenga el nombre guardado en name_of_company
			#esto se hace para borrar la informacion del modelo CompanyData que esta relacionado con el nombre de la compañia que se acaba de crear
			# CompanyName.objects.filter(name=name_of_company).delete()
			#se crea de nuevo una instancia en la tabla de los nombres.
			# n, created = CompanyName.objects.get_or_create(name=name_of_company)
			# s, created = CompanySize.objects.get_or_create(company_size=size_of_company)
			existing_data = CompanyData.objects.filter(name=name_of_company, year_created__year=year_data_collection)
			if existing_data.exists():
				existing_data.delete()

			uploaded_data = handle_uploaded_file(request.FILES['file'])

			for index, row in uploaded_data.iterrows():
				company_data = CompanyData.objects.create(
					name=name_of_company,
					company_size=size_of_company,
					year_created=data_year,
					gender_code=row["gender code"],
					aboriginal_peoples=row["aboriginal peoples"],
					visible_minorities=row["visible minorities"],
					person_with_disabilities=row["person with disabilities"],
					position_category=row["position/role category"],
					)
			messages.success(request, 'data uploaded for ' + form.cleaned_data['company_name'].name + '!')
			return redirect('/admin')
	
	else:
		
		form = DataForm()

	return render(request, 'admin/admin_dashboard.html', {'form': form})

def navbarfooter(request):
	

	return render(request, 'dddashboard/dashboard_navbar_footer.html')

def demographicAboriginal(request):
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	


	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 57)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 57)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 57)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 57)


	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)


	### DATE FILTERED #####
			#### MOST RECENT ########
	aboriginal_executive_second_mostrecent_dchart1, year_info = aboriginal_second_mostrecent_donut_industrychart('Executive')
	aboriginal_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Senior Leader')
	aboriginal_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	aboriginal_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Foreperson')
	aboriginal_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Individual Contributor')
	
	Companydata_executive_aboriginal_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Executive')
	Companydata_senior_leader_aboriginal_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Senior Leader')
	Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Foreperson')
	Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()

	context = { 'aboriginal_executive_barchart':aboriginal_executive_barchart, 
	'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 
	'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 
	'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 
	'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 
	'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 
	'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 
	'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 
	'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 
	'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart,
	'aboriginal_executive_second_mostrecent_dchart1':aboriginal_executive_second_mostrecent_dchart1,
	'aboriginal_senior_leader_second_mostrecent_dchart1':aboriginal_senior_leader_second_mostrecent_dchart1,
	'aboriginal_manager_s_s_second_mostrecent_dchart1':aboriginal_manager_s_s_second_mostrecent_dchart1,
	'aboriginal_foreperson_leader_second_mostrecent_dchart1':aboriginal_foreperson_leader_second_mostrecent_dchart1,
	'aboriginal_individual_contributor_second_mostrecent_dchart1':aboriginal_individual_contributor_second_mostrecent_dchart1,
	'Companydata_executive_aboriginal_second_mostrecent_dchart1':Companydata_executive_aboriginal_second_mostrecent_dchart1,
	'Companydata_senior_leader_aboriginal_second_mostrecent_dchart1':Companydata_senior_leader_aboriginal_second_mostrecent_dchart1,
	'Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1':Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1,
	'Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1':Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1,
	'Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1':Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1,
	'year_info':year_info, 'dashboardusercompany':dashboardusercompany,

		}

	return render(request, 'dddashboard/demographic_variables/aboriginal.html', context)


def demographicDisability(request):
		
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 57)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 57)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 57)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 57)

# Company DATA QUERIES

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	### DATE FILTERED #####
			#### MOST RECENT ########
	disability_executive_second_mostrecent_dchart1, year_info = disability_second_mostrecent_donut_industrychart('Executive')
	disability_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Senior Leader')
	disability_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	disability_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Foreperson')
	disability_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Individual Contributor')
	
	Companydata_executive_disability_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Executive')
	Companydata_senior_leader_disability_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Senior Leader')
	Companydata_manager_s_s_disability_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	Companydata_foreperson_leader_disability_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Foreperson')
	Companydata_individual_contributor_disability_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()



	context = {'disability_executive_barchart':disability_executive_barchart, 
		   'disability_senior_leader_barchart':disability_senior_leader_barchart, 
		   'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 
		   'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 
		   'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,

		  'c_disability_executive_barchart':c_disability_executive_barchart, 
		  'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 
		  'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 
		  'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 
		  'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,

		  	'disability_executive_second_mostrecent_dchart1':disability_executive_second_mostrecent_dchart1,
			'disability_senior_leader_second_mostrecent_dchart1':disability_senior_leader_second_mostrecent_dchart1,
			'disability_manager_s_s_second_mostrecent_dchart1':disability_manager_s_s_second_mostrecent_dchart1,
			'disability_foreperson_leader_second_mostrecent_dchart1':disability_foreperson_leader_second_mostrecent_dchart1,
			'disability_individual_contributor_second_mostrecent_dchart1':disability_individual_contributor_second_mostrecent_dchart1,
			
			'Companydata_executive_disability_second_mostrecent_dchart1':Companydata_executive_disability_second_mostrecent_dchart1,
			'Companydata_senior_leader_disability_second_mostrecent_dchart1':Companydata_senior_leader_disability_second_mostrecent_dchart1,
			'Companydata_manager_s_s_disability_second_mostrecent_dchart1':Companydata_manager_s_s_disability_second_mostrecent_dchart1,
			'Companydata_foreperson_leader_disability_second_mostrecent_dchart1':Companydata_foreperson_leader_disability_second_mostrecent_dchart1,
			'Companydata_individual_contributor_disability_second_mostrecent_dchart1':Companydata_individual_contributor_disability_second_mostrecent_dchart1,
			'year_info':year_info, 'dashboardusercompany':dashboardusercompany,

		}

	

	return render(request, 'dddashboard/demographic_variables/persons_with_disabilities.html', context)


def demographicSex(request):

	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	

	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 57)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 57)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 57)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 57)


# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	### DATE FILTERED #####
			####Second MOST RECENT ########
	sex_executive_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Executive')
	Companydata_executive_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Executive')
	sex_senior_leader_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Senior Leader')
	Companydata_senior_leader_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Senior Leader')
	sex_manager_s_s_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Manager/Supervisor/Superintendent')
	Companydata_manager_s_s_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Manager/Supervisor/Superintendent')
	sex_foreperson_leader_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Foreperson')
	Companydata_foreperson_leader_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Foreperson')
	sex_individual_contributor_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Individual Contributor')
	Companydata_individual_contributor_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()
	


	context = { 'sex_executive_barchart':sex_executive_barchart, 
		'sex_senior_leader_barchart':sex_senior_leader_barchart, 
		'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 
		'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 
		'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 
		
		'c_sex_executive_barchart':c_sex_executive_barchart, 
		'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart,
		'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 
		'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 
		'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart,
		
		'sex_executive_second_mostrecent_dchart1':sex_executive_second_mostrecent_dchart1, 
		'sex_senior_leader_second_mostrecent_dchart1':sex_senior_leader_second_mostrecent_dchart1, 
		'sex_manager_s_s_second_mostrecent_dchart1':sex_manager_s_s_second_mostrecent_dchart1,
		'sex_foreperson_leader_second_mostrecent_dchart1':sex_foreperson_leader_second_mostrecent_dchart1, 
		'sex_individual_contributor_second_mostrecent_dchart1':sex_individual_contributor_second_mostrecent_dchart1, 
		
		'Companydata_executive_sex_second_mostrecent_dchart1':Companydata_executive_sex_second_mostrecent_dchart1,
		'Companydata_senior_leader_sex_second_mostrecent_dchart1':Companydata_senior_leader_sex_second_mostrecent_dchart1,
		'Companydata_manager_s_s_sex_second_mostrecent_dchart1':Companydata_manager_s_s_sex_second_mostrecent_dchart1,
		'Companydata_foreperson_leader_sex_second_mostrecent_dchart1':Companydata_foreperson_leader_sex_second_mostrecent_dchart1,
		'Companydata_individual_contributor_sex_second_mostrecent_dchart1':Companydata_individual_contributor_sex_second_mostrecent_dchart1,
		'year_info':year_info, 'dashboardusercompany':dashboardusercompany,
		}

	

	return render(request, 'dddashboard/demographic_variables/sex.html', context)


def demographicMinority(request):
		
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	


	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 49)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 49)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 49)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 49)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 49)


	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 49)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 49)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 49)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 49)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 49)


	### DATE FILTERED #####
			####Second MOST RECENT ########
	minority_executive_second_mostrecent_dchart1, year_info = minority_second_mostrecent_donut_industrychart('Executive')
	Companydata_executive_minority_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Executive')
	minority_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Senior Leader')
	Companydata_senior_leader_minority_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Senior Leader')
	minority_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	Companydata_manager_s_s_minority_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	minority_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Foreperson')
	Companydata_foreperson_leader_minority_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Foreperson')
	minority_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Individual Contributor')
	Companydata_individual_contributor_minority_second_mostrecent_dchart1, year_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Individual Contributor')


	dashboardusercompany = str(dashboardusercompany).upper()



	context = {'minority_executive_barchart':minority_executive_barchart,
	'minority_senior_leader_barchart':minority_senior_leader_barchart, 
	'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 
	'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 
	'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart,
	
	'c_minority_executive_barchart':c_minority_executive_barchart, 
	'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart,
	'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 
	'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart,
	'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart,
	
	'minority_executive_second_mostrecent_dchart1':minority_executive_second_mostrecent_dchart1,
	'minority_senior_leader_second_mostrecent_dchart1':minority_senior_leader_second_mostrecent_dchart1,
	'minority_manager_s_s_second_mostrecent_dchart1':minority_manager_s_s_second_mostrecent_dchart1,
	'minority_foreperson_leader_second_mostrecent_dchart1':minority_foreperson_leader_second_mostrecent_dchart1,
	'minority_individual_contributor_second_mostrecent_dchart1':minority_individual_contributor_second_mostrecent_dchart1,
	
	'Companydata_executive_minority_second_mostrecent_dchart1':Companydata_executive_minority_second_mostrecent_dchart1,
	'Companydata_senior_leader_minority_second_mostrecent_dchart1':Companydata_senior_leader_minority_second_mostrecent_dchart1,
	'Companydata_manager_s_s_minority_second_mostrecent_dchart1':Companydata_manager_s_s_minority_second_mostrecent_dchart1,
	'Companydata_foreperson_leader_minority_second_mostrecent_dchart1':Companydata_foreperson_leader_minority_second_mostrecent_dchart1,
	'Companydata_individual_contributor_minority_second_mostrecent_dchart1':Companydata_individual_contributor_minority_second_mostrecent_dchart1,
	'year_info':year_info, 'dashboardusercompany':dashboardusercompany,
	}


	return render(request, 'dddashboard/demographic_variables/visible_minority.html', context)

##### Demographic Sex filtered by size #######

def small_demographicSex(request):

	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	

	#SEX DATA PER POSITION
	
	sex_executive_barchart = size_sex_barchart_industrychart('Executive', 'small', 57)
	sex_senior_leader_barchart = size_sex_barchart_industrychart('Senior Leader', 'small', 57)
	sex_manager_s_s_leader_barchart = size_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 'small', 57)
	sex_foreperson_leader_barchart = size_sex_barchart_industrychart('Foreperson', 'small', 57)
	sex_individual_contributor_leader_barchart = size_sex_barchart_industrychart('Individual Contributor', 'small', 57)


# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	### DATE FILTERED #####
			####Second MOST RECENT ########
	sex_executive_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Executive')
	Companydata_executive_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Executive')
	sex_senior_leader_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Senior Leader')
	Companydata_senior_leader_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Senior Leader')
	sex_manager_s_s_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Manager/Supervisor/Superintendent')
	Companydata_manager_s_s_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Manager/Supervisor/Superintendent')
	sex_foreperson_leader_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Foreperson')
	Companydata_foreperson_leader_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Foreperson')
	sex_individual_contributor_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Individual Contributor')
	Companydata_individual_contributor_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()
 	




	context = { 'sex_executive_barchart':sex_executive_barchart, 
		'sex_senior_leader_barchart':sex_senior_leader_barchart, 
		'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 
		'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 
		'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 
		
		'c_sex_executive_barchart':c_sex_executive_barchart, 
		'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart,
		'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 
		'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 
		'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart,
		
		'sex_executive_second_mostrecent_dchart1':sex_executive_second_mostrecent_dchart1, 
		'sex_senior_leader_second_mostrecent_dchart1':sex_senior_leader_second_mostrecent_dchart1, 
		'sex_manager_s_s_second_mostrecent_dchart1':sex_manager_s_s_second_mostrecent_dchart1,
		'sex_foreperson_leader_second_mostrecent_dchart1':sex_foreperson_leader_second_mostrecent_dchart1, 
		'sex_individual_contributor_second_mostrecent_dchart1':sex_individual_contributor_second_mostrecent_dchart1, 
		
		'Companydata_executive_sex_second_mostrecent_dchart1':Companydata_executive_sex_second_mostrecent_dchart1,
		'Companydata_senior_leader_sex_second_mostrecent_dchart1':Companydata_senior_leader_sex_second_mostrecent_dchart1,
		'Companydata_manager_s_s_sex_second_mostrecent_dchart1':Companydata_manager_s_s_sex_second_mostrecent_dchart1,
		'Companydata_foreperson_leader_sex_second_mostrecent_dchart1':Companydata_foreperson_leader_sex_second_mostrecent_dchart1,
		'Companydata_individual_contributor_sex_second_mostrecent_dchart1':Companydata_individual_contributor_sex_second_mostrecent_dchart1,
		'year_info':year_info, 'dashboardusercompany':dashboardusercompany,
		}

	

	return render(request, 'dddashboard/demographic_variables/small_sex.html', context)

def large_demographicSex(request):

	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	

	#SEX DATA PER POSITION
	
	sex_executive_barchart = size_sex_barchart_industrychart('Executive', 'large', 57)
	sex_senior_leader_barchart = size_sex_barchart_industrychart('Senior Leader', 'large', 57)
	sex_manager_s_s_leader_barchart = size_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 'large', 57)
	sex_foreperson_leader_barchart = size_sex_barchart_industrychart('Foreperson', 'large', 57)
	sex_individual_contributor_leader_barchart = size_sex_barchart_industrychart('Individual Contributor', 'large', 57)


# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	### DATE FILTERED #####
			####Second MOST RECENT ########
	sex_executive_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Executive')
	Companydata_executive_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Executive')
	sex_senior_leader_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Senior Leader')
	Companydata_senior_leader_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Senior Leader')
	sex_manager_s_s_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Manager/Supervisor/Superintendent')
	Companydata_manager_s_s_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Manager/Supervisor/Superintendent')
	sex_foreperson_leader_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Foreperson')
	Companydata_foreperson_leader_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Foreperson')
	sex_individual_contributor_second_mostrecent_dchart1, year_info = sex_donut_second_mostrecent_industrychart('Individual Contributor')
	Companydata_individual_contributor_sex_second_mostrecent_dchart1, year_info = Companydata_sex_donut_second_mostrecent_industrychart(dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()
	


	context = { 'sex_executive_barchart':sex_executive_barchart, 
		'sex_senior_leader_barchart':sex_senior_leader_barchart, 
		'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 
		'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 
		'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 
		
		'c_sex_executive_barchart':c_sex_executive_barchart, 
		'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart,
		'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 
		'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 
		'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart,
		
		'sex_executive_second_mostrecent_dchart1':sex_executive_second_mostrecent_dchart1, 
		'sex_senior_leader_second_mostrecent_dchart1':sex_senior_leader_second_mostrecent_dchart1, 
		'sex_manager_s_s_second_mostrecent_dchart1':sex_manager_s_s_second_mostrecent_dchart1,
		'sex_foreperson_leader_second_mostrecent_dchart1':sex_foreperson_leader_second_mostrecent_dchart1, 
		'sex_individual_contributor_second_mostrecent_dchart1':sex_individual_contributor_second_mostrecent_dchart1, 
		
		'Companydata_executive_sex_second_mostrecent_dchart1':Companydata_executive_sex_second_mostrecent_dchart1,
		'Companydata_senior_leader_sex_second_mostrecent_dchart1':Companydata_senior_leader_sex_second_mostrecent_dchart1,
		'Companydata_manager_s_s_sex_second_mostrecent_dchart1':Companydata_manager_s_s_sex_second_mostrecent_dchart1,
		'Companydata_foreperson_leader_sex_second_mostrecent_dchart1':Companydata_foreperson_leader_sex_second_mostrecent_dchart1,
		'Companydata_individual_contributor_sex_second_mostrecent_dchart1':Companydata_individual_contributor_sex_second_mostrecent_dchart1,
		'year_info':year_info, 'dashboardusercompany':dashboardusercompany,
		}

	

	return render(request, 'dddashboard/demographic_variables/large_sex.html', context)

#######################

##### Demographic Sex filtered by size #######

def small_demographicAboriginal(request):
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	


	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = size_aboriginal_barchart_industrychart('Executive', 'small', 57)
	aboriginal_senior_leader_barchart = size_aboriginal_barchart_industrychart('Senior Leader', 'small', 57)
	aboriginal_manager_s_s_leader_barchart = size_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 'small', 57)
	aboriginal_foreperson_leader_barchart = size_aboriginal_barchart_industrychart('Foreperson', 'small', 57)
	aboriginal_individual_contributor_leader_barchart = size_aboriginal_barchart_industrychart('Individual Contributor', 'small', 57)


	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)


	### DATE FILTERED #####
			#### MOST RECENT ########
	aboriginal_executive_second_mostrecent_dchart1, year_info = aboriginal_second_mostrecent_donut_industrychart('Executive')
	aboriginal_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Senior Leader')
	aboriginal_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	aboriginal_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Foreperson')
	aboriginal_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Individual Contributor')
	
	Companydata_executive_aboriginal_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Executive')
	Companydata_senior_leader_aboriginal_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Senior Leader')
	Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Foreperson')
	Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()


	context = { 'aboriginal_executive_barchart':aboriginal_executive_barchart, 
	'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 
	'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 
	'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 
	'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 
	'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 
	'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 
	'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 
	'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 
	'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart,
	'aboriginal_executive_second_mostrecent_dchart1':aboriginal_executive_second_mostrecent_dchart1,
	'aboriginal_senior_leader_second_mostrecent_dchart1':aboriginal_senior_leader_second_mostrecent_dchart1,
	'aboriginal_manager_s_s_second_mostrecent_dchart1':aboriginal_manager_s_s_second_mostrecent_dchart1,
	'aboriginal_foreperson_leader_second_mostrecent_dchart1':aboriginal_foreperson_leader_second_mostrecent_dchart1,
	'aboriginal_individual_contributor_second_mostrecent_dchart1':aboriginal_individual_contributor_second_mostrecent_dchart1,
	'Companydata_executive_aboriginal_second_mostrecent_dchart1':Companydata_executive_aboriginal_second_mostrecent_dchart1,
	'Companydata_senior_leader_aboriginal_second_mostrecent_dchart1':Companydata_senior_leader_aboriginal_second_mostrecent_dchart1,
	'Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1':Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1,
	'Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1':Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1,
	'Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1':Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1,
	'year_info':year_info, 'dashboardusercompany':dashboardusercompany,

		}

	return render(request, 'dddashboard/demographic_variables/small_aboriginal.html', context)

def large_demographicAboriginal(request):
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	


	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = size_aboriginal_barchart_industrychart('Executive', 'large', 57)
	aboriginal_senior_leader_barchart = size_aboriginal_barchart_industrychart('Senior Leader', 'large', 57)
	aboriginal_manager_s_s_leader_barchart = size_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 'large', 57)
	aboriginal_foreperson_leader_barchart = size_aboriginal_barchart_industrychart('Foreperson', 'large', 57)
	aboriginal_individual_contributor_leader_barchart = size_aboriginal_barchart_industrychart('Individual Contributor', 'large', 57)


	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)


	### DATE FILTERED #####
			#### MOST RECENT ########
	aboriginal_executive_second_mostrecent_dchart1, year_info = aboriginal_second_mostrecent_donut_industrychart('Executive')
	aboriginal_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Senior Leader')
	aboriginal_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	aboriginal_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Foreperson')
	aboriginal_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = aboriginal_second_mostrecent_donut_industrychart('Individual Contributor')
	
	Companydata_executive_aboriginal_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Executive')
	Companydata_senior_leader_aboriginal_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Senior Leader')
	Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Foreperson')
	Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('aboriginal_peoples', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()


	context = { 'aboriginal_executive_barchart':aboriginal_executive_barchart, 
	'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 
	'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 
	'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 
	'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 
	'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 
	'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 
	'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 
	'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 
	'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart,
	'aboriginal_executive_second_mostrecent_dchart1':aboriginal_executive_second_mostrecent_dchart1,
	'aboriginal_senior_leader_second_mostrecent_dchart1':aboriginal_senior_leader_second_mostrecent_dchart1,
	'aboriginal_manager_s_s_second_mostrecent_dchart1':aboriginal_manager_s_s_second_mostrecent_dchart1,
	'aboriginal_foreperson_leader_second_mostrecent_dchart1':aboriginal_foreperson_leader_second_mostrecent_dchart1,
	'aboriginal_individual_contributor_second_mostrecent_dchart1':aboriginal_individual_contributor_second_mostrecent_dchart1,
	'Companydata_executive_aboriginal_second_mostrecent_dchart1':Companydata_executive_aboriginal_second_mostrecent_dchart1,
	'Companydata_senior_leader_aboriginal_second_mostrecent_dchart1':Companydata_senior_leader_aboriginal_second_mostrecent_dchart1,
	'Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1':Companydata_manager_s_s_aboriginal_second_mostrecent_dchart1,
	'Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1':Companydata_foreperson_leader_aboriginal_second_mostrecent_dchart1,
	'Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1':Companydata_individual_contributor_aboriginal_second_mostrecent_dchart1,
	'year_info':year_info, 'dashboardusercompany':dashboardusercompany,

		}

	return render(request, 'dddashboard/demographic_variables/large_aboriginal.html', context)

#######################

##### Demographic Sex filtered by size #######

def small_demographicDisability(request):
		
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	

	#disabilities DATA PER POSITION
	disability_executive_barchart = size_disability_barchart_industrychart('Executive', 'small', 57)
	disability_senior_leader_barchart = size_disability_barchart_industrychart('Senior Leader', 'small', 57)
	disability_manager_s_s_leader_barchart = size_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 'small', 57)
	disability_foreperson_leader_barchart = size_disability_barchart_industrychart('Foreperson', 'small', 57)
	disability_individual_contributor_leader_barchart = size_disability_barchart_industrychart('Individual Contributor', 'small', 57)

# Company DATA QUERIES

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	### DATE FILTERED #####
			#### MOST RECENT ########
	disability_executive_second_mostrecent_dchart1, year_info = disability_second_mostrecent_donut_industrychart('Executive')
	disability_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Senior Leader')
	disability_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	disability_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Foreperson')
	disability_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Individual Contributor')
	
	Companydata_executive_disability_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Executive')
	Companydata_senior_leader_disability_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Senior Leader')
	Companydata_manager_s_s_disability_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	Companydata_foreperson_leader_disability_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Foreperson')
	Companydata_individual_contributor_disability_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()

	

	context = {'disability_executive_barchart':disability_executive_barchart, 
		   'disability_senior_leader_barchart':disability_senior_leader_barchart, 
		   'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 
		   'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 
		   'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,

		  'c_disability_executive_barchart':c_disability_executive_barchart, 
		  'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 
		  'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 
		  'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 
		  'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,

		  	'disability_executive_second_mostrecent_dchart1':disability_executive_second_mostrecent_dchart1,
			'disability_senior_leader_second_mostrecent_dchart1':disability_senior_leader_second_mostrecent_dchart1,
			'disability_manager_s_s_second_mostrecent_dchart1':disability_manager_s_s_second_mostrecent_dchart1,
			'disability_foreperson_leader_second_mostrecent_dchart1':disability_foreperson_leader_second_mostrecent_dchart1,
			'disability_individual_contributor_second_mostrecent_dchart1':disability_individual_contributor_second_mostrecent_dchart1,
			
			'Companydata_executive_disability_second_mostrecent_dchart1':Companydata_executive_disability_second_mostrecent_dchart1,
			'Companydata_senior_leader_disability_second_mostrecent_dchart1':Companydata_senior_leader_disability_second_mostrecent_dchart1,
			'Companydata_manager_s_s_disability_second_mostrecent_dchart1':Companydata_manager_s_s_disability_second_mostrecent_dchart1,
			'Companydata_foreperson_leader_disability_second_mostrecent_dchart1':Companydata_foreperson_leader_disability_second_mostrecent_dchart1,
			'Companydata_individual_contributor_disability_second_mostrecent_dchart1':Companydata_individual_contributor_disability_second_mostrecent_dchart1,
			'year_info':year_info, 'dashboardusercompany':dashboardusercompany,

		}

	

	return render(request, 'dddashboard/demographic_variables/small_persons_with_disabilities.html', context)

def large_demographicDisability(request):
		
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	

	#disabilities DATA PER POSITION
	disability_executive_barchart = size_disability_barchart_industrychart('Executive', 'large', 57)
	disability_senior_leader_barchart = size_disability_barchart_industrychart('Senior Leader', 'large', 57)
	disability_manager_s_s_leader_barchart = size_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 'large', 57)
	disability_foreperson_leader_barchart = size_disability_barchart_industrychart('Foreperson', 'large', 57)
	disability_individual_contributor_leader_barchart = size_disability_barchart_industrychart('Individual Contributor', 'large', 57)

# Company DATA QUERIES

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	### DATE FILTERED #####
			#### MOST RECENT ########
	disability_executive_second_mostrecent_dchart1, year_info = disability_second_mostrecent_donut_industrychart('Executive')
	disability_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Senior Leader')
	disability_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	disability_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Foreperson')
	disability_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = disability_second_mostrecent_donut_industrychart('Individual Contributor')
	
	Companydata_executive_disability_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Executive')
	Companydata_senior_leader_disability_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Senior Leader')
	Companydata_manager_s_s_disability_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	Companydata_foreperson_leader_disability_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Foreperson')
	Companydata_individual_contributor_disability_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('person_with_disabilities', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()


	context = {'disability_executive_barchart':disability_executive_barchart, 
		   'disability_senior_leader_barchart':disability_senior_leader_barchart, 
		   'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 
		   'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 
		   'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,

		  'c_disability_executive_barchart':c_disability_executive_barchart, 
		  'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 
		  'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 
		  'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 
		  'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,

		  	'disability_executive_second_mostrecent_dchart1':disability_executive_second_mostrecent_dchart1,
			'disability_senior_leader_second_mostrecent_dchart1':disability_senior_leader_second_mostrecent_dchart1,
			'disability_manager_s_s_second_mostrecent_dchart1':disability_manager_s_s_second_mostrecent_dchart1,
			'disability_foreperson_leader_second_mostrecent_dchart1':disability_foreperson_leader_second_mostrecent_dchart1,
			'disability_individual_contributor_second_mostrecent_dchart1':disability_individual_contributor_second_mostrecent_dchart1,
			
			'Companydata_executive_disability_second_mostrecent_dchart1':Companydata_executive_disability_second_mostrecent_dchart1,
			'Companydata_senior_leader_disability_second_mostrecent_dchart1':Companydata_senior_leader_disability_second_mostrecent_dchart1,
			'Companydata_manager_s_s_disability_second_mostrecent_dchart1':Companydata_manager_s_s_disability_second_mostrecent_dchart1,
			'Companydata_foreperson_leader_disability_second_mostrecent_dchart1':Companydata_foreperson_leader_disability_second_mostrecent_dchart1,
			'Companydata_individual_contributor_disability_second_mostrecent_dchart1':Companydata_individual_contributor_disability_second_mostrecent_dchart1,
			'year_info':year_info, 'dashboardusercompany':dashboardusercompany,

		}

	

	return render(request, 'dddashboard/demographic_variables/large_persons_with_disabilities.html', context)

#######################

##### Demographic Sex filtered by size #######

def small_demographicMinority(request):
		
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	


	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = size_minority_barchart_industrychart('Executive', "small", 49)
	minority_senior_leader_barchart = size_minority_barchart_industrychart('Senior Leader', "small", 49)
	minority_manager_s_s_leader_barchart = size_minority_barchart_industrychart('Manager/Supervisor/Superintendent', "small", 49)
	minority_foreperson_leader_barchart = size_minority_barchart_industrychart('Foreperson', "small", 49)
	minority_individual_contributor_leader_barchart = size_minority_barchart_industrychart('Individual Contributor', "small", 49)


	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 49)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 49)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 49)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 49)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 49)


	### DATE FILTERED #####
			####Second MOST RECENT ########
	minority_executive_second_mostrecent_dchart1, year_info = minority_second_mostrecent_donut_industrychart('Executive')
	Companydata_executive_minority_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Executive')
	minority_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Senior Leader')
	Companydata_senior_leader_minority_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Senior Leader')
	minority_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	Companydata_manager_s_s_minority_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	minority_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Foreperson')
	Companydata_foreperson_leader_minority_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Foreperson')
	minority_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Individual Contributor')
	Companydata_individual_contributor_minority_second_mostrecent_dchart1, year_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()
	



	context = {'minority_executive_barchart':minority_executive_barchart,
	'minority_senior_leader_barchart':minority_senior_leader_barchart, 
	'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 
	'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 
	'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart,
	
	'c_minority_executive_barchart':c_minority_executive_barchart, 
	'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart,
	'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 
	'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart,
	'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart,
	
	'minority_executive_second_mostrecent_dchart1':minority_executive_second_mostrecent_dchart1,
	'minority_senior_leader_second_mostrecent_dchart1':minority_senior_leader_second_mostrecent_dchart1,
	'minority_manager_s_s_second_mostrecent_dchart1':minority_manager_s_s_second_mostrecent_dchart1,
	'minority_foreperson_leader_second_mostrecent_dchart1':minority_foreperson_leader_second_mostrecent_dchart1,
	'minority_individual_contributor_second_mostrecent_dchart1':minority_individual_contributor_second_mostrecent_dchart1,
	
	'Companydata_executive_minority_second_mostrecent_dchart1':Companydata_executive_minority_second_mostrecent_dchart1,
	'Companydata_senior_leader_minority_second_mostrecent_dchart1':Companydata_senior_leader_minority_second_mostrecent_dchart1,
	'Companydata_manager_s_s_minority_second_mostrecent_dchart1':Companydata_manager_s_s_minority_second_mostrecent_dchart1,
	'Companydata_foreperson_leader_minority_second_mostrecent_dchart1':Companydata_foreperson_leader_minority_second_mostrecent_dchart1,
	'Companydata_individual_contributor_minority_second_mostrecent_dchart1':Companydata_individual_contributor_minority_second_mostrecent_dchart1,
	'year_info':year_info, 'dashboardusercompany':dashboardusercompany,
	}


	return render(request, 'dddashboard/demographic_variables/small_visible_minority.html', context)

def large_demographicMinority(request):
		
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	
	dashboardusercompany = dashboarduserinfo.company_name
	


	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = size_minority_barchart_industrychart('Executive', "large", 49)
	minority_senior_leader_barchart = size_minority_barchart_industrychart('Senior Leader', "large", 49)
	minority_manager_s_s_leader_barchart = size_minority_barchart_industrychart('Manager/Supervisor/Superintendent', "large", 49)
	minority_foreperson_leader_barchart = size_minority_barchart_industrychart('Foreperson', "large", 49)
	minority_individual_contributor_leader_barchart = size_minority_barchart_industrychart('Individual Contributor', "large", 49)


	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 49)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 49)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 49)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 49)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 49)


	### DATE FILTERED #####
			####Second MOST RECENT ########
	minority_executive_second_mostrecent_dchart1, year_info = minority_second_mostrecent_donut_industrychart('Executive')
	Companydata_executive_minority_second_mostrecent_dchart1, Companydata_executive_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Executive')
	minority_senior_leader_second_mostrecent_dchart1, sexchart_senior_leader_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Senior Leader')
	Companydata_senior_leader_minority_second_mostrecent_dchart1, Companydata_senior_leader_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Senior Leader')
	minority_manager_s_s_second_mostrecent_dchart1, sexchart_manager_s_s_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Manager/Supervisor/Superintendent')
	Companydata_manager_s_s_minority_second_mostrecent_dchart1, Companydata_manager_s_s_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Manager/Supervisor/Superintendent')
	minority_foreperson_leader_second_mostrecent_dchart1, sexchart_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Foreperson')
	Companydata_foreperson_leader_minority_second_mostrecent_dchart1, Companydata_sexchart_hole_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Foreperson')
	minority_individual_contributor_second_mostrecent_dchart1, sexchart_second_mostrecent_hole_info = minority_second_mostrecent_donut_industrychart('Individual Contributor')
	Companydata_individual_contributor_minority_second_mostrecent_dchart1, year_info = Companydata_create_donut_second_mostrecent_chart('visible_minorities', dashboardusercompany, 'Individual Contributor')

	dashboardusercompany = str(dashboardusercompany).upper()




	context = {'minority_executive_barchart':minority_executive_barchart,
	'minority_senior_leader_barchart':minority_senior_leader_barchart, 
	'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 
	'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 
	'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart,
	
	'c_minority_executive_barchart':c_minority_executive_barchart, 
	'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart,
	'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 
	'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart,
	'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart,
	
	'minority_executive_second_mostrecent_dchart1':minority_executive_second_mostrecent_dchart1,
	'minority_senior_leader_second_mostrecent_dchart1':minority_senior_leader_second_mostrecent_dchart1,
	'minority_manager_s_s_second_mostrecent_dchart1':minority_manager_s_s_second_mostrecent_dchart1,
	'minority_foreperson_leader_second_mostrecent_dchart1':minority_foreperson_leader_second_mostrecent_dchart1,
	'minority_individual_contributor_second_mostrecent_dchart1':minority_individual_contributor_second_mostrecent_dchart1,
	
	'Companydata_executive_minority_second_mostrecent_dchart1':Companydata_executive_minority_second_mostrecent_dchart1,
	'Companydata_senior_leader_minority_second_mostrecent_dchart1':Companydata_senior_leader_minority_second_mostrecent_dchart1,
	'Companydata_manager_s_s_minority_second_mostrecent_dchart1':Companydata_manager_s_s_minority_second_mostrecent_dchart1,
	'Companydata_foreperson_leader_minority_second_mostrecent_dchart1':Companydata_foreperson_leader_minority_second_mostrecent_dchart1,
	'Companydata_individual_contributor_minority_second_mostrecent_dchart1':Companydata_individual_contributor_minority_second_mostrecent_dchart1,
	'year_info':year_info, 'dashboardusercompany':dashboardusercompany,
	}


	return render(request, 'dddashboard/demographic_variables/large_visible_minority.html', context)

#######################

def contact(request):

	username = request.user
	dashboarduserinfo = Dashboard_user.objects.get(name=username)
	dashboarduseremail = dashboarduserinfo.email


	if request.method == 'POST':
		
		
		message = request.POST['message']
		message_from = 'message from: ' + str(dashboarduseremail)
		message = str(message_from) +str(" ") +"message: " + str(message)
		

		send_mail(
			username,
			message,
			dashboarduseremail, 
			['hello@envolstrategies.com'],
			)
		return render (request, 'dddashboard/contact.html', {'username': username, 'message': message})

	else:
		context = {'username': username, 'dashboarduseremail':dashboarduseremail}
		return render(request, 'dddashboard/contact.html', context)




def test(request):
	dashboarduser = request.user
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	dashboardusercompany = dashboarduserinfo.company_name
	dashboardusercompany_ID = dashboarduserinfo.company_name_id
	
	chart_key_1 = 'queryset1'
	cached_queryset1 = cache.get(chart_key_1)
	if not cached_queryset1:

		queryset1 = CompanyData.objects.all().select_related('name')
		cache.set(chart_key_1, queryset1, 3600)
		cached_queryset1 = cache.get(chart_key_1)

	chart_key_2 = f'queryset2_{dashboardusercompany_ID}'
	cached_queryset2 = cache.get(chart_key_2)
	if not cached_queryset2:

		queryset2 = CompanyData.objects.filter(name_id=dashboardusercompany_ID).select_related('name')
		cache.set(chart_key_2, queryset2, 3600)
		cached_queryset2 = cache.get(chart_key_2)

	context = jcontextCreator(dashboardusercompany_ID, dashboardusercompany, cached_queryset1, cached_queryset2)

	return render(request, 'dddashboard/test.html', context)

