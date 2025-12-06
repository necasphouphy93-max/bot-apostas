import requests
import sys

# ==========================================
# DADOS QUE VAMOS TESTAR
# ==========================================
TELEGRAM_TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"
GRUPO_ID = "-1003385933313"
# ==========================================

print("--- INICIANDO DIAGNÓSTICO DE CONEXÃO ---")

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": GRUPO_ID,
    "text": "🚨 **TESTE FINAL GITHUB** 🚨\n\nSe leres isto, o bot tem permissão para falar!",
    "parse_mode": "Markdown"
}

try:
    print(f"A tentar enviar mensagem para o ID: {GRUPO_ID}...")
    response = requests.post(url, json=payload)
    
    # MOSTRAR O QUE O TELEGRAM RESPONDEU
    print(f"Código HTTP: {response.status_code}")
    print(f"Resposta do Telegram: {response.text}")

    if response.status_code == 200:
        print("✅ SUCESSO! A mensagem foi aceite.")
    else:
        print("❌ FALHA CRÍTICA! O Telegram recusou.")
        # Isto vai fazer o GitHub ficar VERMELHO
        sys.exit(1)

except Exception as e:
    print(f"❌ Erro de Python: {e}")
    sys.exit(1)
