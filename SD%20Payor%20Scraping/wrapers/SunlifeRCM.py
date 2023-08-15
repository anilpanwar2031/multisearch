
import random,string
from FileDownload import Downloader
import tika
import pandas as pd
from tika import parser
from Utilities.pdf_utils import *

def filedownload_(url):

    file_path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdf"
    print(file_path)
    input_file = url.replace("%20", " ")
    print("input_file>>>>>>>>>>>>>>", input_file)
    Downloader('Revenue Cycle Management', file_path, input_file)
    return file_path

def master_scraper(file_path):
    tika.initVM()
    parsed_pdf = parser.from_file(file_path)
    pdf_content = parsed_pdf['content']
    df_li,workd=get_data_in_format(file_path)
    master_df=pd.DataFrame()
    for i in range(len(df_li)):
        if 'Code ' in df_li[i].columns:
            master_df=pd.concat([master_df,df_li[i]],axis=0)
    master_df=master_df.fillna("")
    temp_col=['Code','Messages','Unnamed: 2','Unnamed: 3','Unnamed: 4','Unnamed: 5']
    
    if len(master_df)==0:
        master_df=pd.DataFrame()
        for i in range(len(df_li)):
            for j in df_li[i].columns:
                if 'Code' in j:
                    master_df=pd.concat([master_df,df_li[i]],axis=0)
        temp_col=['Code','Messages','Unnamed: 2','Unnamed: 3','Unnamed: 4','Unnamed: 5']
        drop_index=[]
        master_df=master_df.fillna('')
        for j in range(master_df.shape[0]):
            for i in range(master_df.shape[1]):
                if 'Code' in master_df.iloc[j,:][i]:
                    drop_index.append(j)
                    break
        for i in range(len(drop_index)):
            master_df.drop(drop_index[i],inplace=True)
        master_df.reset_index(inplace=True)
        if 'index' in list(master_df.columns):
                master_df=master_df.drop('index',axis=1)
        master_df['Unnamed: 2']=''
        master_df['Unnamed: 3']=''
        master_df['Unnamed: 4']=''
        master_df['Unnamed: 5']=''
        master_df.columns=temp_col
        for i in range(len(df_li)):
            for j in df_li[i].columns:
                if 'Draft' in j:
                    master_df.loc[len(master_df)]=list(df_li[i].columns)        
                    master_df.loc[len(master_df.index)]=list(df_li[i].iloc[0,:])
    temp_data=pdf_content.split('Adjustment Payment Payee')[1].strip().split('\n\n')[0]
    check_no=temp_data.split(' ')[0]
    benefit=temp_data.split(' ')[1]
    cob_amount=temp_data.split(' ')[2]
    adjustment=temp_data.split(' ')[3]
    payment=temp_data.split(' ')[4]
    payee=' '.join(temp_data.split(' ')[5:])
    provider=pdf_content.split('Provider:')[1].split('\n\n')[0].strip()
    relationship=pdf_content.split('Relationship:')[1].split('\n\n')[0].strip()
    insured=pdf_content.split('Insured:')[1].split('\n\n')[0].strip()
    used_amount=pdf_content.split('You have used ')[1].split(' ')[0]
    remaing_amount=pdf_content.split('You have used ')[1].split('You have')[1].strip().split(' ')[0]
    plan_value=pdf_content.split('You have used ')[1].split("your plan's allowable")[1].strip().split('\n')[0]
    satisfied_amount=pdf_content.split('Plan Year Allowable Maximum')[1].strip().split('\n\n')[0].split(' ')[0]
    play_year_deduct=pdf_content.split('Plan Year Allowable Maximum')[1].strip().split('\n\n')[0].split(' ')[1]
    for i in pdf_content.split('\n\n'):
        if 'Claim #:' in i:
            claim=i.split(' ')[0]
            break
    dos=pdf_content.split('Date:')[1].split('\n\n')[0].strip()
    for i in pdf_content.split('\n\n'):
        if 'Client' in i:
            group_no=i.split('Claim #:')[1].split('Client')[0].strip()
            break
    for i in pdf_content.split('\n\n'):
        if 'Network:' in i:
            network=i.split('Network:')[0]
            break
    patient_name=pdf_content.split('Customer Service contacts noted above.')[1].strip().split('\n\n')[0]
    processing_policy=[]
    for j in range(master_df.shape[0]):
        for i in range(master_df.shape[1]):
            if 'Draft/Check' in master_df.iloc[j,:][i]:
                for x in range(0,j):
                    processing_policy.append(master_df.iloc[x,:][0]+" - "+master_df.iloc[x,:][1].strip())
    processing_policy=[i.strip() for i in processing_policy]
    claim_df=pd.DataFrame()
    for i in range(len(df_li)):
        df_li[i]=df_li[i].fillna('')
        for j in range(len(df_li[i])):
            if 'Amount billed to' in df_li[i].iloc[:,0][j]:
                claim_df=df_li[i]
    billed_amount=''
    paid_by_sunlife=''
    paid_by_patient=''
    for i in list(claim_df.iloc[:,0]):
        if 'by your dentist' in i:
            billed_amount="$"+i.strip().split('$')[-1].split(' ')[0]
        if 'paid your dentist' in i:
            paid_by_sunlife="$"+i.strip().split('$')[-1].split(' ')[0]
        if 'Your Responsibility' in i:
            paid_by_patient="$"+i.strip().split('$')[-1].split(' ')[0]
    temp_dict={
                "ClaimNumber":claim,
                "Patient":patient_name.replace('NOT_RECEIVED','').strip(),
                "GroupPolicyNumber":group_no,
                "ProviderName":provider,
                "PricingNetwork":network,
                "DatePaid":dos,
                "Insured":insured,
                "Relationship":relationship,
                "CheckNumber":check_no,
                "Benefit":benefit,
                "COBAmount":cob_amount,
                "Adjustment":adjustment,
                "Payment":payment,
                "Payee":payee,
                "ProcessingPolicy":processing_policy,
                "AmountBilledToSunLifeByYourDentist":billed_amount,
                "AmountSunLifePaidYourDentist":paid_by_sunlife,
                "YourResponsibility":paid_by_patient,
                "SatisfiedAmount":satisfied_amount,
                "PlanYearDeductible":play_year_deduct,
                "UsedAmountFromPaln":used_amount,
                "PlanBenefitsRemainingAmount":remaing_amount,
                "PlanYearAllowableMaximum":plan_value,
        
              }
    return temp_dict

