import win32com.client
import time


def TTS(Text, Rate=2, Volume=100, SleepTime: int = 0):
    Speaker = win32com.client.Dispatch("SAPI.SpVoice")
    Speaker.Rate = Rate
    Speaker.Volume = Volume
    Speaker.Speak(Text)
    time.sleep(SleepTime)

if __name__ == "__main__":
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    print(f"系统中可用的语音: {len(voices)} 种")
    for i, voice in enumerate(voices):
        print(f"{i+1}. {voice.GetDescription()}")
    
    # 可以调整语速和音量
    # text_to_speech("这是语速较慢的演示", rate=-2, volume=80)
class PlanS():
    def __init__(self):
        self.PassTest = False
    def Test(self):
        try: 
            TTS("""正在进行语音测试...""")
            self.PassTest = True
        except:
            self.PassTest = False
    def Start(self):
        self.Test()
        if not self.PassTest:
            print("语音环境测试失败...")
        time.sleep(1)
        TTS("正在进行环境探测")
        TTS("设备符合运行要求")
        TTS("重置中", 0.5)
        TTS("正在尝试与服务器重新构建安全连接", 0.5)
        TTS("""# **Understanding RSA Encryption: A Comprehensive Guide**

## **Introduction**
RSA (Rivest-Shamir-Adleman) is one of the first and most widely used public-key cryptosystems, named after its inventors: Ron Rivest, Adi Shamir, and Leonard Adleman. It enables secure data transmission over insecure channels and is fundamental in modern cryptography, used in SSL/TLS, digital signatures, and secure communications.

---

## **How RSA Works**
RSA relies on the mathematical properties of large prime numbers and modular arithmetic. The process involves three main steps: key generation, encryption, and decryption.

### **1. Key Generation**
- **Choose two distinct large prime numbers (p and q)**
These primes should be kept secret and are typically very large (hundreds of digits).

- **Compute n = p × q**
`n` is the modulus used in both public and private keys.

- **Compute Euler's totient function: φ(n) = (p-1)(q-1)**
This function counts integers up to `n` that are coprime with `n`.

- **Choose an integer e (public exponent) such that:**
- `1 < e < φ(n)`
- `gcd(e, φ(n)) = 1` (i.e., `e` and `φ(n)` are coprime)
Common choices for `e` are 3, 5, or 65537 (for efficiency in encryption).

- **Compute d (private exponent) as the modular inverse of e:**
`d ≡ e⁻¹ mod φ(n)`
This means `(e × d) mod φ(n) = 1`.

- **Public Key: (e, n)** – Shared openly.
- **Private Key: (d, n)** – Kept secret.

### **2. Encryption**
To encrypt a message `M` (represented as an integer where `0 ≤ M < n`), the sender uses the recipient's public key `(e, n)` to compute:
`C ≡ Mᵉ mod n`
`C` is the ciphertext.

### **3. Decryption**
The recipient uses their private key `(d, n)` to recover the original message:
`M ≡ Cᵈ mod n`

---

## **Why RSA is Secure**
The security of RSA depends on the **factoring problem**:
- An attacker who knows `n` must factorize it into `p` and `q` to compute `φ(n)` and derive `d`.
- Factoring large numbers is computationally infeasible with classical computers (though Shor's algorithm on quantum computers poses a future threat).

---

## **Example (Simplified)**
Let’s choose small primes for demonstration:
- **p = 61, q = 53**
- **n = 61 × 53 = 3233**
- **φ(n) = (61-1)(53-1) = 3120**
- **Choose e = 17** (since `gcd(17, 3120) = 1`)
- **Compute d ≡ 17⁻¹ mod 3120 = 2753** (since `17 × 2753 mod 3120 = 1`)

**Keys:**
- Public Key: `(e=17, n=3233)`
- Private Key: `(d=2753, n=3233)`

**Encrypting "M = 65":**
`C ≡ 65¹⁷ mod 3233 = 2790`

**Decrypting "C = 2790":**
`M ≡ 2790²⁷⁵³ mod 3233 = 65`

The original message is recovered!

---

## **Practical Considerations**
- **Key Size**: Modern RSA uses 2048-bit or 4096-bit keys to resist brute-force attacks.
- **Padding (OAEP)**: Raw RSA is deterministic and insecure; padding schemes like OAEP add randomness.
- **Performance**: RSA is slower than symmetric encryption (e.g., AES), so hybrid systems (RSA + AES) are common.
- **Quantum Threat**: Shor’s algorithm can break RSA if large-scale quantum computers exist, prompting post-quantum cryptography research.

---

## **Conclusion**
RSA remains a cornerstone of secure communications despite emerging threats. Its elegance lies in the simplicity of its mathematical foundation and its robustness when properly implemented. Understanding RSA is essential for anyone interested in cryptography and cybersecurity.

Would you like a deeper dive into any specific aspect of RSA?""")

PlanS().Start()