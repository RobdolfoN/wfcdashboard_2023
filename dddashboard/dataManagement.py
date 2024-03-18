import pathlib

import pandas as pd
from .models import *
import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Count, Q, Max
from django.core.cache import cache
from datetime import datetime, timedelta
from functools import wraps
import json
import datetime




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







def Companydata_sex_donut_industrychart(company):
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    male = CompanyData.objects.filter(gender_code='M', name=company, year_created=most_recent_date_str).count()
    female = CompanyData.objects.filter(gender_code='F', name=company, year_created=most_recent_date_str).count()
    other = CompanyData.objects.filter(gender_code='O', name=company, year_created=most_recent_date_str).count()
    total = CompanyData.objects.filter(name=company, year_created=most_recent_date_str).count()


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
        config = {'displayModeBar': False}
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())


        return chart, "No Company info"

def Companydata_create_donut_chart(field_name, company):
    # Get the count of 'Y' and 'N' values for the field
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    
    data = CompanyData.objects.filter(name=company, year_created=most_recent_date_str).values(field_name).annotate(count=Count(field_name))
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
        config = {'displayModeBar': False}
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, "No Company Info"

def customize_chart(fig, cheight):
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

def sex_barchart_industrychart(position, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    gender_codes = ['M', 'F', 'O']
    data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('gender_code').annotate(count=Count('gender_code'))
    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def c_sex_barchart_industrychart(position, company, cheight):
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    gender_codes = ['M', 'F', 'O']
    data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date_str)).values('gender_code').annotate(count=Count('gender_code'))

    if len(data) == 0:
        return None


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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart


def minority_barchart_industrychart(position, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    visible_minorities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('visible_minorities').annotate(count=Count('visible_minorities'))
    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def c_minority_barchart_industrychart(position, company, cheight):
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    visible_minorities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date_str)).values('visible_minorities').annotate(count=Count('visible_minorities'))

    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def aboriginal_barchart_industrychart(position, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    aboriginal_peoples = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
    if len(data) == 0:
        return None
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
                textfont=dict(color='white', size=10),

                orientation='h',
                marker=dict(
                    color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())


        return chart

def c_aboriginal_barchart_industrychart(position, company, cheight):
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    aboriginal_peoples = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date_str)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
    
    if len(data) == 0:
        return None
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
                textfont=dict(color='white', size=10),

                orientation='h',
                marker=dict(
                    color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def disability_barchart_industrychart(position, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    person_with_disabilities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def c_disability_barchart_industrychart(position, company, cheight):
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    person_with_disabilities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(name=company) & Q(year_created=most_recent_date_str)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

### company size  filter##
def size_sex_barchart_industrychart(position, size, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    gender_codes = ['M', 'F', 'O']
    data = CompanyData.objects.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('gender_code').annotate(count=Count('gender_code'))
    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())

        return chart

def size_minority_barchart_industrychart(position, size, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    visible_minorities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('visible_minorities').annotate(count=Count('visible_minorities'))
    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())


        return chart

def size_aboriginal_barchart_industrychart(position, size, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    aboriginal_peoples = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
    if len(data) == 0:
        return None
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
                textfont=dict(color='white', size=10),

                orientation='h',
                marker=dict(
                    color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())


        return chart

def size_disability_barchart_industrychart(position, size, cheight):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    person_with_disabilities = ['Y', 'N']
    data = CompanyData.objects.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
    if len(data) == 0:
        return None
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
        customize_chart(fig, cheight)
        chart = json.dumps(fig.to_dict())


        return chart

def size_create_donut_chart(field_name, size):
    # Get the count of 'Y' and 'N' values for the field
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    data = CompanyData.objects.filter(company_size=size, year_created=most_recent_date_str).values(field_name).annotate(count=Count(field_name))
    yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
    no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
    total = yes_count + no_count

    labels = ['Yes','No']
    values = [yes_count, no_count]
    colors = [colour2, colour3]

    if total is not 0:

        hole_info = ((yes_count*100)/total)
        hole_info = str(round(hole_info)) + '%'

        # Create the donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        chart = json.dumps(fig.to_dict())


        return chart, hole_info
    
    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        chart = json.dumps(fig.to_dict())


        return chart, "0"

def size_sex_donut_industrychart(size):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    male = CompanyData.objects.filter(gender_code='M', company_size=size, year_created=most_recent_date_str).count()
    female = CompanyData.objects.filter(gender_code='F', company_size=size, year_created=most_recent_date_str).count()
    other = CompanyData.objects.filter(gender_code='O', company_size=size, year_created=most_recent_date_str).count()
    total = CompanyData.objects.filter(company_size=size, year_created=most_recent_date_str).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0: 
        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')
        print(hole_info)


                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')#, default_width='150')

        return chart, hole_info

    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        chart = json.dumps(fig.to_dict())


        return chart, "0"

def create_donut_chart(category, category_field, labels, colors, hole_info_text):
    """
    Creates a donut chart for the given category

    Args:
    category (str): The name of the category for the chart (e.g. 'Disability')
    category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
    labels (list of str): The labels for the chart's segments
    colors (list of str): The colors for the chart's segments
    hole_info_text (str): The text to be displayed in the center of the chart

    Returns:
    tuple: containing chart data in html format and hole_info
    """
    # filter the data and count the number of items that match the filter
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    data = {}
    for label, value in zip(labels, ['Y', 'N', 'O']):
        data[label] = CompanyData.objects.filter(**{category_field: value}, year_created=most_recent_date_str).count()
    total = CompanyData.objects.all().count()

    # calculate the percentage of the hole_info
    hole_info = ((data[hole_info_text]*100)/total)
    hole_info = str(round(hole_info))+str('%')

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
        height=175,
         )
    fig.update_traces(textinfo='none')
    chart = json.dumps(fig.to_dict())

    return chart, hole_info

def sex_donut_industrychart():
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    male = CompanyData.objects.filter(gender_code='M', year_created=most_recent_date_str).count()
    female = CompanyData.objects.filter(gender_code='F', year_created=most_recent_date_str).count()
    other = CompanyData.objects.filter(gender_code='O', year_created=most_recent_date_str).count()
    total = CompanyData.objects.filter(year_created=most_recent_date_str).count()

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
    chart = json.dumps(fig.to_dict())


    return chart, hole_info

def minority_donut_industrychart():
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_donut_chart("Minority", "visible_minorities", labels, colors, "Yes")

def aboriginal_donut_industrychart():
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_donut_chart('Aboriginal', "aboriginal_peoples", labels, colors, "Yes")

def disability_donut_industrychart():
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_donut_chart("Disability", "person_with_disabilities", labels, colors, "Yes")


############### For Size ##########################








############## DEMOGRAPHIC VARIABLES DATE FILTERED FUNCTIONS _ second most recentd date ###############

def sex_donut_second_mostrecent_industrychart(position):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    most_recent_date_str = most_recent_date_str.split('-')[0]
    most_recent_date_str = int(most_recent_date_str)
    second_most_recent_date = (most_recent_date_str - 1)
    second_most_recent_date = f"{str(second_most_recent_date)}-01-01"

    male = CompanyData.objects.filter(gender_code='M', position_category=position, year_created=second_most_recent_date).count()
    female = CompanyData.objects.filter(gender_code='F', position_category=position, year_created=second_most_recent_date).count()
    other = CompanyData.objects.filter(gender_code='O', position_category=position, year_created=second_most_recent_date).count()
    total = CompanyData.objects.filter(position_category=position, year_created=second_most_recent_date).count()

    print('second most recent',male)

    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]
    
    if total != 0:

        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')

                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())
        
        return chart, hole_info
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())


        return chart, "No Company info"