def details_scraper(file_path):
    df_li,workd=get_data_in_format(file_path)
    new_df=pd.DataFrame()
    for i in range(len(df_li)):
        for j in df_li[i].columns:
            if 'Claim #' in j or 'Client/Group No' in j:
                new_df=pd.concat([new_df,df_li[i]],axis=0)
    detail_columns=['Service Date','Description','Tth No.','Submitted Services','Submitted Charges','Allowed Service',
                    'Allowed Amount','Co-Pay%','Deductible','PPO Savings','Patient Resp','Remark Code(s)','Plan Payment']
    drop_index=[]
    new_df=new_df.fillna('')
    for j in range(new_df.shape[0]):
        for i in range(new_df.shape[1]):
            if 'Service Date' in new_df.iloc[j,:][i]:
                drop_index.append(j)
                break
            if 'TOTALS' in new_df.iloc[j,:][i]:
                drop_index.append(j)
                break
            if 'Total Patient Responsibility' in new_df.iloc[j,:][i]:
                drop_index.append(j)
                break
            if 'Client/Group No' in new_df.iloc[j,:][i]:
                drop_index.append(j)
                break
    new_df.columns=detail_columns
    for j in drop_index:
        new_df.drop(j,inplace=True)
    new_df.reset_index(inplace=True)
    if 'index' in list(new_df.columns):
        new_df=new_df.drop('index',axis=1)
    for i in detail_columns:
        new_df[i]=new_df[i].str.strip()        

    return new_df.to_dict('records')

def main(data):
    """
        This function takes in a dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.
        It modifies keys of the RcmEobClaimDetail.

        Args:
        - data: A dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.

        Returns:
        - A modified 'data' dictionary with the changed keys in 'RcmEobClaimDetail'.
    """
    for i in range(len(data['RcmEobClaimMaster'])):
        url = data["RcmEobClaimMaster"][i]["url"].replace('%20', ' ')
        pdf_file=filedownload_(url)
        temp_data=master_scraper(pdf_file)
        data['RcmEobClaimMaster'][i].update(temp_data)

    data['RcmEobClaimDetail']=details_scraper(pdf_file)

    
    
    return data






