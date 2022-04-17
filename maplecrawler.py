from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import maplerefs


def get_character_info(charName):
    charInfo = {}

    encodedCharName = parse.quote(charName)
    mapleURL = "https://maplestory.nexon.com"
    html = urlopen(mapleURL + f"/Ranking/World/Total?c={encodedCharName}&w=0")
    bsObject = BeautifulSoup(html, "html.parser")

    path = ""
    for elem in bsObject.find_all("a"):
        href = elem.get("href")
        if (
            elem.text.strip().lower() == charName.lower()
            and href
            and href.startswith("/Common/Character/Detail")
        ):
            path = href
            break

    if not path:
        return charInfo

    html = urlopen(mapleURL + path)
    bsObject = BeautifulSoup(html, "html.parser")

    for img in bsObject.find_all("img"):
        src = img.get("src")
        if src.startswith("https://avatar.maplestory.nexon.com"):
            charInfo["캐릭터 이미지"] = src
            break

    for elem in bsObject.find_all("dl"):
        text = elem.text.strip()
        if text:
            if text.startswith("LV."):
                charInfo["레벨"] = text[3:]
            elif "/" in text:
                charInfo["직업"] = text[text.index("/") + 1 :]
            else:
                charInfo["월드"] = text

    elems = bsObject.find_all("span")
    idx = 0
    while idx < len(elems) - 1:
        key = elems[idx].text.strip()
        value = elems[idx + 1].text.strip()

        if key.lower() == charName.lower() + "님":
            charInfo["이름"] = key[:-1]
        elif (
            key.startswith(("경험치", "인기도"))
            and not key[3:] == "님"
            and not key[:3] in charInfo
        ):
            charInfo[key[:3]] = key[3:]

        # 여기에서부터는 캐릭터 정보 공개를 하지 않으면 값을 얻을 수 없음
        elif key.endswith("어빌리티"):
            for br in elems[idx + 1].find_all("br"):
                br.replace_with("\n")
            charInfo[key[-4:]] = elems[idx + 1].text.strip()
            idx += 1

        elif key == "하이퍼스탯":
            for br in elems[idx + 1].find_all("br"):
                br.replace_with("\n")
            charInfo[key] = elems[idx + 1].text.strip()
            idx += 1

        else:
            for ref_key in maplerefs.crawl_keys:
                if key == ref_key and not key in charInfo:
                    charInfo[key] = value
                    idx += 1

        idx += 1

    return charInfo


def main():
    print("캐릭터 이름을 입력하세요: ")
    result = get_character_info(input().strip())
    if result:
        print(result)
    else:
        print("캐릭터가 존재하지 않습니다.")
