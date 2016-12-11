from bottle import route, run, post, request, template, static_file
import os
import csv,sqlite3

con = sqlite3.connect('soap.db')
cur = con.cursor()

@route('/')
def home():
	string = "SELECT name FROM sqlite_master WHERE type='table';"
	cur.execute(string)
	results = cur.fetchall()
	results = ["%s" % x for x in results]
	results = [x.encode('ascii') for x in results]
	if not {'office','rental','agency','agreement'} <= set(results):
		return template('./web/dbErr.html')
	return template('./web/home.html')

@route('/static/<filename>')
def serve_pictures(filename):
    return static_file(filename, root='./web')

@post('/dbFix')
def fix():
	try:
		qry = open('soap.sql', 'r').read()
		cur.executescript(qry)
	except Exception as err:
		return_list = ["Database Fix Failed!"]
		return_list.append(err)
		return template('./web/dbSelect_.html', data=return_list)
	con.commit()
	return template('./web/home.html')

@post('/dbClrConfirm')
def confirm():
	return template('./web/dbClrConfirm.html')

@post('/diagrams')
def diagrams():
	return template('./web/diagrams.html')

@post('/dbFilConfirm')
def confirm():
	return template('./web/dbFilConfirm.html')

@post('/dbSel')
def dbSel():
	string = request.forms.get('qry')
	if string[:6].lower() not in ["select","delete","insert"]:
		return template('./web/dbSelect_.html', data=["Query must be SELECT, DELETE, or INSERT"])

	if string[:6].lower() == "select":
		try:
			cur.execute(string)
			results = cur.fetchall()
			names = [[description[0] for description in cur.description]]
			results = [[s for s in t] for t in results]
			results = names + results
		except Exception as err:
			return_list = ["SELECT Failed!"]
			return_list.append(err)
			return template('./web/dbSelect_.html', data=return_list)
		return template('./web/dbSelect_result.html', data=results, rows=(len(results)-1))

	else:
		try:
			cur.execute(string)
		except Exception as err:
			return_list = [string[:6].upper() + " Failed!"]
			return_list.append(err)
			return template('./web/dbSelect_.html', data=return_list)
		con.commit()
		return template('./web/dbSelect_.html', data=[string[:6].upper() + " Success!", str(cur.rowcount) + " rows affected."])


@post('/dbClr')
def dbClr():
	try:
		qry = open('soap.sql', 'r').read()
		cur.executescript(qry)
	except Exception as err:
		return_list = ["Clear Failed!"]
		return_list.append(err)
		return template('./web/dbSelect_.html', data=return_list)
	con.commit()
	return template('./web/dbSelect_.html', data=["Tables Cleared!"])

@post('/dbFil')
def dbFil():
	table = request.forms.get('table')
	upload = request.files.get('upload')
	name, ext = os.path.splitext(upload.filename)
	if ext != ".csv":
		return_list = ["Upload Failed!","Select a .csv file."]
		return template('./web/dbSelect_.html', data=return_list)

	save_path = "./csv/{category}".format(category=table)
	if not os.path.exists(save_path):
		os.makedirs(save_path)

	file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
	try:
		upload.save(file_path,overwrite=True)
	except Exception as err:
		return_list = ["Load Failed!"]
		return_list.append(err)
		return template('./web/dbSelect_.html', data=return_list)

	file = open(file_path,"r")
	reader = csv.reader(file)
	headers = next(reader, None)
	
	try:
		if table == "office" and headers == ['city','name']:
			cur.executemany("INSERT OR IGNORE INTO office (city, name) VALUES (?, ?);", reader)
		elif table == "agreement" and headers == ['agency_ID','rental_ID']:
			cur.executemany("INSERT OR IGNORE INTO agreement (agency_ID, rental_ID) VALUES (?, ?);", reader)
		elif table == "agency" and headers == ['agency_ID','name','address','city','phone']:
			cur.executemany("INSERT OR IGNORE INTO agency (agency_ID, name, address, city, phone) VALUES (?, ?, ?, ?, ?);", reader)
		elif table == "rental" and headers == ['rental_ID','amount','endDate','squareFt','name']:
			cur.executemany("INSERT OR IGNORE INTO rental (rental_ID, amount, endDate, squareFt, name) VALUES (?, ?, ?, ?, ?);", reader)
		else:
			raise Exception("CSV column headers do not match selected table.")
	except Exception as err:
		return_list = ["Load Failed!"]
		return_list.append(err)
		file.close()
		os.remove(file_path)
		return template('./web/dbSelect_.html', data=return_list)
	
	con.commit()

	return_list = ["Load Success!", str(cur.rowcount) + " rows added."]
	if cur.rowcount <= 0:
		return_list.append("No changes were made. Check the format of your CSV file.")

	return template('./web/dbSelect_.html', data=return_list)

run(host='localhost', port=8080)

con.close()