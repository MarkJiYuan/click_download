from Crypto.Cipher import AES
import base64


class AES_crypt():
    def __init__(self, key, model=AES.MODE_ECB, iv=0):
        self.key = self.add_16(key)
        self.model = model
        self.iv = iv

    def add_16(self, par):
        if type(par) == str:
            par = par.encode()
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self, text):
        text = self.add_16(text)
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key, self.model, self.iv) 
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key, self.model) 
        encrypt_text = self.aes.encrypt(text)
        return encrypt_text

    def aesdecrypt(self, text):
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key,self.model,self.iv) 
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key,self.model) 
        decrypt_text = self.aes.decrypt(text)
        decrypt_text = decrypt_text.strip(b"\x00")
        return decrypt_text

def getcryptor():
    passwd = "123456781234567"
    cryptor = AES_crypt(passwd, AES.MODE_ECB, "")
    return cryptor


if __name__ == '__main__':
    passwd = "123456781234567"
    iv = '1234567812345678'

    aescryptor = AES_crypt(passwd, AES.MODE_CBC, iv) # CBC模式
    # aescryptor = AES_crypt(passwd,AES.MODE_ECB,"") # ECB模式
    text = "好好学习"
    en_text = aescryptor.aesencrypt(text)
    print(en_text)
    en_text = base64.b64encode(en_text)
    print(en_text)
    en_text = en_text.decode("utf-8")
    print(en_text)
    en_text = en_text.encode("utf-8")
    print(en_text)
    en_text = base64.b64decode(en_text)
    print(en_text)

    text = aescryptor.aesdecrypt(en_text)
    print("明文:",text.decode("utf-8"))




















