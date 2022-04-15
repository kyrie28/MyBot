import requests
import re


class CharacterInfo:
    AvatarImgURL: str = None
    WorldName: str = None
    CharacterName: str = None
    Lev: str = None
    Exp: str = None
    Job: str = None
    JobDetail: str = None
    Pop: str = None
    TotRank: str = None
    WorldRank: str = None


def GetCharacterInfo(AccountID):
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetCharacterInfoByAccountID xmlns="https://api.maplestory.nexon.com/soap/">
      <AccountID>{AccountID}</AccountID>
    </GetCharacterInfoByAccountID>
  </soap12:Body>
</soap12:Envelope>"""
    url = "http://api.maplestory.nexon.com/soap/maplestory.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "Content-Length": str(len(xml)),
    }

    resp = requests.post(url, headers=headers, data=xml)

    result = CharacterInfo()
    result.AvatarImgURL = re.findall("<AvatarImgURL>(.*?)</AvatarImgURL>", resp.text)[0]
    result.WorldName = re.findall("<WorldName>(.*?)</WorldName>", resp.text)[0]
    result.CharacterName = re.findall(
        "<CharacterName>(.*?)</CharacterName>", resp.text
    )[0]
    result.Lev = re.findall("<Lev>(.*?)</Lev>", resp.text)[0]
    result.Exp = re.findall("<Exp>(.*?)</Exp>", resp.text)[0]
    result.Job = re.findall("<Job>(.*?)</Job>", resp.text)[0]
    result.JobDetail = re.findall("<JobDetail>(.*?)</JobDetail>", resp.text)[0]
    result.Pop = re.findall("<Pop>(.*?)</Pop>", resp.text)[0]
    result.TotRank = re.findall("<TotRank>(.*?)</TotRank>", resp.text)[0]
    result.WorldRank = re.findall("<WorldRank>(.*?)</WorldRank>", resp.text)[0]

    return result
