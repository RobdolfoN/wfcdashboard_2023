import pathlib

import pandas as pd
from .models import *
import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Count, Q
from django.core.cache import cache
from datetime import datetime, timedelta
from functools import wraps
import json
from django.http import JsonResponse
import plotly.utils
from plotly.utils import PlotlyJSONEncoder
import plotly.io as pio



def handle_uploaded_file(f):
    #checar extension del archivo "f"
    file_extension = str(f)
    file_extension = pathlib.Path(file_extension).suffix
    
    if file_extension == ".csv":
        #leer archivo csv y crear 'data frame'
        df = pd.read_csv(f, index_col=False)
        #cambiar la leyenda de las columnas a minusculas
        df.columns = df.columns.str.lower()
        #crear nuevo dataframe con las columnas seleccionadas
        seleccionadas = df[["gender code", "aboriginal peoples", "visible minorities", "person with disabilities", "position/role category"]]
        #selecciona una sola columna
        # print(seleccionadas["gender code"])
        #cambia el conteido a minuscula
        # print(seleccionadas["gender code"].str.lower())
    
    elif file_extension == ".xls":
        df = pd.read_excel(f)
        df = df.to_csv(df)
        df = df.read_csv(df, index_col=False)
        df.columns = df.columns.str.lower()
        print(df)
        # seleccionadas = df[["gender code", "aboriginal peoples", "visible minorities", "person with disabilities", "position/role category"]]

    elif file_extension == ".xlsx":
        df = pd.read_excel(f)
        df = df.to_csv(df)
        df = df.read_csv(df, index_col=False)
        df.columns = df.columns.str.lower()
        print(df)
        # seleccionadas = df[["gender code", "aboriginal peoples", "visible minorities", "person with disabilities", "position/role category"]]

    else:
        print("quien sabe")

    return seleccionadas




#chart colours
colour1 = '#2789AB' #blueformale
colour2 = '#8ACAD8' #blueforfemale#noforVisivleminority#noaboriginal#nodisabilitie
colour3 = '#F6CB7F' #othersexamarillo
pie_anotations_font_color = '#174F6D'


