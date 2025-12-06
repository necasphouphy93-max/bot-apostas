import requests
import sys

# ==============================================================================
# 👇 PREENCHE ISTO 👇
# ==============================================================================

TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"

# COLOCA AQUI O ID QUE ACHAS QUE É O CERTO (com o -100 se tiver)
CHAT_ID = "-1003385933313" 

# ==============================================================================

print(f"--- 🕵️‍♂️ DIAGNÓSTICO DE ERRO ---")
print(f"1. A usar o Token: {TOKEN[:10]}... (OK)")
print(f"2. A tentar enviar para o ID: {CHAT_ID}")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "🔥 **TESTE DE VIDA** 🔥\nSe leres isto, o pesadelo acabou!",
    "parse_mode": "Markdown"
}

try:
    print("3. A enviar pedido ao Telegram...")
    response = requests.post(url, json=data)
    
    # AQUI ESTÁ A CHAVE: VAMOS LER O QUE O TELEGRAM RESPONDEU
    resultado = response.json()
    
    print(f"\n--- RESPOSTA DO SERVIDOR TELEGRAM ---")
    print(f"Código: {response.status_code}")
    print(f"Mensagem: {response.text}")
    print(f"-------------------------------------\n")

    if response.status_code == 200:
        print("✅ SUCESSO! O Telegram aceitou a mensagem.")
    else:
        print("❌ FALHA! O Telegram rejeitou.")
        print("👉 LEIA A MENSAGEM ACIMA PARA SABER O PORQUÊ!")
        sys.exit(1) # ISTO VAI POR O GITHUB VERMELHO

except Exception as e:
    print(f"❌ Erro de conexão: {e}")
    sys.exit(1)
