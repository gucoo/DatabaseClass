# Academic-World-Dashboard
CS411 Database Systems Final Project


## Title: Faculty and University Performance
  Purpose: What is the application scenario? Who are the target users? What are the objectives?


### Scenario: 
  On comparing performance of each school as well as their individual faculty achievement
  
### Users: 
  HR/School & applicant/Researcher 
  
  - Can be used by graduate school applicants or researchers, who can use this information to look at schools to apply 
    to or faculty members to connect with based on the applicant's interest.
  - Can also be used by HR for special recrument.

  
### Objectives:

1.It uses number of publication and citation as a major measurment

2.It provides the history data and also the trend of data to evalute the faculty's performance in the past and see their potential in the future.

2.It shows how often people/univerisities work together

3.It has keywords filter for faculty or publication to measure the publication and citation under specific fields

4.It integrates the external sources to verify publication and faculty citation

5.It provides the functionalities to make a note on the user's finding 



## Demo: Give the link to your video demo.
### https://mediaspace.illinois.edu/media/t/1_n6mvy8vy


## Installation: How to install the application?
#### 1.Load the database collection for each database based on MP1-3 instruction

Make sure to change the user and password:[The following username and password is just a example]

*mysql.connector.connect(host="localhost",user="root",password="777",auth_plugin='mysql_native_password',database='academicworld')

*Neo4jConnection(uri="bolt://localhost:7687", user = 'neo4j', pwd = 'password')

*MongoClient("mongodb://localhost:27017/")
	
#### 2.Install various python libararies using pip install or pip3 install

*pip install mysql.connector 

*pip install mysql-connector-python -> may needs to delete and reinstall if it keeps having failure

*pip install pymongo

*pip install neo4j

*pip install google-search-results

*pip install pandas,plotly or other more common libraries


#### 3.Apply for api key from https://serpapi.com [Free version only have 100 calls per month]



## Usage: How to use it? 

Run Neo4j
Run python3 app.py in Mac or python app.py in windows console/cmd
Open broswer with URL http://127.0.0.1:8050/
The Dashboard will show and user can type in input for looking graph and also save the faculty information and make the comment
and verify the faculty or publication's citation.



## Design: What is the design of the application? Overall architecture and components.


1. We have 4 components: app.py mysql_connect.py, mongo_connect.py and neo4j_connect.py.

2. app.py using python3 dash framework and combines html and bootstrap's style.

3. app.py also imports functions from mysql_connect.py, mongo_connect.py and neo4j_connect.py.

4. We grouped the functions based on what database we get the data from to show the graph. 

5. We added the serpapi as external API calls with free key

7. Our dashboard consists of 13 widgets.
	
	Three of these widgets do not take user input:
	 - Total University, Faculty, and Publication; This is included to give an inital overview of the dataset
	 - University and Faculty Collaboration Performance: There are to give a unique view on top performance of schools/faculty members, rather than being measured purely by output, these tables show the top 10 schools/faculty that have collaborated the most with other faculty/universities (have published papers with highest number of distinct other schools/faculty)

	Six of these widgets take user input and display a graph based on the input. These widgets are meant to allow the user to explore different faculty members and top universities, and check their performance within a particular topic (keyword), mainly in terms of publication output and number of times cited. For universities, there is also a widget to display performance in terms of amount of faculty researching a specific topic. These widgets are:
	  - Faculty with Most Number of Publications
	  - University with Most Number of Publications
	  - Faculty with the Most Number of Citations and Publications
	  - Universities with the Most Number of Faculty
	  - Faculty Improvement
	  - Show all Publication for the faculty
	  
	Two widgets take user input and perform updates the backend of the database. these are:
	  - Add or Delete Your Favorite Faculty Members
	  - Add Comments to Favorite Faculty
	  
	Two widgets take user input and use external API data sources:
	  - Verify with Google Scholar; to verify faculty's information and the publication's information and newest citations.
	  
	 

## Implementation: How did you implement it?

1. We have the basic collections stored in our 3 database Mysql, Neo4j and mongo, which complete the basic data source for the academic world

2. We uses Python Dash as a server and frontend to query and graph the data from 3 database.

3. Inside the app.py, We decide the layout on Dash App and create layout to put different graph inside the application

4. When program starts, it will prepare the favorite table and two view on favorite and verification, and add the comment attribute to the faculty table.

5. In each graphs, we have the different @callout to response to the user input value

