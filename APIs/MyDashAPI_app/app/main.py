import dash
from dash import html
from dash import dcc
import os
import sys
import dash_table
from dash.dash_table.Format import Group
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
from app.elastic import get_es_client, JOBMARKET_INDEX

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

# Connect to Elasticsearch
es = get_es_client()

# Test connection to Elasticsearch
try:
    if es:
        es.info()
        print("Connected to Elasticsearch")
    else:
        print("Failed to create Elasticsearch client")
except Exception as e:
    print(f"Error connecting to Elasticsearch: {e}")
    sys.exit(1)

# Fonction pour obtenir la liste des localisations
def get_location_options():
    query = {
        "size": 0,
        "aggs": {
            "locations": {
                "terms": {
                    "field": "location.keyword",
                    "size": 50  # Limiter le nombre de localisations
                }
            }
        }
    }
    res = es.search(index=JOBMARKET_INDEX, body=query)
    buckets = res['aggregations']['locations']['buckets']
    return [{'label': bucket['key'], 'value': bucket['key']} for bucket in buckets]

# Liste des options pour le dropdown de localisation
location_options = get_location_options()

# Fonction pour obtenir la liste des postes
def get_title_options():
    query = {
        "size": 0,
        "aggs": {
            "postes": {
                "terms": {
                    "field": "title.keyword",
                    "size": 50  # Limiter le nombre de postes
                }
            }
        }
    }
    res = es.search(index=JOBMARKET_INDEX, body=query)
    buckets = res['aggregations']['postes']['buckets']
    return [{'label': bucket['key'], 'value': bucket['key']} for bucket in buckets]

# Liste des options pour le dropdown des postes
poste_options = get_title_options()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Mise à jour de l'index
index_page = html.Div([
    html.H1('Job Market Dash Application', style={'color': 'aquamarine', 'textAlign': 'center'}),
    html.Div([
        html.Button(dcc.Link('Vue générale', href='/page-1'), style={'width': '250px', 'margin': '5px'}),
        html.Br(),
        html.Button(dcc.Link('Compétences par poste', href='/page-2'), style={'width': '250px', 'margin': '5px'})
    ], style={'textAlign': 'center'})
], style={'alignItems': 'center'})

# Layout1 avec le bouton de retour au menu principal et le dropdown de localisation
layout_1 = html.Div([
    html.H2('Vue générale des données', style={'color': 'aquamarine', 'textAlign': 'center'}),
    html.Div([
        html.Div([
            #html.Button("Retour", id="button-retour-1", style={'margin-bottom': '20px', 'margin-right': 'auto', 'backgroundColor': 'lightgrey'})
            html.Button(dcc.Link('Retour', href='/'), style={'margin-bottom': '20px', 'margin-right': 'auto', 'backgroundColor': 'lightgrey'})
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown-locations',
                options=location_options,
                value=None,  # Valeur initiale par défaut
                clearable=True,
                placeholder='Sélectionner une localisation',
                style={'width': '300px', 'margin-bottom': '20px'}
            )
        ], style={'display': 'flex', 'justify-content': 'center', 'flex-grow': '1'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}),

    html.Div(style={'display': 'flex', 'justify-content': 'space-around'}, children=[
        html.Div([
            dcc.Graph(id='graph-1-donut')
        ], style={'width': '48%'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown-nbrlocations',
                options=[
                    {'label': str(i), 'value': i} for i in [5, 10, 15, 20]
                ],
                value=10,
                clearable=False,
                style={'width': '200px', 'margin-left': '15px'}),
            dcc.Graph(id='graph-1-locations')
        ], style={'width': '48%'}),
    ]),
    html.Div(style={'display': 'flex', 'justify-content': 'space-around'}, children=[
        html.Div([
           dcc.Dropdown(
               id='dropdown-postes',
               options=[
                   {'label': str(i), 'value': i} for i in [5, 10, 15, 20]
                ],
                value=10,
                clearable=False,
                style={'width': '200px'}
            ),
            dcc.Graph(id='graph-1-postes')
        ], style={'width': '48%'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown-companies',
                options=[
                    {'label': str(i), 'value': i} for i in [5, 10, 15, 20]
                ],
                value=10,
                clearable=False,
                style={'width': '200px'}
            ),
            dcc.Graph(id='graph-1-companies')
        ], style={'width': '48%'})
    ])
])

