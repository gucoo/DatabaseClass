from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import time
import mongo_connect as mongo_c
import mysql_connect as mysql_c
import dash_bootstrap_components as dbc
import neo4j_connect as neo4j_c
from serpapi import GoogleSearch
import plotly.graph_objects as go
import dash




app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



mysql_c.createDefault()
overview = mysql_c.mysql_start()
options= mysql_c.get_option()


fig1={}
fig11= {} #mysql_c.q2_graph(mysql_c.q22("data mining",10))
fig2={}
fig3={}
f_table = mysql_c.facultygraph()
details="cannot show"

# Show 4rd graph
fig4 = neo4j_c.q4_table(neo4j_c.q4())
fig41= neo4j_c.q5_table(neo4j_c.q5())

# Show 5th graph
fig5=mysql_c.favfacultygraph()
fig6 = {}#mysql_c.FacultyPublicationView(0)
fig9 = {}#mysql_c.univpub_graph(mysql_c.univpub("data mining",10))


#----------------------------------------------------------------------------------layout

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

card1 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Total Faculty", className="card-title"),                    
                    html.P(str(overview[0]), className="card-text"),
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-primary",
            style={"maxWidth": 75},
        ),
    ],
    className="mt-4 shadow",
)

card2 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Total University", className="card-title"),
                    html.P(str(overview[2]), className="card-text"),
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-globe", style=card_icon),
            className="bg-info",
            style={"maxWidth": 75},
        ),
    ],className="mt-4 shadow",
)

card3 = dbc.CardGroup(
    [
        dbc.Card(
        
            dbc.CardBody(
                [
                    html.H5("Total Publication", className="card-title"),
                    html.P(str(overview[1]), className="card-text"),
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-globe", style=card_icon),
            className="bg-primary",
            style={"maxWidth": 75},
        ),
    ],className="mt-4 shadow",
)


#-------------- Graph 1

Graph1 = dbc.CardGroup(
    [
    
        dbc.Card([
         dbc.CardHeader(html.H3(children='Faculty with Most Number of Publications')),
        
         dbc.CardBody(
                [   	
    				html.Div([
    				html.P(children='1. Enter a Keyword for a specific topic or "all" for an overview including publications of any topic:   2. Enter Top # of Faculty:   '),
    				dcc.Input(id='input-on-submit', value='data mining', type='text'),
    				dcc.Input(id='input-on-submit2', value='10', type='number'),
    				html.Button('Submit', id='submit-val', n_clicks=0)
    			]
        ),
    
    
        dcc.Graph(
        	id='example-graph1',
        	figure=fig1
    	)
        ]
            )
        ]), 
    ],className="mt-4 shadow", 
)

#-------------- Graph 9

Graph9 = dbc.CardGroup(
    [
    
        dbc.Card([
         dbc.CardHeader(html.H3(children='University with Most Number of Publications')),
        
         dbc.CardBody(
                [   	
    				html.Div([
    				html.P(children='1. Enter a Keyword for a specific topic or "all" for an overview including publications of any topic:   2. Enter Top # of University:   '),
    				dcc.Input(id='input9', value='data mining', type='text'),
    				dcc.Input(id='input9-2', value='10', type='number'),
    				html.Button('Submit', id='submit9', n_clicks=0)
    			]
        ),
    
    
        dcc.Graph(
        	id='graph9',
        	figure=fig9
    	)
        ]
            )
        ]), 
    ],className="mt-4 shadow", 
)

#-------------- Graph 11

Graph11 = dbc.CardGroup(
    [
    
        dbc.Card([
         dbc.CardHeader(html.H3(children='Faculty with the Most Number of Citations and Publications')),
        
         dbc.CardBody(
                [
    				html.Div([
    				html.P(children='1. Enter Keyword for a specific topic or "all" for an overview including citations of any topic:   2. Enter Top # of Faculty:   '),
    				dcc.Input(id='input-on-submit-1', value='data mining', type='text'),
    				dcc.Input(id='input-on-submit2-1', value='10', type='number'),
    				html.Button('Submit', id='submit-val-1', n_clicks=0)
    			]
        ),
    
    
        dcc.Graph(
        	id='example-graph1-1',
        	figure=fig11
    	)
        ]
            )
        ]),
    ],className="mt-4 shadow",
)


#-------------- Graph 2

Graph2 = dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='Universities with the Most Number of Faculty')),
        
            dbc.CardBody(
                [
    				html.P(children='1. Enter a Keyword for faculty studying a specific topic or all for an overview including faculty studying any topic:   2. Enter Top # of Universities:   '),
    				dcc.Input(id='input-on-submit3', value='data mining', type='text'),
    				dcc.Input(id='input-on-submit3-1', value='5', type='number'),
    				html.Button('Submit', id='submit-val2', n_clicks=0)
                ]
            ),
            dcc.Graph(
       				 id='example-graph2',
        			figure=fig2
    				)
        ])
    ],className="mt-4 shadow",
)

