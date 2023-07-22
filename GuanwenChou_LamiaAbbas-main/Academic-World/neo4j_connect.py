from neo4j import GraphDatabase
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Neo4j connection
class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
        
def q4():
    
    # Neo4j Connection
    conn = Neo4jConnection(uri="bolt://localhost:7687", user = 'neo4j', pwd = 'password')
    
    # Neo4j query 
    query_string = '''
MATCH (university1:INSTITUTE)<-[affiliate:AFFILIATION_WITH]-(faculty1:FACULTY)-[publish:PUBLISH]->(publication:PUBLICATION)<-[publish2:PUBLISH]-(faculty2:FACULTY)-[a2:AFFILIATION_WITH]->(university2:INSTITUTE) WHERE university1.name<>university2.name AND faculty1<>faculty2 RETURN university1.name, COUNT(distinct university2.name) AS univ_count order by univ_count desc limit 10
'''
    result = conn.query(query_string, db='academicworld')
    return result


def q4_table(result):
    
    # DataFrame
    df = pd.DataFrame(result, columns=['name','univ_count'])
    
    # Table
    fig = go.Figure(data=[go.Table(
    header=dict(values=['<b>Name</b>', '<b>Number of Universities Collaborated With</b>'],
                fill_color='gold',
                align='center', font=dict(size=14)),
    cells=dict(values=[df.name, df.univ_count],
               fill_color='lightyellow',
               align='center', font=dict(size=12)))
    ])
    return fig

# neo4j query 
def q5():
    conn = Neo4jConnection(uri="bolt://localhost:7687", user = 'neo4j', pwd = 'password')
    query_string2 = '''
MATCH (faculty1:FACULTY)-[publish:PUBLISH]->(publication:PUBLICATION)<-[publish2:PUBLISH]-(faculty2:FACULTY) WHERE faculty1<>faculty2 RETURN faculty1.name, COUNT(distinct faculty2.name) AS distinct_faculty_count order by distinct_faculty_count desc limit 10
'''
    result = conn.query(query_string2, db='academicworld')
    return result

def q5_table(result):
    
    # DataFrame
    df = pd.DataFrame(result, columns=['name','faculty_count'])
    
    # Table
    fig = go.Figure(data=[go.Table(
    header=dict(values=['<b>Name</b>','<b>Number of Faculty Collaborated With</b>'],
                fill_color='coral',
                align='center', font=dict(size=14)),
    cells=dict(values=[df.name, df.faculty_count],          
        fill_color='mistyrose',
        align='center', font=dict(size=12)))
    ])
    return fig

