from pymongo import MongoClient
import pymongo
import plotly.express as px
import pandas as pd
import time


# Basic MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['academicworld']


def q2(keyword,top):

    # mongodb query
    if keyword == 'all':
    	pipeline = [{"$unwind":"$keywords"},{"$group":{"_id":"$affiliation.name", "faculty_count":{"$sum":1}}}, {"$sort":{"faculty_count":-1}}, {"$limit":top}] 
    else:
    	pipeline = [{"$unwind":"$keywords"},{"$match":{"keywords.name":keyword}},{"$group":{"_id":"$affiliation.name", "faculty_count":{"$sum":1}}}, {"$sort":{"faculty_count":-1}}, {"$limit":top}]
    q2_result = list(db.faculty.aggregate(pipeline)) 
    return q2_result

def q2_graph(result):    

    # DataFrame
    df = pd.DataFrame(result)
    
    # Graph 
    fig1 = px.pie(df, values='faculty_count', names = '_id')
    return fig1
    
