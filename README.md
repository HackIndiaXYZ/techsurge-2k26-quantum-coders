# 🛡️ FinShield AI

### AI-Powered Financial Scam Detection & Safety Assistant

FinShield AI is a smart financial safety assistant designed to help users identify suspicious messages, links, and payment requests before they take action.

## 🚨 Problem Statement

People frequently receive phishing messages, fake payment requests, OTP scams, suspicious links, prize scams, and account-blocking threats.

Many users cannot easily identify whether these messages are genuine or fraudulent.

## 💡 Our Solution

FinShield AI analyzes suspicious financial content and provides:

- 🚨 Risk Score
- 🏷️ Scam Category
- ⚠️ Warning Signs
- 🛡️ Recommended Safety Actions

The goal is to help users understand potential financial threats before making a risky decision.

## ✨ Features

### 📩 Message Scanner
Detects suspicious SMS, WhatsApp messages, emails and notifications.

### 🔗 Link Scanner
Analyzes URL structure for suspicious patterns without opening the website.

Checks for:
- Missing HTTPS
- IP-based URLs
- Suspicious keywords
- @ symbols
- Unusually long URLs

### 💳 Payment Scanner
Analyzes suspicious payment and money-transfer requests.

### 🕘 Scan History
Stores recent scans during the current session so users can review previous results.

### 📊 Risk Classification

| Score | Risk |
|---|---|
| 0–39 | 🟢 Low Risk |
| 40–69 | ⚠️ Medium Risk |
| 70–100 | 🚨 High Risk |

## 🧠 Technology Stack

- Python
- Streamlit
- Google Gemini
- Regular Expressions
- URL Parsing
- python-dotenv

## 🏗️ How It Works

```text
User Input
    ↓
FinShield AI
    ↓
Message / Link / Payment Analysis
    ↓
Risk Score
    ↓
Scam Category
    ↓
Warning Signs
    ↓
Recommended Safety Actions