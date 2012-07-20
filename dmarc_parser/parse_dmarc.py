import time
import MySQLdb as mysql
import xml.etree.ElementTree as ET

__author__ = 'Elmer Thomas'
__version__ = '0.1'

class parse_dmarc:
	"""Parse a DMARC XML formatted report"""
	def __init__(self, input_filename, config):
		"""Attributes needed for file processing

		Keyword arguements:
		input_filename -- file that needs to be parsed 
		dir -- directory where the parsed file will be stored 
		"""
		self.input_filename = input_filename
		self.db = mysql.connect(config['mysql_host'], config['mysql_user'], config['mysql_pass'], config['mysql_db'])
		self.cursor = self.db.cursor()
		"""These are foreign keys that link the reports to their metadata and policy information"""
		self.metadata_fk = ""
		self.policy_fk = ""

	def parser(self):
		"""Open the file to be Parsed and input the XML into the DOM"""
		dom = ET.parse(self.input_filename)
		self.doc = dom.getroot()

	def get_report_metadata(self):
		"""Extract the DMARC metadata as defined here: 
		http://www.dmarc.org/draft-dmarc-base-00-02.txt in Appendix C
		If no data is found, return NA
		"""
		orgName = self.doc.findtext("report_metadata/org_name", default="NA")
		email = self.doc.findtext("report_metadata/email", default="NA")
		extraContactInfo = self.doc.findtext("report_metadata/extra_contact_info", default="NA")
		reportID = self.doc.findtext("report_metadata/report_id", default="NA")
		dateRangeBegin = self.doc.findtext("report_metadata/date_range/begin", default="NA")
		dateRangeBegin = int(dateRangeBegin)
		dateRangeEnd = self.doc.findtext("report_metadata/date_range/end", default="NA")
		dateRangeEnd = int(dateRangeEnd)

		"""Insert report metadata"""
		sql = """INSERT INTO report_metadata(organization, email, extra_contact_information, report_id, date_range_begin, date_range_end) 
					VALUES("%s", "%s", "%s", "%s", %d, %d)""" %(orgName, email, extraContactInfo, reportID, dateRangeBegin, dateRangeEnd)
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()

		self.metadata_fk = self.cursor.lastrowid

	def get_policy_published(self):
		"""Extract the DMARC policy published information as defined here: 
		http://www.dmarc.org/draft-dmarc-base-00-02.txt in Section 6.2
		If no data is found, return NA
		"""
		domain = self.doc.findtext("policy_published/domain", default="NA")
		adkim = self.doc.findtext("policy_published/adkim", default="NA")
		aspf = self.doc.findtext("policy_published/aspf", default="NA")
		p = self.doc.findtext("policy_published/p", default="NA")
		pct = self.doc.findtext("policy_published/pct", default="NA")
		pct = int(pct)
		sql = """INSERT INTO policy_published(domain, adkim, aspf, p, pct) 
					VALUES("%s", "%s", "%s", "%s", %d)""" %(domain, adkim, aspf, p, pct)
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()

		self.policy_fk = self.cursor.lastrowid

	def get_records(self):
		"""Extract the DMARC records as defined here: 
		http://www.dmarc.org/draft-dmarc-base-00-02.txt in Appendix C
		If no data is found, return NA
		"""
		container = self.doc.findall("record")
		for elem in container:
			source_ip = elem.findtext("row/source_ip", default="NA")
			count = elem.findtext("row/count", default="NA")
			count = int(count)
			disposition = elem.findtext("row/policy_evaluated/disposition", default="NA")
			dkim = elem.findtext("row/policy_evaluated/dkim", default="NA")
			spf = elem.findtext("row/policy_evaluated/spf", default="NA")
			type = elem.findtext("row/policy_evaluated/reason/type", default="NA")
			comment = elem.findtext("row/policy_evaluated/reason/comment", default="NA")
			header_from = elem.findtext("identifiers/header_from", default="NA")
			dkim_domain = elem.findtext("auth_results/dkim/domain", default="NA")
			dkim_result = elem.findtext("auth_results/dkim/result", default="NA")
			dkim_hresult = elem.findtext("auth_results/dkim/human_result", default="NA")
			spf_domain = elem.findtext("auth_results/spf/domain", default="NA")
			spf_result = elem.findtext("auth_results/spf/result", default="NA")
			
			sql = """INSERT INTO records(source_ip, count, disposition, dkim, spf, type, comment, header_from, dkim_domain, dkim_result, dkim_hresult, spf_domain, spf_result, metadata_fk, published_fk) 
						VALUES("%s", %d, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %d, %d)""" %(source_ip, count, disposition, dkim, spf, type, comment, header_from, dkim_domain, dkim_result, dkim_hresult, spf_domain, spf_result, self.metadata_fk, self.policy_fk)
			try:
				self.cursor.execute(sql)
				self.db.commit()
			except:
				self.db.rollback()
			
		self.db.close()