def size_sex_donut_second_mostrecent_industrychart(position, size):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    most_recent_date_str = most_recent_date_str.split('-')[0]
    most_recent_date_str = int(most_recent_date_str)
    second_most_recent_date = (most_recent_date_str - 1)
    second_most_recent_date = f"{str(second_most_recent_date)}-01-01"


    male = CompanyData.objects.filter(gender_code='M', position_category=position, year_created=second_most_recent_date, company_size=size).count()
    female = CompanyData.objects.filter(gender_code='F', position_category=position, year_created=second_most_recent_date, company_size=size).count()
    other = CompanyData.objects.filter(gender_code='O', position_category=position, year_created=second_most_recent_date, company_size=size).count()
    total = CompanyData.objects.filter(position_category=position, year_created=second_most_recent_date).count()

    print('second most recent',male)

    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]
    
    if total is not 0:

        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')

                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())
        
        return chart, hole_info
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}

        chart = json.dumps(fig.to_dict())



        return chart, "No Company info"


def Companydata_sex_donut_second_mostrecent_industrychart(company, position):
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    most_recent_date_str = most_recent_date_str.split('-')[0]
    most_recent_date_str = int(most_recent_date_str)
    second_most_recent_date = (most_recent_date_str - 1)
    second_most_recent_date = f"{str(second_most_recent_date)}-01-01"


    male = CompanyData.objects.filter(gender_code='M', name=company, position_category=position, year_created=second_most_recent_date).count()
    female = CompanyData.objects.filter(gender_code='F', name=company, position_category=position, year_created=second_most_recent_date).count()
    other = CompanyData.objects.filter(gender_code='O', name=company, position_category=position, year_created=second_most_recent_date).count()
    total = CompanyData.objects.filter(name=company, position_category=position, year_created=second_most_recent_date).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0:

            # hole_info 
        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')
        print(hole_info)


                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, hole_info
    
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, "No Company info"

def size_Companydata_sex_donut_second_mostrecent_industrychart(company, position, size):
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    most_recent_date_str = most_recent_date_str.split('-')[0]
    most_recent_date_str = int(most_recent_date_str)
    second_most_recent_date = (most_recent_date_str - 1)
    second_most_recent_date = f"{str(second_most_recent_date)}-01-01"
    male = CompanyData.objects.filter(gender_code='M', name=company, position_category=position, year_created=second_most_recent_date, company_size=size).count()
    female = CompanyData.objects.filter(gender_code='F', name=company, position_category=position, year_created=second_most_recent_date, company_size=size).count()
    other = CompanyData.objects.filter(gender_code='O', name=company, position_category=position, year_created=second_most_recent_date, company_size=size).count()
    total = CompanyData.objects.filter(name=company, position_category=position, year_created=second_most_recent_date).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0:

            # hole_info 
        hole_info = ((female*100)/total)
        hole_info = str(round(hole_info))+str('%')
        print(hole_info)


                # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())
        # chart = fig.to_html(config=config, default_height='150')#, default_width='150')

        return chart, hole_info
    
    else:
                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=11, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.47, font_size=9, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        # chart = fig.to_html(config=config, default_height='150')#, default_width='150')

        return chart, "No Company Info"


