# 🔐 CryptoHack 現代密碼學全挑戰題庫目錄 (CryptoHack Challenge Catalog)

> 本目錄自動同步自 [CryptoHack](https://cryptohack.org/) 官方挑戰區，收錄全部 14 大核心分類、300+ 道現代密碼學關卡。
> **所有題目 100% 免費開放**，涵蓋對稱加密 (AES)、公鑰密碼 (RSA/Diffie-Hellman)、橢圓曲線 (ECC)、雜湊函式與後量子密碼學。

**同步題數統計**: 共收錄 `308` 道實戰關卡（🟢 全部 100% 免費）。

---

## 📊 一、 分類與難度分佈矩陣

| 主題領域 (Category) | 題目數量 | 難度分佈 | 代表知識點 |
| :--- | :--- | :--- | :--- |
| **Introduction** | 3 | Easy:3 | Med:0 | Hard:0 | Ins:0 | Beginner onboarding and flag submission basics |
| **General** | 19 | Easy:7 | Med:11 | Hard:1 | Ins:0 | Data formats, XOR operations, mathematics foundations |
| **Mathematics** | 15 | Easy:0 | Med:4 | Hard:3 | Ins:8 | Modular arithmetic, lattices, quadratic residues |
| **Diffie-Hellman** | 14 | Easy:1 | Med:4 | Hard:4 | Ins:5 | Discrete log, MITM, parameter injection, group theory |
| **RSA** | 29 | Easy:3 | Med:9 | Hard:7 | Ins:10 | Public key crypto, factorization attacks, padding oracles, Wiener's attack |
| **Block Ciphers (AES)** | 27 | Easy:4 | Med:3 | Hard:13 | Ins:7 | ECB, CBC, OFB, CTR, padding oracle, GCM vulnerabilities |
| **Elliptic Curves** | 23 | Easy:2 | Med:4 | Hard:5 | Ins:12 | ECDSA, curve parameters, invalid curve attacks, Montgomery curves |
| **Hash Functions** | 14 | Easy:0 | Med:3 | Hard:4 | Ins:7 | MD5, SHA, collision attacks, length extension, HMAC |
| **Crypto on the Web** | 17 | Easy:5 | Med:8 | Hard:0 | Ins:4 | JWT forgery, token manipulation, TLS/SSL weaknesses |
| **Post-Quantum** | 18 | Easy:5 | Med:5 | Hard:4 | Ins:4 | Lattice-based cryptography, Kyber, Dilithium fundamentals |
| **Isogenies** | 23 | Easy:1 | Med:8 | Hard:7 | Ins:7 | Supersingular isogeny Diffie-Hellman and supersingular curves |
| **Zero Knowledge** | 17 | Easy:1 | Med:4 | Hard:4 | Ins:8 | Interactive proofs, Sigma protocols, Schnorr identification |
| **Miscellaneous** | 14 | Easy:0 | Med:1 | Hard:0 | Ins:13 | Interactive algorithmic crypto, esoteric cipher systems |
| **CTF Archive** | 75 | Easy:75 | Med:0 | Hard:0 | Ins:0 | Past CryptoHack CTF and wargame challenge archive |

---

## 📚 二、 各分類題庫詳細清單

### 📌 Introduction（3 Challenges）
*Beginner onboarding and flag submission basics*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Finding Flags** | 2 | `Easy` | 110,604 | [前往解題](https://cryptohack.org/challenges/introduction/) | Each challenge is designed to help introduce you to a new piece of cryptography. Solving a... |
| **Great Snakes** | 3 | `Easy` | 93,305 | [前往解題](https://cryptohack.org/challenges/introduction/) | Modern cryptography involves code, and code involves coding. CryptoHack provides a good op... |
| **Network Attacks** | 5 | `Easy` | 33,824 | [前往解題](https://cryptohack.org/challenges/introduction/) | Several of the challenges are dynamic and require you to talk to our challenge servers ove... |

### 📌 General（19 Challenges）
*Data formats, XOR operations, mathematics foundations*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ASCII** | 5 | `Easy` | 85,903 | [前往解題](https://cryptohack.org/challenges/general/) | ASCII is a 7-bit encoding standard which allows the representation of text using the integ... |
| **Hex** | 5 | `Easy` | 79,911 | [前往解題](https://cryptohack.org/challenges/general/) | When we encrypt something the resulting ciphertext commonly has bytes which are not printa... |
| **Base64** | 10 | `Easy` | 72,866 | [前往解題](https://cryptohack.org/challenges/general/) | Another common encoding scheme is Base64, which allows us to represent binary data as an A... |
| **Bytes and Big Integers** | 10 | `Easy` | 60,229 | [前往解題](https://cryptohack.org/challenges/general/) | Cryptosystems like RSA works on numbers, but messages are made up of characters. How shoul... |
| **Encoding Challenge** | 40 | `Medium` | 16,064 | [前往解題](https://cryptohack.org/challenges/general/) | Now you've got the hang of the various encodings you'll be encountering, let's have a look... |
| **XOR Starter** | 10 | `Easy` | 52,652 | [前往解題](https://cryptohack.org/challenges/general/) | XOR is a bitwise operator which returns 0 if the bits are the same, and 1 otherwise. In te... |
| **XOR Properties** | 15 | `Easy` | 44,771 | [前往解題](https://cryptohack.org/challenges/general/) | In the last challenge, you saw how XOR worked at the level of bits. In this one, we're goi... |
| **Favourite byte** | 20 | `Medium` | 42,852 | [前往解題](https://cryptohack.org/challenges/general/) | For the next few challenges, you'll use what you've just learned to solve some more XOR pu... |
| **You either know, XOR you don&#39;t** | 30 | `Medium` | 37,826 | [前往解題](https://cryptohack.org/challenges/general/) | I've encrypted the flag with my secret key, you'll never be able to guess it. Remember the... |
| **Lemur XOR** | 40 | `Medium` | 13,199 | [前往解題](https://cryptohack.org/challenges/general/) | I've hidden two cool images by XOR with the same secret key so you can't see them! This ch... |
| **Greatest Common Divisor** | 15 | `Easy` | 36,199 | [前往解題](https://cryptohack.org/challenges/general/) | The Greatest Common Divisor (GCD), sometimes known as the highest common factor, is the la... |
| **Extended GCD** | 20 | `Medium` | 29,935 | [前往解題](https://cryptohack.org/challenges/general/) | Let $a$ and $b$ be positive integers. The extended Euclidean algorithm is an efficient way... |
| **Modular Arithmetic 1** | 20 | `Medium` | 29,556 | [前往解題](https://cryptohack.org/challenges/general/) | Imagine you lean over and look at a cryptographer's notebook. You see some notes in the ma... |
| **Modular Arithmetic 2** | 20 | `Medium` | 28,017 | [前往解題](https://cryptohack.org/challenges/general/) | We'll pick up from the last challenge and imagine we've picked a modulus $p$, and we will ... |
| **Modular Inverting** | 25 | `Medium` | 26,903 | [前往解題](https://cryptohack.org/challenges/general/) | As we've seen, we can work within a finite field $\Fp$, adding and multiplying elements, a... |
| **Privacy-Enhanced Mail?** | 25 | `Medium` | 9,678 | [前往解題](https://cryptohack.org/challenges/general/) | As we've seen in the encoding section, cryptography involves dealing with data in a wide v... |
| **CERTainly not** | 30 | `Medium` | 8,735 | [前往解題](https://cryptohack.org/challenges/general/) | As mentioned in the previous challenge, PEM is just a nice wrapper above DER encoded ASN.1... |
| **SSH Keys** | 35 | `Medium` | 6,880 | [前往解題](https://cryptohack.org/challenges/general/) | Secure Shell Protocol (SSH) is a network protocol that uses cryptography to establish a se... |
| **Transparency** | 50 | `Hard` | 6,936 | [前往解題](https://cryptohack.org/challenges/general/) | CryptoHack challenge in General (50 pts). |

### 📌 Mathematics（15 Challenges）
*Modular arithmetic, lattices, quadratic residues*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Quadratic Residues** | 25 | `Medium` | 21,832 | [前往解題](https://cryptohack.org/challenges/maths/) | We've looked at multiplication and division in modular arithmetic, but what does it mean t... |
| **Legendre Symbol** | 35 | `Medium` | 17,190 | [前往解題](https://cryptohack.org/challenges/maths/) | In Quadratic Residues we learnt what it means to take the square root modulo an integer. W... |
| **Modular Square Root** | 35 | `Medium` | 14,547 | [前往解題](https://cryptohack.org/challenges/maths/) | In Legendre Symbol we introduced a fast way to determine whether a number is a square root... |
| **Chinese Remainder Theorem** | 40 | `Medium` | 14,958 | [前往解題](https://cryptohack.org/challenges/maths/) | The Chinese Remainder Theorem gives a unique solution to a set of linear congruences if th... |
| **Successive Powers** | 60 | `Hard` | 5,065 | [前往解題](https://cryptohack.org/challenges/maths/) | The following integers: $\{588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237\}$ are... |
| **Adrien&#39;s Signs** | 80 | `Hard` | 11,353 | [前往解題](https://cryptohack.org/challenges/maths/) | Adrien's been looking at ways to encrypt his messages with the help of symbols and minus s... |
| **Modular Binomials** | 80 | `Hard` | 9,443 | [前往解題](https://cryptohack.org/challenges/maths/) | Rearrange the following equations to get the primes p,q $N = p \cdot q$ $c_1 = (2 \cdot p ... |
| **Broken RSA** | 100 | `Insane` | 3,098 | [前往解題](https://cryptohack.org/challenges/maths/) | I tried to send you an important message with RSA, however I messed up my RSA implementati... |
| **No Way Back Home** | 100 | `Insane` | 2,005 | [前往解題](https://cryptohack.org/challenges/maths/) | Quantum Computers are going to break some of the standard cryptosystems like RSA, ECC and ... |
| **Ellipse Curve Cryptography** | 125 | `Insane` | 1,481 | [前往解題](https://cryptohack.org/challenges/maths/) | I overheard my professor talking about ellipse curve cryptography. I tried googling it, bu... |
| **Roll your Own** | 125 | `Insane` | 1,257 | [前往解題](https://cryptohack.org/challenges/maths/) | Cracking discrete logarithms is hard. Change my mind. I'll even let you to use your own pa... |
| **Unencryptable** | 125 | `Insane` | 1,843 | [前往解題](https://cryptohack.org/challenges/maths/) | I swear I knew what I was doing, but I encrypted some data on my hard drive and nothing ha... |
| **Cofactor Cofantasy** | 150 | `Insane` | 1,111 | [前往解題](https://cryptohack.org/challenges/maths/) | Do you have the power to break out of my cofactor cofantasy? Calculating the solution shou... |
| **Real Eisenstein** | 150 | `Insane` | 1,193 | [前往解題](https://cryptohack.org/challenges/maths/) | I've hidden my secret among the primes. Reducing the number back down to the flag shouldn'... |
| **Prime and Prejudice** | 200 | `Insane` | 1,213 | [前往解題](https://cryptohack.org/challenges/maths/) | You may look through my window and see my flag, but to maintain my modesty, only the first... |

### 📌 Diffie-Hellman（14 Challenges）
*Discrete log, MITM, parameter injection, group theory*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Working with Fields** | 10 | `Easy` | 10,664 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | The set of integers modulo $N$, together with the operations of both addition and multipli... |
| **Generators of Groups** | 20 | `Medium` | 9,287 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Every element of a finite field $\Fp$ can be used to make a subgroup $H$ under repeated ac... |
| **Computing Public Values** | 25 | `Medium` | 9,344 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | The Diffie-Hellman protocol is used because the discrete logarithm is assumed to be a "har... |
| **Computing Shared Secrets** | 30 | `Medium` | 8,963 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Now it's time to calculate a shared secret using data received from your friend Alice. Lik... |
| **Deriving Symmetric Keys** | 40 | `Medium` | 8,050 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Alice wants to send you her secret flag and asks you to generate a shared secret with her.... |
| **Parameter Injection** | 60 | `Hard` | 6,507 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | You're in a position to not only intercept Alice and Bob's DH key exchange, but also rewri... |
| **Export-grade** | 100 | `Insane` | 5,654 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Alice and Bob are using legacy codebases and need to negotiate parameters they both suppor... |
| **Static Client** | 100 | `Insane` | 2,596 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | You've just finished eavesdropping on a conversation between Alice and Bob. Now you have a... |
| **Additive** | 70 | `Hard` | 2,793 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Alice and Bob decided to do their DHKE in an additive group rather than a multiplicative g... |
| **Static Client 2** | 120 | `Insane` | 1,910 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Bob got a bit more careful with the way he verifies parameters. He's still insisting on us... |
| **Script Kiddie** | 70 | `Hard` | 2,464 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Found this cool script on Github and I've been using it to keep my secrets from anyone lis... |
| **The Matrix** | 75 | `Hard` | 1,462 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | I must get out of here. I must get free, and in this mind is the key, my key! Challenge fi... |
| **The Matrix Reloaded** | 100 | `Insane` | 1,025 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | It's happening exactly as before... Well, not exactly. Challenge files: - matrix_reloaded.... |
| **The Matrix Revolutions** | 125 | `Insane` | 833 | [前往解題](https://cryptohack.org/challenges/diffie-hellman/) | Everything that has a beginning has an end, Neo. Challenge files: - matrix_revolutions.zip... |

### 📌 RSA（29 Challenges）
*Public key crypto, factorization attacks, padding oracles, Wiener's attack*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Modular Exponentiation** | 10 | `Easy` | 19,057 | [前往解題](https://cryptohack.org/challenges/rsa/) | All operations in RSA involve modular exponentiation . Modular exponentiation is an operat... |
| **Public Keys** | 15 | `Easy` | 18,232 | [前往解題](https://cryptohack.org/challenges/rsa/) | RSA encryption is modular exponentiation of a message with an exponent $e$ and a modulus $... |
| **Euler&#39;s Totient** | 20 | `Medium` | 17,361 | [前往解題](https://cryptohack.org/challenges/rsa/) | RSA relies on the difficulty of the factorisation of the modulus N . If the prime factors ... |
| **Private Keys** | 20 | `Medium` | 16,518 | [前往解題](https://cryptohack.org/challenges/rsa/) | The private key $d$ is used to decrypt ciphertexts created with the corresponding public k... |
| **RSA Decryption** | 20 | `Medium` | 15,902 | [前往解題](https://cryptohack.org/challenges/rsa/) | I've encrypted a secret number for your eyes only using your public key parameters: N = 88... |
| **RSA Signatures** | 25 | `Medium` | 12,349 | [前往解題](https://cryptohack.org/challenges/rsa/) | How can you ensure that the person receiving your message knows that you wrote it? You've ... |
| **Factoring** | 15 | `Easy` | 12,250 | [前往解題](https://cryptohack.org/challenges/rsa/) | So far we've been using the product of small primes for the modulus, but small primes aren... |
| **Inferius Prime** | 30 | `Medium` | 7,897 | [前往解題](https://cryptohack.org/challenges/rsa/) | Here is my super-strong RSA implementation, because it's 1600 bits strong it should be unb... |
| **Monoprime** | 30 | `Medium` | 11,222 | [前往解題](https://cryptohack.org/challenges/rsa/) | Why is everyone so obsessed with multiplying two primes for RSA. Why not just use one? Cha... |
| **Square Eyes** | 35 | `Medium` | 7,384 | [前往解題](https://cryptohack.org/challenges/rsa/) | It was taking forever to get a 2048 bit prime, so I just generated one and used it twice. ... |
| **Manyprime** | 40 | `Medium` | 9,870 | [前往解題](https://cryptohack.org/challenges/rsa/) | Using one prime factor was definitely a bad idea so I'll try using over 30 instead. If it'... |
| **Salty** | 20 | `Medium` | 10,087 | [前往解題](https://cryptohack.org/challenges/rsa/) | Smallest exponent should be fastest, right? Challenge files: - salty.py - output.txt --> |
| **Modulus Inutilis** | 50 | `Hard` | 9,414 | [前往解題](https://cryptohack.org/challenges/rsa/) | My primes should be more than large enough now! Challenge files: - modulus_inutilis.py - o... |
| **Everything is Big** | 70 | `Hard` | 5,460 | [前往解題](https://cryptohack.org/challenges/rsa/) | We have a supercomputer at work, so I've made sure my encryption is secure by picking mass... |
| **Crossed Wires** | 100 | `Insane` | 4,885 | [前往解題](https://cryptohack.org/challenges/rsa/) | I asked my friends to encrypt our secret flag before sending it to me, but instead of usin... |
| **Everything is Still Big** | 100 | `Insane` | 4,140 | [前往解題](https://cryptohack.org/challenges/rsa/) | Okay so I got a bit carefree with my last script, but this time I've protected myself whil... |
| **Endless Emails** | 150 | `Insane` | 3,513 | [前往解題](https://cryptohack.org/challenges/rsa/) | Poor Johan has been answering emails all day and many of the students are asking the same ... |
| **Infinite Descent** | 50 | `Hard` | 4,263 | [前往解題](https://cryptohack.org/challenges/rsa/) | Finding large primes is slow, so I've devised an optimisation. Challenge files: - descent.... |
| **Marin&#39;s Secrets** | 50 | `Hard` | 4,145 | [前往解題](https://cryptohack.org/challenges/rsa/) | I've found a super fast way to generate primes from my secret list. Challenge files: - mar... |
| **Fast Primes** | 75 | `Hard` | 2,822 | [前往解題](https://cryptohack.org/challenges/rsa/) | I need to produce millions of RSA keys quickly and the standard way just doesn't cut it. H... |
| **Ron was Wrong, Whit is Right** | 90 | `Insane` | 2,801 | [前往解題](https://cryptohack.org/challenges/rsa/) | Here's a bunch of RSA public keys I gathered from people on the net together with messages... |
| **RSA Backdoor Viability** | 175 | `Insane` | 2,140 | [前往解題](https://cryptohack.org/challenges/rsa/) | It seems like my method to generate fast primes was not completely secure. I came up with ... |
| **Bespoke Padding** | 100 | `Insane` | 1,940 | [前往解題](https://cryptohack.org/challenges/rsa/) | Been cooking up my own padding scheme, now my encrypted flag is different everytime! Conne... |
| **Null or Never** | 100 | `Insane` | 2,094 | [前往解題](https://cryptohack.org/challenges/rsa/) | Can custom padding save one from some of the mistakes we already covered? Challenge files:... |
| **Signing Server** | 60 | `Hard` | 2,829 | [前往解題](https://cryptohack.org/challenges/rsa/) | My boss has so many emails he's set up a server to just sign everything automatically. He ... |
| **Let&#39;s Decrypt** | 80 | `Hard` | 2,074 | [前往解題](https://cryptohack.org/challenges/rsa/) | If you can prove you own CryptoHack.org, then you get access to one of our secrets. Connec... |
| **Blinding Light** | 120 | `Insane` | 2,009 | [前往解題](https://cryptohack.org/challenges/rsa/) | Here's my token signing and verification server. I'm not sure it's doing signing properly,... |
| **Vote for Pedro** | 150 | `Insane` | 1,714 | [前往解題](https://cryptohack.org/challenges/rsa/) | If you want my flag, you better vote for Pedro! Can you sign your vote to the server as Al... |
| **Let&#39;s Decrypt Again** | 175 | `Insane` | 1,185 | [前往解題](https://cryptohack.org/challenges/rsa/) | Let's Decrypt was too easy, let's do it again! Connect at socket.cryptohack.org 13394 Chal... |

### 📌 Block Ciphers (AES)（27 Challenges）
*ECB, CBC, OFB, CTR, padding oracle, GCM vulnerabilities*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Keyed Permutations** | 5 | `Easy` | 20,922 | [前往解題](https://cryptohack.org/challenges/aes/) | AES, like all good block ciphers, performs a "keyed permutation". This means that it maps ... |
| **Resisting Bruteforce** | 10 | `Easy` | 19,252 | [前往解題](https://cryptohack.org/challenges/aes/) | If a block cipher is secure, there should be no way for an attacker to distinguish the out... |
| **Structure of AES** | 15 | `Easy` | 15,880 | [前往解題](https://cryptohack.org/challenges/aes/) | To achieve a keyed permutation that is infeasible to invert without the key, AES applies a... |
| **Round Keys** | 20 | `Medium` | 14,709 | [前往解題](https://cryptohack.org/challenges/aes/) | We're going to skip over the finer details of the KeyExpansion phase for now. The main poi... |
| **Confusion through Substitution** | 25 | `Medium` | 13,336 | [前往解題](https://cryptohack.org/challenges/aes/) | The first step of each AES round is SubBytes . This involves taking each byte of the state... |
| **Diffusion through Permutation** | 30 | `Medium` | 12,198 | [前往解題](https://cryptohack.org/challenges/aes/) | We've seen how S-box substitution provides confusion. The other crucial property described... |
| **Bringing It All Together** | 50 | `Hard` | 10,505 | [前往解題](https://cryptohack.org/challenges/aes/) | Apart from the KeyExpansion phase, we've sketched out all the components of AES. We've sho... |
| **Modes of Operation Starter** | 15 | `Easy` | 11,058 | [前往解題](https://cryptohack.org/challenges/aes/) | The previous set of challenges showed how AES performs a keyed permutation on a block of d... |
| **Passwords as Keys** | 50 | `Hard` | 9,508 | [前往解題](https://cryptohack.org/challenges/aes/) | It is essential that keys in symmetric-key algorithms are random bytes, instead of passwor... |
| **ECB CBC WTF** | 55 | `Hard` | 8,110 | [前往解題](https://cryptohack.org/challenges/aes/) | Here you can encrypt in CBC but only decrypt in ECB. That shouldn't be a weakness because ... |
| **ECB Oracle** | 60 | `Hard` | 8,126 | [前往解題](https://cryptohack.org/challenges/aes/) | ECB is the most simple mode, with each plaintext block encrypted entirely independently. I... |
| **Flipping Cookie** | 60 | `Hard` | 7,338 | [前往解題](https://cryptohack.org/challenges/aes/) | You can get a cookie for my website, but it won't help you read the flag... I think. Play ... |
| **Lazy CBC** | 60 | `Hard` | 4,386 | [前往解題](https://cryptohack.org/challenges/aes/) | I'm just a lazy dev and want my CBC encryption to work. What's all this talk about initial... |
| **Triple DES** | 60 | `Hard` | 3,387 | [前往解題](https://cryptohack.org/challenges/aes/) | Data Encryption Standard was the forerunner to AES, and is still widely used in some slow-... |
| **Symmetry** | 50 | `Hard` | 6,515 | [前往解題](https://cryptohack.org/challenges/aes/) | Some block cipher modes, such as OFB, CTR, or CFB, turn a block cipher into a stream ciphe... |
| **Bean Counter** | 60 | `Hard` | 6,102 | [前往解題](https://cryptohack.org/challenges/aes/) | I've struggled to get PyCrypto's counter mode doing what I want, so I've turned ECB mode i... |
| **CTRIME** | 70 | `Hard` | 3,089 | [前往解題](https://cryptohack.org/challenges/aes/) | There may be a lot of redundancy in our plaintext, so why not compress it first? Play at h... |
| **Logon Zero** | 80 | `Hard` | 2,329 | [前往解題](https://cryptohack.org/challenges/aes/) | Before using the network, you must authenticate to Active Directory using our timeworn CFB... |
| **Stream of Consciousness** | 80 | `Hard` | 2,635 | [前往解題](https://cryptohack.org/challenges/aes/) | Talk to me and hear a sentence from my encrypted stream of consciousness. Play at https://... |
| **Dancing Queen** | 120 | `Insane` | 1,750 | [前往解題](https://cryptohack.org/challenges/aes/) | I don't trust other developers so I made my own ChaCha20 implementation. In this way, I am... |
| **Oh SNAP** | 120 | `Insane` | 1,500 | [前往解題](https://cryptohack.org/challenges/aes/) | Here's the start of my fast network authentication protocol, so far I've only implemented ... |
| **Pad Thai** | 80 | `Hard` | 1,232 | [前往解題](https://cryptohack.org/challenges/aes/) | Sometimes the classic challenges can be the most delicious Connect at socket.cryptohack.or... |
| **The Good, The Pad, The Ugly** | 100 | `Insane` | 968 | [前往解題](https://cryptohack.org/challenges/aes/) | The first twist of the classic challenge, how can you handle an oracle with errors? Connec... |
| **Oracular Spectacular** | 150 | `Insane` | 563 | [前往解題](https://cryptohack.org/challenges/aes/) | This oracle lies! Can you still recover the message XOR are you going to have to give up? ... |
| **Paper Plane** | 120 | `Insane` | 1,376 | [前往解題](https://cryptohack.org/challenges/aes/) | I've found an authenticated encryption mode called Infinite Garble Extension where an erro... |
| **Forbidden Fruit** | 150 | `Insane` | 1,042 | [前往解題](https://cryptohack.org/challenges/aes/) | Galois Counter Mode (GCM) is the most widely used block cipher mode in TLS today. It's an ... |
| **Beatboxer** | 150 | `Insane` | 710 | [前往解題](https://cryptohack.org/challenges/aes/) | Welcome to my military grade encryption service! It's based on AES but with some tweaks to... |

### 📌 Elliptic Curves（23 Challenges）
*ECDSA, curve parameters, invalid curve attacks, Montgomery curves*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Background Reading** | 5 | `Easy` | 7,226 | [前往解題](https://cryptohack.org/challenges/ecc/) | Elliptic Curve Cryptography (ECC) is an asymmetric cryptographic protocol that, like RSA a... |
| **Point Negation** | 10 | `Easy` | 6,291 | [前往解題](https://cryptohack.org/challenges/ecc/) | In the background section, we covered the basics of how we can view point addition over an... |
| **Point Addition** | 30 | `Medium` | 5,601 | [前往解題](https://cryptohack.org/challenges/ecc/) | While working with elliptic curve cryptography, we will need to add points together. In th... |
| **Scalar Multiplication** | 35 | `Medium` | 5,101 | [前往解題](https://cryptohack.org/challenges/ecc/) | Scalar multiplication of two points is defined by repeated addition: $[3]P = P + P + P$. I... |
| **Curves and Logs** | 40 | `Medium` | 4,858 | [前往解題](https://cryptohack.org/challenges/ecc/) | The Elliptic Curve Discrete Logarithm Problem (ECDLP) is the problem of finding an integer... |
| **Efficient Exchange** | 50 | `Hard` | 4,399 | [前往解題](https://cryptohack.org/challenges/ecc/) | Alice and Bob are looking at the Elliptic Curve Discrete Logarithm Problem and thinking ab... |
| **Smooth Criminal** | 60 | `Hard` | 3,019 | [前往解題](https://cryptohack.org/challenges/ecc/) | Spent my morning reading up on ECC and now I'm ready to start encrypting my messages. Sent... |
| **Exceptional Curves** | 100 | `Insane` | 1,567 | [前往解題](https://cryptohack.org/challenges/ecc/) | Learning from my mistakes... This time I've ensured my curve is of prime order. This flag ... |
| **Micro Transmissions** | 120 | `Insane` | 1,180 | [前往解題](https://cryptohack.org/challenges/ecc/) | Been fine tuning my bit lengths to ensure my data packages and calculation times are super... |
| **Elliptic Nodes** | 150 | `Insane` | 1,121 | [前往解題](https://cryptohack.org/challenges/ecc/) | I've included an extra layer of security by picking my own curve parameters a,b and keepin... |
| **Moving Problems** | 150 | `Insane` | 1,906 | [前往解題](https://cryptohack.org/challenges/ecc/) | I've learnt that when life gives you lemons, if you look at things the right way they tast... |
| **A Twisted Mind** | 80 | `Hard` | 403 | [前往解題](https://cryptohack.org/challenges/ecc/) | I implemented the scalar multiplication from another challenge. It is secure enough, so yo... |
| **An Exceptional Twisted Mind** | 125 | `Insane` | 301 | [前往解題](https://cryptohack.org/challenges/ecc/) | For this last one, I chose a very secure elliptic curve. Finally, my private key is safe. ... |
| **Checkpoint** | 150 | `Insane` | 306 | [前往解題](https://cryptohack.org/challenges/ecc/) | During an internal audit, you find a custom service performing ECDH key exchange to establ... |
| **An Evil Twisted Mind** | 175 | `Insane` | 271 | [前往解題](https://cryptohack.org/challenges/ecc/) | For more security, I made some changes on the curve parameters! This time, I am sure my pr... |
| **Real Curve Crypto** | 200 | `Insane` | 412 | [前往解題](https://cryptohack.org/challenges/ecc/) | When developing a secure crypto system, the most important rule is to keep it real. Challe... |
| **Digestive** | 60 | `Hard` | 878 | [前往解題](https://cryptohack.org/challenges/ecc/) | Should ECDSA be avoided for better digestive health? Play at https://web.cryptohack.org/di... |
| **Curveball** | 100 | `Insane` | 2,206 | [前往解題](https://cryptohack.org/challenges/ecc/) | Here's my secure search engine, which will only search for hosts it has in its trusted cer... |
| **ProSign 3** | 100 | `Insane` | 1,870 | [前往解題](https://cryptohack.org/challenges/ecc/) | This is my secure timestamp signing server. Only if you can produce a signature for "unloc... |
| **No Random, No Bias** | 120 | `Insane` | 775 | [前往解題](https://cryptohack.org/challenges/ecc/) | Relying on randomness is bad with a bad entropy source, so I got rid of it and changed to ... |
| **Edwards Goes Degenerate** | 100 | `Insane` | 692 | [前往解題](https://cryptohack.org/challenges/ecc/) | I heard elliptic curves in Edwards form have nice and efficient point addition formulas th... |
| **Montgomery&#39;s Ladder** | 40 | `Medium` | 2,341 | [前往解題](https://cryptohack.org/challenges/ecc/) | This category is filled with insecure implementations of elliptic curve cryptography. Pick... |
| **Double and Broken** | 50 | `Hard` | 811 | [前往解題](https://cryptohack.org/challenges/ecc/) | We've managed to get power readings from scalar multiplication on the Secp256k1 curve. Can... |

### 📌 Hash Functions（14 Challenges）
*MD5, SHA, collision attacks, length extension, HMAC*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Jack&#39;s Birthday Hash** | 20 | `Medium` | 4,581 | [前往解題](https://cryptohack.org/challenges/hashes/) | Today is Jack's birthday, so he has designed his own cryptographic hash as a way to celebr... |
| **Jack&#39;s Birthday Confusion** | 30 | `Medium` | 3,982 | [前往解題](https://cryptohack.org/challenges/hashes/) | The last computation has made Jack a little worried about the safety of his hash, and afte... |
| **Collider** | 50 | `Hard` | 3,057 | [前往解題](https://cryptohack.org/challenges/hashes/) | Check out my document system about particle physics, where every document is uniquely refe... |
| **Hash Stuffing** | 50 | `Hard` | 2,065 | [前往解題](https://cryptohack.org/challenges/hashes/) | With all the attacks on MD5 and SHA1 floating around, we thought it was time to start roll... |
| **PriMeD5** | 100 | `Insane` | 1,518 | [前往解題](https://cryptohack.org/challenges/hashes/) | Primality checking is expensive so I made a service that signs primes, allowing anyone to ... |
| **Twin Keys** | 100 | `Insane` | 931 | [前往解題](https://cryptohack.org/challenges/hashes/) | Cryptohack's secure safe requires two keys to unlock its secret. However, Jack and Hyperre... |
| **No Difference** | 175 | `Insane` | 1,084 | [前往解題](https://cryptohack.org/challenges/hashes/) | It's easy to come across a collision for MD5, but can you find one in my custom hash funct... |
| **MD0** | 80 | `Hard` | 1,754 | [前往解題](https://cryptohack.org/challenges/hashes/) | I've invented a nice simple version of HMAC authentication, hopefully it isn't vulnerable ... |
| **MDFlag** | 125 | `Insane` | 739 | [前往解題](https://cryptohack.org/challenges/hashes/) | MD0 had a serious weakness, here is a new improved MD5-based HMAC. Connect at socket.crypt... |
| **Mixed Up** | 120 | `Insane` | 1,112 | [前往解題](https://cryptohack.org/challenges/hashes/) | Due to the properties of XOR and hash functions, it shouldn't be possible to unmix the fla... |
| **Invariant** | 250 | `Insane` | 730 | [前往解題](https://cryptohack.org/challenges/hashes/) | It's said that you shouldn't roll your own hash function. But how easy is it to break one?... |
| **Merkle Trees** | 25 | `Medium` | 933 | [前往解題](https://cryptohack.org/challenges/hashes/) | A Merkle tree is a fundamental concept in computer science, particularly utilized within b... |
| **WOTS Up** | 75 | `Hard` | 805 | [前往解題](https://cryptohack.org/challenges/hashes/) | With the need to find post-quantum schemes, hash-based signatures are cool again. Challeng... |
| **WOTS Up 2** | 90 | `Insane` | 748 | [前往解題](https://cryptohack.org/challenges/hashes/) | I fixed the problem with my last scheme, now I can confidently sign my WOTScoin transactio... |

### 📌 Crypto on the Web（17 Challenges）
*JWT forgery, token manipulation, TLS/SSL weaknesses*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Token Appreciation** | 5 | `Easy` | 6,616 | [前往解題](https://cryptohack.org/challenges/web/) | JavaScript Object Signing and Encryption (JOSE) is a framework specifying ways to securely... |
| **JWT Sessions** | 10 | `Easy` | 5,552 | [前往解題](https://cryptohack.org/challenges/web/) | The traditional way to store sessions is with session ID cookies. After you login to a web... |
| **No Way JOSE** | 20 | `Medium` | 4,531 | [前往解題](https://cryptohack.org/challenges/web/) | Let's look at JWT algorithms. The first part of a JWT is the JOSE header, and when you dec... |
| **JWT Secrets** | 25 | `Medium` | 4,124 | [前往解題](https://cryptohack.org/challenges/web/) | The most common signing algorithms used in JWTs are HS256 and RS256 . The first is a symme... |
| **RSA or HMAC?** | 35 | `Medium` | 2,675 | [前往解題](https://cryptohack.org/challenges/web/) | There's another issue caused by allowing attackers to specify their own algorithms but not... |
| **JSON in JSON** | 40 | `Medium` | 2,776 | [前往解題](https://cryptohack.org/challenges/web/) | We've explored how flawed verification can break the security of JWTs, but it can sometime... |
| **RSA or HMAC? Part 2** | 100 | `Insane` | 1,265 | [前往解題](https://cryptohack.org/challenges/web/) | It is possible to abuse JWT public keys without the public key being public? This challeng... |
| **Secure Protocols** | 5 | `Easy` | 2,503 | [前往解題](https://cryptohack.org/challenges/web/) | CryptoHack challenge in Crypto on the Web (5 pts). |
| **Sharks on the Wire** | 10 | `Easy` | 2,025 | [前往解題](https://cryptohack.org/challenges/web/) | The best way to understand a network protocol is to watch real traffic. For this challenge... |
| **TLS Handshake** | 15 | `Easy` | 1,862 | [前往解題](https://cryptohack.org/challenges/web/) | CryptoHack challenge in Crypto on the Web (15 pts). |
| **Saying Hello** | 20 | `Medium` | 1,755 | [前往解題](https://cryptohack.org/challenges/web/) | CryptoHack challenge in Crypto on the Web (20 pts). |
| **Decrypting TLS 1.2** | 30 | `Medium` | 1,313 | [前往解題](https://cryptohack.org/challenges/web/) | Let's rewind for a moment and talk about TLS 1.2, and why it has been superseded by TLS 1.... |
| **Decrypting TLS 1.3** | 35 | `Medium` | 1,246 | [前往解題](https://cryptohack.org/challenges/web/) | To recap, the TLS handshake can be split up into four main stages. Despite changes in TLS ... |
| **Authenticated Handshake** | 40 | `Medium` | 729 | [前往解題](https://cryptohack.org/challenges/web/) | CryptoHack challenge in Crypto on the Web (40 pts). |
| **Megalomaniac 1** | 100 | `Insane` | 399 | [前往解題](https://cryptohack.org/challenges/web/) | In June 2022, a team of researchers from the Applied Crypto Group at ETH Zurich discovered... |
| **Megalomaniac 2** | 120 | `Insane` | 283 | [前往解題](https://cryptohack.org/challenges/web/) | In a realistic scenario, an evil server would want to be able to recover it with a minimal... |
| **Megalomaniac 3** | 120 | `Insane` | 308 | [前往解題](https://cryptohack.org/challenges/web/) | Now it is about time to recover the actual data uploaded by a user! Connect at socket.cryp... |

### 📌 Post-Quantum（18 Challenges）
*Lattice-based cryptography, Kyber, Dilithium fundamentals*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Vectors** | 10 | `Easy` | 5,660 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | Before defining a lattice or talking about how lattices appear in cryptography, let's revi... |
| **Size and Basis** | 15 | `Easy` | 5,414 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | We say a set of vectors $v_{1}, v_{2}, \ldots, v_{k} \in V$ are linearly independent if th... |
| **Gram Schmidt** | 30 | `Medium` | 4,039 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | In the last challenge we saw that there is a special kind of basis called an orthogonal ba... |
| **What&#39;s a Lattice?** | 40 | `Medium` | 4,225 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | We're now ready to start talking about lattices. Given a set of linearly independent vecto... |
| **Gaussian Reduction** | 50 | `Hard` | 3,753 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | If you look closely enough, lattices start appearing everywhere in cryptography. Sometimes... |
| **Find the Lattice** | 100 | `Insane` | 2,433 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | As we've seen, lattices contain hard problems which can form trapdoor functions for crypto... |
| **Backpack Cryptography** | 120 | `Insane` | 1,615 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | I love this cryptosystem so much, I carry it everywhere in my backpack. To lighten the loa... |
| **LWE Background** | 5 | `Easy` | 1,752 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | Before beginning this section you should have completed at least the "Lattices" section ab... |
| **LWE Intro** | 10 | `Easy` | 1,396 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | CryptoHack challenge in Post-Quantum (10 pts). |
| **LWE High Bits Message** | 15 | `Easy` | 1,019 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | CryptoHack challenge in Post-Quantum (15 pts). |
| **LWE Low Bits Message** | 20 | `Medium` | 946 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | CryptoHack challenge in Post-Quantum (20 pts). |
| **From Private to Public Key LWE** | 25 | `Medium` | 1,034 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | This can be turned into a public key cryptosystem by using the "additively homomorphic" pr... |
| **Noise Free** | 40 | `Medium` | 797 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | The addition of the noise term is what makes learning into learning with errors. How well ... |
| **Bounded Noise** | 50 | `Hard` | 550 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | I find implementing gaussian sampling to be hard and slow, so I prefer binary sampling Cha... |
| **Nativity** | 60 | `Hard` | 529 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | LWE is easy, so I made my own implementation that works with native integers. Challenge fi... |
| **Missing Modulus** | 80 | `Hard` | 493 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | I just created my first LWE cryptosystem, I hope I didn't forget anything important... Con... |
| **Noise Cheap** | 90 | `Insane` | 432 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | A core part of making LWE secure is having the noise terms be larger than what lattice red... |
| **Too Many Errors** | 100 | `Insane` | 654 | [前往解題](https://cryptohack.org/challenges/post-quantum/) | To protect my flag against quantum computers, I've used a quantum-safe Learning With Error... |

### 📌 Isogenies（23 Challenges）
*Supersingular isogeny Diffie-Hellman and supersingular curves*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Introduction to Isogenies** | 10 | `Easy` | 859 | [前往解題](https://cryptohack.org/challenges/isogenies/) | Before beginning this section you should have attempted many of the challenges in the "Ell... |
| **The j-invariant** | 20 | `Medium` | 762 | [前往解題](https://cryptohack.org/challenges/isogenies/) | Much like in modular arithmetic, where many computations are only equal up to an equivalen... |
| **Where&#39;s the Supersingular Curve** | 25 | `Medium` | 578 | [前往解題](https://cryptohack.org/challenges/isogenies/) | For the majority of this category (and all challenges at the time of writing) we are inter... |
| **Image Point Arithmetic** | 30 | `Medium` | 592 | [前往解題](https://cryptohack.org/challenges/isogenies/) | As mentioned in the introduction, an isogeny is not only a rational map between curves, bu... |
| **Montgomery Curves** | 30 | `Medium` | 523 | [前往解題](https://cryptohack.org/challenges/isogenies/) | Here's an isogeny challenge which many of you may have already solved before. An isomorphi... |
| **DLOG on the Surface** | 40 | `Medium` | 425 | [前往解題](https://cryptohack.org/challenges/isogenies/) | For the isogenies we compute together, we'll generally be computing the isogeny from a ker... |
| **Two Isogenies** | 30 | `Medium` | 440 | [前往解題](https://cryptohack.org/challenges/isogenies/) | It's time to compute our first two-isogeny! In this set of challenges we will work our way... |
| **Three Isogenies** | 35 | `Medium` | 428 | [前往解題](https://cryptohack.org/challenges/isogenies/) | This challenge is very similar to the previous one, only now the isogeny is going to be a ... |
| **Composite Isogenies** | 60 | `Hard` | 408 | [前往解題](https://cryptohack.org/challenges/isogenies/) | You may have noticed two things so far. One is that the algorithms you're using are linear... |
| **SIDH Key Exchange** | 80 | `Hard` | 378 | [前往解題](https://cryptohack.org/challenges/isogenies/) | By this point you should be able to efficiently compute an isogeny of large smooth degree ... |
| **Breaking SIDH** | 250 | `Insane` | 268 | [前往解題](https://cryptohack.org/challenges/isogenies/) | The SIDH protocol is a great way to learn some of the machinery of isogeny-based cryptogra... |
| **Special Isogenies** | 30 | `Medium` | 366 | [前往解題](https://cryptohack.org/challenges/isogenies/) | For the SIDH challenges, the torsion basis $E[n] = \langle P, Q \rangle$ had two generator... |
| **Prime Power Isogenies** | 50 | `Hard` | 352 | [前往解題](https://cryptohack.org/challenges/isogenies/) | For SIDH, we used a prime of the form $p = 2^{e_A} \cdot 3^{e_B} - 1$ and we computed isog... |
| **Secret Exponents** | 60 | `Hard` | 342 | [前往解題](https://cryptohack.org/challenges/isogenies/) | In the CSIDH key exchange, a private key is a list of integers as long as the number of od... |
| **Twisted CSIDH Isogenies** | 70 | `Hard` | 330 | [前往解題](https://cryptohack.org/challenges/isogenies/) | In the challenge "CSIDH prime power isogenies" we explored the $\ell$-isogeny graphs for t... |
| **CSIDH Key Exchange** | 90 | `Insane` | 316 | [前往解題](https://cryptohack.org/challenges/isogenies/) | You are now ready to implement a full CSIDH key exchange! In the source file you are given... |
| **What&#39;s My Kernel** | 70 | `Hard` | 322 | [前往解題](https://cryptohack.org/challenges/isogenies/) | Here's my SIDH public key, can you solve the isogeny problem and recover the kernel? Chall... |
| **André Encoding** | 80 | `Hard` | 296 | [前往解題](https://cryptohack.org/challenges/isogenies/) | I've developed a novel encryption protocol, the only thing left is to look into compressio... |
| **Better than Linear** | 85 | `Insane` | 303 | [前往解題](https://cryptohack.org/challenges/isogenies/) | For isogenies of "large" prime degree, we can compute isogenies with a square-root speed u... |
| **Abelian SIDH** | 90 | `Insane` | 279 | [前往解題](https://cryptohack.org/challenges/isogenies/) | I found a way to do SIDH without sending torsion points! Challenge files: - source.sage - ... |
| **Dual Masters** | 90 | `Insane` | 264 | [前往解題](https://cryptohack.org/challenges/isogenies/) | In "What's my Kernel" maybe I gave you too much data... I think this new public key should... |
| **Meet me in the Claw** | 120 | `Insane` | 251 | [前往解題](https://cryptohack.org/challenges/isogenies/) | Alice forgot to send me her torsion data! How am I going to compute the shared secret?? Ch... |
| **A True Genus** | 175 | `Insane` | 244 | [前往解題](https://cryptohack.org/challenges/isogenies/) | If only Gauss were here... Challenge files: - source.sage - output.txt Challenge contribut... |

### 📌 Zero Knowledge（17 Challenges）
*Interactive proofs, Sigma protocols, Schnorr identification*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ZKP Introduction** | 5 | `Easy` | 1,667 | [前往解題](https://cryptohack.org/challenges/zkp/) | A zero-knowledge proof (ZKP) is a technique that enables one party (the prover) to demonst... |
| **Proofs of Knowledge** | 20 | `Medium` | 877 | [前往解題](https://cryptohack.org/challenges/zkp/) | Zero knowledge proofs are a tool in modern cryptography which allows you to prove that you... |
| **Special Soundness** | 25 | `Medium` | 789 | [前往解題](https://cryptohack.org/challenges/zkp/) | The last challenge showed that this protocol satisfies (perfect) completeness! That is, if... |
| **Honest Verifier Zero Knowledge** | 30 | `Medium` | 712 | [前往解題](https://cryptohack.org/challenges/zkp/) | The previous challenge showed that this protocol satisfies Special Soundness! That is, if ... |
| **Non-Interactive** | 35 | `Medium` | 666 | [前往解題](https://cryptohack.org/challenges/zkp/) | We have now shown that the Schnorr protocol for proving knowledge of a discrete logarithm ... |
| **Too Honest** | 50 | `Hard` | 618 | [前往解題](https://cryptohack.org/challenges/zkp/) | Recall that we only proved Schnorr's protocol to be SHVZK, and while this was enough to ma... |
| **OR Proof** | 75 | `Hard` | 482 | [前往解題](https://cryptohack.org/challenges/zkp/) | We have already seen how proving a protocol to be a $\Sigma$-Protocol essentially gives us... |
| **Hamiltonicity 1** | 100 | `Insane` | 354 | [前往解題](https://cryptohack.org/challenges/zkp/) | CryptoHack challenge in Zero Knowledge (100 pts). |
| **Hamiltonicity 2** | 175 | `Insane` | 235 | [前往解題](https://cryptohack.org/challenges/zkp/) | In the last challenge we showed how not to do the Fiat-Shamir transform for a multi-round ... |
| **Fischlin Transform** | 180 | `Insane` | 251 | [前往解題](https://cryptohack.org/challenges/zkp/) | Recall the definition of "Proof of Knowledge" from the NIZK challenge. The notion of a "Pr... |
| **Ticket Maestro** | 200 | `Insane` | 216 | [前往解題](https://cryptohack.org/challenges/zkp/) | We previously showed the existence of Zero Knowledge for all of NP, through the graph Hami... |
| **Pairing-Based Cryptography** | 50 | `Hard` | 349 | [前往解題](https://cryptohack.org/challenges/zkp/) | CryptoHack challenge in Zero Knowledge (50 pts). |
| **Mister Saplin&#39;s Preview** | 80 | `Hard` | 294 | [前往解題](https://cryptohack.org/challenges/zkp/) | Mister Saplins has implemented a system to view some nodes and would like you to test it t... |
| **Couples** | 100 | `Insane` | 291 | [前往解題](https://cryptohack.org/challenges/zkp/) | Couples form, others separate, but in the end the only constant remains the bilinear mappi... |
| **Let&#39;s Prove It** | 120 | `Insane` | 265 | [前往解題](https://cryptohack.org/challenges/zkp/) | I've been told that home implementation is never a good idea. But I followed the implement... |
| **Mister Saplins The Prover** | 125 | `Insane` | 276 | [前往解題](https://cryptohack.org/challenges/zkp/) | Mister Saplins and proofs, that's 2. Connect at socket.cryptohack.org 13432 Challenge file... |
| **Let&#39;s Prove It Again** | 175 | `Insane` | 263 | [前往解題](https://cryptohack.org/challenges/zkp/) | Okay maybe last time I did it wrong, but this time I gave my project to my intern and he r... |

### 📌 Miscellaneous（14 Challenges）
*Interactive algorithmic crypto, esoteric cipher systems*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gotta Go Fast** | 40 | `Medium` | 2,338 | [前往解題](https://cryptohack.org/challenges/misc/) | I won't have to worry about running out of entropy, I'm going to have my OTP generated for... |
| **No Leaks** | 100 | `Insane` | 1,767 | [前往解題](https://cryptohack.org/challenges/misc/) | Each time you connect, I generate a new one time pad. I also check for leaks, so there's n... |
| **Lo-Hi Card Game** | 120 | `Insane` | 960 | [前往解題](https://cryptohack.org/challenges/misc/) | I'm opening a virtual casino and this is my first game. It's all luck-based and biased tow... |
| **Nothing Up My Sleeve** | 150 | `Insane` | 591 | [前往解題](https://cryptohack.org/challenges/misc/) | My first casino game was a big hit, but there was an issue with the RNG. Some players chea... |
| **RSA vs RNG** | 150 | `Insane` | 555 | [前往解題](https://cryptohack.org/challenges/misc/) | Here's a new fast way I've found for generating RSA keys for smart cards. Challenge files:... |
| **Trust Games** | 150 | `Insane` | 482 | [前往解題](https://cryptohack.org/challenges/misc/) | Following the issues with our casino games, we're testing a stronger random number generat... |
| **L-Win** | 120 | `Insane` | 599 | [前往解題](https://cryptohack.org/challenges/misc/) | Can you recover the input for a simple Linear Feedback Shift Register with unknown taps? C... |
| **Jeff&#39;s LFSR** | 150 | `Insane` | 475 | [前往解題](https://cryptohack.org/challenges/misc/) | Jeff heard that LFSRs used as stream ciphers aren't very secure, so he combined three LFSR... |
| **LFSR Destroyer** | 250 | `Insane` | 275 | [前往解題](https://cryptohack.org/challenges/misc/) | You are well on your way to mastering LFSRs if you can crack this. Hurry, your time is lim... |
| **Bit by Bit** | 100 | `Insane` | 739 | [前往解題](https://cryptohack.org/challenges/misc/) | I heard ElGamal has some cool properties. I've encrypted every bit with a different secret... |
| **Armory** | 100 | `Insane` | 859 | [前往解題](https://cryptohack.org/challenges/misc/) | Here's my improvement on Shamir's scheme with deterministically derived shares. Great for ... |
| **Toshi&#39;s Treasure** | 150 | `Insane` | 612 | [前往解題](https://cryptohack.org/challenges/misc/) | You are hyperreality and you are playing an online treasure hunt with your team mpeg, code... |
| **Bruce Schneier&#39;s Password** | 100 | `Insane` | 767 | [前往解題](https://cryptohack.org/challenges/misc/) | https://www.schneierfacts.com/facts/842 The challenge server is running 64-bit Linux, whic... |
| **Bruce Schneier&#39;s Password: Part 2** | 250 | `Insane` | 315 | [前往解題](https://cryptohack.org/challenges/misc/) | Bruce Schneier's password was too easy to Bruce-force, so some Schneiertational complexity... |

### 📌 CTF Archive（75 Challenges）
*Past CryptoHack CTF and wargame challenge archive*

| 關卡名稱 (Title) | 分數 (Pts) | 難度 | 解題人數 | 線上傳送門 | 關卡簡介 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Authentification 1 (Breizh CTF)** | 10 | `Easy` | 116 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I secured my web application with AES-GCM implemented by the intern! Great idea, isn't it ... |
| **Authentification 2 (Breizh CTF)** | 10 | `Easy` | 69 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Damn, I'd forgotten to check the integrity... Good thing the intern pointed it out to me, ... |
| **Do you have good eyes? (Breizh CTF)** | 10 | `Easy` | 52 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Can you tell the difference? Challenge contributed by skilo Connect at archive.cryptohack.... |
| **U-turn (Breizh CTF)** | 10 | `Easy` | 71 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | HaSh functIonS are one-way, right? Challenge contributed by skilo Challenge files: - u-tur... |
| **Verilicious (Cyber Apocalypse 2025)** | 10 | `Easy` | 52 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | A sacred ward, once thought unbreakable, is built upon a foundation of misplaced trust. Th... |
| **Additional problems (CSC Belgium)** | 10 | `Easy` | 63 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Version 1.0 of our new encryption service has just launched! It is blazingly fast and uses... |
| **ECLCG (HITCON CTF)** | 10 | `Easy` | 43 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | LCG is fun, ECDSA is fun too, so why not combine them together? Challenge contributed by m... |
| **Fischlin&#39;s Transformation (CryptoHack)** | 10 | `Easy` | 190 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mirror of Challenge for the ZKP Section Challenge contributed by killerdog and oberon Conn... |
| **Greatest Common Multiple (CODEGATE CTF)** | 10 | `Easy` | 32 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "My boss 1nteger_c said we will come back with a better GCM challenge. I hereby present, t... |
| **Hamiltonicity (CryptoHack)** | 10 | `Easy` | 297 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mirror of Challenge for the ZKP Section Challenge contributed by killerdog Connect at arch... |
| **Hamiltonicity 2 (CryptoHack)** | 10 | `Easy` | 188 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mirror of Challenge for the ZKP Section Challenge contributed by killerdog and Lance Roy C... |
| **Hyper512 (HITCON CTF)** | 10 | `Easy` | 33 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I don’t know how to design a secure stream cipher, but a large key space should be suffici... |
| **OR Proof (CryptoHack)** | 10 | `Easy` | 386 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mirror of Challenge for the ZKP Section Challenge contributed by killerdog Connect at arch... |
| **OffTopic (ECSC 2024 (Italy))** | 10 | `Easy` | 35 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Did you know that you only need FHE to build OT? _The timeout on the remote is 60 seconds.... |
| **One Round Crypto (ECSC 2024 (Italy))** | 10 | `Easy` | 31 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | It's just one round of encryption. How hard can it be? _The timeout on the remote is 300 s... |
| **Quo vadis? (ECSC 2024 (Italy))** | 10 | `Easy` | 30 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Do algebraic ducks go "quo quo"? _The timeout on the remote is 600 seconds._ Challenge con... |
| **RSATogether (ECSC 2024 (Italy))** | 10 | `Easy` | 31 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | RSA is cool, but I don't wanna do it alone. I found a way to do RSA together with my frien... |
| **Smithing contest (ECSC 2024 (Italy))** | 10 | `Easy` | 31 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Ok, so, I didn't read the part about this being a *cryptography* competition - my bad. Now... |
| **Ticket Maestro (CryptoHack)** | 10 | `Easy` | 163 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mirror of Challenge for the ZKP Section Challenge contributed by Mathias Hall-Andersen, zk... |
| **Blind (ECSC 2023 (Norway))** | 10 | `Easy` | 66 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Is this what people mean by "message blinding"? Challenge contributed by CryptoHack Challe... |
| **GLP420 (HackTM CTF)** | 10 | `Easy` | 30 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I have developed a variant of GLP, GLP420! Challenge contributed by y011d4 Connect at arch... |
| **Hide and seek (ECSC 2023 (Norway))** | 10 | `Easy` | 86 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I have hidden my flag among the elliptic curve points. Go seek! Challenge contributed by C... |
| **Irish flan (ECSC 2023 (Norway))** | 10 | `Easy` | 43 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Yum, time for dessert. Challenge contributed by CryptoHack Challenge files: - output.txt -... |
| **Leet Universe (ImaginaryCTF (Daily))** | 10 | `Easy` | 52 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | The flag is hidden somewhere in the 1337th universe. Challenge contributed by maple3142 Co... |
| **Put a ring on it (ECSC 2023 (Norway))** | 10 | `Easy` | 43 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Ring Signatures are used in some cryptocurrencies to provide anonymity for who has signed ... |
| **RRSSAA (ECSC 2023 (Norway))** | 10 | `Easy` | 141 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | My primes are prefectly random. I wonder if you can find them. Challenge contributed by Cr... |
| **Share (HITCON CTF)** | 10 | `Easy` | 36 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I hope I actually implemented Shamir Secret Sharing correctly this year. I am pretty sure ... |
| **Sus (ImaginaryCTF)** | 10 | `Easy` | 46 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Apparently, there is something weird happening with the prime generation. Challenge contri... |
| **Tough decisions (ECSC 2023 (Norway))** | 10 | `Easy` | 74 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Champagne for my real friends, real pain for my sham friends. Challenge contributed by Cry... |
| **Twist and shout (ECSC 2023 (Norway))** | 10 | `Easy` | 69 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I'll shout about my curve all day, it's totally secure. You'll have to pull the solution f... |
| **What a Curve! (Breizh CTF)** | 10 | `Easy` | 39 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Elliptic curves were originally studied for their beauty, then mathematics came. Challenge... |
| **broken oracle (HackTM CTF)** | 10 | `Easy` | 37 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I have reimplemented a cryptosystem, but it sometimes behaves strangely. But I don't think... |
| **d-phi-enc (HackTM CTF)** | 10 | `Easy` | 157 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | In CTF, there are many people who mistakenly encrypt p, q in RSA. But this time... Challen... |
| **kaitenzushi (HackTM CTF)** | 10 | `Easy` | 47 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | also known as conveyor belt sushi Challenge contributed by y011d4 Challenge files: - chall... |
| **unrandom DSA (HackTM CTF)** | 10 | `Easy` | 31 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | What if /dev/urandom is unrandom...? Challenge contributed by y011d4 Connect at archive.cr... |
| **Authenticator (Firebird Internal CTF)** | 10 | `Easy` | 33 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Hash-based authentication is great and I have invented one. Can you prove that my system i... |
| **C0ll1d3r (Firebird Internal CTF)** | 10 | `Easy` | 40 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "Find a collision for my hash algorithm! It is basically military-graded: The output is 25... |
| **Dark Arts (CODEGATE CTF)** | 10 | `Easy` | 38 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Breaking random functions is a dark art, and I need your help in this. Challenge contribut... |
| **FaILProof (SekaiCTF)** | 10 | `Easy` | 37 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "I have designed a failproof encryption system with possibly arbitrarily small public keys... |
| **FaILProof Revenge (SekaiCTF)** | 10 | `Easy` | 32 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "I am sure it's failproof now, I have increased the security levels too!¬" Challenge contr... |
| **Functional (ICC Athens)** | 10 | `Easy` | 33 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | It only took me four heat deaths of the universe to encrypt this flag. Challenge contribut... |
| **Key recovery (DCTF)** | 10 | `Easy` | 33 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I got bored and made a new block cipher, but someone stole my flag and now i need to break... |
| **Lack of Entropy (Firebird Internal CTF)** | 10 | `Easy` | 81 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mystiz's computer is lack of entropy. He needs to reuse randomness to generate the primes ... |
| **Maybe Someday (GoogleCTF)** | 10 | `Easy` | 33 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Find a collision for my hash algorithm! It is basically military-graded: The output is 256... |
| **Maybe Someday (Maybe Someday CTF)** | 10 | `Easy` | 31 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Find a collision for my hash algorithm! It is basically military-graded: The output is 256... |
| **Probability (SEETF)** | 10 | `Easy` | 36 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I've been learning about probability distributions, but it's all very confusing so I'm jus... |
| **RSA Permutation (WACON)** | 10 | `Easy` | 38 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | So I got all the hex digits of the private key, but it seems that the hex digits went thro... |
| **RSA Secret Sharing (WACON)** | 10 | `Easy` | 40 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | ON 2-out-of-3 SECRET SHARING BASED ON RSA - MemeCrypt 2022 Challenge contributed by rkm095... |
| **Signature (TSJ CTF)** | 10 | `Easy` | 39 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Another boring crypto challenge about signatures. Challenge contributed by maple3142 Chall... |
| **Unbalanced (ICC Athens)** | 10 | `Easy` | 43 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I want to keep my private key small, but I've heard this is dangerous. I think I've found ... |
| **diffecient (SekaiCTF)** | 10 | `Easy` | 31 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "Welcome to the Diffecient Security Key Database API, for securely and efficiently saving ... |
| **ed25519 magic (ICC Athens)** | 10 | `Easy` | 54 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Ed25519 is all the rage these days - it's fast, has small keys and signatures, and is desi... |
| **pekobot (AIS3 Pre-Exam)** | 10 | `Easy` | 53 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I am a bot imitating Pekora. You can talk with me through Elliptic-curve Diffie–Hellman pr... |
| **1337crypt v2 (DownUnderCTF)** | 10 | `Easy` | 44 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | 1337crypt is back. This time, with added complexity. Challenge contributed by joseph Chall... |
| **1n_jection (Zh3r0 CTF V2)** | 10 | `Easy` | 65 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "COVID: *exists* vaccine jokes: *challenge_name*" Challenge contributed by deuterium Chall... |
| **A Joke Cipher (HKCERT CTF)** | 10 | `Easy` | 82 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | In the beginning of 2020, Khaled A. Nagaty invented a cryptosystem based on key exchange. ... |
| **Chaos (Zh3r0 CTF V2)** | 10 | `Easy` | 48 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "What's the fun of rolling up a hash function if it's not chaotic enough?" Challenge contr... |
| **Cipher Mode Picker (HKCERT CTF)** | 10 | `Easy` | 75 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Every slightest mistake in cryptography would lead to a disastrous result. Let's see what ... |
| **Key Backup Service 1 (HKCERT CTF)** | 10 | `Easy` | 51 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mystiz made a key vault which could encrypts his darkest secrets (i.e., the flag). Everyth... |
| **Key Backup Service 2 (HKCERT CTF)** | 10 | `Easy` | 49 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Mystiz is really lazy. He expects that someone would crack the bank-level encryption, but ... |
| **Oofbleck (Firebird Internal CTF)** | 10 | `Easy` | 51 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Some of the block cipher modes of operation are pretty vulnerable, which includes but not ... |
| **Real Mersenne (Zh3r0 CTF V2)** | 10 | `Easy` | 42 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "Do you believe in games of luck? I hope you make your guesses real or you'll be floating ... |
| **Sign In Please, Again (HKCERT CTF)** | 10 | `Easy` | 39 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Okay. My secure authentication system was proved insecure (see [here](https://github.com/s... |
| **SpongeBob SquarePants / Battle for Bikini Bottom - Rehydrated (HTB Cyber Apocalypse)** | 10 | `Easy` | 35 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | * Wait, `spongebob` and `squarepants` don't hash to the same thing? Challenge contributed ... |
| **Sratslla SEA (HKCERT CTF)** | 10 | `Easy` | 43 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | `AddRoundKey`, `SubBytes`, `ShiftRows` and `MixColumns` are four crucial components are AE... |
| **Substitution Cipher III (DownUnderCTF)** | 10 | `Easy` | 36 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Wait a MInute, that's not a substitution cipher! Challenge contributed by joseph Challenge... |
| **Tenet: The Plagarism (HKCERT CTF)** | 10 | `Easy` | 52 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | The deadline for writing challenges is coming! Mystiz, who claimed himself not well-known ... |
| **Twist and Shout (Zh3r0 CTF V2)** | 10 | `Easy` | 44 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "Wise men once said, “Well, shake it up, baby, now Twist and shout come on and work it on ... |
| **Unevaluated (TETCTF)** | 10 | `Easy` | 53 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | We’re about to launch a new public key cryptosystem, but its security has not been careful... |
| **Unimplemented (TETCTF)** | 10 | `Easy` | 84 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | A new public key encryption algorithm is being invented, but the author is not quite sure ... |
| **import numpy as MT (Zh3r0 CTF V2)** | 10 | `Easy` | 46 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | "Python is so slow! Lets use nUmPy tO MAkE iT FaSTer. Only if there was a module for crypt... |
| **1337crypt (DownUnderCTF)** | 10 | `Easy` | 119 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Can you solve my factorisation problem if I give you a hint? Challenge contributed by jose... |
| **2020 (TETCTF)** | 10 | `Easy` | 107 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | Can you guess the 2020th number? Challenge contributed by ndh Connect at archive.cryptohac... |
| **Calm Down (HKCERT CTF)** | 10 | `Easy` | 104 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I am so excited having a chance talking to Alice. She told me to calm down - and sent me a... |
| **Sign in Please (HKCERT CTF)** | 10 | `Easy` | 151 | [前往解題](https://cryptohack.org/challenges/ctf-archive/) | I have implemented a secure authentication system. You can't eavesdrop the passwords, can ... |
