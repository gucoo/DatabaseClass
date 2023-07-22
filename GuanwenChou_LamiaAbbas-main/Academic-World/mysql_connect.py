
import mysql.connector
import pandas as pd
import plotly.express as px
import time
import plotly.graph_objects as go
import time
from serpapi import GoogleSearch

# Mysql Connection
def createDB_connect():
	mydb = mysql.connector.connect(host="localhost",user="root",password="test_root",auth_plugin='mysql_native_password',database='academicworld')
	return mydb

def mysql_start():
	mydb = createDB_connect()
	cursor = None
	result = None
	try:
		cursor = mydb.cursor()
		query="select count(faculty.id) from faculty;"
		cursor.execute(query)
		result1 = cursor.fetchall()
		
		query="select count(publication.id) from publication;"
		cursor.execute(query)
		result2 = cursor.fetchall()
		
		query="select count(university.id) from university;"
		cursor.execute(query)
		result3 = cursor.fetchall()		
		cursor.close()
	except:
		print("except")
	
	return [result1[0][0],result2[0][0],result3[0][0]]
 
def q11(kw,top):
	mydb = createDB_connect()
	cursor = None
	result=None
	try:
		cursor = mydb.cursor()
		if(kw==all):
			query = "select faculty.id, faculty.name, university.name, count(publication.id) as numPub from faculty_publication, faculty, publication,publication_keyword,keyword, university where "
			query = query +"publication_keyword.keyword_id = keyword.id AND faculty.id = faculty_publication.faculty_id AND publication.id = faculty_publication.publication_id AND publication_keyword.publication_id = publication.id AND university.id = faculty.university_id group by faculty.id ORDER BY COUNT(numPub) DESC LIMIT "
			query= query+ str(top)+";"
		else:	
			query = "select faculty.id, faculty.name, university.name, count(publication.id) as numPub from faculty_publication, faculty, publication,publication_keyword,keyword ,university where keyword.name Like \"%"
			query = query + kw +"%\" AND publication_keyword.keyword_id = keyword.id AND faculty.id = faculty_publication.faculty_id AND publication.id = faculty_publication.publication_id AND publication_keyword.publication_id = publication.id AND university.id = faculty.university_id group by faculty.id ORDER BY COUNT(numPub) DESC LIMIT "
			query= query+ str(top)+";"
			
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()
	except:
		print("except")
	
	return result
 

def q1_graph(result):    

    # Data Frame
    df = pd.DataFrame(result, columns=['id','professor','university', "numPublication"])
    df['Faculty Member']=+df['professor']+'- id:'+(df['id']).astype(str) #+ '-'+df['university']
    df['Number of Publications'] = df['numPublication']
    # Graph
    fig0 = px.bar(df, x='Faculty Member', y='Number of Publications', text='numPublication',color="Faculty Member")
	
    #fig.show()
    fig0.update_layout(showlegend = False)
    return fig0
    
def q22(kw,top):
	mydb = createDB_connect()
	cursor = None
	result=None
	try:
		cursor = mydb.cursor()
		if(kw==all):
			
			query = "select faculty.id, faculty.name, university.name, count(publication.id) as totalnumPub, sum(publication.num_citations) as totalnumCitation from faculty_publication, faculty, publication,publication_keyword,keyword,university where "
			query = query + "publication_keyword.keyword_id = keyword.id AND faculty.id = faculty_publication.faculty_id AND publication.id = faculty_publication.publication_id AND publication_keyword.publication_id = publication.id and university.id = faculty.university_id group by faculty.id ORDER BY COUNT(totalnumPub) DESC LIMIT "
			query= query+ str(top)+";"
		else:	
			
			query = "select faculty.id, faculty.name, university.name, count(publication.id) as totalnumPub, sum(publication.num_citations) as totalnumCitation from faculty_publication, faculty, publication,publication_keyword,keyword,university where keyword.name Like \"%"
			query = query + kw +"%\" AND publication_keyword.keyword_id = keyword.id AND faculty.id = faculty_publication.faculty_id AND publication.id = faculty_publication.publication_id AND publication_keyword.publication_id = publication.id and university.id = faculty.university_id group by faculty.id ORDER BY COUNT(totalnumPub) DESC LIMIT "
			query= query+ str(top)+";"

			
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()
	except:
		print("except")
	
	return result
 

