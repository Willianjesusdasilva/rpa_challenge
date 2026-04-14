# 🚀 Desafio Técnico - Automação de APIs Seguras

Este repositório contém a resolução de três desafios técnicos progressivos (`easy`, `hard` e `extreme`), focados em automação, segurança e comunicação com APIs protegidas.

---

## 📁 Estrutura do Projeto

```
.
├── easy.py       # Desafio básico (autenticação simples)
├── hard.py       # Desafio intermediário (challenge + certificado)
├── extreme.py    # Desafio avançado (WebSocket + PoW + criptografia)
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.10+
- Dependências:
  - httpx
  - cryptography
  - websockets

Instalação:

```bash
pip install httpx cryptography websockets
```

---

## 🧠 Desafios

---

### 🟢 Easy

📄 Arquivo: `easy.py`

#### ✔️ Descrição

Realiza autenticação simples via API REST utilizando `username` e `password`.

#### 🔧 Fluxo

1. Envia requisição POST para `/api/easy/login`
2. Recebe resposta com status e payload

#### ▶️ Execução

```bash
python easy.py
```

#### ⏱️ Tempo de execução

~0.2s

---

### 🟡 Hard

📄 Arquivo: `hard.py`

#### ✔️ Descrição

Fluxo autenticado com:

- Challenge baseado em hash
- Download de certificado `.pfx`
- Conversão para `.pem`
- Autenticação mTLS (client certificate)

#### 🔧 Fluxo

1. Gera `nonce` e `timestamp`
2. Calcula hash SHA256 (challenge)
3. Realiza login
4. Baixa certificado `.pfx`
5. Converte para `.pem`
6. Faz requisição autenticada com certificado

#### ▶️ Execução

```bash
python hard.py
```

#### ⏱️ Tempo de execução

~1 a 2 segundos

---

### 🔴 Extreme

📄 Arquivo: `extreme.py`

#### ✔️ Descrição

Desafio avançado envolvendo:

- WebSocket seguro (WSS)
- Proof of Work (PoW)
- Criptografia AES-CBC
- Token intermediário
- OTP dinâmico

#### 🔧 Fluxo

1. Inicializa sessão via `/api/extreme/init`
2. Conecta via WebSocket
3. Resolve desafio de PoW (multi-thread)
4. Recebe token intermediário
5. Valida token via API
6. Recebe payload criptografado
7. Descriptografa usando AES
8. Extrai OTP
9. Finaliza autenticação

#### ▶️ Execução

```bash
python extreme.py
```

#### ⏱️ Tempo de execução

~3 a 10 segundos (dependendo da dificuldade do PoW e CPU)

---

## 🔐 Técnicas Utilizadas

- HTTP Client (`httpx`)
- WebSocket (`websockets`)
- Hashing (`SHA-256`)
- Criptografia simétrica (`AES-CBC`)
- PKCS#7 Padding
- Certificados digitais (PFX → PEM)
- mTLS (Mutual TLS)
- Multithreading (Proof of Work)

---

## ⚠️ Observações

- O projeto utiliza `verify=False` por se tratar de ambiente local (`localhost`).
- Certificados são manipulados dinamicamente e removidos após uso.
- O desafio `extreme` pode consumir CPU devido ao PoW.

---

## 👨‍💻 Autor

Projeto desenvolvido como parte de um teste técnico focado em automação e segurança.
