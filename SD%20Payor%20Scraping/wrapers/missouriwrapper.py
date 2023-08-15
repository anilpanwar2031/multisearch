import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from Utilities.pdf_utils import *
from FileDownload import Downloader
from mapPDF import mapEligibilityPatientVerification
from PyPDF2 import PdfReader
from datetime import datetime
import pandas as pd
import re
from collections import defaultdict
import tabula
import numpy as np


def changeNone(text):
    if(text=="None" or text=="N/A" or text==None):
        return ""
    else:
        return text
def calculate_difference(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    difference=f'${float(a)-float(b)}'
    if(difference=="$0.00"): return "0.00"
    return f'${round(float(a)-float(b) , 2)}'
def getsum(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)+float(b)}'


def is_date_format(value, pattern):
    return bool(re.match(pattern, str(value)))

def get_age_details(text):
    
    # return age_detaildef get_age_details(text):
    dependent_children_covered = ''
    if 'Dependent Children Covered:' in text:
        dependent_children_covered = text.split('Dependent Children Covered:')[1]
        if 'Full Time Students Covered:' in dependent_children_covered:
            dependent_children_covered = dependent_children_covered.split('Full Time Students Covered:')[0]
        else:
            dependent_children_covered = dependent_children_covered.split('\r')[0]
            
    full_time_student_covered = ''
    if 'Full Time Students Covered:' in text:
        full_time_student_covered = text.split('Full Time Students Covered:')[1]
        if 'Qualifying Children Covered:' in full_time_student_covered:
            full_time_student_covered = full_time_student_covered.split('Qualifying Children Covered:')[0]
        else:
            full_time_student_covered = full_time_student_covered.split('\r')[0]
    
    qualifying_children_covered = ''
    if 'Qualifying Children Covered:' in text:
        qualifying_children_covered = text.split('Qualifying Children Covered:')[1]
        if 'Orthodontic Age Limit:' in qualifying_children_covered:
            qualifying_children_covered = qualifying_children_covered.split('Orthodontic Age Limit:')[0]
        else:
            qualifying_children_covered = qualifying_children_covered.split('\r')[0]
    
    orthodentgic_age_limit = ''
    if 'Orthodontic Age Limit:' in text:
        orthodentgic_age_limit = text.split('Orthodontic Age Limit:')[1]
        if 'Other Information Where Applicable' in orthodentgic_age_limit:
            orthodentgic_age_limit = orthodentgic_age_limit.split('Other Information Where Applicable')[0]
        else:
            orthodentgic_age_limit = orthodentgic_age_limit.split('\r')[0]
    
    age_detail = {
        'DependentChildrenCovered': dependent_children_covered.strip('\n').strip('\r'),
        'FullTimeStudentsCovered': full_time_student_covered.strip('\n').strip('\r'),
        'QualifyingChildrenCovered': qualifying_children_covered.strip('\n').strip('\r'),
        'OrthodonticAgeLimit': orthodentgic_age_limit.strip('\n').strip('\r')
    }
    
    return age_detail

def get_df_from_tabula_for_benefit_coverage_details(file_path):
    data_context_dict = []
    key = [i for i in range(1, 20)]
    options = {"lattice": True, "guess": True, "encoding": "ISO-8859-1"}

    df_list = tabula.read_pdf(
        file_path, **options, pages="all", pandas_options={'header': key})
    data_frames = [data_frame for data_frame in df_list if len(data_frame.columns) == 7]

    concatenated_df = pd.concat(data_frames)
    concatenated_df = concatenated_df.reset_index(drop=True)

    third_table_headers = ['Procedure',
                           'Delta Dental PPO',
                           'Delta Dental\rPremier',
                           'Non Par Dentist',
                           'Frequency if\rApplicable',
                           'Age Limit if\rApplicable',
                           'Limitations / Notes\rif Applicable - See\rCode List']
    alternate_third_index = ['Procedure',
                             'Delta Dental PPO',
                             'Delta Dental\rPremier (Allowed\rAmount based on\rPPO Schedule)',
                             'Non Par Dentist',
                             'Frequency if\rApplicable',
                             'Age Limit if\rApplicable',
                             'Limitations / Notes\rif Applicable - See\rCode List']
    fourth_table_headers = [np.nan,
                            'Individual Annual\rDeductible Met\rPPO Network',
                            'Individual Annual\rDeductible Met\rPremier Network',
                            'Individual Annual\rDeductible Met\rNon Par',
                            'Individual Annual\rMaximum Met\rPPO Network',
                            'Individual Annual\rMaximum Met\rPremier Network',
                            'Individual Annual\rMaximum Met Non\rPar']

    first_table_row_index = (concatenated_df.isin(third_table_headers)).all(axis=1).idxmax()
    if first_table_row_index == 0:
        first_table_row_index = (concatenated_df.isin(alternate_third_index)).all(axis=1).idxmax()

    # Find the index of the row that matches all values in the second table headers
    second_table_row_index = (concatenated_df.isin(fourth_table_headers)).all(axis=1).idxmax()

    # Check if first table row index is the same as the second table row index
    if first_table_row_index == second_table_row_index:
        # Find the next occurrence of the second table headers after the first table headers
        second_table_row_index = (concatenated_df.loc[first_table_row_index:, :].isin(fourth_table_headers)).all(
            axis=1).idxmax()

    # Create a new DataFrame containing the rows from the first table header row to the second table header row
    new_df = concatenated_df.loc[first_table_row_index:second_table_row_index - 1].copy()
    new_df.fillna("", inplace=True)

    new_df.columns = new_df.iloc[0]
    # print(new_df.columns)

    for j, row in new_df.iterrows():
        if all([str(val).strip().replace(".", "").lower()
                == str(col).strip().replace(".", "").lower()
                for val, col in zip(row, new_df.columns)]):
            new_df.drop(j, inplace=True)

    new_df.columns = ['Procedure', 'DeltaDentalPPO', 'DeltadentalPremier', 'Nonpardentist', 'Frequency',
                      'Agelimitation',
                      'LimitationORNotes']

    for record in new_df.to_dict('records'):
        data_context_dict.append(record)

    return data_context_dict
 