def q2_graph(result):    

    # Data Frame
    df = pd.DataFrame(result, columns=['id','professor',"university.name","totalnumPub", "totalnumCitation"])
    df['info']=df['professor']+'- id:'+(df['id']).astype(str) + df['university.name']
    df['Total Number of Citations'] = df['totalnumCitation']
    df['Total Number of Publications'] = df['totalnumPub']
    # Graph
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
    x=df['info'],
    y=df['Total Number of Citations'],
    text=df['Total Number of Citations'],
    name='Total Number of Citations'
    
    ))
    
    fig3.add_trace(go.Scatter(
    x=df['info'],
    y=df['Total Number of Publications'],
    name='Total Number of Publications',
    mode='markers+text',
    textposition='top center',
    text=df['Total Number of Publications'],
    #mode="lines",
    marker=dict(
        size=10,     
        color=df['Total Number of Publications'], #set color equal to a variable
        colorscale='Viridis', # one of plotly colorscales
        showscale=True
    )
    ))
    
    fig3.update_layout(legend=dict(groupclick="toggleitem"))
    fig3.update_layout(legend_x=-0.35)
    
    return fig3

def q3():
	mydb = createDB_connect()
	cursor = mydb.cursor()
	fig3 = go.Figure()   
	traces = []
	id_options=[0,2,3]
	x=0
	for x in id_options:
		query="select faculty.id, faculty.name,publication.year,sum(publication.num_citations) from faculty,faculty_publication,publication " + "where faculty.id = " + str(x)+" and faculty.id = faculty_publication.faculty_id and faculty_publication.publication_id = publication.id group by year;"
		cursor.execute(query)
		result = cursor.fetchall()
		
		df = pd.DataFrame(result, columns=["pro_id","pro_name","year","Total_numCitation"])
		df['info']=df['pro_name']+' - id:'+(df['pro_id']).astype(str)
		nam = str(x)
		df=df.sort_values(by=['year'])
		fig3.add_trace(go.Scatter(x=df['year'], y=df['Total_numCitation'],mode='markers+lines',name=nam))
	cursor.close()
	return fig3

def q33(list_options):
    
    
    fig3 = go.Figure()   
    traces = []
    id_options=list_options
    mydb=createDB_connect()
    cursor = mydb.cursor()
    for x in id_options:
    	# loop each faculty.id
    	query="select faculty.id, faculty.name,publication.year,sum(publication.num_citations) from faculty,faculty_publication,publication " + "where faculty.id = " + str(x)+" and faculty.id = faculty_publication.faculty_id and faculty_publication.publication_id = publication.id group by year;"
    	cursor.execute(query)
    	result = cursor.fetchall()
    	
    	
    
    	import pandas as pd
    	df = pd.DataFrame(result, columns=["pro_id","pro_name","year","Total_numCitation"])
    	df['info']=df['pro_name']+' - id:'+(df['pro_id']).astype(str)
    	if len(df)!=0:
    		
    		nam = str(x) + df['pro_name'].iloc[0]
    		df=df.sort_values(by=['year'])
    	
    		traces.append({'x':df['year'], 'y': df['Total_numCitation'], 'name':nam})
    	else:
    		
    		
    		df2 = {'year': 2015, 'Total_numCitation':0}
    		df=df.append(df2,ignore_index = True)
    		traces.append({'x':df['year'], 'y': df['Total_numCitation'], 'name':str(x)})
    
    
    cursor.close()
    fig3 = {
        # set data equal to traces
        'data': traces,
        # use string formatting to include all symbols in the chart title
        'layout': {'title':'Professor total number of citation yearly'}
    }
    
    
    
    return fig3
    
