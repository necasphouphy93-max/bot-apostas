import requests
import sys

# ==========================================
# 👇 PREENCHE AQUI 👇
# ==========================================

TELEGRAM_TOKEN = "8420090733:AAEqYWQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"
GRUPO_ID = "-1003385933313" 

# ==========================================

print("--- INICIANDO DIAGNÓSTICO ---")
print(f"1. A usar o Token: {TELEGRAM_TOKEN[:10]}... (oculto)")
print(f"2. A tentar enviar para o Grupo ID: {GRUPO_ID}")

# Montar o pedido direto à API
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": GRUPO_ID,
    "text": "🚨 TESTE DE DIAGNÓSTICO GITHUB 🚨\nSe leres isto, funcionou.",
    "parse_mode": "Markdown"
}

try:
    print("3. Enviando pedido ao Telegram...")
    response = requests.post(url, json=payload)
    
    # IMPRIMIR A RESPOSTA EXATA DO TELEGRAM
    print(f"--- RESPOSTA DO SERVIDOR ---")
    print(f"Código HTTP: {response.status_code}")
    print(f"Mensagem: {response.text}")
    print(f"------------------------------")

    if response.status_code == 200:
        print("✅ SUCESSO! A mensagem foi entregue.")
    else:
        print("❌ FALHA! O Telegram rejeitou o pedido.")
        sys.exit(1) # Isto força o GitHub a ficar VERMELHO

except Exception as e:
    print(f"❌ ERRO CRÍTICO NO PYTHON: {e}")
    sys.exit(1)
