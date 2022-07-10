import pandas as pd
import requests
import json

fileName = input("파일 이름을 입력하세요. (ex: file.csv)")
addressIndex = input("주소 부분 필드명을 입력하세요. (ex: addr1)")
resultFileName = input("저장할 파일 이름을 입력하세요. (ex: result.csv)")
resultAddressIndex = input("저장할 파일에서 주소 필드명을 입력하세요. (ex: address)")
if fileName == "":
    fileName = "file.csv"
if addressIndex == "":
    addressIndex = "addr1"
if resultFileName == "":
    resultFileName = "result.csv"
if resultAddressIndex == "":
    resultAddressIndex = "address"

keyFile = open("./key/juso.txt")
key = keyFile.readline()
keyFile.close()

df = pd.read_csv("./data/" + fileName)
df[resultAddressIndex] = ""
count = 0
error = []
for (index, data) in df.iterrows():
    request = requests.get(f"https://www.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage=10"
                           f"&resultType=json&keyword={data[addressIndex]}&confmKey={key}")
    addressData = json.loads(request.text)
    if addressData["results"]["common"]["errorCode"] == "0" and len(addressData["results"]["juso"]) > 0:
        address = addressData["results"]["juso"][0]["roadAddr"]
        df.loc[index, resultAddressIndex] = address
        count += 1
    else:
        error.append(index)
    print(f"변경 중 {index + 1}/{len(df)}({(index + 1) / len(df) * 100}%)")
print(f"{count}/{index + 1}({count / (index + 1) * 100}%) 주소 변경을 완료하였습니다.")
df.to_csv(f"./data/{resultFileName}", index=False)