def jcontextCreator(dashboardusercompany, companyname, cached_queryset1, cached_queryset2):
    minority_dchart1, minority_hole_info =  q_minority_donut_industrychart(cached_queryset1)
    sex_dchart1, sexchart_hole_info =  q_sex_donut_industrychart(cached_queryset1)
    aboriginal_dchart1, aboriginal_hole_info =  q_aboriginal_donut_industrychart(cached_queryset1)
    disability_dchart1, disability_hole_info =  q_disability_donut_industrychart(cached_queryset1)

    sex_executive_barchart = q_sex_barchart_industrychart('Executive', 25, cached_queryset1)
    sex_senior_leader_barchart = q_sex_barchart_industrychart('Senior Leader', 25, cached_queryset1)
    sex_manager_s_s_leader_barchart = q_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset1)
    sex_foreperson_leader_barchart = q_sex_barchart_industrychart('Foreperson', 25, cached_queryset1)
    sex_individual_contributor_leader_barchart = q_sex_barchart_industrychart('Individual Contributor', 25, cached_queryset1)

    minority_executive_barchart = q_minority_barchart_industrychart('Executive', 25, cached_queryset1)
    minority_senior_leader_barchart = q_minority_barchart_industrychart('Senior Leader', 25, cached_queryset1)
    minority_manager_s_s_leader_barchart = q_minority_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset1)
    minority_foreperson_leader_barchart = q_minority_barchart_industrychart('Foreperson', 25, cached_queryset1)
    minority_individual_contributor_leader_barchart = q_minority_barchart_industrychart('Individual Contributor', 25, cached_queryset1)

    aboriginal_executive_barchart = q_aboriginal_barchart_industrychart('Executive', 25, cached_queryset1)
    aboriginal_senior_leader_barchart = q_aboriginal_barchart_industrychart('Senior Leader', 25, cached_queryset1)
    aboriginal_manager_s_s_leader_barchart = q_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset1)
    aboriginal_foreperson_leader_barchart = q_aboriginal_barchart_industrychart('Foreperson', 25, cached_queryset1)
    aboriginal_individual_contributor_leader_barchart = q_aboriginal_barchart_industrychart('Individual Contributor', 25, cached_queryset1)

    disability_executive_barchart = q_disability_barchart_industrychart('Executive', 25, cached_queryset1)
    disability_senior_leader_barchart = q_disability_barchart_industrychart('Senior Leader', 25, cached_queryset1)
    disability_manager_s_s_leader_barchart = q_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset1)
    disability_foreperson_leader_barchart = q_disability_barchart_industrychart('Foreperson', 25, cached_queryset1)
    disability_individual_contributor_leader_barchart = q_disability_barchart_industrychart('Individual Contributor', 25, cached_queryset1)
    
    Companydata_sex_dchart1, Companydata_sexchart_hole_info =  q_Companydata_sex_donut_industrychart(cached_queryset2)
    Companydata_minority_dchart1, Companydata_minority_hole_info =  q_Companydata_create_donut_chart('visible_minorities', cached_queryset2)
    Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  q_Companydata_create_donut_chart('aboriginal_peoples', cached_queryset2)
    Companydata_disability_dchart1, Companydata_disability_hole_info =  q_Companydata_create_donut_chart('person_with_disabilities', cached_queryset2)

    c_sex_executive_barchart = q_c_sex_barchart_industrychart('Executive', 25, cached_queryset2)
    c_sex_senior_leader_barchart = q_c_sex_barchart_industrychart('Senior Leader', 25, cached_queryset2)
    c_sex_manager_s_s_leader_barchart = q_c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset2)
    c_sex_foreperson_leader_barchart = q_c_sex_barchart_industrychart('Foreperson', 25, cached_queryset2)
    c_sex_individual_contributor_leader_barchart = q_c_sex_barchart_industrychart('Individual Contributor', 25, cached_queryset2)

    c_minority_executive_barchart = q_c_minority_barchart_industrychart('Executive', 25, cached_queryset2)
    c_minority_senior_leader_barchart = q_c_minority_barchart_industrychart('Senior Leader', 25, cached_queryset2)
    c_minority_manager_s_s_leader_barchart = q_c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset2)
    c_minority_foreperson_leader_barchart = q_c_minority_barchart_industrychart('Foreperson', 25, cached_queryset2)
    c_minority_individual_contributor_leader_barchart = q_c_minority_barchart_industrychart('Individual Contributor', 25, cached_queryset2)

    c_aboriginal_executive_barchart = q_c_aboriginal_barchart_industrychart('Executive', 25, cached_queryset2)
    c_aboriginal_senior_leader_barchart = q_c_aboriginal_barchart_industrychart('Senior Leader', 25, cached_queryset2)
    c_aboriginal_manager_s_s_leader_barchart = q_c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset2)
    c_aboriginal_foreperson_leader_barchart = q_c_aboriginal_barchart_industrychart('Foreperson', 25, cached_queryset2)
    c_aboriginal_individual_contributor_leader_barchart = q_c_aboriginal_barchart_industrychart('Individual Contributor', 25, cached_queryset2)

    c_disability_executive_barchart = q_c_disability_barchart_industrychart('Executive', 25, cached_queryset2)
    c_disability_senior_leader_barchart = q_c_disability_barchart_industrychart('Senior Leader', 25, cached_queryset2)
    c_disability_manager_s_s_leader_barchart = q_c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 25, cached_queryset2)
    c_disability_foreperson_leader_barchart = q_c_disability_barchart_industrychart('Foreperson', 25, cached_queryset2)
    c_disability_individual_contributor_leader_barchart = q_c_disability_barchart_industrychart('Individual Contributor', 25, cached_queryset2)


    dashboardusercompany = str(dashboardusercompany).upper()

    context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 
		'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 
		'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 
		'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 
		'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 
		'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		'companyname':companyname,
		}
    return context