def create_second_mostrecent_donut_chart(position, category, category_field, labels, colors, hole_info_text):
    """
    Creates a donut chart for the given category

    Args:
    category (str): The name of the category for the chart (e.g. 'Disability')
    category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
    labels (list of str): The labels for the chart's segments
    colors (list of str): The colors for the chart's segments
    hole_info_text (str): The text to be displayed in the center of the chart

    Returns:
    tuple: containing chart data in html format and hole_info
    """
    # filter the data and count the number of items that match the filter
    data = {}
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    most_recent_date_str = most_recent_date_str.split('-')[0]
    most_recent_date_str = int(most_recent_date_str)
    second_most_recent_date = (most_recent_date_str - 1)
    second_most_recent_date = f"{str(second_most_recent_date)}-01-01"
    
    total = 0
    for label, value in zip(labels, ['Y', 'N', 'O']):
        data[label] = CompanyData.objects.filter(**{category_field: value}, year_created=second_most_recent_date, position_category=position).count()
        count = data[label]
        total += count
    # total = CompanyData.objects.all().count()

    # calculate the percentage of the hole_info
    if total != 0:
        hole_info = ((data[hole_info_text]*100)/total)
        hole_info = str(round(hole_info))+str('%')
    else:
        hole_info = 0
    

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = json.dumps(fig.to_dict())

    # chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info

def size_create_second_mostrecent_donut_chart(position, category, category_field, labels, colors, hole_info_text, size):
    """
    Creates a donut chart for the given category

    Args:
    category (str): The name of the category for the chart (e.g. 'Disability')
    category_field (str): The field of the CompanyData object to filter on (e.g. 'person_with_disabilities')
    labels (list of str): The labels for the chart's segments
    colors (list of str): The colors for the chart's segments
    hole_info_text (str): The text to be displayed in the center of the chart

    Returns:
    tuple: containing chart data in html format and hole_info
    """
    # filter the data and count the number of items that match the filter
    data = {}
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    most_recent_date_str = most_recent_date_str.split('-')[0]
    most_recent_date_str = int(most_recent_date_str)
    second_most_recent_date = (most_recent_date_str - 1)
    second_most_recent_date = f"{str(second_most_recent_date)}-01-01"
    
    

    
    
    for label, value in zip(labels, ['Y', 'N', 'O']):
        data[label] = CompanyData.objects.filter(**{category_field: value}, year_created=second_most_recent_date, position_category=position).count()
    total = CompanyData.objects.all().count()

    # calculate the percentage of the hole_info
    hole_info = ((data[hole_info_text]*100)/total)
    hole_info = str(round(hole_info))+str('%')

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=list(data.values()), hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text=hole_info_text, x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
         )
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}
    chart = json.dumps(fig.to_dict())

    # chart = fig.to_html(config=config, default_height='175')#, default_width='150')

    return chart, hole_info


def minority_second_mostrecent_donut_industrychart(position):
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_second_mostrecent_donut_chart(position, "Minority", "visible_minorities", labels, colors, "Yes")

def aboriginal_second_mostrecent_donut_industrychart(position):
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_second_mostrecent_donut_chart(position, 'Aboriginal', "aboriginal_peoples", labels, colors, "Yes")

def disability_second_mostrecent_donut_industrychart(position):
    labels = ['Yes','No']
    colors = [colour2, colour3]
    return create_second_mostrecent_donut_chart(position, "Disability", "person_with_disabilities", labels, colors, "Yes")

def Companydata_create_donut_second_mostrecent_chart(field_name, company, position):
    most_recent_date = CompanyData.objects.filter(name=company).aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    most_recent_date_str = most_recent_date_str.split('-')[0]
    most_recent_date_str = int(most_recent_date_str)
    second_most_recent_date = (most_recent_date_str - 1)
    second_most_recent_date = f"{str(second_most_recent_date)}-01-01"

    # Get the count of 'Y' and 'N' values for the field
    data = CompanyData.objects.filter(name=company, position_category=position, year_created=second_most_recent_date).values(field_name).annotate(count=Count(field_name))
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
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        # chart = fig.to_html(config=config, default_height='175')
        chart = json.dumps(fig.to_dict())
        return chart, hole_info
    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=0, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        # chart = fig.to_html(config=config, default_height='175')
        chart = json.dumps(fig.to_dict())

        return chart, "No Company Info"


############# MEMOIZATION ##################
def memoize(func):
    cache = {}
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper
#####################################################



################# TEST Functions ###################

@memoize
def q_Companydata_sex_donut_industrychart(cached_queryset2):
    

    most_recent_date = cached_queryset2.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    male = cached_queryset2.filter(gender_code='M', year_created=most_recent_date_str).count()
    female = cached_queryset2.filter(gender_code='F', year_created=most_recent_date_str).count()
    other = cached_queryset2.filter(gender_code='O', year_created=most_recent_date_str).count()
    total = cached_queryset2.filter(year_created=most_recent_date_str).count()


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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, hole_info

    else:

                        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text='No Company Info', x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')#, default_width='150')

        return None, None # chart, "No Company info"


@memoize
def q_Companydata_create_donut_chart(field_name, cached_queryset2):
    # Get the count of 'Y' and 'N' values for the field
    most_recent_date = cached_queryset2.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    data = cached_queryset2.filter(year_created=most_recent_date_str).values(field_name).annotate(count=Count(field_name))
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, hole_info

    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="No Company Info", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = fig.to_html(config=config, default_height='175')

        return None, None # chart, "No Company Info"



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


