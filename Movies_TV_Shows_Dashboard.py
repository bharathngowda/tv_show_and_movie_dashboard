#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import requests
import re
import json
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
import imdb
ia=imdb.IMDb()


# In[9]:


# Style

page_bg={'backgroundColor':'#47126b'}
performance_tab_bg={'backgroundColor':'#000000'}
black_bg={'backgroundColor':'#000000'}
head_style={'textAlign':'center','color':'white','fontWeight': 'bold'}
title_style={'textAlign':'left','color':'white','fontWeight': 'bold','backgroundColor':'#2a9d8f','margin-top': '0px',
             'margin-bottom': '0px','margin-right': '0px','margin-left': '0px','padding':'2px'}
subtitle_style={'textAlign':'center','color':'white','fontWeight': 'bold','margin-right': '0px','margin-left': '0px',
                'padding':'2px','backgroundColor':'#2a9d8f'}
subtitle_style2={'textAlign':'center','color':'white','fontWeight': 'bold','margin-right': '0px','margin-left': '0px',
                'padding':'2px','backgroundColor':'#2a9d8f','border-radius': '20px'}
body_style={'textAlign':'left','color':'white','margin-right': '0px','margin-left': '0px',
            'padding':'2px'}
p_style={'textAlign':'left','color':'white','margin-right': '0px','margin-left': '0px',
            'padding':'2px','whiteSpace': 'pre-wrap'}
_style={'textAlign':'left','color':'white','margin-top': '0px',
             'margin-bottom': '0px','margin-right': '0px','margin-left': '0px','padding':'2px'}
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'backgroundColor': '#2a9d8f',
    'border':'none',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': 'white',
}

tab_selected_style = {
    'borderTop': '4px solid #2a9d8f',
    'borderBottom': '1px solid #52b788',
    'borderLeft': '1px solid #52b788',
    'borderRight': '1px solid #52b788',
    'backgroundColor': '#52b788',
    'color': 'white',
    'padding': '6px',
}


search_bar={'width':'100%', 'display':'table-cell', 'verticalAlign':'middle'}

button={'backgroundColor': '#2a9d8f', 
        'color':'white',
        'width':'100%', 
        'border':'1.5px 2a9d8f solid', 
        'text-align':'center',
        'marginLeft': '0px', 
        'marginTop': '0px'}
search_results={'backgroundColor': '#e9c46a', 
        'color':'black',
        'border-radius': '20px', 
        'border':'1.5px #e9c46a solid', 
        'text-align':'center',
        'marginLeft': '5px',
        'marginRight': '5px',
        'marginTop': '5px',
        'marginBottom': '5px'}
selected_btn={'backgroundColor': '#e76f51', 
        'color':'white',
        'border-radius': '20px', 
        'border':'1.5px #e76f51 solid', 
        'text-align':'center',
        'marginLeft': '5px',
        'marginRight': '5px',
        'marginTop': '5px',
        'marginBottom': '5px'}
genre_style={'backgroundColor': '#f4a261', 
        'color':'black',
        'border-radius': '20px', 
        'border':'1.5px #e9c46a solid', 
        'text-align':'center',
        'marginLeft': '5px',
        'marginRight': '5px',
        'marginTop': '5px',
        'marginBottom': '5px'}

data_table_header_style={'backgroundColor': 'rgb(231, 111, 81)'}
data_table_cell_style={'backgroundColor':'rgb(38, 70, 83)','color': 'white','text_align': 'left','whiteSpace':'normal',
                       'height':'auto','font_size': '14px','font-family':'Helvetica'}


# In[10]:


# App Layout

app=dash.Dash(__name__)
server=app.server #For deploying

app.layout=html.Div([
html.Div(html.H1("TV Shows & Movies Information",style=head_style),className='row',style=page_bg),
    html.Div([
        dcc.Input(id='search_bar',type='text',n_submit=0,placeholder='Enter a Movie/TV Show Name/IMDb ID',debounce=False,style=search_bar)
    ],className='row',style=page_bg),
    html.Div([
        html.Div(id='search_result')],className='rows',style=page_bg),
    html.Div([
        html.Br()
    ],className='row',style=page_bg),
    html.Div(id='movie_info',children=[],className='row',style=page_bg)
],className='row',style=page_bg)


