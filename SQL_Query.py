import sqlite3

def Create_SQL_Query_Medical_Headers(diag_codes = [],  exclusion_codes = []):
  medical_headers_query = "SELECT * FROM medical_headers WHERE ("
  temp = "("
  for x in diag_codes:
    temp = temp + "'" + x + "'" + ',' 
  temp = temp[:-1] + ")"
  icd9_col = ['DA']
  for i in range(1,26):
    icd9_col.append('D' + str(i))
  temp2 = []
  for x in icd9_col:
    temp2.append( x + " IN " + temp + " OR ")
  for x in temp2:
    medical_headers_query = medical_headers_query + x
  medical_headers_query = medical_headers_query[:-4]

  temp = "'"
  for x in exclusion_codes:
    temp = temp + x + ".%'"
  temp3 = []
  for x in icd9_col:
    temp3.append(x + " NOT LIKE " + temp + " AND ")
  medical_headers_query = medical_headers_query + ")" + " AND "
  for x in temp3:
    medical_headers_query = medical_headers_query + x
  medical_headers_query = medical_headers_query[:-4]

  return(medical_headers_query)

  def Create_SQL_Query_Medical_Service_Lines(cpt_codes = []):
  medical_service_lines_query = "SELECT * FROM medical_service_lines WHERE PROCEDURE IN "
  temp = "("
  for x in cpt_codes:
    temp = temp + "'" + x + "'" + ","
  temp = temp[:-1] + ")"
  medical_service_lines_query = medical_service_lines_query + temp
  return(medical_service_lines_query)


def load_db(dbfile, query):
  con = sqlite3.connect(dbfile)
  return(pd.read_sql_query(query, con))