6. Inside the mysql_connect.py, we have a function to create a mysql connection, and functions to create/update several widgets lsited below: 
	  - Total University, Faculty, and Publication
	   	- This widget uses a sumple query to determine the count in each of three mysql tables: University, Faculty, Publication

	  - Faculty and University with Most Number of Publications
	   	- These two widgets uses a mysql query to select the count of publication ids published by each professor (or by faculty members affiliated with each university), in descending order. There is an option to look at all publications published by a faculty member (or by faculty members affiliated with a unviersity), or only publications that have a specified keyword. The results are displayed in a plotly bar graph.

	  - Faculty with the Most Number of Citations and Publications
	   	- This widget uses a mysql query to sum all the citations for each faculty members publications. There is an option to look at all citations of publications published by a faculty member, or only citations of publications that have a specified keyword. The results are displayed in a plotly bar graph.
	   	
	  - Faculty Improvement
	 	- This widget uses a mysql query to calculate the sum of all of a faculty's publication citations grouped by year. The results are displayed in a line graph to clearly show the trend of citations over time for a specific professor. 
	 	
	  - Favorite Faculty Members (the table, add/delete, and add comments widgets)
	   	- These widgets use a set of functions that first creates a table called 'favorites' with an id attribute, adds an attribute 'comments' to the 'faculty' table, and a view called 'favfaculty' to show faculty information, affiliation name and comments. The favorites table has a foreign key constraint, so that only faculty that already exist in the faculty table can be added to the favorites table. There are separate functions to add and delete faculty members from the favorites table and therefore the favfaculty view, and to add comments to the faculty table and therefore the favfaculty view. These insertions, deletions and updates all use prepared statements. The favfaculty view is displayed in a plotly table.
	   	
	  - Show All Publications for the Faculty 
	   	- This widget uses a function to create a view for a given faculty's publications and each publications citations number. This view is then displayed in a plotly table.

	 - Verify Faculty and Publication citation with Google Scholar- extra credit
	   	- This widget uses external source to to API get request for searching the author and publication. Once users enter author name + affliation or title of publication. It will show the relavant data from Google Scholar with updated citation. We also provide raw query result as a reference, so that users could do further investigate, if they are interested with the author or publication. The search includes all faculty fields or publication keyword.

7. Inside the mongo_connect.py, we have functions to create/update this widget: 
	  - Universities with the Most Number of Faculty
	   	- This widget uses a query to select the each university and its count of affiliated faculty, in descending order. There is an option to view count of all faculty in a university, or only faculty related to a specific keyword topic. There is also an option to limit the results by a top number- the default is top 5 universities. The results of this query are displayed in a plotly pie chart. 

8. Inside the neo4j_connect.py, we have functions to create tables for Top University and Faculty members in terms of Collaboration on Publications. Neo4j was specifically selected for these two widgets since it is easy to query patterns of relationships between instances of a relation. Using a pattern, we were able to easily query faculty members that published papers that were also published by the most other distinct faculty members, as well as universities that had faculty members that published papers that were also published by faculty from the most other university.
	  - These two widgets used queries to select each faculty member and its distinct count other faculty members that they had worked with (the two faculty members had published a paper together), and each unviersity and its distinct count of other universities that they had collaborated with (the two universities had faculty members who published a paper together). The top 10 results of each query were displayed in descending order in a plotly table.
	


## Database Techniques: What database techniques have you implemented? How?
1. View - 

For all faculty with their publication we created the view called verification. It is used later with special faculty id as the user input for the faculty and publication table.

For favorites figure, we created a view to contain only faculty members denoted as favorites (from user input) as well as the university name they are affiliated with. The favorite faculty ids are contained in a new relation called 'favorites', and the view is created using only faculty members whose ids are in that relation.

2. Contraint - 

The favorites relation has a foreign key constraint, such that the attribute 'id' that references the 'id' attribute in the 'faculty' relation. This is so you cannot add a faculty member to the favorites table that does not exist in the faculty relation. The foreign key constraint is added when the favorites relation is created.


3. Prepare statement - 

For many of our queries we use prepared statements to include user input. Prepared statements were used to add and delete faculty to the favorites table and view, add comments to the faculty table (in the functions 'addfav', 'delfav', and 'add_comments' in mysql_connect.py file) based on user input.



## Extra-Credit Capabilities: What extra-credit capabilities have you developed, if any?
External API data sources from Google scholar to verify faculty's information and the publication's information and newest citations.
At first, we plan to get all citations number but since we have the limitation on API calls so we decide to let user specify the single faculty or publication to verfy.


## Contributions: How each member has contributed, in terms of 1) tasks done and 2) time spent?

We equally shared all sections as much as possible, and spent 45-48 hours in total to decide the basic layout, implement basic functionalities and debug.

  - Guanwen: 
  	- Layout, design, user input and callback functions, mysql connection and functions
  	- API calls, extra credit
  	- Widgets: 'Total University, Faculty, and Publication', 'Faculty with Most Number of Publications', 'Faculty with the Most Number of Citations and Publications'. 'Faculty Improvement', 'Show all Publication for the faculty', 'Verify faculty citation with Google Scholar', 'Verify publication citation with Google Scholar'

  - Lamia: University Graph, publication Tables and favorites table design and code, debug prepare statement, view and contraint, document.
   	- mongodb and neo4j database connections and functions
   	- Database constraints: prepare statement, view and foreign key constraint in favorites widgets
   	- Widgets: 'University and Faculty Collaboration Performance', 'University with Most Number of Publications', 'Universities with the Most Number of Faculty', 'Add or Delete Your Favorite Faculty Members', 'Add Comments to Favorite Faculty' 

## Debug Note

##### External API Google Scholar - For All keyword
1. External source only have 100 times per month API calls for free
2. Need to type more closer to the name of faculty or publication. 
3. "Cannot Find " could happen if the input is vague to the API search Engine. 
4. Ther are some special cases for searching. For example "College of William & Mary" will not work with its full name but will work with "William Mary"
5. The number is for "all" faculty field or publication keyword

##### University Pie chart
1. The top number will be limited by how popular among different Universities.
If there are not as many universities with any faculty researching the chosen keyword as selected in the top #, the pie chart will only show the most universities possible. For example, there are only 5 universities with faculty focused on 'cyber security', so if the user selected '16' top universities, the pie chart wil still only show 5 universities.

##### MySQL functions
1. Since so many of our queries are using the mysql database, we had a lot of server jams and our application slowed down and barely ran after we added our favorites table. We create a new cursor for each query in each of our functions for this reason.

