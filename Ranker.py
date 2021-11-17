import pandas as pd
import numpy as np

def create_rank(medical_headers, medical_service_lines, icd9_proc, colonoscopy_codes, resection_codes):
  icd9_proc_col = []
  for i in range(1,16):
    icd9_proc_col.append('P' + str(i))
    icd9_proc_col
  df_icd9_proc = medical_headers[(medical_headers[icd9_proc_col] == icd9_proc).any(axis = 1)].merge(medical_service_lines[medical_service_lines['procedure'].isin(colonoscopy_codes)], on='encounter_key', how = 'left')
  df = medical_headers.merge(medical_service_lines[medical_service_lines['procedure'].isin(colonoscopy_codes)], on='encounter_key')
  df = pd.concat([df, df_icd9_proc])
  df2 = df.merge(medical_service_lines[medical_service_lines['procedure'].isin(resection_codes)], on='encounter_key', how = 'left')
  df3 = df2[df2[icd9_proc_col].apply(lambda x: x.str.contains("^45.8|^45.7")).any(axis = 1)]
  df3['procedure_y'][pd.isna(df3['procedure_y'])] = '44110'
  df4 = df2[~df2[icd9_proc_col].apply(lambda x: x.str.contains("^45.8|^45.7")).any(axis = 1)]
  df_final = pd.concat([df3, df4])
  temp1 = pd.DataFrame(df_final.groupby('doctor_id')['encounter_key'].nunique())
  temp2 = df2.groupby('doctor_id')['procedure_y'].apply(lambda x: (x.isin(resection_codes) ).sum()).reset_index(name='num_resections')
  temp3 = temp1.merge(temp2, on = 'doctor_id')
  temp3['violation_rate'] = temp3['num_resections'] / temp3['encounter_key']
  return(temp3.sort_values(by = 'encounter_key',  ascending= False)).rename(columns = {"encounter_key":"num_benign_tumors"})