def extract_codes(filename):
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)
    data =[reader.pages[page].extract_text() for page in range(number_of_pages) if "Limitation Code List"][0]
    data = []
    for page in range(number_of_pages):    
        text = reader.pages[page].extract_text()
        data.append(text)
        tot_text = ''.join(data)
        if "Limitation Code List" in tot_text:
            tot_text =tot_text.split("Limitation Code List")[1]
        if "Individual Annual" in tot_text:
            tot_text =tot_text.split("Individual Annual")[0]
        numbers =range(1,21)
        tot_text =tot_text.split("\n") 
        # print(tot_text) 

        formatted_data = {}
        for item in tot_text[:]:
            match = re.search(r'Page \d+ of \d+', item)
            if match:
                tot_text.remove(item)
        key = None  
        for item in tot_text:
            match = re.search(r'Page \d+ of \d+', item)
            if match:
                item.replace(match.group(),'')
            item = item.strip('.')
            if item.isdigit():
                key = item
                formatted_data[key] = None
            elif key is not None:
                if formatted_data[key] is None:
                    formatted_data[key] = item
                else:
                    formatted_data[key] += ' ' + item

        formatted_data = {k: v for k, v in formatted_data.items() if v is not None} 
        # print(formatted_data)

        
    age_details = get_age_details(tot_text)
    return formatted_data , age_details

def get_eligibility_benefits(df_list):
    eligibility_benefits = []

    benefit_columns = ['Date of Service', 'Tooth', 'Surface', 'Procedure', 'Description']
    benefit_columns_updated = ['Dateofservice', 'Tooth', 'Surface', 'Procedure', 'Description']
    benefit_columns_six_element = ['Dateofservice', 'Tooth', 'name', 'Surface', 'Procedure', 'Description', 'No']

    for df in df_list:
        if all(col in df.columns for col in benefit_columns):
            df.columns = benefit_columns_updated
            df.fillna('', inplace=True)
            eligibility_benefits.extend(df.to_dict('records'))
        elif len(df.columns) <= 5:
            first_column = df.iloc[:, 0].astype(str).str.strip()  # Selecting the first column and removing whitespaces
            if pd.notnull(first_column.at[0]):
                first_value = first_column.at[0].strip()
                is_date_format = False

                if first_value:
                    if re.match(r"\d{1,2}[/|-]\d{1,2}[/|-]\d{2,4}", first_value):
                        is_date_format = True
                    elif re.match(r"\d{1,2}\s+\w{3}\s+\d{2,4}", first_value):
                        is_date_format = True

                if is_date_format:
                    if len(df.columns) == 5:
                        df.columns = benefit_columns_updated
                    elif len(df.columns) == 4:
                        df.loc[len(df)] = df.columns
                        df['Surface'] = ''
                        df.columns = benefit_columns_updated

                    df.fillna('', inplace=True)
                    eligibility_benefits.extend(df.to_dict('records'))
        elif len(df.columns) <= 7:
            first_column = df.iloc[:, 0].astype(str).str.strip()  # Selecting the first column and removing whitespaces
            if pd.notnull(first_column.at[0]):
                first_value = first_column.at[0].strip()
                is_date_format = False

                if first_value:
                    if re.match(r"\d{1,2}[/|-]\d{1,2}[/|-]\d{2,4}", first_value):
                        is_date_format = True
                    elif re.match(r"\d{1,2}\s+\w{3}\s+\d{2,4}", first_value):
                        is_date_format = True

                if is_date_format:
                    if len(df.columns) == 5:
                        df.columns = benefit_columns_updated
                    elif len(df.columns) == 4:
                        df.loc[len(df)] = df.columns
                        df['Surface'] = ''
                        df.columns = benefit_columns_updated
                    elif len(df.columns) <= 7:
                        df.loc[len(df)] = df.columns
                        df['Surface'] = ''
                        df.columns = benefit_columns_six_element    

                    df.fillna('', inplace=True)
                    eligibility_benefits.extend(df.to_dict('records'))

    # print(eligibility_benefits)
    return eligibility_benefits

    

