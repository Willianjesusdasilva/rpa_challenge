# 🚀 Desafio Técnico - Automação de APIs Seguras

Este repositório contém a resolução de três desafios técnicos progressivos (`easy`, `hard` e `extreme`), focados em automação, segurança e comunicação com APIs protegidas.

---

## 📁 Estrutura do Projeto

```
.
├── challenges/easy.py       # Desafio básico (autenticação simples)
├── challenges/hard.py       # Desafio intermediário (challenge + certificado)
├── challenges/extreme.py    # Desafio avançado (WebSocket + PoW + criptografia)
└── README.md
```

---

## ⚙️ Execução (Sem dor de dependência)

Este projeto utiliza o padrão de scripts com dependências embutidas.

👉 Basta usar o `uv run` para executar qualquer desafio sem instalar nada manualmente.

Instale o uv (caso não tenha):

```bash
pip install uv
```

---

## 🧠 Desafios

---

### 🟢 Easy

📄 Arquivo: `easy.py`

#### ▶️ Execução

```bash
uv run ./challenges/easy.py
```

---

### 🟡 Hard

📄 Arquivo: `hard.py`

#### ▶️ Execução

```bash
uv run ./challenges/hard.py
```

---

### 🔴 Extreme

📄 Arquivo: `extreme.py`

#### ▶️ Execução

```bash
uv run ./challenges/extreme.py
```

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

- Não é necessário instalar dependências manualmente
- O `uv run` resolve tudo automaticamente a partir do header dos scripts
- O desafio `extreme` pode consumir CPU devido ao PoW