@app.callback(
Output('search_result','children'),
Input('search_bar','value'),
)

def search(val):
    child=[]
    if val is not None:
        series=ia.search_movie(val)
        titles={}
        for i in range(len(series)):
            titles[(series[i]['title'])]=series[i].movieID
        keys=[x for x in titles.keys()]
        values=[x for x in titles.values()]
        
        for i in range(len(titles)):
            child.append(html.Button(keys[i],id={'type':'btn','index':values[i]},n_clicks=0,value=values[i],style=search_results))
    return child

@app.callback(
Output({'type':'btn','index':ALL},'style'),
[Input({'type':'btn','index':ALL},'n_clicks'),
State({'type':'btn','index':ALL},'id')])

def selected_button(n_clicks,id):
    try:
        ctx = dash.callback_context
        sel_btn=ctx.triggered[0]['prop_id'].split('.')[0]
        button_id=json.loads(sel_btn)
        style=[]
        for i in range(len(id)):
            if button_id['index']==id[i]['index']:
                style.append(selected_btn)
            else:
                style.append(search_results)
    except:
        style=[search_results]*len(id)

    return style
  
@app.callback(
Output('movie_info','children'),
[Input({'type':'btn','index':ALL},'n_clicks'),
State({'type':'btn','index':ALL},'id')])