#-------------- Graph 3

Graph3=dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='Faculty Improvement')),
            dbc.CardBody(
                [
                    html.H5("Total Citation yearly", className="card-title"),
                    html.P("Search and add Faculty id or name", className="card-text"),
                    dcc.Dropdown(
            			id='my_ticker_symbol',
            			options=options,
            			value=[7,777],
            			multi=True
        			),
        			html.Button(
                        id='submit-button',
            			n_clicks=0,
            			children='Submit',
            			style={'fontSize':20, 'marginLeft':'0px'}
        			),

                    dcc.Graph(
        				id='example-graph3',
        				figure=fig3
    					)
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)

#-------------- Graph 4
Graph4=dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='University Collaboration Performance')),
            dbc.CardBody(
                [
                    html.H5("Top 10 Universities Based on the Number of Other Universities they have Collaborated with on Publications", className="card-title"),
                    dcc.Graph(
        				
        				figure=fig4
    					)
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)

Graph41=dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='Faculty Collaboration Performance')),
            dbc.CardBody(
                [           
                    html.H5("Top 10 Faculty Based on the Number of Other Faculty they have Collaborated With on Publications", className="card-title"),
                    dcc.Graph(
        				
        				figure=fig41
    					)
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)

#-------------- Graph 5
Graph5=dbc.CardGroup(
    [
        dbc.Card(
        [
         #dbc.CardHeader(html.H3(children='Add or Delete Favorite Faculty')),
            dbc.CardBody(
                [
                    html.H5("Add or Delete Your Favorite Faculty Members", className="card-title"),
                    #html.P("This card has some text content", className="card-text"),
                    dcc.Dropdown(
            			id='dropdown5',
            			options=options,
            			value=[],
            			multi=True
        			),
    				html.Button('Add', id='submit5add', n_clicks=0),
				    html.Button('Delete', id='submit5del', n_clicks=0)
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)

#-------------- Graph 6
Graph6=dbc.CardGroup(
    [
        dbc.Card(
        [
         #dbc.CardHeader(html.H3(children='Add Comments to Favorite Faculty')),
            dbc.CardBody(
                [
                    html.H5("Add Comments to Favorite Faculty", className="card-title"),
                    #html.P("This card has some text content", className="card-text"),
                    dcc.Dropdown(
            			id='dropdown6',
            			options=options,
            			value=[2],
            			multi=True
        			),
                    dcc.Input(id='input6', value='Looks good. Co-author', type='text',size='70'),
    				html.Button('Submit', id='submit6', n_clicks=0),
                    
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)

#-------------- Graph 6
Graph61=dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='Favorite Faculty')),
            dbc.CardBody(
                [
                    #html.H5("Favorite Faculty", className="card-title"),
                    
                    dcc.Graph(
        				id='example-graph5',
        				figure=fig3
    					)
                    
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)

#-------------- Graph 7 fig


Graph7=dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='Show all Publication for the faculty')),
            dbc.CardBody(
                [ 
                   
                    html.P("Select faculty name to start ", className="card-text"),
                    
                    dcc.Dropdown(
            			id='input-v2',
            			options=options,
            			value=2
            			,multi=False
        			),
    				html.Button('Show Faculty Publication', id='submit-v2', n_clicks=0),
    				#html.Button('Verify Publication', id='submit-v2-2 ', n_clicks=0),
    				
    				dcc.Graph(
        				id='example-graph6',
        				figure=fig6
    					),
    				html.Br(),
    				html.Br(),
    				
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)


Graph7_1=dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='Verify Faculty Citation with Google Scholar')),
            dbc.CardBody(
                [
                    html.H5("Verify Faculty", className="card-title"),
                    html.P("Enter faculty name + name of university to start", className="card-text"),
                    
                    dcc.Input(id='input-v1', value='Vipin Kumar University of Minnesota', type='text',size='50'),
    				html.Button('verify F', id='submit-v1', n_clicks=0),
    				html.Br(),
    				html.Br(),
    				html.H5("Result",className="card-title"),
                    html.Div(id='output-v1'),

                    
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)


Graph7_2=dbc.CardGroup(
    [
        dbc.Card(
        [
         dbc.CardHeader(html.H3(children='Verify Publication Citation with Google Scholar')),
            dbc.CardBody(
                [
                    
    				html.H5("Verify Publication", className="card-title"),
                    dcc.Input(id='input-v1-1', value='3D trajectory matching by pose normalization', type='text',size='50'),
                    html.Button('Verify P', id='submit-v1-1', n_clicks=0),
                    html.Br(),
    				html.Br(),
                    html.H5("Result",className="card-title"),
                    html.Div(id='output-v1-1')
                    
                ]
            )
        ])
    ],
    className="mt-4 shadow",
)
# -------------------------------------------------------------------------- app.layout

app.layout = html.Div(children=[
   html.Br(),
   html.H1(children='Faculty and University Performance'),
   

   
   dbc.Row([ dbc.Col([card1]),dbc.Col([card2]),dbc.Col([card3]) ]),
   html.Br(),html.Br(),
   

   dbc.Row([ dbc.Col([Graph1], width=6), dbc.Col([Graph9], width=6) ]),
   dbc.Row([ dbc.Col([Graph11]) ]),
   dbc.Row([ dbc.Col([Graph2], width=5), dbc.Col([Graph3], width=7) ]),
#   dbc.Row([ dbc.Col([Graph3], width=8) ]),
   dbc.Row([ dbc.Col([Graph4]),dbc.Col([Graph41]) ]),
   dbc.Row([ dbc.Col([Graph5]),dbc.Col([Graph6]) ]), dbc.Row([ dbc.Col([Graph61])]), 
 dbc.Row([ dbc.Col([Graph7]) ]),
   dbc.Row([ dbc.Col([Graph7_1],width=6),dbc.Col([Graph7_2],width=6) ]),
   html.Br(),html.Br(),
   
])

#-------------------------------------------------------------------------------callback

# Graph 1
@app.callback(
    Output('example-graph1', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    State('input-on-submit2', 'value')
)
def update_output(n_clicks, value1, value2):
    fig1 = mysql_c.q1_graph(mysql_c.q11(value1,value2))
    
    return fig1

# Graph 9
@app.callback(
    Output('graph9', 'figure'),
    Input('submit9', 'n_clicks'),
    State('input9', 'value'),
    State('input9-2', 'value')
)
def update_output(n_clicks, value1, value2):
    fig9 = mysql_c.univpub_graph(mysql_c.univpub(value1,value2))
    
    return fig9

    
# Graph 11
@app.callback(
    Output('example-graph1-1', 'figure'),
    Input('submit-val-1', 'n_clicks'),
    State('input-on-submit-1', 'value'),
    State('input-on-submit2-1', 'value')
)
def update_output(n_clicks, value1, value2):
	time.sleep(2)
	fig11 = mysql_c.q2_graph(mysql_c.q22(value1,value2))
	return fig11
    
# Graph 2
@app.callback(
    Output('example-graph2', 'figure'),
    Input('submit-val2', 'n_clicks'),
    State('input-on-submit3', 'value'),
    State('input-on-submit3-1', 'value')
    
)
def update_output(n_clicks, value1,value2):
    top = int (value2)
    fig2 = mongo_c.q2_graph(mongo_c.q2(value1,top))
    
    return fig2


# Graph 3
@app.callback(
    Output('example-graph3', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('my_ticker_symbol', 'value')
)
def update_graph(n_clicks, list_options):
   
    #fig3={}
    #time.sleep(4)
    fig3 = mysql_c.q33(list_options)
    
    
    return fig3

# Graph 5 6
@app.callback(
    Output('example-graph5', 'figure'),
    Input('submit5add', 'n_clicks'),
    Input('submit5del', 'n_clicks'),
    Input('submit6', 'n_clicks'),
    State('dropdown5', 'value'),
    State('dropdown6', 'value'),
    State('input6', 'value')
)
def update_graph_add(n_clicks1,n_clicks2, n_clicks3, list_options1, list_options2, comment):
   
    #time.sleep(3)
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    

    if input_id == 'submit5add':
	    mysql_c.addfav(list_options1)
    elif input_id == 'submit5del':
        mysql_c.delfav(list_options1)
    else:
        mysql_c.add_comments(comment, list_options2)  
    
    fig5 = mysql_c.favfacultygraph()
      
    return fig5
    

# Graph 7F
@app.callback(
    Output('output-v1', 'children'),
    Input('submit-v1', 'n_clicks'),
    State('input-v1', 'value')
)
def update_faculty(n_clicks,in_v1):

	return mysql_c.verifyF(in_v1)

@app.callback(
    Output('output-v1-1', 'children'),
    Input('submit-v1-1', 'n_clicks'),
    State('input-v1-1', 'value')
)
def update_article(n_clicks,in_v1):

	return mysql_c.verifyP(in_v1)


# Graph 7-1
@app.callback(
    Output('example-graph6', 'figure'),
    Input('submit-v2', 'n_clicks'),
    State('input-v2', 'value')
)
def update_graph_V2(n_clicks, value):
   
    #time.sleep(3)
    #fig3 = mysql_c.q33(list_options)
    
    fig = mysql_c.FacultyPublicationView(value)
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
