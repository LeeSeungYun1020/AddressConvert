import pandas as pd
import requests
import json

fileName = input("파일 이름을 입력하세요.")
addressIndex = input("주소 부분을 입력하세요.")
resultFileName = input("저장할 파일 이름을 입력하세요.")
keyFile = open("./key/juso.txt")
key = keyFile.readline()
keyFile.close()

df = pd.read_csv("./data/" + fileName)
count = 0
error = []
for (index, data) in df.iterrows():
    request = requests.get(f"https://www.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage=10"
                           f"&resultType=json&keyword={data[addressIndex]}&confmKey={key}")
    addressData = json.loads(request.text)
    if addressData["results"]["common"]["errorCode"] == "0" and len(addressData["results"]["juso"]) > 0:
        address = addressData["results"]["juso"][0]["roadAddr"]
        df.loc[index, addressIndex] = address
        count += 1
    else:
        error.append(index)
    print(f"변경 중 {index + 1}/{len(df)}({(index + 1) / len(df)}%)")
print(f"{count}/{index + 1}({count / (index + 1)}%)주소 변경을 완료하였습니다.")
df.to_csv(f"./data/{resultFileName}", index=False)