def Update_Details(n_clicks,id):
    child=[]
    ctx = dash.callback_context
    sel_btn=ctx.triggered[0]['prop_id'].split('.')[0]
    button_id=json.loads(sel_btn)
    for i in range(len(id)):
        if button_id['index']==id[i]['index']:
            movie_id=button_id['index']
            movies=ia.get_movie(movie_id,info=['reviews','awards','recommendations','main','plot'])
            try:
                cast=''
                for i in [str(x) for x in movies.get('cast')[:10]]:
                    if len(movies.get('cast'))>1 and i !='':
                        cast=cast+', '+str(i)
                        if cast[0]==',':
                            cast=cast[2:]
                    else:
                        cast=str(i)
            except:
                cast=' '
            try:
                fcast=''
                for i in [str(x) for x in movies.get('cast')]:
                    if len(movies.get('cast'))>1 and i !='':
                        fcast=fcast+', '+str(i)
                        if fcast[0]==',':
                            fcast=fcast[2:]
                    else:
                        fcast=str(i)
            except:
                fcast=' '        
            if movies['kind'] !='movie'and movies['kind'] !='video game':
                series=ia.get_movie(movie_id,info=['reviews','awards','recommendations','main','plot','episodes'])
                try:
                    writer=''
                    for i in [str(x) for x in series.get('writer')]:
                        if len(series.get('writer'))>1 and i !='':
                            writer=writer+', '+str(i)
                            if writer[0]==',':
                                writer=writer[2:]
                        else:
                            writer=str(i)
                except:
                    writer=''
                certificate=dict()
                try:
                    for i in series.get('certificate'):
                        certificate[re.split(':',i)[0]]=re.split(':',i)[1]
                    try:
                        certi=certificate['India']
                    except:
                        certi=certificate['United States']
                except:
                    certi=''
                try:
                    mins=int(series.get('runtime')[0])
                    hours=mins//60
                    minutes=mins%60
                    dur=str(hours)+'h '+str(minutes)+'m'
                except:
                    dur=' '
                try:
                    rating=''
                    for i in ['⭐']*round(series.get('rating')):
                        rating=rating+i
                except:
                    rating=' '
                try:
                    genre=''
                    genre=series.get('genre')
                except:
                    genre=' '
                try:
                    plot=''
                    for i in series.get('plot'):
                        plot=plot+'\n\n'+i
                        if plot[0]=='\n':
                            plot=plot[1:]
                except:
                    plot=' '
                try:
                    awards=series.get('awards')
                    for j in range(len(awards)):
                        to=''
                        for i in awards[j]['to']:
                            if len(awards[j]['to'])>1 and i !='' and isinstance(awards[j]['to'],list)==True:
                                to=to+', '+str(i)
                                if to[0]==',':
                                    to=to[2:]
                            elif len(awards[j]['to'])==0:
                                to=' '
                            else:
                                to=str(i)
                        awards[j].update({'to':to})
                    awards=pd.DataFrame(data=awards)
                    awards['result']=awards.result.apply(lambda x: '🏆' if x=='Winner' else x)
                except:
                    awards=pd.DataFrame(columns=['award', 'year', 'result', 'category', 'notes', 'to'],
                                       data=[])
                try:
                    reviews=pd.DataFrame(data=series.get('reviews'))
                    reviews.fillna(0,inplace=True)
                    reviews['Like/Dislike']=reviews[['helpful',
                                              'not_helpful']].apply(lambda x: '👍 • '+str(x['helpful'])+'  👎 • '
                                                                    +str(x['not_helpful']),axis=1)
                    reviews['rating']=reviews.rating.apply(lambda x:np.nan if pd.isnull(x) else 
                                                           re.sub('[\'\']','',re.sub('[\[\]]','',
                                                                                     str(['⭐']*round(int(x),0)))))
                    reviews=reviews[['content','rating','Like/Dislike','date']]
                except:
                    reviews=pd.DataFrame(columns=['content','rating','Like/Dislike','date'],
                                       data=[])
                try:
                    votes=series.get('votes')
                except:
                    votes=' '
                try:
                    seasons=series.get('number of seasons')
                except:
                    seasons=' '
                try:
                    episodes=series.get('number of episodes')
                except:
                    episodes=' '
                try:
                    language=re.sub('[\'\']','',re.sub('[\[\]]','',str(series.get('language'))))
                except:
                    language=' '
                episode_info={'result':[]}
                for i in series.get('episodes').keys():
                    for j in series.get('episodes')[i]:
                        try:
                            episode='Episode '+str(j)
                        except:
                            episode=' '
                        try:
                            title=series.get('episodes')[i][j]['title']
                        except:
                            title=' '
                        try:
                            plot=series.get('episodes')[i][j]['plot'].replace('\n','')
                        except:
                            plot=' '
                        try:
                            rating2=''
                            for k in ['⭐']*round(series.get('episodes')[i][j]['rating']):
                                rating2=rating2+k
                        except:
                            rating2=' '
                        try:
                            air_date=series.get('episodes')[i][j]['original air date']
                        except:
                            air_date=' '
                        episode_info['result'].append({'season':'Season '+str(i),
                            'episode':episode,
                            'title':title,
                            'plot':plot,
                            'rating':rating2,
                            'air date':air_date})
                episodeguide=pd.DataFrame(episode_info['result'])
                child=[
                    html.Div(
                        html.Div(
                            html.H3(series.get('title'),style=title_style),className='six columns',style=page_bg),
                        className='row', style=page_bg),
                    html.Div(
                        html.Div(
                            html.H6(str(series.get('kind')).upper() + ' • '+str(series.get('series years'))+' • '+str(certi),
                                    style=_style),
                            className='six columns',style=page_bg),
                        className='row', style=page_bg),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(
                                    html.H5('Rating',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(rating,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Writer',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(writer,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Seasons',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(html.H6(seasons,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Episodes',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(episodes,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Votes',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(votes,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg)],
                            className='six columns',style=page_bg),
                        html.Div([
                                html.Div([
                                    html.Div(
                                        html.H5('Genre',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    [html.Button(x,id=x,n_clicks=0,value=x,style=genre_style) for x in genre],
                                    className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                    html.Div(
                                        html.H5('Cast',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(
                                        html.H6(cast,style=body_style),className='nine columns',style=page_bg)
                            ],className='row', style=page_bg),
                            html.Div([
                                    html.Div(
                                        html.H5('Runtime',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(
                                        html.H6(dur,style=body_style),className='nine columns',style=page_bg)
                            ],className='row', style=page_bg),
                            html.Div([
                                html.Div([
                                    html.Div(
                                        html.H5('Language',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(
                                        html.H6(language,style=body_style),className='nine columns',style=page_bg)],
                                    className='row', style=page_bg)
                            ],className='row', style=page_bg)
                            ],className='six columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Episode Guide',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            dash_table.DataTable(id='episodeguide',columns=[{"name": i.upper(), "id": i} for i in episodeguide.columns],
                                                 data=episodeguide.to_dict('records'),style_cell=data_table_cell_style,
                                                 style_header={'backgroundColor': '#e76f51','fontWeight': 'bold',
                                                              'border': '0px solid #2a9d8f'},
                                                 page_size=10,style_as_list_view=True
                                                ),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Plot',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            html.P(plot,style=p_style),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Full Cast',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            html.P(fcast,style=p_style),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Awards',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            dash_table.DataTable(id='awards',columns=[{"name": i.upper(), "id": i} for i in awards.columns],
                                                 data=awards.to_dict('records'),style_cell=data_table_cell_style,
                                                 style_header={'backgroundColor': '#e76f51','fontWeight': 'bold',
                                                              'border': '0px solid #264653'},
                                                 style_as_list_view=True,
                                                 page_size=10
                                                ),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Reviews',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            dash_table.DataTable(id='reviews',columns=[{"name": i.upper(), "id": i} for i in reviews.columns],
                                                 data=reviews.to_dict('records'),style_cell=data_table_cell_style,
                                                 style_header={'backgroundColor': '#e76f51','fontWeight': 'bold',
                                                              'border': '0px solid #264653'},
                                                 style_as_list_view=True,
                                                 page_size=5
                                                ),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                ]
            else:
                try:
                    director=''
                    for i in [str(x) for x in movies.get('director')]:
                        if len(movies.get('director'))>1 and i !='':
                            director=director+', '+str(i)
                            if director[0]==',':
                                director=director[2:]
                        else:
                            director=str(i)
                except:
                    director=' '
                try:
                    writer=''
                    for i in [str(x) for x in movies.get('writers')]:
                        if len(movies.get('writers'))>1 and i !='':
                            writer=writer+', '+str(i)
                            if writer[0]==',':
                                writer=writer[2:]
                        else:
                            writer=str(i)
                except:
                    writer=' '
                try:
                    producer=''
                    for i in [str(x) for x in movies.get('producers')]:
                        if len(movies.get('producers'))>1 and i !='':
                            producer=producer+', '+str(i)
                            if producer[0]==',':
                                producer=producer[2:]
                        else:
                            producer=str(i)
                except:
                    producer=' '
                certificate=dict()
                try:
                    for i in series.get('certificate'):
                        certificate[re.split(':',i)[0]]=re.split(':',i)[1]
                    try:
                        certi=certificate['India']
                    except:
                        certi=certificate['United States']
                except:
                    certi=''
                try:
                    mins=int(movies.get('runtime')[0])
                    hours=mins//60
                    minutes=mins%60
                    dur=str(hours)+'h '+str(minutes)+'m'
                except:
                    dur=' '
                try:
                    rating=''
                    for i in ['⭐']*round(movies.get('rating')):
                        rating=rating+i
                except:
                    rating=' '
                try:
                    genre=''
                    genre=movies.get('genre')
                except:
                    genre=' '
                try:
                    plot=''
                    for i in movies.get('plot'):
                        plot=plot+'\n\n'+i
                        if plot[0]=='\n':
                            plot=plot[1:]
                except:
                    plot=' '
                try:
                    awards=movies.get('awards')
                    for j in range(len(awards)):
                        to=''
                        for i in awards[j]['to']:
                            if len(awards[j]['to'])>1 and i !='' and isinstance(awards[j]['to'],list)==True:
                                to=to+', '+str(i)
                                if to[0]==',':
                                    to=to[2:]
                            elif len(awards[j]['to'])==0:
                                to=''
                            else:
                                to=str(i)
                        awards[j].update({'to':to})
                    awards=pd.DataFrame(data=awards)
                    awards['result']=awards.result.apply(lambda x: '🏆' if x=='Winner' else x)
                except:
                    awards=pd.DataFrame(columns=['award', 'year', 'result', 'category', 'notes', 'to'],
                                       data=[])
                try:
                    reviews=pd.DataFrame(data=movies.get('reviews'))
                    reviews.fillna(0,inplace=True)
                    reviews['Like/Dislike']=reviews[['helpful',
                                              'not_helpful']].apply(lambda x: '👍 • '+str(x['helpful'])+'  👎 • '
                                                                    +str(x['not_helpful']),axis=1)
                    reviews['rating']=reviews.rating.apply(lambda x:np.nan if pd.isnull(x) else 
                                                           re.sub('[\'\']','',re.sub('[\[\]]','',
                                                                                     str(['⭐']*round(int(x),0)))))
                    reviews=reviews[['content','rating','Like/Dislike','date']]
                except:
                    reviews=pd.DataFrame(columns=['content','rating','Like/Dislike','date'],
                                       data=[])
                try:
                    boxoffice=pd.DataFrame(data=movies.get('box office').values(),index=movies.get('box office').keys()).T
                except:
                    boxoffice=pd.DataFrame(columns=['Budget', 'Opening Weekend United States','Cumulative Worldwide Gross'],
                                       data=[])
                try:
                    airdate=movies.get('original air date')
                except:
                    airdate=' '
                try:
                    votes=movies.get('votes')
                except:
                    votes=' '
                try:
                    language=re.sub('[\'\']','',re.sub('[\[\]]','',str(movies.get('language'))))
                except:
                    language=' '
                child=[
                    html.Div(
                        html.Div(
                            html.H3(movies.get('title'),style=title_style),className='six columns',style=page_bg),
                        className='row', style=page_bg),
                    html.Div(
                        html.Div(
                            html.H6(movies.get('kind').upper() + ' • '+str(movies.get('year')) + ' • '+certi+' • '+dur,style=_style),
                            className='six columns',style=page_bg),
                        className='row', style=page_bg),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(
                                    html.H5('Rating',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(rating,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Director',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(director,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Writer',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(html.H6(writer,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Air Date',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(airdate,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                html.Div(
                                    html.H5('Votes',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    html.H6(votes,style=body_style),className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                                html.Div([
                                    html.Div(
                                        html.H5('Language',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(
                                        html.H6(language,style=body_style),className='nine columns',style=page_bg)],
                                    className='row', style=page_bg)],
                            className='six columns',style=page_bg),
                        html.Div([
                                html.Div([
                                    html.Div(
                                        html.H5('Genre',style=subtitle_style2),className='three columns',style=page_bg),
                                html.Div(
                                    [html.Button(x,id=x,n_clicks=0,value=x,style=genre_style) for x in genre],
                                    className='nine columns',style=page_bg)],
                                className='row', style=page_bg),
                            html.Div([
                                    html.Div(
                                        html.H5('Cast',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(
                                        html.H6(cast,style=body_style),className='nine columns',style=page_bg)
                            ],className='row', style=page_bg),
                            html.Div([
                                    html.Div(
                                        html.H5('Producer',style=subtitle_style2),className='three columns',style=page_bg),
                                    html.Div(
                                        html.H6(producer,style=body_style),className='nine columns',style=page_bg)
                            ],className='row', style=page_bg)
                            ],className='six columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Box Office',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            dash_table.DataTable(id='boxoffice',columns=[{"name": i.upper(), "id": i} for i in boxoffice.columns],
                                                 data=boxoffice.to_dict('records'),style_cell=data_table_cell_style,
                                                 style_header={'backgroundColor': '#e76f51','fontWeight': 'bold',
                                                              'border': '0px solid #2a9d8f'},
                                                 style_data={'border': '0px solid #264653'},
                                                 
                                                ),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Plot',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            html.P(plot,style=p_style),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Full Cast',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            html.P(fcast,style=p_style),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Awards',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            dash_table.DataTable(id='awards',columns=[{"name": i.upper(), "id": i} for i in awards.columns],
                                                 data=awards.to_dict('records'),style_cell=data_table_cell_style,
                                                 style_header={'backgroundColor': '#e76f51','fontWeight': 'bold',
                                                              'border': '0px solid #264653'},
                                                 style_as_list_view=True,
                                                 page_size=10
                                                ),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                    html.Div([
                        html.Div(
                            html.H5('Reviews',style=subtitle_style),className='twelve columns',style=page_bg),
                        html.Div(
                            dash_table.DataTable(id='reviews',columns=[{"name": i.upper(), "id": i} for i in reviews.columns],
                                                 data=reviews.to_dict('records'),style_cell=data_table_cell_style,
                                                 style_header={'backgroundColor': '#e76f51','fontWeight': 'bold',
                                                              'border': '0px solid #264653'},
                                                 style_as_list_view=True,
                                                 page_size=5
                                                ),className='twelve columns',style=page_bg)
                    ],className='row', style=page_bg),
                ]

    return child
if __name__=='__main__':
    #app.run_server(debug=True,use_reloader=False)
    app.run_server(debug=False)