# Layout2
layout_2 = html.Div([
    html.H2('Compétences par poste', style={'color': 'aquamarine', 'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Button(dcc.Link('Retour', href='/'), style={'margin-bottom': '20px', 'margin-right': 'auto', 'backgroundColor': 'lightgrey'})
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown-2-postes',
                options=poste_options,
                value=None,  # Valeur initiale par défaut
                clearable=True,
                placeholder='Sélectionner un poste',
                style={'width': '300px', 'margin-bottom': '20px'}
            ),
            dcc.Dropdown(
                id='dropdown-2-locations',
                options=location_options,
                value=None,  # Valeur initiale par défaut
                clearable=True,
                placeholder='Sélectionner une localisation',
                style={'width': '300px', 'margin-bottom': '20px', 'margin-left': '20px'}
            )
        ], style={'display': 'flex', 'justify-content': 'center', 'flex-grow': '1'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'}),

    html.Div([
        dash_table.DataTable(
            id='table-2-offres',
            columns=[
                {'name': 'Titre', 'id': 'title'},
                {'name': 'Entreprise', 'id': 'company'},
                {'name': 'Localisation', 'id': 'location'},
                {'name': 'Expériences', 'id': 'experiences'},
                {'name': 'Salaire', 'id': 'salary'},
                {'name': 'Lien', 'id': 'link', 'presentation': 'markdown'},
            ],
            data=[],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            page_size=10,
            page_action='native',
        )
    ], style={'margin-bottom': '20px', 'width': '90%', 'padding': '10px', 'margin-left': '10px'}),
    html.Div([
        dcc.Graph(id='graph-2-skills')
    ], style={'margin-bottom': '20px', 'width': '90%', 'padding': '10px', 'margin-left': '10px'})
])

# Callback main page
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return layout_1
    elif pathname == '/page-2':
        return layout_2
    else:
        return index_page

# Callback page1
@app.callback(
    [Output('graph-1-donut', 'figure'),
     Output('graph-1-postes', 'figure'),
     Output('graph-1-companies', 'figure'),
     Output('graph-1-locations', 'figure')],
    [Input('url', 'pathname'),
     Input('dropdown-postes', 'value'),
     Input('dropdown-companies', 'value'),
     Input('dropdown-nbrlocations', 'value'),
     Input('dropdown-locations', 'value')]
)
def update_graph_1(pathname, n_postes, n_companies, n_locations, selected_location):
    if pathname == '/page-1':
        if es is None:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # Requête pour récupérer le nombre d'offres par poste depuis Elasticsearch
        query_postes = {
            "size": 0,
            "aggs": {
                "titles_count": {
                    "terms": {
                        "field": "title.keyword",
                        "size": n_postes,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            }
        }

        # Requête pour récupérer la répartition des offres par source de données depuis Elasticsearch
        query_sources = {
            "size": 0,
            "aggs": {
                "sources_count": {
                    "terms": {
                        "field": "source.keyword",
                        "size": 10
                    }
                }
            }
        }

        # Requête pour récupérer le nombre d'offres par entreprise depuis Elasticsearch
        query_companies = {
            "size": 0,
            "aggs": {
                "companies_count": {
                    "terms": {
                        "field": "company.keyword",
                        "size": n_companies,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            }
        }

        # Requête pour récupérer les données de localisation
        query_locations = {
            "size": 0,
            "aggs": {
                "top_locations": {
                    "terms": {
                        "field": "location.keyword",
                        "size": n_locations
                    }
                }
            }
        }

        # Ajouter un filtre pour la localisation sélectionnée si elle est spécifiée
        if selected_location:
            query_postes['query'] = {'match': {'location.keyword': selected_location}}
            query_sources['query'] = {'match': {'location.keyword': selected_location}}
            query_companies['query'] = {'match': {'location.keyword': selected_location}}
            query_locations['query'] = {'match': {'location.keyword': selected_location}}

        try:
            res_postes = es.search(index=JOBMARKET_INDEX, body=query_postes)
            res_sources = es.search(index=JOBMARKET_INDEX, body=query_sources)
            res_companies = es.search(index=JOBMARKET_INDEX, body=query_companies)
            res_locations = es.search(index=JOBMARKET_INDEX, body=query_locations)
        except Exception as e:
            print(f"Error executing search queries for graphs: {e}")
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # Extraire les données d'agrégation pour les postes
        try:
            buckets_postes = res_postes['aggregations']['titles_count']['buckets']
            total_offers = sum(bucket['doc_count'] for bucket in buckets_postes)
            data_postes = {
                'Poste': [bucket['key'][:20] for bucket in buckets_postes],
                'Nombre_Offres': [bucket['doc_count'] for bucket in buckets_postes]
            }
            df_postes = pd.DataFrame(data_postes)
        except KeyError as e:
            print(f"Error processing search results for postes: {e}")
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

        # Créer un graphique en barres pour les postes
        fig_postes = px.bar(df_postes, x='Poste', y='Nombre_Offres', title='Nombre d\'offres par poste')
        fig_postes.update_layout(
            title=f'Nombre d\'offres par poste',
            xaxis_title='Poste',
            yaxis_title='Nombre d\'offres',
            xaxis_tickangle=-45,
            annotations=[
                dict(
                    x=1,
                    y=1,
                    text=f'Total des offres: {total_offers}',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    font=dict(size=14, color='red'),
                    align='right',
                    xanchor='right',
                    yanchor='top'
                )
            ]
        )

        # Extraire les données d'agrégation pour les sources
        try:
            buckets_sources = res_sources['aggregations']['sources_count']['buckets']
            data_sources = {
                'Source': [bucket['key'][:20] for bucket in buckets_sources],
                'Nombre_Offres': [bucket['doc_count'] for bucket in buckets_sources]
            }
            df_sources = pd.DataFrame(data_sources)
        except KeyError as e:
            print(f"Error processing search results for sources: {e}")
            return fig_sources, dash.no_update, dash.no_update, dash.no_update

        # Calculer le total des offres
        total_sources_offers = df_sources['Nombre_Offres'].sum()

        # Créer un graphique donut pour les sources
        fig_sources = px.pie(df_sources, names='Source', values='Nombre_Offres', title='Répartition des offres par source de données')
        fig_sources.update_traces(hole=0.4)
        fig_sources.update_layout(
            annotations=[
                dict(
                    text=f"Total des offres: {total_sources_offers}",
                    showarrow=False,
                    font=dict(size=14),
                    x=0.5,
                    y=-0.1,
                    xref='paper',
                    yref='paper'
                )
            ]
        )

       # Extraire les données d'agrégation pour les entreprises
        try:
            buckets_companies = res_companies['aggregations']['companies_count']['buckets']
            data_companies = {
                'Entreprise': [bucket['key'][:20] for bucket in buckets_companies],
                'Nombre_Offres': [bucket['doc_count'] for bucket in buckets_companies]
            }
            df_companies = pd.DataFrame(data_companies)
        except KeyError as e:
            print(f"Error processing search results for companies: {e}")
            return fig_sources, fig_postes, dash.no_update, dash.no_update

        # Créer un graphique en barres pour les entreprises
        fig_companies = px.bar(df_companies, x='Entreprise', y='Nombre_Offres', title='Top 10 des entreprises qui recrutent le plus')
        fig_companies.update_layout(
            title='Top 10 des entreprises qui recrutent le plus',
            xaxis_title='Entreprise',
            yaxis_title='Nombre d\'offres',
            xaxis_tickangle=-45
        )

        # Extraire les données de localisation
        try:
            buckets_locations = res_locations['aggregations']['top_locations']['buckets']
            loc_data = {
                'Location': [loc['key'][:20] for loc in buckets_locations],
                'Nombre_Offres': [loc['doc_count'] for loc in buckets_locations]
            }
            df_locations = pd.DataFrame(loc_data)
            df_locations = df_locations[df_locations['Nombre_Offres'] > 0]  # Filtrer les localisations sans offres
            df_locations = df_locations.sort_values(by='Nombre_Offres', ascending=False)  # Trier par nombre d'offres

            # Créer un graphique en barres pour la répartition géographique des offres
            fig_locations = px.bar(
                df_locations,
                x='Location',
                y='Nombre_Offres',
                title='Répartition géographique des offres d\'emploi',
                color_discrete_sequence=['green']  # Couleur verte
            )
            fig_locations.update_layout(
                title='Répartition géographique des offres d\'emploi',
                xaxis_title='Localisation',
                yaxis_title='Nombre d\'offres',
                xaxis_tickangle=-45
            )
        except KeyError as e:
            print(f"Error processing search results for locations: {e}")
            return fig_postes, fig_sources, fig_companies, dash.no_update

        return fig_sources, fig_postes, fig_companies, fig_locations
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Callback page2
@app.callback(
    Output('table-2-offres', 'data'),
    [Input('url', 'pathname'),
    Input('dropdown-2-postes', 'value'),
    Input('dropdown-2-locations', 'value')]
)
def update_table(pathname, selected_poste, selected_location):
    if pathname == '/page-2':
        if es is None:
            return dash.no_update  # Évitez les erreurs si `es` est None

        if not selected_poste:
            return []

        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

        if selected_poste:
            query['query']['bool']['must'].append({"match": {"title": selected_poste}})

        if selected_location:
            query['query']['bool']['must'].append({"match": {"location": selected_location}})

        res = es.search(index=JOBMARKET_INDEX, body=query, size=3000)
        offres = res['hits']['hits']
        table_data = []
        for offre in offres:
            source = offre['_source']
            details = source.get('details', {})

            # Obtenir experiences et salary soit à partir de details soit directement à partir de la source
            experiences = details.get('Experience', source.get('Experience', []))
            salary = details.get('Salary', source.get('Salary', []))

            # S'assurer que experiences et salary sont des listes
            if not isinstance(experiences, list):
                experiences = [experiences]
            if not isinstance(salary, list):
                salary = [salary]

            # Filtrer les valeurs None dans experiences et salary
            experiences = [exp for exp in experiences if exp is not None]
            salary = [sal for sal in salary if sal is not None]

            # Gestion du lien
            link = source.get('link', '')
            if link:
                link = f"[Lien]({link})"
            else:
                link = ''

            table_data.append({
                'id': offre['_id'],
                'title': source.get('title', ''),
                'company': source.get('company', ''),
                'location': source.get('location', ''),
                'experiences': ", ".join(experiences),
                'salary': ", ".join(salary),
                'link': link
            })

        return table_data

    else:
        return dash.no_update

@app.callback(
    Output('graph-2-skills', 'figure'),
    [Input('table-2-offres', 'active_cell'), Input('table-2-offres', 'data')]
)
def update_graph(active_cell, data):
    if not active_cell or not data:
        return {}

    row = active_cell['row']
    offer_id = data[row]['id']

    # Rechercher l'offre par ID
    query = {
        "query": {
            "match": {
                "_id": offer_id
            }
        }
    }

    res = es.search(index=JOBMARKET_INDEX, body=query)
    offre = res['hits']['hits'][0]
    skills_data = offre['_source'].get('skills', {})

    #print(f"#### Skills data: {skills_data}")

    skills = []
    frequencies = []
    for category, skills_list in skills_data.items():
        for skill in skills_list:
            skills.append(skill)
            frequencies.append(1)

    df = pd.DataFrame({'Compétences': skills, 'Fréquence': frequencies})

    fig = px.bar(df, x='Compétences', y='Fréquence', labels={'x': 'Compétences', 'y': 'Fréquence'},
                 title=f"Compétences pour le poste : {offre['_source']['title']}")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