def PDFScrape(data):

    file_path =''.join(random.choices(string.ascii_uppercase +string.digits, k=10)) + ".pdf"
    print(file_path)

    input_file = data["EligibilityPatientVerification"][0]["url"].replace("%20", " ")
    Downloader('Eligibility',file_path,input_file)
    # file_path ="DDMi_2.pdf"

    data_frames, work_dict = get_data_in_format(file_path)  
    # print(data_frames) 
    
    
    limitationcontent , age_limit = extract_codes(file_path)
    # print(limitationcontent)
    

    def stringify(text):
        if text is not None or text != "":
            if type(text) is not str:
                text = str(text).strip()
            else:
                text = text.strip()
   
    GroupNumber = "" 
    missingtoothcluse = ""   

    for i,item in enumerate(work_dict.get('elements')):
        
        text = item.get('Text')
        if text is not None:
            if 'Mailing Address' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                # print('subtextformailingaddress',sub_text)
                Claimaddress = sub_text.split(':')[1].strip()
                # print(Claimaddress) 

            if 'Print Date' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                printdate = sub_text.split(':')[1].strip()
                # print(printdate)
            if 'Electronic Payer ID' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                electronicpayorid = sub_text.split(':')[-1].strip()
                # print(electronicpayorid)
            if 'Fax' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                Fax = sub_text.split(':')[-1].strip()
                # print(Fax)
            if 'Group Name' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+4]
                # print('sub_ele:- ',sub_ele)
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                # print('sub_text:-', sub_text)
                Groupname = sub_text.split('Group Name:')[1].split('Missing')[0].strip()
                # print('Groupname:-',Groupname)

                if Groupname is not None and 'Program:' in Groupname:
                     Groupname = Groupname.split('Program:')[1].strip()

            
            if 'Group Number' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+8]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                match = re.search(r'Group Number: (\d+)', sub_text)
                if match:
                    GroupNumber = match.group(1)
                
                if GroupNumber == '':
                    if 'Missing tooth' in sub_text:
                        GroupNumber = sub_text.split('apply')[1].split('Delta')[0].strip()
            
                print('GroupNumber:-',GroupNumber)

                if 'Missing tooth clause does not apply' in GroupNumber:
                    GroupNumber = GroupNumber.replace('Missing tooth clause does not apply','')
                

            if 'Program Type' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                Programtype = sub_text.split('Program Type:')[1].split('Benefit')[0].strip()
                # print(Programtype)
            if 'Benefit Cycle' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                benefitcycle = sub_text.split('Benefit Cycle:')[1].split('COB')[0].strip()
                # print(benefitcycle)
            if 'COB Type' in text:
                # print('cobtype:-',text)
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                # print('sub_text :- ',sub_text)
                COBtype = sub_text.split('COB Type:')[1].split('Healthy')[0].strip()
                # print(COBtype)
            if 'Healthy Smiles Healthy Lives Program' in text:
                searchindex = i
                sub_ele = work_dict["elements"][searchindex :searchindex+2]
                sub_text = "".join(elem["Text"] for elem in sub_ele)
                HealthySmilesHealthyLivesProgram = sub_text.split(':')[-1].strip()
                # print(HealthySmilesHealthyLivesProgram)           
          
            # Missing tooth clause applies
            if 'Missing tooth clause does not apply' in text:
                missingtoothcluse = 'Missing tooth clause does not apply'
            elif 'Missing Tooth Clause Applies' in text:  
                missingtoothcluse = 'Missing tooth clause applies'

    # print('groupname :-', GroupNumber)

    data["EligibilityPatientVerification"][0].update(
        {'ClaimAddress': str(Claimaddress).strip(),
         'printdate': str(printdate).strip(),
         'electronicpayorid': str(electronicpayorid).strip(),
         'Fax': str(Fax).strip(),
         'Groupname': str(Groupname).strip(),
         'GroupNumber': str(GroupNumber).strip(),
         'Programtype': str(Programtype).strip(),
         'benefitcycle': str(benefitcycle).strip(),
         'COBtype': str(COBtype).strip(),
         'DependentChildrenCovered': age_limit.get('DependentChildrenCovered'),
         'FullTimeStudentsCovered': age_limit.get('FullTimeStudentsCovered'),
         'QualifyingChildrenCovered': age_limit.get('QualifyingChildrenCovered'),
         'Missingtoothclausedoesnotapply': str(missingtoothcluse).strip()
        }
        )            

   
    
    
    # coverage_benefit_columns =['Typical Coverage Levels Procedure ', 'Delta Dental PPO ', 'Delta Dental Premier (Allowed Amount based on PPO Schedule) ',
    #    'Non Par Dentist ', 'Frequency if Applicable ', 'Age Limit if Applicable ','Limitations / Notes if Applicable - See Code List ']
    
    # coverage_O_benefit_col = ['Typical Coverage Levels Procedure ', 'Delta Dental PPO ',
    #    'Delta Dental Premier ', 'Non Par Dentist ', 'Frequency if Applicable ',
    #    'Age Limit if Applicable ',
    #    'Limitations / Notes if Applicable - See Code List ']
    
    # coverage_column_benefit_col = ['Procedure ', 'Delta Dental PPO ', 'Delta Dental Premier ',
    #    'Non Par Dentist ', 'Frequency if Applicable ',
    #    'Age Limit if Applicable ',
    #    'Limitations / Notes if Applicable - See Code List ']

    Individual_maximum_columns =['Individual Maximums - Per Benefit Period ','Individual PPO Network ','Individual Premier Network ',
        'Individual Non Par ','Individual PPO Network Lifetime ','Individual Premier Network Lifetime ','Individual Non Par Lifetime ']
    
    individual_max_col_2 = ['Unnamed: 0', 'Individual PPO Network ', 'Individual Premier Network ',
       'Individual Non Par ', 'Individual PPO Network Lifetime ',
       'Individual Premier Network Lifetime ', 'Individual Non Par Lifetime ']

    Individual_anuual_columns =['Unnamed: 0','Individual Annual Deductible Met PPO Network ','Individual Annual Deductible Met Premier Network ',
        'Individual Annual Deductible Met Non Par ','Individual Annual Maximum Met PPO Network ','Individual Annual Maximum Met Premier Network ',
        'Individual Annual Maximum Met Non Par ']

    Elig_patient_verification_column =['Name ','Relationship ','Date Of Birth ','Enrollment Effective Date ','Waiting Period End Date ',
                                       'Eligible ']    
    

    if 'EligibilityBenefits' not in data:
        data['EligibilityBenefits'] = []
    if 'EligibilityServiceTreatmentHistory' not in data:
        data['EligibilityServiceTreatmentHistory'] = []
    if 'EligibilityMaximums' not in data:
        data['EligibilityMaximums'] = []  
    if 'EligibilityDeductible' not in data:
        data['EligibilityDeductible'] = []

    data['EligibilityBenefits'] =  get_eligibility_benefits(data_frames)

