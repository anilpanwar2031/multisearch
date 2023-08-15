import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from FileDownload import Downloader
import random, string
import json
from PyPDF2 import PdfReader
from Utilities.pdf_utils import get_data_in_format, find_item



def main(data):
    print("wrapper initiated")

    data["RcmEobClaimMaster"][0]['Status'] = data["RcmEobClaimMaster"][0].get("Claim").split('(')[-1]

    if data["RcmEobClaimMaster"][0].get("Claim"):
        claim = data["RcmEobClaimMaster"][0].get("Claim")
        format_claim = claim.split("(")
        data["RcmEobClaimMaster"][0]["Claim"] = format_claim[0].strip()

    if data["RcmEobClaimMaster"][0].get("Status"):
        status = data["RcmEobClaimMaster"][0].get("Status")
        format_status = status.replace("(", "").replace(")", "")
        data["RcmEobClaimMaster"][0]["Status"] = format_status
        print(format_status)

    if data["RcmEobClaimMaster"][0].get("Provider"):
        Provider = data["RcmEobClaimMaster"][0].get("Provider")
        format_Provider = Provider.split(",")
        data["RcmEobClaimMaster"][0]["Provider"] = (format_Provider[1].strip() + " " + format_Provider[0])

    if not (data["RcmEobClaimMaster"][0]['Status'].lower() == 'paid'):
        return data

    file_path = ("".join(random.choices(string.ascii_uppercase + string.digits, k=12)) + ".pdf")
    # file_path = "ddVirginia12.pdf"
    input_file = data["RcmEobClaimMaster"][0]["url"].replace("%20", " ")
    print("input_file>>>>>>>>>>>>>>", input_file)
    Downloader("Revenue Cycle Management", file_path, input_file)
    
    dict_list, work_dict = get_data_in_format(file_path)

    # print("dict_list>>>>>>>>>>>>>>>>>>>>>",dict_list)

    unique_adjustments = set()

    for df in dict_list:
        df.fillna("", inplace=True)
        for col_name in ["Unnamed: 11"]:

            if col_name in df.columns:
                unique_values = set(df[col_name].str.strip().unique())
                translation_table = str.maketrans('', '', '[]')
                unique_values = {val.translate(translation_table) for val in unique_values if
                                 val not in ["", '[]', "MESSAGE CODE(S)"]}
                if col_name == "Unnamed: 11":
                    unique_adjustments.update(unique_values)
    lst = []
    for ind, tab in enumerate(dict_list):
        if any("PAYMENT DATE" in col for col in tab.columns):
            new_columns_name = {}
            for i in range(len(tab.columns)):
                old_name = tab.columns[i]
                new_name = f"columns{i + 1}"
                new_columns_name[old_name] = new_name
                tab = tab.rename(columns=new_columns_name)
            lst.append(tab.to_dict("records"))

    temp_lst = []
    for i in range(len(lst)):
        for obj in lst[i]:
            if (
                    "PPO CLAIM NO. " not in obj.values()
                    and "TOTALS " not in obj.values()
                    and "TOOTH or CAVITY " not in obj.values()
                    and "columns2" != None
            ):
                temp_lst.append(obj)
    # print("temp_lst>>>>>>>>>>>>>>1", temp_lst)
    temp_lst1 = []
    for i in range(len(temp_lst)):
        if type(temp_lst[i]["columns2"]) == str:
            temp_lst1.append(temp_lst[i])

    # print("temp_lst1>>>>>>>>>>>>>>1", temp_lst1)

    new_lst = []
    for obj in temp_lst1:
        obj.items()
        if obj["columns2"] != "":
            new_dict = {
                "ToothOrCavity": obj["columns1"],
                "DateOfService": str(obj["columns2"]).replace("nan", ""),
                "ProcedureDescription": obj["columns3"],
                "SubmittedAmount": obj["columns4"],
                "ContractAllowance": obj["columns5"],
                "PlanAllowance": obj["columns6"],
                "Deductible": obj["columns7"],
                "MemberCoins": str(obj["columns9"]).replace("nan", ""),
                "WhatWeWillPay": obj["columns10"],
                "WhatYouOwe": obj["columns11"],
                "MessageCode": obj["columns12"],
            }
            new_lst.append(new_dict)
        else:
            new_dict = {
                "ToothOrCavity": str(obj["columns2"]),
                "DateOfService": str(obj["columns1"]),
                "ProcedureDescription": obj["columns3"],
                "SubmittedAmount": obj["columns4"],
                "ContractAllowance": obj["columns5"],
                "PlanAllowance": obj["columns6"],
                "Deductible": obj["columns7"],
                "MemberCoins": str(obj["columns9"]).replace("nan", ""),
                "WhatWeWillPay": obj["columns10"],
                "WhatYouOwe": obj["columns11"],
                "MessageCode": obj["columns12"],
            }
            new_lst.append(new_dict)

    # print("new_lst>>>>>>>>>>>>>>1", new_lst)
    tList = []
    for i in new_lst:
        if i.get('DateOfService') != "" and "$" in i.get("SubmittedAmount"):
            tList.append(i)
    # print("tList>>>>>>>>>>>>>>>>",tList)

    pdf_list = []
    for i in tList:

        # data["RcmEobClaimDetail"].append(i)
        pdf_list.append(i)
    
    for index, item in enumerate(pdf_list):
        data["RcmEobClaimDetail"][index].update(item)
    
    del data["RcmEobClaimDetail"][-1]

    ################# master data #####################

    # reader = PdfReader(os.path.join("wrapers", "virginiapdfs", "virginiapdfs", "ddVirginia7.pdf"))
    reader = PdfReader(file_path)
    page = reader.pages[0]
    summary = page.extract_text().split("\n")
    # print(summary)
    
    # print("messages>>>>>>>>>>>>>\n", messages)
    # data["RcmEobClaimMaster"][0]["Notes"] = messages
    data["RcmEobClaimMaster"][0]["OrthodontiaPaid"] = summary[-6]
    data["RcmEobClaimMaster"][0]["MaximumUtilized"] = summary[-2]
    data["RcmEobClaimMaster"][0]["DeductibleSatiesfied"] = summary[-3]
    data["RcmEobClaimMaster"][0]["TotalPayment"] = summary[-9]
    data["RcmEobClaimMaster"][0]["PatientResponsibility"] = summary[-8]

    # data["RcmEobClaimDetail"] = list(
    #     {json.dumps(obj, sort_keys=True): obj for obj in data["RcmEobClaimDetail"]}.values())
    
    claim_detail = []
    for item in data["RcmEobClaimDetail"]:
        item["ProcedureCode"] = item[1]
        item["ProcedureDescription"] = item[2]
        del item[1]
        del item[2]
        del item[0]
        del item[3]
        del item[4]
        claim_detail .append(item)
    data["RcmEobClaimDetail"] = claim_detail
    
    return data

#     with open("newJson.json", "w") as jsonFile:
#         json.dump(data, jsonFile, indent=4)


# with open("output.json", "r") as jsonFile:
#     data = json.load(jsonFile)
# main(data)