def get_option():
    
    mydb = createDB_connect()
    cursor = mydb.cursor()
    options = []
    

    # loop each faculty.id
    query="select faculty.id, faculty.name from faculty" 
    cursor.execute(query)
    result = cursor.fetchall()
    
    df = pd.DataFrame(result, columns=["pro_id","pro_name"])
    df['info']=df['pro_name']+' - id:'+(df['pro_id']).astype(str)
    id_list=df['pro_id'].tolist()
    
    for some in id_list:
        options.append({'label':'{} {}'.format(some,df['pro_name'].iloc[some]), 'value':some})
    
    cursor.close()
    return options    


def createDefault():

    mydb = createDB_connect()
    cursor = mydb.cursor()
    
    cursor.execute("SHOW TABLES LIKE 'favorites'")
    result = cursor.fetchone()
    
    
    if result == None:
        cursor.execute("CREATE TABLE favorites ( id int NOT NULL, PRIMARY KEY(id), FOREIGN KEY(id) REFERENCES faculty(id))")
        print("fav table created")
    cursor.execute("SHOW TABLES LIKE 'favfaculty'")
    result = cursor.fetchone()
   
        
    	# add comment attribute if not already in faculty table
    try:
        cursor.execute("ALTER TABLE faculty ADD comments VARCHAR(255) DEFAULT ' '")
    except:
        pass 
    
    if result == None:
        cursor.execute("CREATE VIEW favfaculty AS SELECT distinct f.id, f.name, u.name AS affiliation, f.comments FROM faculty f, university u, favorites fav WHERE f.id = fav.id AND f.university_id = u.id")
        print("fav view created")
    cursor.close()     
    mydb2 = createDB_connect()
    cursor2 = mydb2.cursor()    
    query = "select faculty.id as f_id,publication.id as p_id, publication.title, publication.num_citations as citation from faculty, publication,faculty_publication where faculty.id =faculty_publication.faculty_id and publication.id = faculty_publication.publication_id"
    time.sleep(1)
    cursor2.execute("DROP VIEW IF EXISTS verification ")
    time.sleep(1)
    cursor2.execute("CREATE VIEW verification AS "+ query)
    cursor2.close()
    return


def favfacultygraph():
        mydb=createDB_connect()
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM favfaculty")
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['id', 'name', 'affiliation', 'comments'])

        fig = go.Figure(data=[go.Table(
            header=dict(values=['<b>ID','<b>Name','<b>Affiliation', '<b>Comments'],
                        fill_color='royalblue',
                        align='center', font=dict(size=14)),
            cells=dict(values=[df.id, df.name, df.affiliation, df.comments],
                        fill_color='aliceblue',
                        align='center', font=dict(size=12)))
            ])
        cursor.close()
        return fig

def addfav(listoption):   
    
    mydb=createDB_connect()
    cursor = mydb.cursor()

    for fid in listoption:
    	sql = "INSERT IGNORE INTO favorites (id) VALUES (%s)"
    	val = (fid,)
    	cursor.execute(sql, val)
    	print("1 record inserted, ID:", cursor.lastrowid)
    	mydb.commit()

    cursor.close()
    
    
def delfav(listoption):
    mydb=createDB_connect()
    cursor = mydb.cursor()

    for fid in listoption:
    	sql = "DELETE FROM favorites WHERE id = %s"
    	val = (fid,)
    	cursor.execute(sql, val)
    	mydb.commit()
    	print(cursor.rowcount, "record(s) deleted")
    
    cursor.close()

def create_comments():
	
    
    mydb=createDB_connect()
    cursor = mydb.cursor()

	# add comment attribute if not already in faculty table
    try:
        cursor.execute("ALTER TABLE faculty ADD comments VARCHAR(255) DEFAULT ' '")
    except:
        pass
    cursor.close()
    return

def facultygraph():
    
	# get faculty data
	
    mydb=createDB_connect()
    cursor = mydb.cursor()
    cursor.execute("SELECT id, name, comments FROM faculty WHERE id IN (SELECT * FROM favorites)")
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['id', 'name', 'comments'])

	# make faculty figure
    fig = go.Figure(data=[go.Table(
        header=dict(values=['<b>ID','<b>Name','<b>Comments'],
                    fill_color='royalblue',
                        align='center', font=dict(size=14)),
        cells=dict(values=[df.id, df.name, df.comments],
                    fill_color='aliceblue',
                        align='center', font=dict(size=12)))
            ])

    cursor.close()
    return fig

