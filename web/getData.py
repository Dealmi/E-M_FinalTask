##!/bin/python3

import mysql.connector #This is python's MySQL driver

#Let's connect to the database!
mydb = mysql.connector.connect(
  #host="data",
  host="localhost",
  user="app",
  password="1qaz@WSX",
  database="webapp"
)

# Let's make a SELECT request!
mycursor = mydb.cursor()
mycursor.execute("SELECT Articles.id, magazines.name, article_types.type, author.author \
FROM (((webapp.Articles \
INNER JOIN webapp.magazines ON Articles.magazines_id = magazines.id) \
INNER JOIN webapp.article_types ON Articles.article_types_id = article_types.id) \
INNER JOIN webapp.author ON Articles.author_id = author.id) order by Articles.id;") 
result = mycursor.fetchall() #list of tuples

# Let's make a webpage!
news=open("news.html", "w")
# The upper part of the html page
upperHtml='''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  border: 1px solid #ddd;
}

th, td {
  text-align: left;
  padding: 6px;
}

tr:nth-child(odd) {
  background-color: lightgray;
}
</style>
</head>
<body>

<h1 align=middle>List of magazines and issues</h1>

<table>
<tr>
    <th><h2>N</h2></th>
    <th><h2>MAGAZINE</h2></th>
    <th><h2>TYPE</h2></th>
    <th><h2>AUTHOR</h2></th>
</tr>
'''  # end of the upper part
news.write(upperHtml)

# The middle part of the html page
for tup in result:
  news.write("<tr>")
  news.write("\n")
  for x in tup:
    text = "<th>"+str (x)+"</th>"+"\n"
    news.write(text)
  news.write("</tr>")
  news.write("\n")

# The bottom part of the html page
bottomHtml='''</table>

</body>
</html>
'''
news.write(bottomHtml)

news.close()