@memoize
def q_sex_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_sex_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result


    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    gender_codes = ['M', 'F', 'O']
    data = cached_queryset1.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('gender_code').annotate(count=Count('gender_code'))
    if len(data) == 0:
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart


@memoize
def q_c_sex_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = cached_queryset2.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    gender_codes = ['M', 'F', 'O']
    data = cached_queryset2.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('gender_code').annotate(count=Count('gender_code'))
    if len(data) == 0:
        
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart


@memoize
def q_minority_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_minority_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    visible_minorities = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('visible_minorities').annotate(count=Count('visible_minorities'))
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_c_minority_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = cached_queryset2.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    visible_minorities = ['Y', 'N']
    data = cached_queryset2.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('visible_minorities').annotate(count=Count('visible_minorities'))
    if len(data) == 0:
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_aboriginal_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_aboriginal_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    aboriginal_peoples = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_c_aboriginal_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = cached_queryset2.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    aboriginal_peoples = ['Y', 'N']
    data = cached_queryset2.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
    if len(data) == 0:
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_disability_barchart_industrychart(position, cheight, cached_queryset1):
    cache_key = 'q_disability_barchart_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    person_with_disabilities = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())
        return chart


@memoize
def q_c_disability_barchart_industrychart(position, cheight, cached_queryset2):
    most_recent_date = cached_queryset2.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    person_with_disabilities = ['Y', 'N']
    data = cached_queryset2.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(year_created=most_recent_date_str)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
    if len(data) == 0:
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

### company size  filter##
@memoize
def q_size_sex_barchart_industrychart(position, size, cheight, cached_queryset1):
    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    gender_codes = ['M', 'F', 'O']
    data = cached_queryset1.filter(Q(gender_code__in=gender_codes) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('gender_code').annotate(count=Count('gender_code'))
    if len(data) == 0:
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_size_minority_barchart_industrychart(position, size, cheight, cached_queryset1):
    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    visible_minorities = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=visible_minorities) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('visible_minorities').annotate(count=Count('visible_minorities'))
    if len(data) == 0:
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_size_aboriginal_barchart_industrychart(position, size, cheight, cached_queryset1):
    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    aboriginal_peoples = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=aboriginal_peoples) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('aboriginal_peoples').annotate(count=Count('aboriginal_peoples'))
    if len(data) == 0:
        return None
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
                textfont=dict(color='white', size=10),

                orientation='h',
                marker=dict(
                    color=colour2 if d['aboriginal_peoples'] == 'Y' else colour3,
                ), 
                hovertemplate=str(round(d['count'] / total_count * 100, 1)) + '%',
            ))
        q_customize_chart(fig, cheight)
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_size_disability_barchart_industrychart(position, size, cheight, cached_queryset1):
    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    person_with_disabilities = ['Y', 'N']
    data = cached_queryset1.filter(Q(visible_minorities__in=person_with_disabilities) & Q(position_category=position) & Q(company_size=size) & Q(year_created=most_recent_date_str)).values('person_with_disabilities').annotate(count=Count('person_with_disabilities'))
    if len(data) == 0:
        return None
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart

@memoize
def q_size_create_donut_chart(field_name, size, cached_queryset1):
    # Get the count of 'Y' and 'N' values for the field
    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    data = cached_queryset1.filter(company_size=size, year_created=most_recent_date_str).values(field_name).annotate(count=Count(field_name))
    yes_count = next((item for item in data if item[field_name] == 'Y'), {'count': 0})['count']
    no_count = next((item for item in data if item[field_name] == 'N'), {'count': 0})['count']
    total = yes_count + no_count

    labels = ['Yes','No']
    values = [yes_count, no_count]
    colors = [colour2, colour3]

    if total is not 0:

        hole_info = ((yes_count*100)/total)
        hole_info = str(round(hole_info)) + '%'

        # Create the donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            height=175
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, hole_info
    
    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors=colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            height=175
            )

        # Disable hover text
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, "0"

@memoize
def q_size_sex_donut_industrychart(size, cached_queryset1):
    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    male = cached_queryset1.filter(gender_code='M', company_size=size, year_created=most_recent_date_str).count()
    female = cached_queryset1.filter(gender_code='F', company_size=size, year_created=most_recent_date_str).count()
    other = cached_queryset1.filter(gender_code='O', company_size=size, year_created=most_recent_date_str).count()
    total = cached_queryset1.filter(company_size=size, year_created=most_recent_date_str).count()


    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    if total is not 0: 
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
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())


        return chart, hole_info

    else:
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
        fig.update_layout(showlegend=False, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
            annotations=[ 
            dict(text="0", x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)],
            height=175,
            )
        
        
        fig.update_traces(textinfo='none')
        config = {'displayModeBar': False}
        chart = json.dumps(fig.to_dict())

        return chart, "0"

@memoize
def q_create_donut_chart(category, category_field, labels, colors, hole_info_text, cached_queryset1):

    # filter the data and count the number of items that match the filter
    most_recent_date = CompanyData.objects.aggregate(Max('year_created'))['year_created__max']
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