def add_comments(comments, fid):
    
    mydb = createDB_connect()
    cursor = mydb.cursor()
    for fac in fid:
        sql = "UPDATE faculty SET comments = (%s) WHERE id = (%s)"
        val = (comments, str(fac))
        cursor.execute(sql, val)
        mydb.commit()
    cursor.close()
    print("1 comment added, ID:", cursor.lastrowid)
    return

def FacultyPublicationView(f_id):
	query = "select * from verification where f_id = "+ str(f_id)
	mydb = createDB_connect()
	cursor = mydb.cursor()
	cursor.execute(query)
	result2 = cursor.fetchall()
	cursor.close()

	df2 = pd.DataFrame(result2, columns=['f_id','p_id','title','citation'])

	fig = go.Figure(data=[go.Table(
            header=dict(values=['<b>faculty_ID','<b>Publication_ID','<b>Title','<b>Citation'],
                        fill_color='royalblue',
                        align='center', font=dict(size=14)),
            cells=dict(values=[df2.f_id, df2.p_id, df2.title, df2.citation],
                        fill_color='aliceblue',
                        align='center', font=dict(size=12)))
            ])
	return fig

def verifyP(pub):

	params = {"engine": "google_scholar","q": "","api_key": "58bf21c194e06d0746bad34436d1c39771f53d227076a824f65904310f2b91f1"}
	params["q"]=pub
	search = GoogleSearch(params)
	new_citation=''
	try:
		info = search.get_dict()['organic_results'][0]
		new_citation=str(info['inline_links']['cited_by']['total']) +'      Details-------------->'+ str(info)

	except:
		new_citation = 'Cannot find'
		
	return new_citation
              

def verifyF(name):

	params = {"api_key": "58bf21c194e06d0746bad34436d1c39771f53d227076a824f65904310f2b91f1","engine": "google_scholar_profiles",  # profile results search engine
        "mauthors": " ", }

	params["mauthors"]=name
	search = GoogleSearch(params)
	new_citation=''
	
	try:
		info = search.get_dict()['profiles'][0]
		new_citation =str(info['cited_by']) +'      Details-------------->'+ str(info)

	except:
		new_citation='Cannot find'
		
	return new_citation
	
	#details =  '------------> Details: '+ str(a)
	#x = 'Cited_by ' + str(a['cited_by']) + ' ------------> Details: '+ str(a)


def univpub(kw,top):
    mydb = createDB_connect()
    cursor = None
    result=None
    cursor = mydb.cursor()

    if kw == "all":
        query = "SELECT university.name, COUNT(faculty_publication.publication_id) AS pubCount FROM faculty, faculty_publication, university WHERE faculty.id = faculty_publication.faculty_id AND university.id=faculty.university_id GROUP BY faculty.university_id ORDER BY pubCount DESC LIMIT "
        query= query+ str(top)+";"
        cursor.execute(query)

    else:
        query = "SELECT university.name, COUNT(faculty_publication.publication_id) AS pubCount FROM faculty, faculty_publication, university WHERE faculty.id = faculty_publication.faculty_id AND university.id=faculty.university_id AND faculty_publication.publication_id IN (SELECT pk.publication_id FROM publication_keyword pk, keyword k WHERE pk.keyword_id = k.id AND k.name LIKE %s) GROUP BY faculty.university_id ORDER BY pubCount DESC LIMIT "
        query= query+ str(top)+";"
        val = (kw,)
        cursor.execute(query, val)

    result = cursor.fetchall()
    cursor.close()

    return result

def univpub_graph(result):    

    # Data Frame
    df = pd.DataFrame(result, columns=['name','pubcount'])
    df['University']=df['name']
    df['Number of Publications']=df['pubcount']
    #
    # Graph
    fig0 = px.bar(df, x='University', y='Number of Publications', text='pubcount',color="name")
    fig0.update_layout(showlegend = False)

    return fig0

	

