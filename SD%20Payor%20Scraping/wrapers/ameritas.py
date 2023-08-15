from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json
from re import search
from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
import os.path
import zipfile
import json
import logging
import random
import string
import sys
import zipfile
import pandas as pd
import logging
import json

def zip_processor(path1, path2):
    df_list = []
    archive1 = zipfile.ZipFile(path1, 'r')
    file_names1 = archive1.namelist()
    table_files1 = [name for name in file_names1 if name.startswith('tables/') and name.endswith(".xlsx")]

    #load extra info from benefit summary
    structureData = []
    mailingAdress = ""
    payorID = ""
    with zipfile.ZipFile(path1, "r") as zip_file:
        with zip_file.open("structuredData.json") as json_file:
            structureData = json.load(json_file)
    elements = structureData.get("elements")
    for item in elements:
        if item.get("Path") == "//Document/P/Sub":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[2]":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[3]":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[4]":
            mailingAdress = mailingAdress + item.get("Text")
        elif item.get("Path") == "//Document/P/Sub[5]":
            payorID = item.get("Text")

    archive2 = zipfile.ZipFile(path2, 'r')
    file_names2 = archive2.namelist()
    table_files2 = [name for name in file_names2 if name.startswith('tables/') and name.endswith(".xlsx")]
    
    data = {
        "EligibilityPatientVerification":[],
        "EligibilityMaximums":[],
        "EligibilityOtherProvisions":[],
        "EligibilityBenefits":[]
        }
    
    data["EligibilityPatientVerification"].append({"ClaimMailingAddress":mailingAdress})
    data["EligibilityPatientVerification"].append({"PayorID":payorID})

    for idx, name in enumerate(table_files1):
        with archive1.open(name) as file:
            try:
                df = pd.read_excel(file)
                if len(df.index) >= 1 or df.columns.str.contains('TOTAL', case=False).any():
                    if df.columns.str.contains('_x000D_', case=False).any():
                        df = df.replace('_x000D_', '', regex=True)
                    if any('_x000D_' in col for col in df.columns):
                        df = df.rename(columns=lambda x:x.replace("_x000D_", ""))

                    df_list.append(df)
            except pd.errors.ParserError as e:
                logging(f"Error parsing {name}: {e}")

    for idx, name in enumerate(table_files2):
        with archive2.open(name) as file:
            try:
                df = pd.read_excel(file)
                if len(df.index) >= 1 or df.columns.str.contains('TOTAL', case=False).any():
                    if df.columns.str.contains('_x000D_', case=False).any():
                        df = df.replace('_x000D_', '', regex=True)
                    if any('_x000D_' in col for col in df.columns):
                        df = df.rename(columns=lambda x:x.replace("_x000D_", ""))

                    df_list.append(df)
            except pd.errors.ParserError as e:
                logging(f"Error parsing {name}: {e}")
    
    for tables in df_list:
        ##Benefits Summary##
        if tables.columns.str.contains('Plan Member: ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Title', 'Detail']    
            data["EligibilityPatientVerification"].append({"PlanMember":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Coverage Status Information: ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Title', 'Detail']    
            data["EligibilityPatientVerification"].append({"Coverage":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Benefit Type/Plan Benefit: ', case=False).any() or ("Benefit Type/Plan Benefit:" in tables.loc[0][0]):
            if len(tables.columns) == 4:
                tables.columns = ['Benefit Type/Plan Benefit', 'Percentage', 'value', 'Elimination Period']    
                data["EligibilityOtherProvisions"].append({"BenefitTypePlan":tables.to_dict(orient='records')})
            elif len(tables.columns) == 5:
                tables.columns = ['Benefit Type/Plan Benefit', 'Detail', 'Percentage', 'value', 'Elimination Period']    
                data["EligibilityOtherProvisions"].append({"BenefitTypePlan":tables.to_dict(orient='records')})
            elif len(tables.columns) == 3:
                tables.columns = ['Benefit Type/Plan Benefit', 'value', 'Elimination Period']    
                data["EligibilityOtherProvisions"].append({"BenefitTypePlan":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Orthodontics: ', case=False).any():
            if len(tables.columns) == 2:
                tables.columns = ['Title', 'Detail']    
                data["EligibilityOtherProvisions"].append({"Orthodontics":tables.to_dict(orient='records')})
        elif (tables == "Contributing Procedures ").any(axis=1).any():
            if len(tables.columns) == 5:
                tables.columns = ['Service', 'Benefit Type', 'Frequency', 'Contributing Procedures', 'Additional Information']    
                data["EligibilityBenefits"].append({"Benefits with proc":tables.to_dict(orient='records')})
            elif len(tables.columns) == 6:
                tables.columns = ['Service', 'Benefit Type', 'extra', 'Frequency', 'Contributing Procedures', 'Additional Information']    
                data["EligibilityBenefits"].append({"Benefits with proc":tables.to_dict(orient='records')})
        elif (tables == "Frequency ").any(axis=1).any() and len(tables.columns) == 4:
            tables.columns = ['Service', 'Benefit Type', 'Frequency', 'Additional Information']    
            data["EligibilityBenefits"].append({"Benefits":tables.to_dict(orient='records')})
        
        ##Patient Summary##
        elif tables.columns.str.contains('Benefit Type Percentage Type 1 - Preventive ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Title', 'Detail']   
            data["EligibilityMaximums"].append({"MaximumsAll":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Next Eligible ', case=False).any():
            tables.columns = ['Procedure', 'Next Eligible']   
            data["EligibilityBenefits"].append({"Procedure Dates":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Type 1 - Preventive ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Benefit Type', 'Percentage']   
            data["EligibilityMaximums"].append({"BenefitTypeByPercentage":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Preventive/Basic/Major ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Deductible', 'Detail']   
            data["EligibilityMaximums"].append({"Deductible":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Basic/Major ', case=False).any():
            columns = tables.columns
            column_row = pd.DataFrame([columns], columns=tables.columns)
            tables = pd.concat([column_row, tables], ignore_index=True)
            tables.columns = ['Deductible', 'Detail']
            data["EligibilityMaximums"].append({"Deductible":tables.to_dict(orient='records')})
        elif tables.columns.str.contains('Maximum ', case=False).any():
            if len(tables.columns) == 2:
                tables.columns = ['Maximum', 'Detail']   
                data["EligibilityMaximums"].append({"Maximums":tables.to_dict(orient='records')})
            elif len(tables.columns) == 3:
                tables.columns = ['Maximum', 'Detail', 'Detail2']   
                data["EligibilityMaximums"].append({"Maximums":tables.to_dict(orient='records')})

    
    # json_data = json.dumps(data, indent=2)
    
    # with open ("outputPatient.json", "w") as f:
    #     f.write(json_data)

    return data



current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from FileDownload import Downloader

def PdfExcelMaker(url,output_zip):
    #soutput_zip = "./ExtractTextInfoFromPDFtry.zip"

    if os.path.isfile(output_zip):
        os.remove(output_zip)
    file_path =''.join(random.choices(string.ascii_uppercase +string.digits, k=10)) + ".pdf"    
    Downloader('Eligibility',file_path,url)
    input_pdf = file_path
    
    try:

        #Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder()\
            .from_file("./pdfservices-api-credentials.json") \
            .build()

        #Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        #Set operation input from a source file.
        source = FileRef.create_from_local_file(input_pdf)
        extract_pdf_operation.set_input(source)

        #Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .with_element_to_extract(ExtractElementType.TABLES) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        #Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)
        print(result)
        print("\n",FileRef)

        

        #Save the result to the specified location.
        result.save_as(output_zip)

        print("Successfully extracted information from PDF. Printing H1 Headers:\n");

        archive = zipfile.ZipFile(output_zip, 'r')
        print(archive.namelist())
        jsonentry = archive.open('structuredData.json')
        jsondata = jsonentry.read()
        data = json.loads(jsondata)
        for element in data["elements"]:
            if(element["Path"].endswith("/H1")):
                print(element["Text"])
            

    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")







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
    return f'${float(a)-float(b)}'
def getsum(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)+float(b)}'
def main(Scraperdata, request):
    urls = Scraperdata.get("EligibilityPatientVerification")[0].get("url")
    for url in urls:
        if url.endswith("BenefitSummary.pdf"):
            PdfExcelMaker(url,"./ExtractTextInfoFromPDFtry.zip")
        if url.endswith("PatientDetails.pdf"):
            PdfExcelMaker(url,"./ExtractTextInfoFromPDFtry2.zip")
                
    data = zip_processor("./ExtractTextInfoFromPDFtry.zip", "./ExtractTextInfoFromPDFtry2.zip")
    patientdata = request.get("PatientData")[0]
    EligibilityFiles = Scraperdata.get("EligibilityFiles")
    scraperEligibilityData = Scraperdata.get("EligibilityPatientVerification")

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    
    historyTemp = []

    SubcriberName = ""
    for items in scraperEligibilityData:
        if items.get("Subscriber Name", None):
            EligibilityPatientVerification.update({"SubscriberName":items.get("Subscriber Name")})
            SubcriberName = items.get("Subscriber Name")
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    
    tempEligibility=data.get("EligibilityPatientVerification")
    for items in tempEligibility:
        if items.get("PlanMember", None):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
            for title in items.get("PlanMember"):       
                if title.get("Title") == "Plan Member: ":
                    EligibilityPatientVerification.update({"SubscriberName":title.get("Detail")})
                elif title.get("Title") == "Plan Number: ":
                    EligibilityPatientVerification.update({"GroupNumber":title.get("Detail")})
                elif title.get("Title") == "Plan Sponsor: ":
                    EligibilityPatientVerification.update({"GroupName":title.get("Detail")})
        if items.get("Coverage", None):
            for title in items.get("Coverage"):       
                if title.get("Title") == "Coverage Status Information: ":
                    EligibilityPatientVerification.update({"ProgramType":title.get("Detail")})
                elif title.get("Title") == "Missing Teeth: ":
                    EligibilityPatientVerification.update({"MissingToothClause":title.get("Detail")})
                elif title.get("Title") == "Child Age: ":
                    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":title.get("Detail")})
                elif title.get("Title") == "Student Age: ":
                    EligibilityPatientVerification.update({"DependentStudentAgeLimit":title.get("Detail")})
        if items.get("ClaimMailingAddress", None):
            EligibilityPatientVerification.update({"ClaimMailingAddress":items.get("ClaimMailingAddress")})
        if items.get("PayorID", None):
            EligibilityPatientVerification.update({"ClaimPayerID":items.get("PayorID")})


    for items in scraperEligibilityData:
        if items.get("DateOfBirth", None):
            if items.get("DateOfBirth") == patientdata.get("BirthDate"):
                EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":items.get("DateOfBirth")})
                EligibilityPatientVerification.update({"FamilyMemberName":items.get("Name")})
            if search(str(items.get("Name")), str(SubcriberName)):
                EligibilityPatientVerification.update({"SubscriberDateOfBirth":items.get("DateOfBirth")})
                EligibilityPatientVerification.update({"SubscriberName":items.get("Name")})
        elif items.get("Plan Number", None):
            EligibilityPatientVerification.update({"GroupNumber":items.get("Plan Number")})
    
    tempMaximium=data.get("EligibilityMaximums")
    flag=0
    for items in tempMaximium:
        if items.get("MaximumsAll", None):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
            for title in items.get("MaximumsAll"):       
                if title.get("Title") == "Annual maximum ":
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":title.get("Detail")})
                elif title.get("Title") == "Remaining maximum ":
                    flag = flag+1
                    if flag == 1:
                        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":title.get("Detail")})
                    if flag == 2:
                        EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":title.get("Detail")})
                elif title.get("Title") == "Basic/Major ":
                    EligibilityPatientVerification.update({"IndividualAnnualDeductible":title.get("Detail")})
                elif title.get("Title") == "Remaining deductible ":
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":title.get("Detail")})
                elif title.get("Title") == "Lifetime Maximum ":
                    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":title.get("Detail")})
        elif items.get("Deductible", None):
            for title in items.get("Deductible"):
                if title.get("Deductible") == "Preventive/Basic/Major ":
                    EligibilityPatientVerification.update({"IndividualAnnualDeductible":title.get("Detail")})
                elif title.get("Deductible") == "Remaining deductible ":
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":title.get("Detail")})
                elif title.get("Deductible") == "Basic/Major ":
                    EligibilityPatientVerification.update({"IndividualAnnualDeductible":title.get("Detail").replace("per plan year", "").strip()})
        elif items.get("Maximums", None):
            for title in items.get("Maximums"):
                if title.get("Maximum") == "Annual maximum ":
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":title.get("Detail")})
                elif title.get("Maximum") == "Remaining maximum ":
                    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":title.get("Detail")})
        elif items.get("BenefitTypeByPercentage", None):
            for title in items.get("BenefitTypeByPercentage"):
                if title.get("Benefit Type") == "Annual maximum ":
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":title.get("Detail")})
                elif title.get("Maximum") == "Remaining maximum ":
                    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":title.get("Detail")})
    
    a= EligibilityPatientVerification.get("IndividualAnnualDeductible").replace("per visit", "").replace("per plan year", "").strip()
    b= EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip()
    EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(a,b)})
    EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":"through the 26th birthday, end of month"})

    EligibilityMaximums.append({
        "Type": "Annual Maximums",
        "Network": "In Network",
        "Amount": EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),
        "Remaining": EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip(),
        "ServiceCategory": "Dental",
        "Family_Individual": "Individual"
    })
    EligibilityDeductiblesProcCode.append({
        "Type": "Annual Deductible",
        "Network": "In Network",
        "Amount": EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),
        "Remaining": EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip(),
        "ServiceCategory": "Dental",
        "Family_Individual": "Individual"
    })

    tempProvisions=data.get("EligibilityOtherProvisions")
    for items in tempProvisions:
        EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
        if items.get("BenefitTypePlan", None):
            for title in items.get("BenefitTypePlan"):       
                if title.get("Elimination Period") != "  None ":
                    EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":str(title.get("Elimination Period"))})
                    break
                else:
                    EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":str(title.get("Elimination Period"))})
                EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":title.get("value")})

    BenefitTypePlan2 = []
    for items2 in tempProvisions:
        if items2.get("BenefitTypePlan", None):
            for title2 in items2.get("BenefitTypePlan"):
                try:
                    if ("Type 1 - Preventive" in title2.get("Benefit Type/Plan Benefit") and "Type 2 - Basic" in title2.get("Benefit Type/Plan Benefit")):
                        newPercentage = title2.get("Percentage").strip().split(" ")
                        plantype1 = title2.get("Benefit Type/Plan Benefit")
                        plantype2 = title2.get("Benefit Type/Plan Benefit")
                        BenefitTypePlan2.append({
                            "Benefit Type/Plan Benefit": plantype1.replace("Type 2 - Basic",""),
                            "Percentage": newPercentage[0],
                            "value": title2.get("value"),
                            "Elimination Period": title2.get("Elimination Period")
                        })
                        BenefitTypePlan2.append({
                            "Benefit Type/Plan Benefit": plantype1.replace("Type 1 - Preventive","").replace("Benefit Type/Plan",""),
                            "Percentage": newPercentage[1],
                            "value": title2.get("value"),
                            "Elimination Period": title2.get("Elimination Period")
                        })
                        continue
                except:
                    pass
                BenefitTypePlan2.append(title2)

            items2.update({"BenefitTypePlan":BenefitTypePlan2})


    EligibilityBenefits=[]

    tempBenefits=data.get("EligibilityBenefits")
    for items in tempBenefits:
        if items.get("Procedure Dates", None):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
            for title in items.get("Procedure Dates"):       
                historyTemp.append({
                    "ProcedureCodeDescription": title.get("Procedure"),
                    "NED": str(title.get("Next Eligible"))
                })
        elif items.get("Benefits with proc", None):
            for title in items.get("Benefits with proc"):       
                if title.get("Service") != "Service " and str(title.get("Contributing Procedures")) != "nan" and str(title.get("Benefit Type")) != "nan":
                    percentage = ""
                    deductible = ""
                    historyNext = ""
                    for benefitTypes in tempProvisions:
                        if benefitTypes.get("BenefitTypePlan", None):
                            for val in benefitTypes.get("BenefitTypePlan"):                                
                                if search(str(title.get("Benefit Type")).replace("Current Dental Terminology copyrighted American Dental Association. ",""), str(val.get("Benefit Type/Plan Benefit"))):
                                    if search("Preventive", str(title.get("Benefit Type"))) or search("Basic", str(title.get("Benefit Type"))) or search("Major", str(title.get("Benefit Type"))):
                                        deductible = "Yes"
                                    else:
                                        deductible = "No"
                                    if val.get("Percentage", None):
                                        percentage = val.get("Percentage")
                                    if "%" in val.get("Benefit Type/Plan Benefit"):
                                        itemsForPercent = val.get("Benefit Type/Plan Benefit").split()
                                        for loopForPercent in itemsForPercent:
                                            if "%" in loopForPercent:
                                                percentage = loopForPercent
                                    break
                            try:
                                for ddeduct in benefitTypes.get("BenefitTypePlan"):
                                    if ("Deductible" and "$" in ddeduct.get("Benefit Type/Plan Benefit")) and ("Type 1" or "Type 2" or "Type 3" in title.get("Benefit Type")):
                                        deductible = "Yes"
                                        break
                                    else:
                                        deductible = "No"
                            except:
                                pass


                    procCoded = title.get("Contributing Procedures").strip().split(" ")

                    for code in procCoded:
                        EligibilityBenefits.append({
                            "ProcedureCode": code,
                            "ProcedureCodeDescription": title.get("Service").strip(),
                            "Benefits": percentage.strip(),
                            "Deductible": deductible,
                            "Frequency": title.get("Frequency").strip()+", "+str(title.get("Additional Information")).strip(),
                            "History": historyNext
                        })
        elif items.get("Benefits", None):
            amalgam = ""
            composite =""
            for title in items.get("Benefits"):       
                if title.get("Service") == "Amalgam ":
                    if str(title.get("Additional Information")) != "nan":
                        amalgam = str(title.get("Additional Information"))
                if title.get("Service") == "Composite ":
                    if str(title.get("Additional Information")) != "nan":
                        composite = str(title.get("Additional Information"))
            EligibilityPatientVerification.update({"AlternativeBenefitProvision":amalgam + composite})

    allcodeslist = ""
    for itemneed, dictionary  in enumerate(EligibilityBenefits):
        if dictionary['ProcedureCode'] in allcodeslist:
            EligibilityBenefits.pop(itemneed)
            continue
        allcodeslist = allcodeslist +" "+dictionary['ProcedureCode']
    
    for hist in EligibilityBenefits:
        historyNext = ""
        for getVal in historyTemp:
            if search(str(hist.get("ProcedureCodeDescription").strip()), str(getVal.get("ProcedureCodeDescription"))):
                historyNext =  str(getVal.get("NED"))
                break
            else:
                historyNext = "No History"
        hist.update({"History":historyNext})
    
    for item in EligibilityBenefits:
        EligibilityServiceTreatmentHistory.append({
            "ProcedureCode": item.get("ProcedureCode"),
            "LimitationText": item.get("Frequency"),
            "History": item.get("History"),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": item.get("ProcedureCodeDescription")
        })
        TreatmentHistorySummary.append({
            "ProcedureCode": item.get("ProcedureCode"),
            "LimitationText": item.get("Frequency"),
            "History": item.get("History"),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": item.get("ProcedureCodeDescription")
        })


    # EligibilityPatientVerification.update({"FamilyMemberId":temp.get("Member ID").replace("Member ID: ", "")})
    # EligibilityPatientVerification.update({"GroupNumber":temp.get("Insurance Group Number")})
    # EligibilityPatientVerification.update({"FamilyMemberEndDate":temp.get("Insurance End Period")})

    # date_str = temp.get("Insurance End Period")
    # date_format = "%m/%d/%Y"
    # target_date = datetime.strptime(date_str, date_format).date()
    # current_date = datetime.now().date()
    # if target_date > current_date:
    #     EligibilityPatientVerification.update({"EligibilityStatus":"Active"})

    # EligibilityPatientVerification.update({"PlanType":temp.get("Insurance Group Name")})
    # EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":temp.get("Insurance Calendar or Fiscal Policy Year").replace("Calendar Year Max: ", "")})
    # EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":temp.get("Insurance Group Name")})
    # EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":temp.get("Insurance Effective Date")})
    # EligibilityPatientVerification.update({"ClaimMailingAddress":"GEHA PO Box 21542 Eagan, MN 55121"})
    # EligibilityPatientVerification.update({"ClaimsAddress":"GEHA PO Box 21542 Eagan, MN 55121"})

    # EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":plan.get("Calendar year maximum").get("InNetwork").replace(" per person", "")})
    
    # EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":plan.get("Orthodontic").get("InNetworkLifetimeMaximum").replace(" per person", "")})
    # EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":plan.get("Orthodontic").get("InNetworkLifetimeMaximum").replace(" per person", "")})
    
    

    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityFiles":EligibilityFiles})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    
    return output


# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\dev 15 june all testing\dev 17 june\SD%20Payor%20Scraping\test.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\dev 15 june all testing\dev 17 june\SD%20Payor%20Scraping\output_230618_233600_.json", 'r'))
# output=main(data, request)
# with open("AmritasPatientWrapper.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)