#  remove if surface contains procedure code 
    for mergeitem in data['EligibilityBenefits']:
        surface = mergeitem["Surface"]
        if len(surface) >= 5 and surface[0] == "D":
            new_procedure = surface[:5]
            new_description = mergeitem["Procedure"]
            mergeitem["Procedure"] = new_procedure
            mergeitem["Description"] = new_description
            mergeitem["Surface"] = ""
    
    # # Print the modified data
    # for item in data['EligibilityBenefits']:
    #     print(item)

    benefitlevelcode = get_df_from_tabula_for_benefit_coverage_details(file_path)
    # print('benefitlevelcode :- ',benefitlevelcode)
   
    
    data['EligibilityServiceTreatmentHistory'].extend(benefitlevelcode)

    for df in data_frames:               

        if all(col in df.columns for col in Individual_maximum_columns):
            df.columns = ['Individualmaximumperbenefitperiod', 'IndividualPPOnetwork', 'IndividualPremiernetwork','IndividualNonpar',
                          'IndividualPPONetworkLifetime','IndividualPremierNetworkLifetime','IndividualNonParLifetime']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityMaximums'].append(record) 
            # print(df.to_dict('records')) 
        elif all(col in df.columns for col in individual_max_col_2):
            df.columns = ['Individualmaximumperbenefitperiod', 'IndividualPPOnetwork', 'IndividualPremiernetwork','IndividualNonpar',
                          'IndividualPPONetworkLifetime','IndividualPremierNetworkLifetime','IndividualNonParLifetime']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityMaximums'].append(record)  

        if all(col in df.columns for col in Individual_anuual_columns):
            df.columns = ['IndividualAnnualperbenefitperiod', 'IndividualAnnualDeductibleMetPPONetwork', 'IndividualAnnualDeductibleMetPremierNetwork','IndividualAnnualDeductibleMetnonpar',
                          'IndividualAnnualMaximumMetPPONetwork','IndividualAnnualMaximumMetPremierNetwork','IndividualAnnualMaximumMetNonpar']
            df.fillna('',inplace=True)
            for record in df.to_dict('records'):
                data['EligibilityDeductible'].append(record) 
            # print(df.to_dict('records'))       

        if all(col in df.columns for col in Elig_patient_verification_column):
            # df.columns = ['PatientName', 'Relationship', 'Date Of Birth','EffectiveDate','TerminationDate','EligibleStatus']
            if len(df.columns) == 6:
                df.columns = ['PatientName', 'Relationship', 'Date Of Birth','EffectiveDate','TerminationDate','EligibleStatus']
            elif len(df.columns) == 7:
                df.columns = ['PatientName', 'Name', 'Relationship', 'Date Of Birth','EffectiveDate', 'TerminationDate', 'EligibleStatus']
            
            df.fillna('',inplace=True)
            # print(df.to_dict('records')) 
            Patients_info = df.to_dict('records')
            # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',Patients_info)
            for patient in Patients_info:
                PatientName = patient.get('PatientName')
                for item in data['EligibilityPatientVerification']:
                    name = item.get('Name')
                    translation_table = str.maketrans('', '', ' -')
                    if PatientName.translate(translation_table)==name.translate(translation_table):
                        # print('Name MAtched',name)
                        item.update({
                        "Relationship": patient.get('Relationship',''),
                        "DateOfBirth": patient.get('Date Of Birth',''),
                        "EffectiveDate": patient.get('EffectiveDate',''),
                        "TerminationDate": patient.get('TerminationDate',''),
                        "EligibleStatus": patient.get('EligibleStatus','')
                        })

    for procedure in data["EligibilityServiceTreatmentHistory"]:
        # limitationcode = procedure["LimitationORNotes"]

        # if limitationcode and type(limitationcode) is not str:
        #     limitationcode = str(limitationcode)
        # # print('pro:- ',procedure)

        if procedure["LimitationORNotes"]:
            
            if not isinstance(procedure["LimitationORNotes"], str):
                procedure["LimitationORNotes"] = str(procedure["LimitationORNotes"])
                print('code:- ',procedure["LimitationORNotes"])

            if "," in procedure["LimitationORNotes"]:               
                codes =procedure["LimitationORNotes"].split(',')                
                codes_dis=""
                for code in codes:
                    codes_dis+=", "+limitationcontent[code.strip()]

                procedure["LimitationORNotes"] = codes_dis.strip(",")

            elif "." in procedure["LimitationORNotes"]:
                c = procedure["LimitationORNotes"].strip() 
                procedure["LimitationORNotes"] = limitationcontent[str(int(float(c)))]
            else:        
                c = procedure["LimitationORNotes"].strip() 
                procedure["LimitationORNotes"] = limitationcontent[c]                 


#     with open("newJson_19205_new.json", "w") as jsonFile:
#         json.dump(data, jsonFile,indent=4)


# with open("19205_output.json", "r") as jsonFile:
#     data = json.load(jsonFile)
# PDFScrape(data)


