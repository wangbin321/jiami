import pandas as pd
import base64
from Crypto.Cipher import AES

class EncryptData(object):
    def __init__(self, key):
        self.key = key.encode("utf8")  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        '''
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        '''
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData): # 解密函数
            decrData=str(decrData)

            res = base64.decodebytes(decrData.encode("utf8"))
            msg = self.aes.decrypt(res).decode("utf8")
            return self.unpad(msg)





def handwritingClassTest(path):

    eg = EncryptData("!@#qwedsazxc@!@#")
    if path.endswith("xlsx"):

       df = pd.read_excel(path)
    else:
       df=pd.read_csv(path)
    cols=df.columns
    for col in list(cols):
        df[col] = df[col].map(lambda s: eg.decrypt(str(s)))
    return df


if __name__ == '__main__':
    import os
    path=os.getcwd()
    for root, dirs, files in os.walk(path):
        for i in files:
            if i.endswith("xlsx"):
                input_file=os.path.join(root, i)
                data = handwritingClassTest(input_file)
                output_file = input_file.replace(".xlsx", "-decrypt.xlsx")
                data.to_excel(output_file, index=False)
            if i.endswith("csv"):
                input_file = os.path.join(root, i)
                data = handwritingClassTest(input_file)
                output_file = input_file.replace(".csv", "-decrypt.csv")
                data.to_excel(output_file, index=False)




