import requests
import json

# ==========================================
# 👇 CÓDIGO ESPIÃO 👇
# ==========================================
TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"

print("--- 📡 A PROCURAR O ID DO GRUPO ---")

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    # Vai à internet buscar as mensagens recentes
    response = requests.get(url)
    dados = response.json()
    
    if "result" in dados:
        lista = dados["result"]
        print(f"Encontrei {len(lista)} atividades recentes.")
        
        if len(lista) == 0:
            print("⚠️ O Bot não vê mensagens. Tenta remover o bot do grupo e adicionar de novo!")
        
        # Mostra as últimas mensagens
        for item in reversed(lista):
            if "message" in item:
                chat = item["message"]["chat"]
                texto = item["message"].get("text", "(Sem texto)")
                tipo = chat["type"]
                id_real = chat["id"]
                titulo = chat.get("title", "Privado")
                
                print(f"\n📩 Mensagem: '{texto}'")
                print(f"🏠 Grupo: '{titulo}'")
                print(f"🆔 ID PARA COPIAR: {id_real}")
                print("-" * 30)
            
            if "my_chat_member" in item:
                chat = item["my_chat_member"]["chat"]
                nome = chat.get("title", "Grupo")
                id_real = chat["id"]
                print(f"\n👋 O Bot foi adicionado ao grupo: '{nome}'")
                print(f"🆔 ID PARA COPIAR: {id_real}")
                print("-" * 30)
    else:
        print("Erro ao ligar ao Telegram.")

except Exception as e:
    print(f"Erro: {e}")
