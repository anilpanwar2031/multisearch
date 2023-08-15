
def get_claimMaster(data):
    claimmaster = data["RcmEobClaimMaster"][0]
    claimmaster["ClaimNumber"] = claimmaster["ClaimNumber"][1:]
    claimmaster["RcmGridViewId"] = 0

    return claimmaster


def get_claimdetails(data):
    claimdetail = data["RcmEobClaimDetail"]
    for c in claimdetail:
        c['RcmGridViewId'] = 0
    return claimdetail

def main(data):

    claimMaster = [get_claimMaster(data)]
    claimdetails = get_claimdetails(data)


    json_data = {
        'RcmEobClaimMaster': claimMaster,
        'RcmEobClaimDetail': claimdetails,
        'EligibilityFiles': data["EligibilityFiles"]
    }

    return json_data


