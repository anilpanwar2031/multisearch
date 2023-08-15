def main(data):

    print(data["RcmEobClaimMaster"][0]["ClaimNumber"])
    data["RcmEobClaimMaster"][0]["PatientName"] = data["RcmEobClaimMaster"][0]["PatientName"].split(":")[1].strip()
    data["RcmEobClaimMaster"][0]["DateOfService"] = data["RcmEobClaimMaster"][0]["DateOfService"].split(":")[1].strip()
    data["RcmEobClaimMaster"][0]["NetworkStatus"] = data["RcmEobClaimMaster"][0]["NetworkStatus"].split(":")[1].strip()
    data["RcmEobClaimMaster"][0]["ClaimNumber"] = data["RcmEobClaimMaster"][0]["ClaimNumber"].split(":")[1].strip()
    # print(data["RcmEobClaimMaster"][0]["ClaimNumber"])

    claim_details = []
    claim_item = {}

    for key, value in data["RcmEobClaimDetail"][0].items():

      if "ProviderName" in key:
          if value != "":

            claim_item["ProviderName"] = value

      elif "ProviderTaxId" in key:
          if value != "":

            claim_item["ProviderTaxId"] = value

      elif "DateOfService" in key:
          if value != "":

            claim_item["DateOfService"] = value

      elif "ProcedureCode" in key:
          if value != "":

            claim_item["ProcedureCode"] = value

      elif "Occurance" in key:
          if value != "":

            claim_item["Occurance"] = value

      elif "PaymentDate" in key:
          if value != "":

            claim_item["PaymentDate"] = value

      elif "PaymentMadeTo" in key:
          if value != "":

            claim_item["PaymentMadeTo"] = value

      elif "CheckNumber" in key:
          if value != "":

            claim_item["CheckNumber"] = value

      elif "AmountBilled" in key:
          if value != "":

            claim_item["AmountBilled"] = value

      elif "ProviderDiscount" in key:
          if value != "":

            claim_item["ProviderDiscount"] = value

      elif "AllowableAmount" in key:
          if value != "":

            claim_item["AllowableAmount"] = value

      elif "AmountNotPayable" in key:
          if value != "":

            claim_item["AmountNotPayable"] = value

      elif "Deductible" in key:
          if value != "":

            claim_item["Deductible"] = value

      elif "BenefitPercentagePaidByPlan" in key:
          if value != "":

            claim_item["BenefitPercentagePaidByPlan"] = value

      elif "OtherInsurancePaid" in key:
          if value != "":

            claim_item["OtherInsurancePaid"] = value

      elif "AmountPaidByPlan" in key:
          if value != "":

            claim_item["AmountPaidByPlan"] = value

      elif "WithholdAmount" in key:
          if value != "":

            claim_item["WithholdAmount"] = value

      elif "CopayAmount" in key:
          if value != "":

            claim_item["CopayAmount"] = value

      elif "YouPay" in key:
          if value != "":

            claim_item["YouPay"] = value

            claim_details.append(claim_item)

            claim_item = {}

    del data["RcmEobClaimDetail"][0]
    data["RcmEobClaimDetail"] = []

    for i in claim_details:
        data["RcmEobClaimDetail"].append(i)

    # for i, claim in enumerate(data["RcmEobClaimDetail"], start=1):
    #     claim["RecordID"] = i

    return data