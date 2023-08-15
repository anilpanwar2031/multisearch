import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from FileDownload import Downloader
import random, string
from Utilities.pdf_utils import get_data_in_format

def main(data):

    if data["RcmEobClaimMaster"][0].get("url"):
        claim = data["RcmEobClaimMaster"][0].get("Claim")
        format_claim = claim.split("(")
        data["RcmEobClaimMaster"][0]["Claim"] = format_claim[0].strip()
        status = data["RcmEobClaimMaster"][0].get("Status")
        format_status = status.replace("(", "").replace(")", "")
        data["RcmEobClaimMaster"][0]["Status"] = format_status
        Provider = data["RcmEobClaimMaster"][0].get("Provider")
        format_Provider = Provider.split(",")
        data["RcmEobClaimMaster"][0]["Provider"] = (format_Provider[1].strip() + " " + format_Provider[0])

        if data["RcmEobClaimDetail"]:
            del data["RcmEobClaimDetail"][0]
        data["RcmEobClaimDetail"] = []

        file_path = ("".join(random.choices(string.ascii_uppercase + string.digits, k=12)) + ".pdf")
        print("file_path>>>>>>>>>>>>>>", file_path)
        input_file = data["RcmEobClaimMaster"][0].get("url").replace("%20", " ")
        print("input_file>>>>>>>>>>>>>>", input_file)
        Downloader("Revenue Cycle Management", file_path, input_file)
        dict_list, work_dict = get_data_in_format(file_path)

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

        print("Unique Adjustments:", unique_adjustments)
        search_index1 = None
        search_index2 = None
        for i, key in enumerate(work_dict['elements']):
            text = key['Text']
            if 'MESSAGE CODE EXPLANATION:' in text:
                search_index1 = i
            elif any(code in text for code in unique_adjustments):
                search_index2 = i
        messages = ''
        if search_index1 is not None and search_index2 is not None:
            text_elements = work_dict['elements'][search_index1 + 1:search_index2 + 1]
            messages = ' '.join(elem['Text'] for elem in text_elements)
        # print("messages>>>>>>>>>>>>>\n", messages)
        data["RcmEobClaimMaster"][0]["Notes"] = messages

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

        temp_lst1 = []
        for i in range(len(temp_lst)):
            if type(temp_lst[i]["columns2"]) == str:
                temp_lst1.append(temp_lst[i])

        new_lst = []
        for obj in temp_lst1:
            obj.items()
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

        tList = []
        for i in new_lst:
            if i.get('DateOfService') != "":
                tList.append(i)

        for i in tList:
            data["RcmEobClaimDetail"].append(i)
    else:
        if data["RcmEobClaimMaster"][0].get("Claim") != "" and data["RcmEobClaimMaster"][0].get("Status") != "" and data["RcmEobClaimMaster"][0].get("Provider") != "":
            claim = data["RcmEobClaimMaster"][0].get("Claim")
            format_claim = claim.split("(")
            data["RcmEobClaimMaster"][0]["Claim"] = format_claim[0].strip()
            status = data["RcmEobClaimMaster"][0].get("Status")
            format_status = status.replace("(", "").replace(")", "")
            data["RcmEobClaimMaster"][0]["Status"] = format_status
            Provider = data["RcmEobClaimMaster"][0].get("Provider")
            format_Provider = Provider.split(",")
            data["RcmEobClaimMaster"][0]["Provider"] = f"{format_Provider[1].strip()} {format_Provider[0]}"

            data["RcmEobClaimDetail"] = [obj for obj in data["RcmEobClaimDetail"] if obj.get("ProcedureDescription") is not None]

    return data