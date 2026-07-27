# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_GodKeys
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# A particularly simple AES simple encryption library poses a serious threat to the security of this project,
# The normal logic is to transmit the private key first,
# Store the public key locally, and other complex logic, instead of like this,
# It is too simple, and it will be changed when there is time.


from .T_imports import *
from . import T_Tools


class GodKeys:
    def __init__(self, key: bytes | None = None) -> None:
        self.key: bytes = key if key else b"TerminationGodKeyAndLOVE3GZSorry"
        self.AESGCM: AESGCM = AESGCM(self.key)
    def IsGK(self, data: bytes | str) -> bool:
        if isinstance(data, bytes):
            return len(data) >= 28 and data[:4] == b"GKBD"
        elif isinstance(data, str):
            return len(data) >= 56 and data.startswith("GKBD")
        return False
    def encrypt(self, s: str) -> bytes:
        nonce: bytes = os.urandom(12)
        ciphertext: bytes = self.AESGCM.encrypt(nonce, repr(s).encode(), None)
        return b"GKBD" + nonce + ciphertext
    def decrypt(self, s: bytes, con: bool = False) -> str:
        if not self.IsGK(s):
            return s if con else Exception("Invalid GKBD format")
        nonce: bytes
        ciphertext: bytes
        nonce, ciphertext = s[4:16], s[16:]
        try:
            plaintext: str = self.AESGCM.decrypt(nonce, ciphertext, None)
            return ast.literal_eval(plaintext.decode())
        except (ValueError, SyntaxError):
            return plaintext.decode() if con else Exception("Invalid data")
    def encrypt_16(self, s: str) -> str:
        binary: bytes = self.encrypt(s)
        return "GKBD" + binary[4:].hex()
    def decrypt_16(self, s: str, con: bool = False) -> str:
        if not self.IsGK(s):
            return s if con else Exception("Invalid GKBD hex format")
        try:
            binary: bytes = b"GKBD" + bytes.fromhex(s[4:])
            return self.decrypt(binary, con)
        except ValueError:
            return s if con else Exception("Invalid hex data")

