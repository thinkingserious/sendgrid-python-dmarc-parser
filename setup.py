try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
    'description': 'This is a DMARC report parser that accepts either an XML or zipped file as input at an attachment via email',
	'author': 'Elmer Thomas',
	'url': '',
	'download_url': '',
	'author_email': 'elmer.thomas@sendgrid.com',
	'version': '0.1',
	'install_requires': ['nose', 'Flask', 'Flask-SQLAlchemy', 'Jinja2', 'Werkzeug', 'distribute', 'wsgiref', 'mysql-python', 'requests', 'simplejson', 'configobj'],
	'packages': ['dmarc_parser'],
	'scripts': [],
	'name': 'DMARC Parser'
}

setup(**config)
