import pandas as pd
import numpy as numpy
import sqlite3

from SQL_Query import Create_SQL_Query_Medical_Headers
from SQL_Query import Create_SQL_Query_Medical_Service_Lines
from SQL_Query import load_db

dbfile = '/content/drive/MyDrive/Garner Health Project/claims.db'
# dbfile = '[DBFILE HERE]'

diag_codes = ['211.3', '211.4']
# diag_codes = [CODES HERE]
exclusion_codes = ['152']
# exclusion_codes = [CODES HERE]

resection_codes = ['44110','44146', '44150', '44151', '44152', '44153', '44154', '44155', '44156', '44157', '44158', '44159', '44204', '44205', '44206', '44207', '44208', '44210', '44211', '44212']
colonoscopy_codes = ['45378','45380','45381', '45382', '45383', '45384', '45385', '45388']

cpt_codes = colonoscopy_codes + resection_codes
# cpt_codes = [CODES HERE]

query = Create_SQL_Query(diag_codes= diag_codes, exclusion_codes=exclusion_codes)
query2 = query2 = Create_SQL_Query_Medical_Service_Lines(cpt_codes=cpt_codes)

medical_headers = load_db(dbfile, query)
medical_service_lines = load_db(dbfile, query2)

output = create_rank(medical_headers, medical_service_lines, '45.23', colonoscopy_codes, resection_codes)

return(output)