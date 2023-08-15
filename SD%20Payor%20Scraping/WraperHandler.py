
def WraperHandler(InputParameters,data,scraped_data,patient,browser):
    scraped_data =scraped_data
    if InputParameters['AppName'] =='Eligibility':        
        if InputParameters.get('WebsiteId')  =="DELTADENTALINS_001" and InputParameters["AppName"]== "Eligibility":
                    request_ =data
                    request_['PatientData'] =[patient]   
                    from wrapers import deltadentalins                                             
                    scraped_data= deltadentalins.main(scraped_data,request_,browser)  
        elif InputParameters.get('WebsiteId')=="DNOACONNECT_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import dnoa
            scraped_data= dnoa.main(scraped_data)
            
        elif InputParameters.get('WebsiteId')=="DENTALOFFICETOOLKIT001" and InputParameters["AppName"]== "Eligibility":
            request_ =data
            request_['PatientData'] =[patient] 
            from wrapers import dentalofficetoolkit
            scraped_data= dentalofficetoolkit.main(scraped_data,request_) 
        elif InputParameters.get('WebsiteId')=="DENTALDENTALOHIO_001" and InputParameters["AppName"]== "Eligibility":
            request_ =data
            request_['PatientData'] =[patient] 
            from wrapers import deltadentalOhio
            scraped_data= deltadentalOhio.main(scraped_data,request_) 
        elif InputParameters.get('WebsiteId')=="METLIFE001" and InputParameters["AppName"]== "Eligibility":
            request_ =data
            request_['PatientData'] =[patient]
            from wrapers import  metlife
            scraped_data= metlife.main(scraped_data,request_)
        elif InputParameters.get('WebsiteId')=="UNITEDCONCORDIA_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import UC
            scraped_data= UC.main(scraped_data)
        elif InputParameters.get('WebsiteId') in ["CIGNA_001", "2"] and InputParameters["AppName"]== "Eligibility":
            from wrapers import cigna
            scraped_data= cigna.main(scraped_data)    
        elif InputParameters.get('WebsiteId')=="UNITEDHEALTHCARE_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import UHC
            scraped_data= UHC.main(scraped_data) 
        elif InputParameters.get('WebsiteId')=="GUARDIAN_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import guardian
            scraped_data= guardian.main(scraped_data)
        elif InputParameters.get('WebsiteId')=="GEHA_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import geha
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= geha.main(scraped_data,request_)
            
        elif InputParameters.get('WebsiteId')=="AMERITAS_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import ameritas
            request_ =data
            request_['PatientData'] =[patient]  
            scraped_data= ameritas.main(scraped_data,request_)    
        elif InputParameters.get('WebsiteId')=="PRINCIPAL_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import principal
            request_ =data
            request_['PatientData'] =[patient]  
            scraped_data= principal.main(scraped_data,request_)
            
        elif InputParameters.get('WebsiteId')=="ILLINOIS_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import illinois
            request_ =data
            request_['PatientData'] =[patient]
            scraped_data= illinois.main(scraped_data,request_)
        elif InputParameters.get('WebsiteId')=="CONNECTICUT_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import connecticut
            request_ =data
            request_['PatientData'] =[patient]  
            scraped_data= connecticut.main(scraped_data,request_) 
        elif InputParameters.get('WebsiteId')=="NEWJERSEY_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import newjersey
            request_ =data
            request_['PatientData'] =[patient]
            scraped_data= newjersey.main(scraped_data,request_) 
        elif InputParameters.get('WebsiteId')=="WASHINGTON_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import washington
            request_ =data
            request_['PatientData'] =[patient]   
            scraped_data= washington.main(scraped_data,request_) 
        elif InputParameters.get('WebsiteId')=="MASSACHUSETTS_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import massachusetts
            request_ =data
            request_['PatientData'] =[patient]  
            scraped_data= massachusetts.main(scraped_data,request_) 

        elif InputParameters.get('WebsiteId')=="COLORADO_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import coloradowrapper
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= coloradowrapper.main(scraped_data,request_) 
        elif InputParameters.get('WebsiteId')=="RHODEISLAND_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import rhodeIsland
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= rhodeIsland.main(scraped_data,request_)
            
        elif InputParameters.get('WebsiteId')=="OKLAHOMA_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import okalhama
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= okalhama.main(scraped_data,request_)

        elif InputParameters.get('WebsiteId')=="MISSOURI_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import missouriwrapper
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= missouriwrapper.main(scraped_data,request_)
            
        elif InputParameters.get('WebsiteId')=="IOWA_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import iowa
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= iowa.main(scraped_data,request_)            

        elif InputParameters.get('WebsiteId')=="OREGONALASKA_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import oregonAlaska
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= oregonAlaska.main(scraped_data,request_)     
        
        elif InputParameters.get('WebsiteId')=="NORTHEAST_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import maineHempshireVermont
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= maineHempshireVermont.main(scraped_data,request_)  

        elif InputParameters.get('WebsiteId')=="HAWAII_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import hawaiiwrapper
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= hawaiiwrapper.main(scraped_data,request_) 

        elif InputParameters.get('WebsiteId')=="Idaho_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import Idahowrapper
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= Idahowrapper.main(scraped_data,request_)  
        elif InputParameters.get('WebsiteId')=="WYOMING_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import Wyomingwrapper
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= Wyomingwrapper.main(scraped_data,request_)    
        elif InputParameters.get('WebsiteId')=="DENTAQUEST_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import dentaquestwrapper
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= dentaquestwrapper.main(scraped_data,request_)
        elif InputParameters.get('WebsiteId')=="MCNA_MEDICAD_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import mcnaMedicad
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= mcnaMedicad.main(scraped_data,request_) 
        elif InputParameters.get('WebsiteId')=="AETNA_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import aetna
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= aetna.main(scraped_data,request_)  
        elif InputParameters.get('WebsiteId')=="DDVIRGINIA_001" and InputParameters["AppName"]== "Eligibility":
            from wrapers import deltadentalvirginia
            request_ =data
            request_['PatientData'] =[patient] 
            scraped_data= deltadentalvirginia.main(scraped_data,request_)  
        return scraped_data             


    if  InputParameters['AppName']==   "Revenue Cycle Management":            
        if InputParameters['PayorName'] =="Dental Network of America":

            from wrapers import dnoaRCM
            scraped_data=dnoaRCM.main(scraped_data)
        if InputParameters['PayorName'] =="Delta Dental Toolkit": 
            from wrapers import  toolkitRCM                 
            scraped_data=toolkitRCM.main(scraped_data)     
                                        
        if InputParameters['PayorName'] =="United Concordia":
            from wrapers import ucRCM
            scraped_data=ucRCM.main(scraped_data)
                                                    
        if InputParameters['PayorName'] =="Delta Dental.Com":
            from wrapers import ddRCM
            scraped_data=ddRCM.main(scraped_data)   
            
        if InputParameters['PayorName'] =="Cigna":
            from wrapers import cignaRCM
            scraped_data=cignaRCM.main(scraped_data)

        if InputParameters['PayorName'] =="Delta Dental Ins":
            from wrapers import ddinsRCM
            scraped_data=ddinsRCM.main(scraped_data)

        if InputParameters['PayorName'] == "United Healthcare":
            from wrapers import uhcRCM
            scraped_data=uhcRCM.main(scraped_data,data)
        if InputParameters['PayorName'] == "Guardian":
            from wrapers import guardianRCM
            scraped_data=guardianRCM.main(scraped_data)    
        if InputParameters['PayorName'] == "Ameritas":                    
            from wrapers import ameritasRCM
            scraped_data=ameritasRCM.main(scraped_data)   
        if InputParameters['PayorName'] == "Principal":                    
            from wrapers import principalRCM
            scraped_data=principalRCM.main(scraped_data)
        if InputParameters['PayorName'] == "Delta Dental Illinois":
            from wrapers import lIllinoisRCM
            scraped_data=lIllinoisRCM.main(scraped_data)

        if InputParameters['PayorName'] == "Delta Dental Connecticut":
            from wrapers import DDconnecticutRCM
            scraped_data=DDconnecticutRCM.main(scraped_data)
        if InputParameters['PayorName'] == "Delta Dental of New Jersey":
            from wrapers import DDNewjearsyRCM
            scraped_data=DDNewjearsyRCM.main(scraped_data)
        if InputParameters['PayorName'] == "Delta Dental of Washington":
            from wrapers import DDWashingtonRCM
            scraped_data=DDWashingtonRCM.main(scraped_data)
        if InputParameters['PayorName'] == "Delta Dental of Oklahoma":
            from wrapers import DDOklahamaRCM
            scraped_data=DDOklahamaRCM.main(scraped_data)

        if InputParameters['PayorName'] == "Delta Dental of Colorado":
            from wrapers import DDColoradoRCM
            scraped_data=DDColoradoRCM.main(scraped_data)

        if InputParameters['PayorName'] == "Delta Dental Iowa":
            from wrapers import DDIowaRCM
            scraped_data=DDIowaRCM.main(scraped_data)
        if InputParameters['PayorName'] == "Delta Dental of Massachusetts":
            from wrapers import DDMA_RCM
            scraped_data=DDMA_RCM.main(scraped_data)    
        
        if InputParameters['PayorName'] in ["Delta Dental of Oregon", "Delta Dental Alaska"]:
            from wrapers import DDOregonAlaskaRCM
            scraped_data=DDOregonAlaskaRCM.main(scraped_data) 

        if InputParameters['PayorName'] == "Delta Dental New Hampshire":
            from wrapers import DDnortheastRCM
            scraped_data=DDnortheastRCM.main(scraped_data) 
        
        if InputParameters['PayorName'] == "Delta Dental of Missouri":
            from wrapers import DDmissouriRCM
            scraped_data=DDmissouriRCM.main(scraped_data)

        if InputParameters['PayorName'] == "Lincoln Financial":
            from wrapers import LincolnFinancialRCM
            scraped_data=LincolnFinancialRCM.main(scraped_data)
        
        if InputParameters['PayorName'] == "Sun Life":
            from wrapers import SunlifeRCM
            scraped_data=SunlifeRCM.main(scraped_data)

        if InputParameters['PayorName'] == "Delta Dental of Virgina":
            from wrapers import DDVirginiaRCM
            scraped_data=DDVirginiaRCM.main(scraped_data)
        
        if InputParameters['PayorName'] == "UMR":
            from wrapers import umrRCM
            scraped_data=umrRCM.main(scraped_data)

        if InputParameters['PayorName'] == "Managed Care of North America- MCNA":
            from wrapers import mcnaRCM
            scraped_data=mcnaRCM.main(scraped_data)

        if InputParameters['PayorName'] == "Delta Dental of Wisconsin":
            from wrapers import DDWisconsinRCM
            scraped_data = DDWisconsinRCM.main(scraped_data)

        if InputParameters['PayorName'] == "UNUM":
            from wrapers import UnumRCM
            scraped_data = UnumRCM.main(scraped_data)
        
        if InputParameters['PayorName'] == "DentaQuest":
            from wrapers import dentaquestRCM
            scraped_data=dentaquestRCM.main(scraped_data)        

        for i, claim in enumerate(scraped_data["RcmEobClaimMaster"], start=1):
            claim["RecordId"] = i
        for i, claim in enumerate(scraped_data["RcmEobClaimDetail"], start=1):
            claim["RecordId"] = i

    return scraped_data           