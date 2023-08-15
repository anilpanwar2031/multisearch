import json

def main(data,request):
  patientdata = request['PatientData'][0]


  for key in data["RcmEobClaimDetail"]:
    for item_key, item_value in key.items():
      if isinstance(item_value, str) and "$ " in item_value:
        key[item_key] = item_value.replace(' ', '').strip()

  

  for k, v in data['RcmEobClaimMaster'][0].items():
    if ":\n" in v:
      val = v.split(":\n")
      val = val(1)
      data['RcmEobClaimMaster'][0][k] = val.strip()



  patient_data = request['PatientData']
  first_names = [patient['FirstName'] for patient in patient_data]
  last_names = [patient['LastName'] for patient in patient_data]
 

  for d in data["RcmEobClaimMaster"]:
    is_process = "Claim Status" in d and d["Claim Status"] == "In Process" and "Member" in d
    
    if is_process:
       data["RcmEobClaimMaster"] = [d for d in data["RcmEobClaimMaster"] if "Claim Status" in d and d["Claim Status"] == "In Process" and "Member" in d]
    else:
      continue   

    data["RcmEobClaimMaster"][0]["status"] = data["RcmEobClaimMaster"][0].pop("Claim Status")

  return data