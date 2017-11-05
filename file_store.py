from flask import Flask,render_template,request
from flaskext.mysql import MySQL

db=MySQL()
app=Flask(__name__)
app.config['MYSQL_DATABASE_USER']='be9811e51062dd'
app.config['MYSQL_DATABASE_PASSWORD']='850910b7'
app.config['MYSQL_DATABASE_DB']='ibmx_44373acfd49e995'
app.config['MYSQL_DATABASE_HOST']='us-cdbr-sl-dfw-01.cleardb.net'
db.init_app(app)

def writebytesfile(values,file_name):
	with open(file_name,'wb') as f:
		f.write(values)

def readbytesfile(file_name):
	data=""
	with open(file_name,'rb') as file_upload:
		data=file_upload.read()
	return data

@app.route("/")
def main():
	conn=db.connect()
	cursor=conn.cursor()
	query="select * from new_table"
	cursor.execute(query)
	data=cursor.fetchall()
	return render_template("main_page.html",data=data)

@app.route("/upload_file",methods=['POST'])
def upload_file():
	file_name=request.form['uploadfile']
	upfile=readbytesfile(file_name)
	conn=db.connect()
	cursor=conn.cursor()
	cursor.execute("insert into new_table(file_name,idfile) values(%s,%s)",(file_name,upfile))
	conn.commit()
	conn.close()
	conn=db.connect()
	cursor=conn.cursor()
	query="select * from new_table"
	cursor.execute(query)
	data=cursor.fetchall()
	return render_template("main_page.html",message1="File Uploaded To Database",data=data)

@app.route("/download_file")
def download_file():
	file_name=request.args['filename']
	conn=db.connect()
	cursor=conn.cursor()
	cursor.execute("select idfile from new_table where file_name=%s",file_name)
	file_content=cursor.fetchone()[0]
	writebytesfile(file_content,file_name)
	conn.close()
	conn=db.connect()
	cursor=conn.cursor()
	query="select * from new_table"
	cursor.execute(query)
	data=cursor.fetchall()
	return render_template("main_page.html",message="File Downloaded from Database",data=data)

if __name__=="__main__":
	app.run(debug=True)