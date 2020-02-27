import sys
import requests
import xml.etree.ElementTree as ElementTree
import pandas as pd
import numpy as np
import time


PostUrl = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
XmlRaw = "<map id=\"ATTABZAA001R08\"><pubcUserNo/><mobYn>N</mobYn><inqrTrgtClCd>1</inqrTrgtClCd><txprDscmNo>\{CRN\}</txprDscmNo><dongCode>15</dongCode><psbSearch>Y</psbSearch><map id=\"userReqInfoVO\"/></map>"


def call(crn):
    res = requests.post(PostUrl, data=XmlRaw.replace("\{CRN\}", crn), headers={'Content-Type': 'text/xml'})
    xml = ElementTree.fromstring(res.text).findtext("trtCntn")
    result = crn + "\t" + xml.replace("\n", "").replace("\t", " ") + "\n"

    output = ['', '', '', '']
    output[0] = result[:10]

    description = result[10:]

    # Normal cases
    if len(description.split()) == 3:
        output[1] = ' '.join(description.split()[:-1])

    else:
        # Cases with 2 dates
        if '*' in description:

            if '간이과세자' in description:
                output[1] = ' '.join(description.split()[:2])
            else:
                output[1] = description.split()[0]

            output[2] = description.split()[4][5:-1]
            output[3] = description[-19:-6]

        else:
            #case with one date
            output[1] = description.split()[0]
            output[2] = result.split()[-2][5:-1]

    return output

def fetch_from_text(reg_list):

    results = []
    now = time.time()
    for index, item in enumerate(reg_list):
        results.append(call(item))
        if index % 50 == 0:
            print("{} data processed".format(index))
            print("Time enlapsed: {}s".format(time.time() - now))

    results = pd.DataFrame(results, columns=['사업자등록번호', '과세유형', '폐업일', '과세유형 전환일자'])
    results.to_excel('results.xlsx', index=False)
    return results


inputs = open('dataset.txt', 'r', encoding='UTF8')
fetch_from_text(inputs)