def q_minority_donut_industrychart(cached_queryset1):
    cache_key = 'q_minority_donut_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    labels = ['Yes','No']
    colors = [colour2, colour3]
    return q_create_donut_chart("Minority", "visible_minorities", labels, colors, "Yes", cached_queryset1)

def q_sex_donut_industrychart(cached_queryset1):

    cache_key = 'q_sex_donut_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = datetime.now().year
    male = cached_queryset1.filter(gender_code='M', year_created=most_recent_date).count()
    female = cached_queryset1.filter(gender_code='F', year_created=most_recent_date).count()
    other = cached_queryset1.filter(gender_code='O', year_created=most_recent_date).count()
    total = cached_queryset1.filter(year_created=most_recent_date).count()

    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    hole_info = ((female*100)/total)
    hole_info = str(round(hole_info))+str('%')

            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
        height=175,
         )
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}

    chart = json.dumps(fig.to_dict())

    return chart, hole_info

def q_aboriginal_donut_industrychart(cached_queryset1):
    cache_key = 'q_aboriginal_donut_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    labels = ['Yes','No']
    colors = [colour2, colour3]
    return q_create_donut_chart('Aboriginal', "aboriginal_peoples", labels, colors, "Yes", cached_queryset1)

def q_disability_donut_industrychart(cached_queryset1):
    cache_key = 'q_disability_donut_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    labels = ['Yes','No']
    colors = [colour2, colour3]
    return q_create_donut_chart("Disability", "person_with_disabilities", labels, colors, "Yes", cached_queryset1)

