import sys
from pdfFormator import Processor
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from FileDownload import Downloader
import random, string
def remove_extra_spaces(list_of_dicts):
    cleaned_list = []
    for dictionary in list_of_dicts:
        cleaned_dict = {}
        for key, value in dictionary.items():
            cleaned_key = key.strip()
            cleaned_dict[cleaned_key] = value
        cleaned_list.append(cleaned_dict)
    return cleaned_list

def main(data):
    if data.get("RcmEobClaimMaster"):
        if len(data.get("RcmEobClaimMaster")):
            if not data.get("RcmEobClaimMaster")[0].get("url",False):
                data["RcmEobClaimDetail"]   =  []
                return data

    file_path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdf"
    print(file_path)
    input_file = data["RcmEobClaimMaster"][0]["url"].replace("%20", " ")
    print("input_file>>>>>>>>>>>>>>", input_file)
    Downloader('Revenue Cycle Management', file_path, input_file)
    processsor = Processor(file_path)
    output_zip = processsor.zip_processor()
    # print("output_zip>>>>>>>>>>>>>>>>>>>>", output_zip)
    dict_list = processsor.dfGetter(output_zip)
    print("output_zip>>>>>>>>>>>>>>>>>>>>", dict_list[3].columns)

    lst = []
    temp_lst = []
    for ind, tab in enumerate(dict_list):
        if any('Benefit summary' in col for col in tab.columns):
            new_columns_name = {}
            for i in range(len(tab.columns)):
                old_name = tab.columns[i]
                new_name = f'columns{i + 1}'
                new_columns_name[old_name] = new_name
                tab = tab.rename(columns=new_columns_name)
            lst.append(tab.to_dict('records'))
    # print(lst)

    new_lst = []
    for obj in lst:
        new_dict = {}
        for d in obj:
            if 'Total charges submitted:' in d.get('columns1', ''):
                new_dict['Totalchargessubmitted:'] = d.get('columns2', '')
                new_lst.append(new_dict)
            elif 'Total benefits paid:' in d.get('columns1', ''):
                new_dict['Totalbenefitspaid:'] = d.get('columns2', '')
                new_lst.append(new_dict)
            elif 'Provider non-billable amount:' in d.get('columns1', ''):
                new_dict['Providernonbillableamount:'] = d.get('columns2', '')
                new_lst.append(new_dict)
            elif 'Patient responsibility:' in d.get('columns1', ''):
                new_dict['Patientresponsibility:'] = d.get('columns2', '')
                new_lst.append(new_dict)
            # break  # append only the first dictionary in the list

    for i in range(len(data['RcmEobClaimMaster'])):
        if data['RcmEobClaimMaster'][i]['url']:
            data['RcmEobClaimMaster'][i].update(new_lst[0])
            break

    new_lst = []
    for ind, tab in enumerate(dict_list):
        if any('Comments' in col for col in tab.columns):
            lst.append(tab.to_dict('records'))
            # print(tab.to_dict('records'))
    for tab in dict_list:
        if any('Comments' in col for col in tab.columns):
            for d in tab.to_dict('records')[1:]:
                # print(d)
                new_dict = {
                    'Notes': d['Unnamed: 1']
                }
                new_lst.append(new_dict)

    for i in range(len(data['RcmEobClaimMaster'])):
        if data['RcmEobClaimMaster'][i]['url']:
            # data['RcmEobClaimMaster'][i].update(new_lst[0])
            data['RcmEobClaimMaster'][i].update({"Notes": ""})
            break

    desired_columns = ['Item no. ', 'Date of service ', 'ADA code ', 'Description of service ',
                       'Qty ', 'Tooth no. / area ', 'Charge submitted ', 'Code allowance ',
                       'Deductible ', '% Plan pays ', 'Provider non-billable ',
                       'Patient responsibility ', 'Benefit paid ']

    if 'RcmEobClaimDetail' not in data:
        data['RcmEobClaimDetail'] = []

    for df in dict_list:
        if all(col in df.columns for col in desired_columns):
            df.columns = ['Item no. ', 'Dateofservice ', 'ADAcode ', 'Descriptionofservice ',
                          'Qty', 'Toothnoarea', 'Chargesubmitted ', 'Codeallowance ',
                          'Deductible', 'PercentagePlanpays ', 'Providernonbillable ',
                          'Patientresponsibility ', 'Benefitpaid ']
            df.fillna('', inplace=True)
            data['RcmEobClaimDetail'].append(df.to_dict('records'))
    data['RcmEobClaimDetail'] = data['RcmEobClaimDetail'][0]

    data['RcmEobClaimDetail'] = [{k: v for k, v in d.items() if k != 'Item no. '} for d in data['RcmEobClaimDetail']]
    
    data["RcmEobClaimDetail"]   =  remove_extra_spaces(data["RcmEobClaimDetail"])        
    return data