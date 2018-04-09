#coding:utf-8
__author__ = 'Administrator'

import base64
import M2Crypto
from share import logfile

keystring="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA54dIlq44FJP1WaWpUF1Z
I60W8mcZnK0ADr+dKe+bnjcjdztjjzeFzCQJGbDnfUzMrDXkep6SENNNVlZ7pl5V
bJOfaZHKiuD1mvrSQv8TybfixRmnBuJtEA6jKV1oKLnViR0vGQI2ty+1U04xRQcS
SZ+W+Y6ZnMwZLV6jBQsfPMmTUH4cCv6Nk98q3cT1h1xFA4+JMh9XmhG/bUWGKZIx
AQBJPbWWMnixZGlmNv9G67qP8QWy0vKbm+J7JYKayjDZXbss68+MHzjg6z5lcK4G
5NQ9+/2F6T5QQ8Qo5r9gBO0r/y1AZRC2jNWC7DyaVc85FxsTSmiqFOJYI2EIp76o
bwIDAQAB
-----END PUBLIC KEY-----"""
try:
    mb = M2Crypto.BIO.MemoryBuffer(keystring)
    rsa_pub=M2Crypto.RSA.load_pub_key_bio(mb)
except Exception as e:
    logfile.logger.exception(e.message)

class RSAKey(object):
    def _pub_encrypt(self,msg):
        # rsa_pub=M2Crypto.RSA.load_pub_key("pubkey.pem")
        b64_jiami=""
        try:
            jiami=rsa_pub.public_encrypt(msg,M2Crypto.RSA.pkcs1_padding)
            b64_jiami=base64.b64encode(jiami).decode("utf-8")
        except Exception as e:
            logfile.logger.exception(e.message)
        finally:
            return b64_jiami


    def _pub_decrypt(self,msg):
        # rsa_pub=M2Crypto.RSA.load_pub_key("pubkey.pem")
        jiemi=""
        try:
            jiemi_msg=base64.b64decode(msg)
            jiemi=rsa_pub.public_decrypt(jiemi_msg,M2Crypto.RSA.pkcs1_padding).decode("utf-8")
            jiemi=dict(eval(jiemi))
        except Exception as e:
            logfile.logger.exception(e.message)
        finally:
            return jiemi

class AESKey(object):
    def _aes_decrypt(self,aesKey,msg):
        buf=""
        try:
            jiemi_msg=base64.b64decode(msg.encode('utf-8'))
            # ENCRYPT_OP = 1 # 加密操作
            DECRYPT_OP = 0 # 解密操作
            iv='\0'*16
            aes_cipher=M2Crypto.EVP.Cipher(alg='aes_128_ecb', key=aesKey, iv=iv, op=DECRYPT_OP)
            aes_cipher.set_padding(padding=0) #默认padding=1
            buf=aes_cipher.update(jiemi_msg)
            buf=buf+aes_cipher.final()
            del aes_cipher
            buf=buf.decode("utf-8").rstrip('\0')
        except Exception as e:
            logfile.logger.exception(e.message)
        finally:
            return buf

    def _aes_encrypt(self,aesKey,msg):
        ENCRYPT_OP = 1 # 加密操作
        # DECRYPT_OP = 0 # 解密操作
        iv='\0'*16
        PADDING = '\0'
        b64_jiami=""
        try:
            pad_it = lambda s: s+(16 - len(s)%16)*PADDING
            aes_cipher=M2Crypto.EVP.Cipher(alg='aes_128_ecb', key=aesKey, iv=iv, op=ENCRYPT_OP)
            aes_cipher.set_padding(padding=0) # Nopadding方式
            buf=aes_cipher.update(pad_it(msg))
            buf=buf+aes_cipher.final()
            del aes_cipher
            #将明文从字节流转为base64
            b64_jiami=base64.b64encode(buf).decode("utf-8")
        except Exception as e:
            logfile.logger.exception(e.message)
        finally:
            return b64_jiami