def get_unique_procedurecode_datemate(EligibilityBenefitsData):
    result = defaultdict(lambda: defaultdict(list))   

    for benefit in EligibilityBenefitsData:

        procedure = benefit['Procedure'] 
        
        if procedure not in result:
            result[procedure] = {'Tooth': [], 'Surface': [], 'ServiceDate': [], 'Description': []}

        result[procedure]['Tooth'].append(benefit['Tooth'])
        result[procedure]['Surface'].append(benefit['Surface'])
        result[procedure]['ServiceDate'].append(benefit['Dateofservice'])  
        result[procedure]['Description'].append(benefit['Description'])  


    final_results = []

    for procedure, entries in result.items():
        tooth_list = ', '.join(entries['Tooth'])
        surface_list = ', '.join(entries['Surface'])
        service_date_list = ', '.join(str(date) + '('+tooth.strip(' ')+')('+surface.strip(' ')+')' for date, tooth, surface in zip(entries['ServiceDate'], entries['Tooth'], entries['Surface']))
        Description = entries['Description'][0] if entries['Description'] else ''

        final_result = {
            'Tooth': tooth_list,
            'Surface': surface_list,
            'Procedure': procedure,
            'ServiceDate': service_date_list,
            'description': Description
        }

        final_results.append(final_result)


    for result in final_results:
        datedata = result.get('ServiceDate')
        dates = re.split(r',\s*', datedata)
    
    
        # Create a dictionary to store the unique dates and their respective instances
        unique_dates = {}
        for date in dates:
            parts = re.findall(r'\d+/\d+/\d+|\(\d+\)\(\w+\)|\(\d+\)\(\)', date)    
            date_key = parts[0]       
            keys = parts[1:]
            keys = [part.replace('()','') for part in keys if part != "()"]
            instances = ','.join(keys)
            
            
            if date_key in unique_dates:
                unique_dates[date_key] += f",{instances}"
            else:
                unique_dates[date_key] = instances

        # Format the unique dates and instances
        formatted_dates = [f"{date}{instances}" for date, instances in unique_dates.items()]

        # Join the formatted dates using semicolons
        result['ServiceDate'] = '; '.join(formatted_dates)    
    print('final_results from the fuctions:-',final_results)
    return final_results

def pdf_availability_checker(data):
    return data["EligibilityPatientVerification"][0].get('url')


