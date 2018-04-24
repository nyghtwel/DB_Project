from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.contrib import messages
import json
import csv
from django.conf import settings

def populate_form(id, query):
	table = []
	with connection.cursor() as cursor:
			cursor.execute(query)
			table = dictfetchall(cursor)
			# print(table)
			table = [row[id] for row in table]

	return (table, "")


def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]


def export_csv_file(request, data):
	
	# data = [{'NAME': 'Ohio', 'DATA_VALUE': '21%'},
    #      {'NAME': 'Ohio', 'DATA_VALUE': '21%'}, {'NAME': 'Ohio', 'DATA_VALUE': '21%'}, {'NAME': 'Ohio', 'DATA_VALUE': '21%'}]

	response = HttpResponse()
	response['Content-Disposition'] = 'attactment; filename="data.csv"'

	writer = csv.writer(response)
	writer.writerow([key for key in data[0]])

	for row in data:
		writer.writerow([row[i] for i in row])

	return response


def list_to_query(list):
	temp=[]

	if not list:
		return ''
	else:
		for i in list:
			temp.append("'"+i+"'")
		return ', '.join(temp)

## used for dynamic query
def temp_fill(answer):
    return 'is not null' if answer == '' else 'in ({})'.format(answer)


def add_user_query(quer):
	if not settings.USER: return 
 # if request.method == 'POST' and request.POST.get('submit'):
	username = settings.USER_NAME
	query1 = ''' select max(query_id) from query where query_id is not null
	'''
	num = None
	with connection.cursor() as cursor:
		cursor.execute(query1)
		num = cursor.fetchone()
	print(num)
	if num:	
	    # increment the max query_id by 1
		query2 = '''insert into query(query_id, query) 
				values({},'{}')
				'''.format(num+1, quer)
		query3 = '''insert into write(username, query_id, datetime) 
					values('{}', {}, systimestamp)
				'''.format(username, num+1)

	else:
		query2 = '''insert into query(query_id, query) 
				values(1,'{}')
				'''.format(num, quer)

		query3 = '''insert into write(username, query, datetime) 
					values('{}', '{}', systimestamp)
				'''.format(username, num)

	with connection.cursor() as cursor:
		cursor.execute(query2)
		cursor.execute(query3)
