import json
def main(data):
  for key in data["RcmEobClaimDetail"]:
    for item_key, item_value in key.items():
      if isinstance(item_value, str) and "$ " in item_value:
        key[item_key] = item_value.replace(' ', '').strip()

  

  for k, v in data['RcmEobClaimMaster'][0].items():
    if ":\n" in v:
      val = v.split(":\n")
      val = val(1)
      data['RcmEobClaimMaster'][0][k] = val.strip()

  return data

