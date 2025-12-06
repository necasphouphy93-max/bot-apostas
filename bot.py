import requests
import sys

# ==========================================
# 👇 PREENCHE ISTO COM CUIDADO 👇
# ==========================================

# Apaga o texto e põe o teu Token entre aspas
TELEGRAM_TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"

# Apaga o texto e põe o teu ID entre aspas (com o sinal menos!)
GRUPO_ID = "-1003385933313" 

# ==========================================

print("--- INICIANDO DIAGNÓSTICO ---")

# Montar o pedido direto à API do Telegram
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": GRUPO_ID,
    "text": "🚨 TESTE FINAL GITHUB 🚨\nSe leres isto, está tudo a funcionar!",
    "parse_mode": "Markdown"
}

try:
    print(f"A tentar enviar para: {GRUPO_ID}...")
    response = requests.post(url, json=payload)
    
    # IMPRIMIR A RESPOSTA EXATA DO SERVIDOR
    print(f"Código HTTP: {response.status_code}")
    print(f"Mensagem do Telegram: {response.text}")

    if response.status_code == 200:
        print("✅ SUCESSO! Mensagem entregue.")
    else:
        print("❌ FALHA! O Telegram rejeitou.")
        # Isto força o GitHub a ficar VERMELHO para tu veres que falhou
        sys.exit(1) 

except Exception as e:
    print(f"❌ Erro de Ligação: {e}")
    sys.exit(1)
