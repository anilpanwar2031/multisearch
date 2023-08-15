def main(data):

    if data["RcmEobClaimMaster"][0].get('HealthCareClaimStatusCategoryCode') == "" and data["RcmEobClaimMaster"][
        0].get('DateClaimReceived') == "" and data["RcmEobClaimMaster"][0].get('HealthCareClaimStatusCode') == "" and \
            data["RcmEobClaimMaster"][0].get('Checks') == "" and data["RcmEobClaimMaster"][0].get(
            'TotalPaymentAmount') == "":
        del data["RcmEobClaimMaster"][0]['url']

    m = len(data["RcmEobClaimDetail"])
    if data["RcmEobClaimDetail"][0].get('url'):
        data["RcmEobClaimMaster"][0]['url'] = data["RcmEobClaimDetail"][0].get('url')
        del data["RcmEobClaimDetail"][0]['url']

    Status = None
    if data["RcmEobClaimDetail"][m - 1].get('Status') == 'Pending COB':
        Status = True
    else:
        Status = False

    if Status == True:
        data["RcmEobClaimDetail"] = []
    else:
        del data["RcmEobClaimDetail"][m - 1]

    if Status == False:
        n = len(data["RcmEobClaimDetail"])
        for obj in range(n):
            if data["RcmEobClaimDetail"][obj].get("PaymentAmount"):
                data["RcmEobClaimDetail"][obj]["PaymentAmount"] = data["RcmEobClaimDetail"][obj].get("PaymentAmount").split(" ")
                data["RcmEobClaimDetail"][obj]["PaymentAmount"] = data["RcmEobClaimDetail"][obj]["PaymentAmount"][0]
                if data["RcmEobClaimDetail"][obj]["RejectCode"] != "--":
                    RejectCode = data["RcmEobClaimDetail"][obj]["RejectCode"].split(" ", 1)
                    data["RcmEobClaimDetail"][obj]["RejectCode"] = RejectCode[0]
                    if len(RejectCode) > 1:
                        data["RcmEobClaimDetail"][obj]["RejectCodeDescription"] = RejectCode[1]
                    else:
                        data["RcmEobClaimDetail"][obj]["RejectCodeDescription"] = RejectCode[0]

    return data