def q_sex_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_sex_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result


    most_recent_date = datetime.now().year
    gender_codes = ['M', 'F', 'O']
    data = cached_queryset1.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(year_created=most_recent_date)).values('gender_code').annotate(count=Count('gender_code'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count'] / total_count * 100],
                name=d['gender_code'],
                text=d['gender_code'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=10),
                orientation='h',
                marker=dict(
                    color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())


        return chart

def q_minority_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_minority_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = datetime.now().year
    visible_minorities = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(year_created=most_recent_date)).values('visible_minorities').annotate(count=Count('visible_minorities'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count'] / total_count * 100],
                name=d['visible_minorities'],
                text=d['visible_minorities'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=10),
                orientation='h',
                marker=dict(
                    color=colour2 if d['visible_minorities'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def q_aboriginal_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_aboriginal_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = datetime.now().year
    aboriginal_peoples = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(year_created=most_recent_date)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count'] / total_count * 100],
                name=d['aboriginal_peoples'],
                text=d['aboriginal_peoples'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=12),

                orientation='h',
                marker=dict(
                    color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def q_disability_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_disability_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = datetime.now().year
    person_with_disabilities = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(year_created=most_recent_date)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count']],
                name=d['person_with_disabilities'],
                text=d['person_with_disabilities'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=10),

                orientation='h',
                marker=dict(
                    color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())
        return chart

def q_Companydata_sex_donut_industrychart(cached_queryset2):
    

    most_recent_date = datetime.now().year
    male = cached_queryset2.filter(gender_code='M', year_created=most_recent_date).count()
    female = cached_queryset2.filter(gender_code='F', year_created=most_recent_date).count()
    other = cached_queryset2.filter(gender_code='O', year_created=most_recent_date).count()
    total = cached_queryset2.filter(year_created=most_recent_date).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0:

            # hole_info 
        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')
        print(hole_info)


                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            height=175,
            )
        
        
        fig.update_traces(textinfo='none')
        chart = json.dumps(fig.to_dict())

        return chart, hole_info

    else:

                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text='No Company Info', x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            height=175,
            )
        
        
        fig.update_traces(textinfo='none')
        chart = json.dumps(fig.to_dict())
        return chart, "No Company info"

def q_c_sex_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = datetime.now().year
    gender_codes = ['M', 'F', 'O']
    data = cached_queryset2.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(year_created=most_recent_date)).values('gender_code').annotate(count=Count('gender_code'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count'] / total_count * 100],
                name=d['gender_code'],
                text=d['gender_code'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=10),
                orientation='h',
                marker=dict(
                    color=colour1 if d['gender_code'] == 'M' else colour2 if d['gender_code'] == 'F' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def q_c_minority_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = datetime.now().year
    visible_minorities = ['Y', 'N']
    data = cached_queryset2.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(year_created=most_recent_date)).values('visible_minorities').annotate(count=Count('visible_minorities'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count'] / total_count * 100],
                name=d['visible_minorities'],
                text=d['visible_minorities'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=10),
                orientation='h',
                marker=dict(
                    color=colour2 if d['visible_minorities'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def q_c_aboriginal_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = datetime.now().year
    aboriginal_peoples = ['Y', 'N']
    data = cached_queryset2.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(year_created=most_recent_date)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count']],
                name=d['aboriginal_peoples'],
                text=d['aboriginal_peoples'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=10),

                orientation='h',
                marker=dict(
                    color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())


        return chart

def q_c_disability_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = datetime.now().year
    person_with_disabilities = ['Y', 'N']
    data = cached_queryset2.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(year_created=most_recent_date)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
    if len(data) == 0:
        return "No data available."
    else:
        total_count = sum([d['count'] for d in data])
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(
                y=[position],
                x=[d['count'] / total_count * 100],
                name=d['person_with_disabilities'],
                text=d['person_with_disabilities'] + ': ' + str(round(d['count'] / total_count * 100, 1)) + '%',
                textposition='inside',
                textfont=dict(color='white', size=10),
                orientation='h',
                marker=dict(
                    color=colour2 if d['person_with_disabilities'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def q_Companydata_create_donut_chart(field_name, cached_queryset2):
    # Get the count of 'Y' and 'N' values for the field
    most_recent_date = datetime.now().year
    data = cached_queryset2.filter(year_created=most_recent_date).values(field_name).annotate(count=Count(field_name))
    yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
    no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
    total = yes_count + no_count

    labels = ['Yes','No']
    values = [yes_count, no_count]
    colors = [colour2, colour3]

    if total is not 0:

        # hole_info
        hole_info = ((yes_count*100)/total)
        hole_info = str(round(hole_info)) + '%'

        # Create the donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            height=175,
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        chart = json.dumps(fig.to_dict())

        return chart, hole_info

    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="No Company Info", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            height=175,
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        chart = json.dumps(fig.to_dict())


        return chart, "No Company Info"

def q_create_donut_chart(category, category_field, labels, colors, hole_info_text, cached_queryset1):
  
    # filter the data and count the number of items that match the filter
    most_recent_date = datetime.now().year
    data = {}
    for label, value in zip(labels, ['Y', 'N', 'O']):
        data[label] = cached_queryset1.filter(**{category_field: value}, year_created=most_recent_date).count()
    total = cached_queryset1.all().count()

    # calculate the percentage of the hole_info
    hole_info = ((data[hole_info_text]*100)/total)
    hole_info = str(round(hole_info))+str('%')

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, modebar_remove="v1hovermode", autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
        height=175,

         )
    fig.update_traces(textinfo='none')
    
    chart = json.dumps(fig.to_dict())

    return chart, hole_info

def q_customize_chart(fig, cheight):
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),

        barmode='stack',
        plot_bgcolor='#F4F9FA',
        paper_bgcolor='#F4F9FA',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        #width=450,
        height=cheight,
        autosize=True,
    )
    
    config = {'displayModeBar': False}
    return fig