@memoize
def q_sex_donut_industrychart(cached_queryset1):

    cache_key = 'q_sex_donut_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
    male = cached_queryset1.filter(gender_code='M', year_created=most_recent_date_str).count()
    female = cached_queryset1.filter(gender_code='F', year_created=most_recent_date_str).count()
    other = cached_queryset1.filter(gender_code='O', year_created=most_recent_date_str).count()
    total = cached_queryset1.filter(year_created=most_recent_date_str).count()

    labels = ['Male','Female','Other']
    values = [male, female, other]
    colors = [colour1, colour2, colour3]

    hole_info = ((female*100)/total)
    hole_info = str(round(hole_info))+str('%')

            # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker = dict(colors= colors))])
    fig.update_layout(showlegend=False, height=175, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
        annotations=[ 
        dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
        dict(text='Female', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)]
        
         )
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}

    chart = json.dumps(fig.to_dict())

    return chart, hole_info

# @memoize
# def q_minority_donut_industrychart(cached_queryset1):
#     cache_key = 'q_minority_donut_industrychart_{cached_queryset1}'
#     result = cache.get(cache_key)
#     if result is not None:
#         return result

#     labels = ['Yes','No']
#     colors = [colour2, colour3]
#     return q_create_donut_chart("Minority", "visible_minorities", labels, colors, "Yes", cached_queryset1)

# def q_minority_donut_industrychart(cached_queryset1):
#     cache_key = 'q_minority_donut_industrychart_{}'.format(cached_queryset1)
#     result = cache.get(cache_key)
#     if result is not None:
#         return result

#     most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
#     most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date
#     yes = cached_queryset1.filter(visible_minorities='Y', year_created=most_recent_date_str).count()
#     no = cached_queryset1.filter(visible_minorities='N', year_created=most_recent_date_str).count()
#     total = cached_queryset1.filter(year_created=most_recent_date_str).count()

#     labels = ['Yes', 'No']
#     values = [yes, no]
#     colors = [colour2, colour3]

#     if total > 0:  # Prevent division by zero
#         hole_info = ((yes * 100) / total)
#     else:
#         hole_info = 0
#     hole_info = f"{round(hole_info)}%"

#     # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker=dict(colors=colors))])
#     fig.update_layout(showlegend=False, height=175, autosize=True, margin=dict(t=0, b=0, l=0, r=0, pad=0), paper_bgcolor='#F4F9FA',
#                       annotations=[
#                           dict(text=hole_info, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
#                           dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)
#                       ]
#                       )
    
#     fig.update_traces(textinfo='none')
#     config = {'displayModeBar': False}

#     chart = json.dumps(fig.to_dict())

#     # Set the cache with the new result
#     cache.set(cache_key, (chart, hole_info))

#     return chart, hole_info

def q_minority_donut_industrychart(cached_queryset1):
    # Get the most recent date from the queryset
    most_recent_date = cached_queryset1.aggregate(Max('year_created'))['year_created__max']
    most_recent_date_str = most_recent_date.isoformat() if isinstance(most_recent_date, datetime.date) else most_recent_date

    # Count of 'Yes' and 'No' responses for the most recent date
    yes = cached_queryset1.filter(visible_minorities='Y', year_created=most_recent_date_str).count()
    no = cached_queryset1.filter(visible_minorities='N', year_created=most_recent_date_str).count()
    # total = cached_queryset1.filter(year_created=most_recent_date_str).count()
    total = yes + no

    labels = ['Yes', 'No']
    values = [yes, no]
    colors = [colour2, colour3]  # Ensure colour2 and colour3 are defined

    # # Calculate percentage of 'Yes' responses
    # if total > 0:  # Prevent division by zero
    #     hole_info = ((yes * 100) / total)
    # else:
    #     hole_info = 0
    # hole_info_text = f"{round(hole_info)}%"  # Rounded percentage text
    if total > 0:  # Prevent division by zero
        hole_info_text = (yes*100) / total
        hole_info_text = str(round(hole_info_text))+str('%')
    else:
        hole_info = 0
        hole_info_text = f"{round(hole_info)}%"  # Rounded percentage text






    # Creating a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker=dict(colors=colors))])
    fig.update_layout(
        showlegend=False,
        height=175,
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0, pad=0),
        paper_bgcolor='#F4F9FA',
        annotations=[
            dict(text=hole_info_text, x=0.5, y=0.55, font_size=18, font_family="Roboto", font_color='#174F6D', showarrow=False),
            dict(text='Yes', x=0.5, y=0.4, font_size=10, font_family="Roboto", font_color='#174F6D', showarrow=False)
        ]
    )
    
    fig.update_traces(textinfo='none')
    config = {'displayModeBar': False}

    chart = json.dumps(fig.to_dict())

    return chart, hole_info_text








@memoize
def q_aboriginal_donut_industrychart(cached_queryset1):
    cache_key = 'q_aboriginal_donut_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    labels = ['Yes','No']
    colors = [colour2, colour3]
    return q_create_donut_chart('Aboriginal', "aboriginal_peoples", labels, colors, "Yes", cached_queryset1)

@memoize
def q_disability_donut_industrychart(cached_queryset1):
    cache_key = 'q_disability_donut_industrychart_{cached_queryset1}'
    result = cache.get(cache_key)
    if result is not None:
        return result

    labels = ['Yes','No']
    colors = [colour2, colour3]
    return q_create_donut_chart("Disability", "person_with_disabilities", labels, colors, "Yes", cached_queryset1)