class SecureHybridEncryption:
    def __init__(self, PublicExponent: int = 65537, KeySize: int = 2048, Backend: typing.Callable = default_backend):
        self.__init_key__(PublicExponent, KeySize, Backend)
    def __init_key__(self, PublicExponent: int = 65537, KeySize: int = 2048, Backend: typing.Callable = default_backend):
        self.PrivateKey: rsa.RSAPrivateKey = self.CreatePrivateKey(PublicExponent, KeySize, Backend)
        self.PublicKey: rsa.RSAPublicKey = self.CreatePublicKey(self.PrivateKey)
    @staticmethod
    def CreatePrivateKey(PublicExponent: int = 65537, KeySize: int = 2048, Backend: typing.Callable = default_backend) -> rsa.RSAPrivateKey:
        return rsa.generate_private_key(
            public_exponent=PublicExponent,
            key_size=KeySize,
            backend=Backend()
        )
    @staticmethod
    def CreatePublicKey(PrivateKey: rsa.RSAPrivateKey) -> rsa.RSAPublicKey:
        return PrivateKey.public_key()
    @staticmethod
    def SerializePublicKey(PublicKey: rsa.RSAPublicKey,
                           Encoding: serialization.Encoding = serialization.Encoding.DER,
                           Format: serialization.PublicFormat = serialization.PublicFormat.SubjectPublicKeyInfo) -> bytes:
        return PublicKey.public_bytes(encoding = Encoding, format = Format)
    @staticmethod
    def LoadPublicKey(PublicKeyBytes: bytes, Backend: typing.Callable = default_backend) -> rsa.RSAPublicKey:
        return serialization.load_pem_public_key(PublicKeyBytes, backend = Backend())
    @staticmethod
    def LoadDERPublicKey(PublicKeyBytes: bytes, Backend: typing.Callable = default_backend) -> rsa.RSAPublicKey:
        return serialization.load_der_public_key(PublicKeyBytes, backend = Backend())
    @staticmethod
    def SerializePrivateKey(PrivateKey: rsa.RSAPrivateKey, Password: str | None = None, 
                           Encoding: serialization.Encoding = serialization.Encoding.DER,
                           Format: serialization.PrivateFormat = serialization.PrivateFormat.PKCS8, 
                           EncryptionAlgorithm: typing.Callable = serialization.NoEncryption) -> bytes:
        if Password:
            EncryptionAlgorithm = serialization.BestAvailableEncryption(Password.encode())
        return PrivateKey.private_bytes(
            encoding = Encoding,
            format = Format,
            encryption_algorithm = EncryptionAlgorithm()
        )
    @staticmethod
    def LoadPrivateKey(PrivateKeyBytes: bytes, Password: str | None = None, Backend: typing.Callable = default_backend) -> rsa.RSAPrivateKey:
        return serialization.load_pem_private_key(data = PrivateKeyBytes, password = Password.encode() if Password else None, backend = Backend())
    @staticmethod
    def LoadDERPrivateKey(PrivateKeyBytes: bytes, Password: str | None = None, Backend: typing.Callable = default_backend) -> rsa.RSAPrivateKey:
        return serialization.load_der_private_key(data = PrivateKeyBytes, password = Password.encode() if Password else None, backend = Backend())
    @staticmethod
    def EncryptLargeData(PublicKey: rsa.RSAPublicKey, Data: bytes, AesKey: bytes | None = None, 
                         Iv: bytes | None = None, Backend: typing.Callable = default_backend) -> tuple[dict[str, bytes], bytes]:
        AesKey = AesKey if AesKey else os.urandom(32)
        Iv = Iv if Iv else os.urandom(16)
        _Cipher = Cipher(algorithms.AES(AesKey), modes.GCM(Iv), backend = Backend())
        Encryptor = _Cipher.encryptor()
        EncryptedData = Encryptor.update(Data) + Encryptor.finalize()
        EncryptedAesKey = PublicKey.encrypt(
            AesKey,
            padding.OAEP(
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )
        DataPackage = {'Data': EncryptedData, 'Iv': Iv, 'Tag': Encryptor.tag}
        return DataPackage, EncryptedAesKey
    @staticmethod
    def DecryptLargeData(PrivateKey: rsa.RSAPrivateKey, DataPackage: dict[str, bytes], EncryptedAesKey: bytes, 
                         AesKey: bytes | None = None, Backend: typing.Callable = default_backend) -> bytes:
        AesKey = AesKey if AesKey else PrivateKey.decrypt(
            EncryptedAesKey,
            padding.OAEP(
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )
        _Cipher = Cipher(
            algorithms.AES(AesKey),
            modes.GCM(DataPackage['Iv'], DataPackage['Tag']),
            backend = Backend()
        )
        Decryptor = _Cipher.decryptor()
        return Decryptor.update(DataPackage['Data']) + Decryptor.finalize()
    @staticmethod
    def Encrypt(Data: str | bytes | dict, PublicKey: str | rsa.RSAPublicKey, AesKey: bytes | None = None, 
                Iv: bytes | None = None, Backend: typing.Callable = default_backend) -> bytes:
        if isinstance(PublicKey, str): PublicKey = SecureHybridEncryption.LoadPublicKey(PublicKeyBytes=PublicKey.encode(), Backend=Backend)
        if isinstance(Data, dict): Data = json.dumps(Data).encode('utf-8')
        elif isinstance(Data, str): Data = Data.encode('utf-8')
        DataPackage, EncryptedKey = SecureHybridEncryption.EncryptLargeData(
            PublicKey = PublicKey,
            Data = Data,
            AesKey = AesKey,
            Iv = Iv,
            Backend = Backend
        )
        return T_Tools.CombineBytesPrefixed([
            b"TRSA10\x00\x00\n",
            b"This Is Nonsensical Gibberish Until U Can Find Its Corresponding Key.\x00\x00\n",
            EncryptedKey,
            DataPackage['Iv'],
            DataPackage['Tag'],
            DataPackage['Data']
        ])
    @staticmethod
    def Decrypt(Data: bytes, PrivateKey: str | rsa.RSAPrivateKey, Password: str | None = None, 
                AesKey: bytes | None = None, Backend: typing.Callable = default_backend) -> bytes | dict:
        try:
            if isinstance(PrivateKey, str):
                PrivateKey = SecureHybridEncryption.LoadPrivateKey(
                    PrivateKeyBytes = PrivateKey.encode(),
                    Password = Password,
                    Backend = Backend
                )
            Segments = T_Tools.SplitBytesPrefixed(Data)
            if len(Segments) < 6:
                raise ValueError("Invalid encrypted data format")
            DataPackage = {"Iv": Segments[3], "Tag": Segments[4], "Data": Segments[5]}
            EncryptedKey = Segments[2]
            DecryptedData = SecureHybridEncryption.DecryptLargeData(
                PrivateKey = PrivateKey,
                DataPackage = DataPackage,
                EncryptedAesKey = EncryptedKey,
                AesKey = AesKey,
                Backend = Backend
            )
            try: return json.loads(DecryptedData.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError): return DecryptedData
        except:
            return False

'''
You can delete this comment after the code test above is completed.
class SecureHybridEncryption:
    def __init__(self, PublicExponent: int = 65537, KeySize: int = 2048, Backend: typing.Callable = default_backend):
        self.__init_key__(PublicExponent, KeySize, Backend)
    def __init_key__(self, PublicExponent: int = 65537, KeySize: int = 2048, Backend: typing.Callable = default_backend):
        self.PrivateKey: rsa.RSAPrivateKey = self.CreatePrivateKey(PublicExponent, KeySize, Backend)
        self.PublicKey: rsa.RSAPublicKey = self.CreatePublicKey(self.PrivateKey)
    @staticmethod
    def CreatePrivateKey(PublicExponent: int  = 65537, KeySize: int = 2048, Backend: typing.Callable = default_backend) -> rsa.RSAPrivateKey:
        return rsa.generate_private_key(public_exponent = PublicExponent, key_size = KeySize, backend = Backend())
    @staticmethod
    def CreatePublicKey(PrivateKey: rsa.RSAPrivateKey) -> rsa.RSAPublicKey:
        return PrivateKey.public_key()
    def SerializePublicKey(self, Encoding: serialization.Encoding = serialization.Encoding.PEM, Format: serialization.PublicFormat = serialization.PublicFormat.SubjectPublicKeyInfo):
        return self.PublicKey.public_bytes(encoding = Encoding, format = Format)
    @staticmethod
    def LoadPublicKey(PublicKeyBytes, Backend: typing.Callable = default_backend):
        return serialization.load_pem_public_key(PublicKeyBytes, backend = Backend())
    def SerializePrivateKey(self, Password: str | None = None, Encoding: serialization.Encoding = serialization.Encoding.PEM, Format: serialization.PrivateFormat = serialization.PrivateFormat.PKCS8, EncryptionAlgorithm: typing.Callable = serialization.NoEncryption):
        if Password: EncryptionAlgorithm = serialization.BestAvailableEncryption(Password.encode())
        return self.PrivateKey.private_bytes(encoding = Encoding, format = Format, encryption_algorithm = EncryptionAlgorithm())
    @staticmethod
    def LoadPrivateKey(PrivateKeyBytes, Password: str | None = None, Backend: typing.Callable = default_backend):
        return serialization.load_pem_private_key(data = PrivateKeyBytes, password = Password.encode() if Password else None, backend = Backend())
    @staticmethod
    def EncryptLargeData(PublicKey: rsa.RSAPublicKey, Data, AesKey: bytes | None = None, Iv: bytes | None = None, Backend: typing.Callable = default_backend):
        AesKey = AesKey if AesKey else os.urandom(16)
        Iv = Iv if Iv else os.urandom(16)
        cipher = Cipher(algorithms.AES(AesKey), modes.GCM(Iv), backend = Backend())
        Encryptor = cipher.encryptor()
        EncryptedData = Encryptor.update(Data) + Encryptor.finalize()
        EncryptedAesKey = PublicKey.encrypt(AesKey, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
        DataPackage = {'Data': EncryptedData, 'Iv': Iv, 'Tag': Encryptor.tag}
        return DataPackage, EncryptedAesKey
    @staticmethod
    def DecryptLargeData(PrivateKey: rsa.RSAPrivateKey, DataPackage: dict[str, bytes], EncryptedAesKey, AesKey: bytes | None = None, Backend: typing.Callable = default_backend):
        AesKey = AesKey if AesKey else PrivateKey.decrypt(EncryptedAesKey, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
        cipher = Cipher(algorithms.AES(AesKey), modes.GCM(DataPackage['Iv'], DataPackage['Tag']), backend = Backend())
        Decryptor = cipher.decryptor()
        return Decryptor.update(DataPackage['Data']) + Decryptor.finalize()
    @staticmethod
    def Encrypt(Text: str | bytes, PublicKey: str | rsa.RSAPublicKey, AesKey: bytes | None = None, Iv: bytes | None = None, Backend: typing.Callable = default_backend):
        if type(PublicKey) == str: PublicKey: rsa.RSAPublicKey = SecureHybridEncryption.LoadPublicKey(PublicKeyBytes = PublicKey, Backend = Backend)
        DataPackage, EncryptedKey = SecureHybridEncryption.EncryptLargeData(PublicKey = PublicKey, Text = Text, AesKey = AesKey, Iv = Iv, Backend = Backend)
        return CombineBytesPrefixed([b"TRSA10\x00\x00\n", b"This Is Nonsensical Gibberish Until U Can Find Its Corresponding Key.\x00\x00\n", EncryptedKey, DataPackage['Iv'], DataPackage['Tag'], DataPackage['Data']])
    @staticmethod
    def Decrypt(Data: bytes, PrivateKey: str | rsa.RSAPrivateKey, Password: str | None = None, AesKey: bytes | None = None, Backend: typing.Callable = default_backend):
        if type(PrivateKey) == str: PrivateKey: rsa.RSAPrivateKey = SecureHybridEncryption.LoadPrivateKey(PrivateKeyBytes = PrivateKey, Password = Password, Backend = Backend)
        _: list[bytes] = SplitBytesPrefixed(Data)
        DataPackage: dict[str, bytes] = {"Iv": _[3], "Tag": _[4], "Data": _[5]}
        EncryptedKey: bytes = _[2]
        return SecureHybridEncryption.DecryptLargeData(PrivateKey, DataPackage, EncryptedKey, AesKey = AesKey, Backend = Backend)
'''