def main(Scraperdata, request):

    # check_key = lambda x: Scraperdata["EligibilityPatientVerification"][0].get(x) if x in Scraperdata else None
    result = pdf_availability_checker(Scraperdata)    
    
    if result is None or result == "":
        print("PDFURL not found in data\n"*10)        
        output1={}
        output1.update({"EligibilityPatientVerification":[]})
        output1.update({"EligibilityBenefits":""})
        output1.update({"EligibilityMaximums":""})
        output1.update({"EligibilityDeductiblesProcCode":""})
        output1.update({"EligibilityServiceTreatmentHistory":""})
        output1.update({"TreatmentHistorySummary":""})
        output1.update({"EligibilityAgeLimitation":[]})
        output.update1({"EligibilityFiles": []})

        return output1
    
    
    pdf_data = PDFScrape(Scraperdata)

    patientdata = request.get("PatientData")[0]
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityDEductible = Scraperdata.get("EligibilityDeductible")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")
    EligibilityFiles = Scraperdata.get("EligibilityFiles")

    # print(EligibilityBenefitsData)

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]
  



    EligibilityPatientVerification.update(
        {
        "FamilyMemberId":patientdata.get("SubscriberId", ''),
        "SubscriberId":patientdata.get("SubscriberId"),
        "SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName"),
        "InsuranceIDnumber":EligibilityPatient[0].get("InsurancePayerID"),
        "FamilyMemberName":EligibilityPatient[0].get("Name"),
        "FamilyMemberDateOfBirth":patientdata.get("BirthDate"),
        "Relationship":EligibilityPatient[0].get("Relationship"),
        "SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate"),
        "FamilyMemberEffectiveDate":EligibilityPatient[0].get("EffectiveDate"),
        "FamilyMemberEndDate":EligibilityPatient[0].get("TerminationDate"),
        "FamilyMemberWaitingPeriod":EligibilityPatient[0].get("TerminationDate"),
        "InsuranceFeeScheduleUsed":EligibilityPatient[0].get("Programtype"),
        "GroupName":EligibilityPatient[0].get("Groupname"),
        "GroupNumber":EligibilityPatient[0].get("GroupNumber"),
        "DependentStudentAgeLimit":EligibilityPatient[0].get("FullTimeStudentsCovered"),
        "DependentChildCoveredAgeLimit":EligibilityPatient[0].get("DependentChildrenCovered"),
        "InsuranceCalendarOrFiscalPolicyYear":EligibilityPatient[0].get("benefitcycle"),
        "InNetworkOutNetwork":"In Network",
        "oonBenefits":"Yes",
        "MedicallyNecessaryonly":"Yes",
        "CoordinationofBenefitsType":EligibilityPatient[0].get("COBtype"),
        "MissingToothClause":EligibilityPatient[0].get("missingtoothcluse"),
        "ClaimsAddress":EligibilityPatient[0].get("ClaimAddress"),
        "ClaimMailingAddress":EligibilityPatient[0].get("ClaimAddress"),
        "ClaimPayerID":EligibilityPatient[0].get("electronicpayorid"),
        "ProgramType":EligibilityPatient[0].get("Programtype")
        }
    )

    try:
        eligiblestatus = EligibilityPatient[0].get("EligibleStatus")

        if "Yes" in eligiblestatus:
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
    except:
        pass    
      
    
    if EligibilityPatient[0].get("COBtype") == "" or EligibilityPatient[0].get("COBtype") is None:
        EligibilityPatientVerification.update({"CoordinationofBenefits":"No"})
    else:
        EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})


    try:
        alternatebenefit = ""
        for alterbenefit in EligibilityTreatmentHistory:
            # print('at:-', alterbenefit)
            if "Composite/Resin" in alterbenefit.get('Procedure'):
                # print('bjhbjhj')
                alternatebenefit = alterbenefit.get("LimitationORNotes")
                # print('alternatebenefit',alternatebenefit)
        EligibilityPatientVerification.update({"AlternativeBenefitProvision":alternatebenefit})
    except:
        pass


    try:
        index_of_deductibles = -1
        for i in range(len(EligibilityMaximiums)):
            if EligibilityMaximiums[i].get("Individualmaximumperbenefitperiod") == "Individual Deductibles - Per Benefit Period ":
                index_of_deductibles = i
                break
        # Get the required value
        if index_of_deductibles != -1 and index_of_deductibles < len(EligibilityMaximiums) - 1:
            regulars = EligibilityMaximiums[index_of_deductibles + 1]
            individual_ppo_network_value = regulars.get("IndividualPPOnetwork")
            # print(individual_ppo_network_value)
            EligibilityPatientVerification.update({"IndividualAnnualDeductible":individual_ppo_network_value})
        else:
            print('IndividualAnnualDeductible not found')

        EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":EligibilityDEductible[0].get("IndividualAnnualDeductibleMetPPONetwork").strip()})    
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleMet").strip())})                
    except:
        pass


    try:
        index_of_deductibles = -1
        for i in range(len(EligibilityMaximiums)):
            if EligibilityMaximiums[i].get("Individualmaximumperbenefitperiod") == "Family Deductibles - Per Benefit Period ":
                index_of_deductibles = i
                break
        # Get the required value
        if index_of_deductibles != -1 and index_of_deductibles < len(EligibilityMaximiums) - 1:
            regulars = EligibilityMaximiums[index_of_deductibles + 1]
            individual_ppo_network_value = regulars.get("IndividualPPOnetwork")
            # print(individual_ppo_network_value)
            EligibilityPatientVerification.update({"FamilyAnnualDeductible":individual_ppo_network_value})
        else:
            print('FamilyAnnualDeductible not found')
    except:
        pass


    try:
        EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":EligibilityMaximiums[0].get("IndividualPPOnetwork").strip()})   
        EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":EligibilityDEductible[0].get("IndividualAnnualMaximumMetPPONetwork").strip()})     
        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate").strip())})                                    
    except:
        pass

    try:
        index_of_orthodontic = -1
        for i in range(len(EligibilityMaximiums)):
            if EligibilityMaximiums[i].get("Individualmaximumperbenefitperiod") == "Orthodontic ":
                index_of_orthodontic = i
                break
        # Get the required value
        if index_of_orthodontic != -1:
            value = EligibilityMaximiums[index_of_orthodontic].get("IndividualPPONetworkLifetime")
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":value})
            EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":value})
            # print(value)
        else:
            print("OrthodonticLifetimeBenefit :- Orthodontic not found")                
    except:
        pass

    try:
        index_of_orthodontic = -1
        for i in range(len(EligibilityMaximiums)):
            if EligibilityMaximiums[i].get("Individualmaximumperbenefitperiod") == "Orthodontic ":
                index_of_orthodontic = i
                break
        # Get the required value
        if index_of_orthodontic != -1:
            value = EligibilityMaximiums[index_of_orthodontic].get("IndividualPPONetworkLifetime")
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":value})
            EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":value})
            # print(value)
        else:
            print("OrthodonticLifetimeBenefitUsedtoDate :- Orthodontic not found")                
    except:
        pass



    try:
        for benefit in EligibilityServiceTreatmentHistory:
            if benefit.get('Procedure') == "Orthodontics ":
                agelimit = benefit.get('Agelimitation')
                EligibilityPatientVerification.update({"OrthodonticAgeLimits":agelimit})
    except:
        pass    

    EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("OrthodonticLifetimeBenefit").strip(),EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate").strip())})
    EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate").strip())})

    EligibilityMaximums.append({
                "Type":  "Lifetime Maximum",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits"),
                "Remaining": EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })
    EligibilityMaximums.append({
                "Type":  "Annual Maximum",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })     
    EligibilityMaximums.append({
                "Type":  "Orthodontic Lifetime",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("OrthodonticLifetimeBenefit"),
                "Remaining": EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })  
       


    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualAnnualDeductible"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining"),
                "Used": EligibilityPatientVerification.get("IndividualAnnualDeductibleMet"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            }) 
    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("FamilyAnnualDeductible"),
                "Remaining": EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining"),
                "Used": EligibilityPatientVerification.get("FamilyAnnualDeductibleMet"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            }) 



    codes = [
            {"code":"D0150","search":"Comp Exams"},
            {"code":"D0120","search":"Periodic Exams"},
            {"code":"D0140","search":"Limited Exams"},
            {"code":"D0170","search":"RE-EVALUATION - LIMITED PROBLEM FOCUSED"}, 
            {"code":"D9110","search":"PALLIATIVE TX OF DENTAL PAIN PER VISIT"}, 
            {"code":"D0220","search":"INTRAORAL - PERIAPICAL EACH FIRST RADIOGRAPH IMAGE"},
            {"code":"D0230","search":"INTRAORAL - PERIAPICAL EACH ADD RADIOGRAPH IMAGE"},
            {"code":"D0272","search":"Bite-Wing - two radiographic images"},
            {"code":"D0274","search":"Bite-Wing - four radiographic images"},
            {"code":"D0272","search":"Bite-Wing X-Rays"},
            {"code":"D0274","search":"Bite-Wing X-Rays"},
            {"code":"D0210","search":"Full-Mouth X-Rays"},
            {"code":"D0330","search":"Panoramic radiographic image"},
            {"code":"D0240","search":"INTRAORAL - OCCLUSAL RADIOGRAPHIC IMAGE"},
            {"code":"D1110","search":"Cleanings - Adult"},
            {"code":"D1120","search":"Cleanings - Child"},
            {"code":"D1206","search":"Topical application of fluoride varnish"},
            {"code":"D1208","search":"Topical application of fluoride - excluding varnish"},
            {"code":"D1351","search":"Sealants"},
            {"code":"D1354","search":"Interim caries arresting medicament application - per tooth"},
            {"code":"D1516","search":"Space maintainer - fixed -bilateral, maxillary"},
            {"code":"D1517","search":"Space MaintainerSpace maintainer - fixed -bilateral, mandibular"},
            {"code":"D2140","search":"Amalgam - one surface, primary or permanent"},
            {"code":"D2150","search":"Amalgam - two surfaces, primary or permanent"},
            {"code":"D2160","search":"Amalgam - three surfaces, primary or permanent"},
            {"code":"D2161","search":"Amalgam - four or more surfaces, primary or permanent"},
            {"code":"D2391","search":"Resin-based composite - one surface, posterior"},
            {"code":"D2392","search":"Resin-based composite - two surfaces, posterior"},
            {"code":"D2393","search":"Resin-based composite - three surfaces, posterior"},
            {"code":"D2394","search":"Resin-based composite - four or more surfaces, posterior"},
            {"code":"D2391","search":"Composite/Resin"},
            {"code":"D2392","search":"Composite/Resin"},
            {"code":"D2393","search":"Composite/Resin"},
            {"code":"D2394","search":"Composite/Resin"},
            {"code":"D7140","search":"Extraction, erupted tooth or exposed root (elevation and/or forceps removal)"},
            {"code":"D3220","search":"Therapeutic pulpotomy (excluding final restoration) "},
            {"code":"D2930","search":"Prefabricated stainless steel crown - primary tooth"},
            {"code":"D2933","search":"Prefabricated stainless steel crown with resin window"},
            {"code":"D2934","search":"Prefabricated esthetic coated stainless steel crown - primary tooth"},
            {"code":"D9230","search":"Inhalation of nitrous oxide/analgesia, anxiolysis"},
            {"code":"D4341","search":"Scaling and Root Planing"},  
            {"code":"D7140","search":"Simple Extractions"},
            {"code":"D7210","search":"Surgical Extractions"},
            {"code":"D6010","search":"Implants"},
            {"code":"D6066","search":"Implant Crowns"}
        ]
    

    result = defaultdict(lambda: defaultdict(list))  

    benefit_data = []
    pattern = r"\d{1,2}[/|-]\d{1,2}[/|-]\d{2,4}|\d{1,2}\s+\w{3}\s+\d{2,4}"

    EligibilityBenefitsData = [item for item in EligibilityBenefitsData if is_date_format(item.get('Dateofservice'),pattern)]   

    for data in EligibilityBenefitsData:
        benefit_data.append({key.strip(): value.strip() for key, value in data.items()}) 

    for benefit in benefit_data:
        procedure = benefit['Procedure'] 
        
        if procedure not in result:
            result[procedure] = {'Tooth': [], 'Surface': [], 'ServiceDate': [], 'Description': []}

        result[procedure]['Tooth'].append(benefit['Tooth'])
        result[procedure]['Surface'].append(benefit['Surface'])
        result[procedure]['ServiceDate'].append(benefit['Dateofservice'])  
        result[procedure]['Description'].append(benefit['Description'])  


    final_results = []

    for procedure, entries in result.items():
        tooth_list = ', '.join(entries['Tooth'])
        surface_list = ', '.join(entries['Surface'])
        service_date_list = ', '.join(str(date) + '('+tooth.strip(' ')+')('+surface.strip(' ')+')' for date, tooth, surface in zip(entries['ServiceDate'], entries['Tooth'], entries['Surface']))
        Description = entries['Description'][0] if entries['Description'] else ''

        final_result = {
            'Tooth': tooth_list,
            'Surface': surface_list,
            'Procedure': procedure,
            'ServiceDate': service_date_list,
            'description': Description
        }

        final_results.append(final_result)


    for result in final_results:
        datedata = result.get('ServiceDate')
        dates = re.split(r',\s*', datedata)
        
    
        # Create a dictionary to store the unique dates and their respective instances
        unique_dates = {}
        for date in dates:
            # parts = re.findall(r'\d+/\d+/\d+|\(\d+\)\(\w+\)|\(\d+\)\(\)', date)  
            parts = re.findall(r'\d+/\d+/\d+|\(\d+\)\(\w+\)|\(\d+\)\(\)|\w+', date)    
            date_key = parts[0]  
            keys = parts[1:] 
                       
            keys = [part.replace('()','') for part in keys if part != "()"]
            keys = [f"({part})" if not part.startswith('()') and not part.endswith(')') else part.replace('()', '') for part in keys if part != "()"]
            # print('keys:- ',keys)  
            # print('keys:- ',keys) 
            instances = ','.join(keys)
            # print('instances:- ',instances)
            # if '(' not in instances:
            #     instances = '(' + instances + ')'
            
            if date_key in unique_dates:
                unique_dates[date_key] += f",{instances}"
            else:
                unique_dates[date_key] = instances

        # Format the unique dates and instances
        formatted_dates = [f"{date}{instances}" for date, instances in unique_dates.items()]

        # Join the formatted dates using semicolons
        result['ServiceDate'] = '; '.join(formatted_dates)   

    # print('final_results from the fuctions:-',final_results)

    # unique_benefits = get_unique_procedurecode_datemate(EligibilityBenefitsData)
    # print(unique_benefits)

    translation_table = str.maketrans('', '', ' -')
    EligibilityBenefits = []  # initialize the list of benefits

    for code in codes:
        if code.get("code") and code.get("search"):  # only proceed if both fields are present
            limitation = ""
            Benefits = ""
            Agelimit = ""
            deductible = ""
            newdeductible = ""
           
            # corrected variable name
            for searchItem in EligibilityTreatmentHistory:
                descriptionfromEligibilityTreatmentHistory = searchItem.get("Procedure")
                descriptionfromcode =  code.get("search")
                if descriptionfromEligibilityTreatmentHistory.lower() in descriptionfromcode.lower() or descriptionfromcode.lower() in descriptionfromEligibilityTreatmentHistory.lower():
                    # limitation = limitation +", "+searchItem.get("Frequency")
                    # Benefits = Benefits +", "+searchItem.get("DeltaDentalPPO")
                    # Agelimit = Agelimit +", "+searchItem.get("Agelimitation")
                    # print('Match description:- ', descriptionfromcode)
                    if searchItem.get("Frequency") is not None:
                        limitation = limitation +", "+ searchItem.get("Frequency")
                    if searchItem.get("DeltaDentalPPO") is not None:
                        Benefits = Benefits +", "+searchItem.get("DeltaDentalPPO")
                    if searchItem.get("Agelimitation") is not None:
                        Agelimit = Agelimit +", "+searchItem.get("Agelimitation")
                    

                    ndeductible = searchItem.get("LimitationORNotes")
                    # print('ndeductible:-',ndeductible)

                    if "Deductible Exempt" in ndeductible:
                        deductible = "No"                        
                    else:
                        deductible = "Yes" 

                    if deductible != "":
                        limitation = limitation +", "+ndeductible.strip() 

                    if "Deductible Exempt," in limitation:
                        limitation = limitation.replace('Deductible Exempt,','')
                    if "Deductible Exempt" in limitation:
                        limitation = limitation.replace('Deductible Exempt','') 
                    if ", Deductible Exempt" in limitation:
                        limitation = limitation.replace(', Deductible Exempt','') 

            # check if the code is already in the list of benefits
            code_exists = False
            for benefit in EligibilityBenefits:
                if benefit.get("ProcedureCode") == code.get("code"):
                    benefit_limitation = str(benefit["limitation"]+", "+limitation.strip(', ')+" "+ Agelimit.strip(', ')).replace(" N/A","")
                    # print('limitation is ---', benefit_limitation)
                    benefit["limitation"] = benefit_limitation.strip(', ')
                    benefit["Benefits"] = Benefits.strip(', ')
                    benefit["DeductibleApplies"] = deductible.strip(', ')
                    code_exists = True
                    # print('benefit["limitation"]---', benefit["limitation"])

                    break

            if not code_exists:
                limitation_str = limitation.strip(', ') + ", " + Agelimit.strip(', ') if Agelimit.strip(', ') else limitation.strip(', ')
                limitation_str = limitation_str.strip(',')
                Benefits  = Benefits.strip(',')

                if "Deductible Exempt," in limitation_str:
                        limitation_str = limitation_str.replace('Deductible Exempt,','')
                if "Deductible Exempt" in limitation_str:
                        limitation_str = limitation_str.replace('Deductible Exempt','') 
                if ", Deductible Exempt" in limitation_str:
                        limitation_str = limitation_str.replace(', Deductible Exempt','') 
                
                EligibilityBenefits.append({
                    "ProcedureCode": code.get("code").strip(),
                    "ProcedureCodeDescription": code.get("search"),
                    "Amount": "",
                    "Type": "",
                    "limitation": limitation_str.replace("N/A","").strip(),
                    "DeductibleApplies": deductible.strip(', '),
                    "Copay": "",
                    "Benefits": Benefits,
                    "WaitingPeriod": ""
                })


    for itemss in final_results:
        if itemss.get("Procedure") != "" and itemss.get("Procedure", None):
            limitation = ""
            limitapplies = ""
            # print('date:-',itemss.get("ServiceDate"))
            for codees in codes:
                if itemss.get("Procedure").translate(translation_table) == codees.get("code").translate(translation_table):
                    for searchitems in EligibilityTreatmentHistory:
                        limitation = searchitems.get("Frequency")
                        limitapplies = searchitems.get("LimitationORNotes")

            EligibilityServiceTreatmentHistory.append({
                "ProcedureCode": itemss.get("Procedure"),
                "LimitationText": limitation.strip(', '),
                "History": itemss.get("ServiceDate"),
                "Tooth": itemss.get("Tooth"),
                "Surface": itemss.get("Surface").strip(','),
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": itemss.get("description")                
                })  
            TreatmentHistorySummary.append({
                "ProcedureCode": itemss.get("Procedure"),
                "LimitationText": limitation.strip(', '),
                "History": itemss.get("ServiceDate"),
                "Tooth": itemss.get("Tooth"),
                "Surface": itemss.get("Surface").strip(','),
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": itemss.get("description")                
                })        

        
        if itemss.get("Proccode") == "D2391":
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":itemss.get("WaitingPeriod")})



    output={}

    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityFiles": EligibilityFiles})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output




if __name__ == "__main__":
    request = json.load(open(r"C:\Users\BhalchandraWankhede\Desktop\SDB-repo\Elig_dev\SD%20Payor%20Scraping\Missouri.json", 'r'))
    Scraperdata=json.load(open(r"C:\Users\BhalchandraWankhede\Desktop\SDB-repo\Elig_dev\SD%20Payor%20Scraping\output_18082.json", 'r'))
    data = main(Scraperdata,request)
    with open("MissouriOutput_18082_output.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


