import json
def main(data):
    

    for k,v in data['RcmEobClaimMaster'][0].items():
        if ":\n" in v:
            val = v.split(":\n")
            val = val(1)
            data['RcmEobClaimMaster'][0][k] = val

    return data