def contextCreator(dashboardusercompany, companyname, cached_queryset1, cached_queryset2):


    sex_dchart1, sexchart_hole_info =  q_sex_donut_industrychart(cached_queryset1)
    minority_dchart1, minority_hole_info =  q_minority_donut_industrychart(cached_queryset1)
    # minority_dchart1, minority_hole_info =  q_aboriginal_donut_industrychart(cached_queryset1)
    aboriginal_dchart1, aboriginal_hole_info =  q_aboriginal_donut_industrychart(cached_queryset1)
    disability_dchart1, disability_hole_info =  q_disability_donut_industrychart(cached_queryset1)

    sex_executive_barchart = q_sex_barchart_industrychart('Executive', 24, cached_queryset1)
    sex_senior_leader_barchart = q_sex_barchart_industrychart('Senior Leader', 24, cached_queryset1)
    sex_manager_s_s_leader_barchart = q_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset1)
    sex_foreperson_leader_barchart = q_sex_barchart_industrychart('Foreperson', 24, cached_queryset1)
    sex_individual_contributor_leader_barchart = q_sex_barchart_industrychart('Individual Contributor', 24, cached_queryset1)

    minority_executive_barchart = q_minority_barchart_industrychart('Executive', 24, cached_queryset1)
    minority_senior_leader_barchart = q_minority_barchart_industrychart('Senior Leader', 24, cached_queryset1)
    minority_manager_s_s_leader_barchart = q_minority_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset1)
    minority_foreperson_leader_barchart = q_minority_barchart_industrychart('Foreperson', 24, cached_queryset1)
    minority_individual_contributor_leader_barchart = q_minority_barchart_industrychart('Individual Contributor', 24, cached_queryset1)

    aboriginal_executive_barchart = q_aboriginal_barchart_industrychart('Executive', 24, cached_queryset1)
    aboriginal_senior_leader_barchart = q_aboriginal_barchart_industrychart('Senior Leader', 24, cached_queryset1)
    aboriginal_manager_s_s_leader_barchart = q_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset1)
    aboriginal_foreperson_leader_barchart = q_aboriginal_barchart_industrychart('Foreperson', 24, cached_queryset1)
    aboriginal_individual_contributor_leader_barchart = q_aboriginal_barchart_industrychart('Individual Contributor', 24, cached_queryset1)

    disability_executive_barchart = q_disability_barchart_industrychart('Executive', 24, cached_queryset1)
    disability_senior_leader_barchart = q_disability_barchart_industrychart('Senior Leader', 24, cached_queryset1)
    disability_manager_s_s_leader_barchart = q_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset1)
    disability_foreperson_leader_barchart = q_disability_barchart_industrychart('Foreperson', 24, cached_queryset1)
    disability_individual_contributor_leader_barchart = q_disability_barchart_industrychart('Individual Contributor', 24, cached_queryset1)
    
    Companydata_sex_dchart1, Companydata_sexchart_hole_info =  q_Companydata_sex_donut_industrychart(cached_queryset2)
    Companydata_minority_dchart1, Companydata_minority_hole_info =  q_Companydata_create_donut_chart('visible_minorities', cached_queryset2)
    Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  q_Companydata_create_donut_chart('aboriginal_peoples', cached_queryset2)
    Companydata_disability_dchart1, Companydata_disability_hole_info =  q_Companydata_create_donut_chart('person_with_disabilities', cached_queryset2)

    c_sex_executive_barchart = q_c_sex_barchart_industrychart('Executive', 24, cached_queryset2)
    c_sex_senior_leader_barchart = q_c_sex_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_sex_manager_s_s_leader_barchart = q_c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_sex_foreperson_leader_barchart = q_c_sex_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_sex_individual_contributor_leader_barchart = q_c_sex_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_minority_executive_barchart = q_c_minority_barchart_industrychart('Executive', 24, cached_queryset2)
    c_minority_senior_leader_barchart = q_c_minority_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_minority_manager_s_s_leader_barchart = q_c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_minority_foreperson_leader_barchart = q_c_minority_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_minority_individual_contributor_leader_barchart = q_c_minority_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_aboriginal_executive_barchart = q_c_aboriginal_barchart_industrychart('Executive', 24, cached_queryset2)
    c_aboriginal_senior_leader_barchart = q_c_aboriginal_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_aboriginal_manager_s_s_leader_barchart = q_c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_aboriginal_foreperson_leader_barchart = q_c_aboriginal_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_aboriginal_individual_contributor_leader_barchart = q_c_aboriginal_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_disability_executive_barchart = q_c_disability_barchart_industrychart('Executive', 24, cached_queryset2)
    c_disability_senior_leader_barchart = q_c_disability_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_disability_manager_s_s_leader_barchart = q_c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_disability_foreperson_leader_barchart = q_c_disability_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_disability_individual_contributor_leader_barchart = q_c_disability_barchart_industrychart('Individual Contributor', 24, cached_queryset2)
    

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


def companyContextCreator(dashboardusercompany, companyname, cached_queryset1, cached_queryset2):


    sex_dchart1, sexchart_hole_info =  q_sex_donut_industrychart(cached_queryset1)
    minority_dchart1, minority_hole_info =  q_minority_donut_industrychart(cached_queryset1)
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

