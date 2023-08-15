import json
def main(data):

  data["RcmEobClaimDetail"] = [item for item in data["RcmEobClaimDetail"] if item["Description"] is not None]
  print(data["RcmEobClaimDetail"])

  for key in data["RcmEobClaimDetail"]:
    for item_key, item_value in key.items():
      if isinstance(item_value, str) and "$ " in item_value:
        key[item_key] = item_value.replace(' ', '').strip()
  for obj in data["RcmEobClaimDetail"]:
    if obj.get("TTH"):
      obj["Tooth"] = obj.pop("TTH")

  

  return data



