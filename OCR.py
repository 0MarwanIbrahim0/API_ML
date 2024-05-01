import os
import cv2
from paddleocr import PPStructure
from PIL import Image
from matplotlib import pyplot as plt
import re, logging

table_engine = PPStructure(ocr_version='PP-OCRv4', lang='en')
os.makedirs('uploads', exist_ok=True)

list_abbraviation="MCHC|RDW|HGB|HCT||WBC|age|bp|sg|al|su|rbc|pc|pcc|ba|bgr|bu|sc|sod|pot|hemo|pcv|wc|rc|htn|dm|cad|appet|pe|aneage|bp|sg|al|su|rbc|pc|pcc|ba|bgr|bu|sc|sod|pot|hemo|pcv|wc|rc|htn|dm|cad|appet|pe|ane|A1A|A1c|AB|ABG|ABRH|ABT|ACA|ACE|ACID PHOS|ACP|ACT|ACTH|ADA|AFB|AFLM|AFP|AG|ALA|Alb|Alk Phos|ALP|ANA|Anti-HBc|Anti-HBe|Anti-HBs|Anti-HCV|APT|aPTT|ASN|ASO|AT III|B12|BMP|BNP|BUN|C1|C1Q|C2|C3|C4|Ca|CBC|CBCD|CEA|CH50|CK|Cl|CMB|CMP|CMV|CMV Ag|CO|CO2|COHB|CONABO|CPK|Cr|CRCL|CrCl|CRD|CREAT|CRP|Cu|D Bil|DAT|DCAS|DHEA|DHEAS|DIFM|Dig|EOS|EPO|ERA|ESR|ETOH|FBS|Fe|FEP|FFN|Fol|FSH|LH|FT3|FT4|G2PP|G-6-PD|Gamma GT|GCT|GDS|GGT|GH|Glu|H&H|Hapto|HbA1c|HBeAb|HBeAg|HBsAb|HBsAg|HBV titers|hCG|hCG|HCT|HDL|HFP|HGB|HgbA1c|HGH|HIAA|HIV|HPV|HSV|iCa|IEP|IFE|IgA|IgE|IGF|IgG|IgM|INR|Jo-1|KB|K|LD|LDH|LFT|LH|Mag|MIC|MMA|Mn|MONO|NA|NEOTY|NEOXM|NH3|NTR|PAP|Pb|PBG|PCP|PEP|PG|PHOS|PKU|PLT|PO4|PRL|PSA|PT|PTH|PTT|QIG|RBC|RF|RFP|RhIG"
def Read_Text(img: str) -> None:
    image = cv2.imread(img)
    result = table_engine(image)
    text = [item['text'] for line in result for item in line['res'] if isinstance(item, dict) and 'text' in item]
    print (text)
    pattern = fr"'(\b(?:{list_abbraviation})\b)(?:'\D*)(\d*.\d*)"
    matches = re.findall(pattern, str(text),re.IGNORECASE)
    data = {}
    for match in matches:
        key = match[0]
        value = match[1]
        data[key] = value
    return data