def contextCreatorSmallindustry(dashboardusercompany, companyname, cached_queryset1, cached_queryset2):


	
    sex_dchart1, sexchart_hole_info = q_size_sex_donut_industrychart("small", cached_queryset1)
    minority_dchart1, minority_hole_info =  q_size_create_donut_chart('visible_minorities', "small", cached_queryset1)
    aboriginal_dchart1, aboriginal_hole_info =  q_size_create_donut_chart('aboriginal_peoples', "small", cached_queryset1)
    disability_dchart1, disability_hole_info =  q_size_create_donut_chart('person_with_disabilities', "small", cached_queryset1)
            
    sex_executive_barchart = q_size_sex_barchart_industrychart('Executive', "small", 24, cached_queryset1)
    sex_senior_leader_barchart = q_size_sex_barchart_industrychart('Senior Leader', "small", 24, cached_queryset1)
    sex_manager_s_s_leader_barchart = q_size_sex_barchart_industrychart('Manager/Supervisor/Superintendent', "small", 24, cached_queryset1)
    sex_foreperson_leader_barchart = q_size_sex_barchart_industrychart('Foreperson', "small", 24, cached_queryset1)
    sex_individual_contributor_leader_barchart = q_size_sex_barchart_industrychart('Individual Contributor', "small", 24, cached_queryset1)

    minority_executive_barchart = q_size_minority_barchart_industrychart('Executive', "small", 24, cached_queryset1)
    minority_senior_leader_barchart = q_size_minority_barchart_industrychart('Senior Leader', "small", 24, cached_queryset1)
    minority_manager_s_s_leader_barchart = q_size_minority_barchart_industrychart('Manager/Supervisor/Superintendent', "small", 24, cached_queryset1)
    minority_foreperson_leader_barchart = q_size_minority_barchart_industrychart('Foreperson', "small", 24, cached_queryset1)
    minority_individual_contributor_leader_barchart = q_size_minority_barchart_industrychart('Individual Contributor', "small", 24, cached_queryset1)


    aboriginal_executive_barchart = q_size_aboriginal_barchart_industrychart('Executive', "small", 24, cached_queryset1)
    aboriginal_senior_leader_barchart = q_size_aboriginal_barchart_industrychart('Senior Leader', "small", 24, cached_queryset1)
    aboriginal_manager_s_s_leader_barchart = q_size_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', "small", 24, cached_queryset1)
    aboriginal_foreperson_leader_barchart = q_size_aboriginal_barchart_industrychart('Foreperson', "small", 24, cached_queryset1)
    aboriginal_individual_contributor_leader_barchart = q_size_aboriginal_barchart_industrychart('Individual Contributor', "small", 24, cached_queryset1)


    disability_executive_barchart = q_size_disability_barchart_industrychart('Executive', "small", 24, cached_queryset1)
    disability_senior_leader_barchart = q_size_disability_barchart_industrychart('Senior Leader', "small", 24, cached_queryset1)
    disability_manager_s_s_leader_barchart = q_size_disability_barchart_industrychart('Manager/Supervisor/Superintendent', "small", 24, cached_queryset1)
    disability_foreperson_leader_barchart = q_size_disability_barchart_industrychart('Foreperson', "small", 24, cached_queryset1)
    disability_individual_contributor_leader_barchart = q_size_disability_barchart_industrychart('Individual Contributor', "small", 24, cached_queryset1)

    Companydata_sex_dchart1, Companydata_sexchart_hole_info =  q_Companydata_sex_donut_industrychart(cached_queryset2)
    Companydata_minority_dchart1, Companydata_minority_hole_info =  q_Companydata_create_donut_chart('visible_minorities', cached_queryset2)
    Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  q_Companydata_create_donut_chart('aboriginal_peoples', cached_queryset2)
    Companydata_disability_dchart1, Companydata_disability_hole_info =  q_Companydata_create_donut_chart('person_with_disabilities', cached_queryset2)

    c_sex_executive_barchart = q_c_sex_barchart_industrychart('Executive', 24, cached_queryset2)
    c_sex_senior_leader_barchart = q_c_sex_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_sex_manager_s_s_leader_barchart = q_c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_sex_foreperson_leader_barchart = q_c_sex_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_sex_individual_contributor_leader_barchart = q_c_sex_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_minority_executive_barchart = q_c_minority_barchart_industrychart('Executive', 24, cached_queryset2)
    c_minority_senior_leader_barchart = q_c_minority_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_minority_manager_s_s_leader_barchart = q_c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_minority_foreperson_leader_barchart = q_c_minority_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_minority_individual_contributor_leader_barchart = q_c_minority_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_aboriginal_executive_barchart = q_c_aboriginal_barchart_industrychart('Executive', 24, cached_queryset2)
    c_aboriginal_senior_leader_barchart = q_c_aboriginal_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_aboriginal_manager_s_s_leader_barchart = q_c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_aboriginal_foreperson_leader_barchart = q_c_aboriginal_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_aboriginal_individual_contributor_leader_barchart = q_c_aboriginal_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_disability_executive_barchart = q_c_disability_barchart_industrychart('Executive', 24, cached_queryset2)
    c_disability_senior_leader_barchart = q_c_disability_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_disability_manager_s_s_leader_barchart = q_c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_disability_foreperson_leader_barchart = q_c_disability_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_disability_individual_contributor_leader_barchart = q_c_disability_barchart_industrychart('Individual Contributor', 24, cached_queryset2)
    
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

