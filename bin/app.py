#!/usr/bin/python

import os
import sys
"""Allow imports from the dmarc_parser directory"""
sys.path.append('./dmarc_parser')
import parse_dmarc
from parse_dmarc import parse_dmarc
import requests
import simplejson
import unzip
from unzip import unzip
from flask import Flask, Response, request
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
import requests
from configobj import ConfigObj

__author__ = 'Elmer Thomas'
__version__ = '0.1'

app = Flask(__name__)
config = ConfigObj('./config.ini')
app.config['SQLALCHEMY_DATABASE_URI'] = config['mysql_db_url']
db = SQLAlchemy(app)

"""Default route"""
@app.route('/')
def default():
	return "Welcome to the SendGrid.com DMARC parser."

"""Unzip an emailed DMARC report, parse it, store in DB and if applicable return a report"""
def process(file):
	"""Attributes needed for the DMARC processing

	Keyword arguements:
	file -- location of the DMARC file that has been already received and saved on the local server
	"""

	"""Unzip the first attached DMARC report"""
	app = unzip(file, "./")
	app.extract()
	unzipped_filenames = app.get_unzipped_filenames()
	
	"""Parse the DMARC records"""
	app = parse_dmarc(unzipped_filenames[0], config)
	app.parser()
	app.get_report_metadata()	
	app.get_policy_published()
	app.get_records()

"""Convert MySQL tables to Python objects -- WORK IN PROGRESS"""
def load_session():
	""""""    
	engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
	metadata = MetaData(engine)
	sg_policy_published = Table('policy_published', metadata, autoload=True)
	mapper(Policy_Published, sg_policy_published)
	sg_records = Table('records', metadata, autoload=True)
	mapper(Records, sg_records)
	sg_report_metadata = Table('report_metadata', metadata, autoload=True)
	mapper(Report_Metadata, sg_report_metadata)
	Session = sessionmaker(bind=engine)
	session = Session()
	return session

"""Process an incoming request via email using SendGrid.com's Parse API"""
@app.route('/parse', methods=('GET', 'POST'))
def sendgrid_parser():
	if request.method == 'POST':
		"""Required response to SendGrid.com's Parse API"""
		print "HTTP/1.1 200 OK"
		print

		"""Parse the incoming email using SendGrid's Parse API and identify the DMARC report attachement"""
		envelope = simplejson.loads(request.form.get('envelope'))
		to_address = envelope['to'][0]
		from_address = envelope['from']
		text = request.form.get('text')
		subject = request.form.get('subject')
		num_attachments = int(request.form.get('attachments', 0))

		if num_attachments == 1:
			"""Grab the attachment and process it"""
			attachment = request.files.get('attachment1')
			attachment.save("./data/tmp.zip")
			process("./data/tmp.zip")
 
		if to_address != config['slurp_email']:
			""" Take the domain in the subject line to find DMARC reported issues """
			domain = subject			
			""" Send the results via email using SendGrid.com's REST API: http://docs.sendgrid.com/documentation/api/web-api/"""
			payload = {'to': config['report_receiver_email'], 'from': config['report_sending_email'], 'subject': 'DMARC Results sent via SendGrid.com', 'text': from_address, 'html': from_address, 'api_user': config['sendgrid_api_user'], 'api_key': config['sendgrid_api_key']}
			r = requests.get("http://sendgrid.com/api/mail.send.json", params=payload)

		return "HTTP/1.1 200 OK"

if __name__ == "__main__":
	""" Bind to PORT if defined, otherwise default to 5000 via Flask """
	port = int(os.environ.get('PORT', 5000))
	""" Turn this flag to False when in production """
	app.debug = True
	app.run(host='0.0.0.0', port=port)