def contextCreatorLargeindustry(dashboardusercompany, companyname, cached_queryset1, cached_queryset2):


	
    sex_dchart1, sexchart_hole_info = q_size_sex_donut_industrychart("large", cached_queryset1)
    minority_dchart1, minority_hole_info =  q_size_create_donut_chart('visible_minorities', "large", cached_queryset1)
    aboriginal_dchart1, aboriginal_hole_info =  q_size_create_donut_chart('aboriginal_peoples', "large", cached_queryset1)
    disability_dchart1, disability_hole_info =  q_size_create_donut_chart('person_with_disabilities', "large", cached_queryset1)
            
    sex_executive_barchart = q_size_sex_barchart_industrychart('Executive', "large", 24, cached_queryset1)
    sex_senior_leader_barchart = q_size_sex_barchart_industrychart('Senior Leader', "large", 24, cached_queryset1)
    sex_manager_s_s_leader_barchart = q_size_sex_barchart_industrychart('Manager/Supervisor/Superintendent', "large", 24, cached_queryset1)
    sex_foreperson_leader_barchart = q_size_sex_barchart_industrychart('Foreperson', "large", 24, cached_queryset1)
    sex_individual_contributor_leader_barchart = q_size_sex_barchart_industrychart('Individual Contributor', "large", 24, cached_queryset1)

    minority_executive_barchart = q_size_minority_barchart_industrychart('Executive', "large", 24, cached_queryset1)
    minority_senior_leader_barchart = q_size_minority_barchart_industrychart('Senior Leader', "large", 24, cached_queryset1)
    minority_manager_s_s_leader_barchart = q_size_minority_barchart_industrychart('Manager/Supervisor/Superintendent', "large", 24, cached_queryset1)
    minority_foreperson_leader_barchart = q_size_minority_barchart_industrychart('Foreperson', "large", 24, cached_queryset1)
    minority_individual_contributor_leader_barchart = q_size_minority_barchart_industrychart('Individual Contributor', "large", 24, cached_queryset1)


    aboriginal_executive_barchart = q_size_aboriginal_barchart_industrychart('Executive', "large", 24, cached_queryset1)
    aboriginal_senior_leader_barchart = q_size_aboriginal_barchart_industrychart('Senior Leader', "large", 24, cached_queryset1)
    aboriginal_manager_s_s_leader_barchart = q_size_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', "large", 24, cached_queryset1)
    aboriginal_foreperson_leader_barchart = q_size_aboriginal_barchart_industrychart('Foreperson', "large", 24, cached_queryset1)
    aboriginal_individual_contributor_leader_barchart = q_size_aboriginal_barchart_industrychart('Individual Contributor', "large", 24, cached_queryset1)


    disability_executive_barchart = q_size_disability_barchart_industrychart('Executive', "large", 24, cached_queryset1)
    disability_senior_leader_barchart = q_size_disability_barchart_industrychart('Senior Leader', "large", 24, cached_queryset1)
    disability_manager_s_s_leader_barchart = q_size_disability_barchart_industrychart('Manager/Supervisor/Superintendent', "large", 24, cached_queryset1)
    disability_foreperson_leader_barchart = q_size_disability_barchart_industrychart('Foreperson', "large", 24, cached_queryset1)
    disability_individual_contributor_leader_barchart = q_size_disability_barchart_industrychart('Individual Contributor', "large", 24, cached_queryset1)

    Companydata_sex_dchart1, Companydata_sexchart_hole_info =  q_Companydata_sex_donut_industrychart(cached_queryset2)
    Companydata_minority_dchart1, Companydata_minority_hole_info =  q_Companydata_create_donut_chart('visible_minorities', cached_queryset2)
    Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  q_Companydata_create_donut_chart('aboriginal_peoples', cached_queryset2)
    Companydata_disability_dchart1, Companydata_disability_hole_info =  q_Companydata_create_donut_chart('person_with_disabilities', cached_queryset2)

    c_sex_executive_barchart = q_c_sex_barchart_industrychart('Executive', 24, cached_queryset2)
    c_sex_senior_leader_barchart = q_c_sex_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_sex_manager_s_s_leader_barchart = q_c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_sex_foreperson_leader_barchart = q_c_sex_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_sex_individual_contributor_leader_barchart = q_c_sex_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_minority_executive_barchart = q_c_minority_barchart_industrychart('Executive', 24, cached_queryset2)
    c_minority_senior_leader_barchart = q_c_minority_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_minority_manager_s_s_leader_barchart = q_c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_minority_foreperson_leader_barchart = q_c_minority_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_minority_individual_contributor_leader_barchart = q_c_minority_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_aboriginal_executive_barchart = q_c_aboriginal_barchart_industrychart('Executive', 24, cached_queryset2)
    c_aboriginal_senior_leader_barchart = q_c_aboriginal_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_aboriginal_manager_s_s_leader_barchart = q_c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_aboriginal_foreperson_leader_barchart = q_c_aboriginal_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_aboriginal_individual_contributor_leader_barchart = q_c_aboriginal_barchart_industrychart('Individual Contributor', 24, cached_queryset2)

    c_disability_executive_barchart = q_c_disability_barchart_industrychart('Executive', 24, cached_queryset2)
    c_disability_senior_leader_barchart = q_c_disability_barchart_industrychart('Senior Leader', 24, cached_queryset2)
    c_disability_manager_s_s_leader_barchart = q_c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', 24, cached_queryset2)
    c_disability_foreperson_leader_barchart = q_c_disability_barchart_industrychart('Foreperson', 24, cached_queryset2)
    c_disability_individual_contributor_leader_barchart = q_c_disability_barchart_industrychart('Individual Contributor', 24, cached_queryset2)
    
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








