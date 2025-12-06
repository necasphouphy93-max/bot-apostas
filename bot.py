import requests
import sys

# O TEU TOKEN
TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"

print("--------------------------------------------------")
print("👀 OLÁ! EU SOU O CÓDIGO NOVO (ESPIÃO) 👀")
print("Se estás a ler isto, o código antigo JÁ ERA!")
print("--------------------------------------------------")

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    print("A perguntar ao Telegram por mensagens recentes...")
    response = requests.get(url)
    dados = response.json()
    
    if "result" in dados:
        lista = dados["result"]
        print(f"Encontrei {len(lista)} atividades.")
        
        for item in reversed(lista):
            # Procura mensagens de grupo
            if "message" in item:
                chat = item["message"]["chat"]
                nome = chat.get("title", "Privado")
                id_real = chat["id"]
                texto = item["message"].get("text", "Sem texto")
                
                print(f"\n📢 Mensagem: {texto}")
                print(f"🏠 Grupo: {nome}")
                print(f"🆔 ID OBRIGATÓRIO: {id_real}")
                print("-----------------------------------")
                
            # Procura convites para grupo
            if "my_chat_member" in item:
                chat = item["my_chat_member"]["chat"]
                nome = chat.get("title", "Grupo")
                id_real = chat["id"]
                print(f"\n👋 FUI ADICIONADO A: {nome}")
                print(f"🆔 ID OBRIGATÓRIO: {id_real}")
                print("-----------------------------------")

    else:
        print("Erro: O Token pode estar errado.")

except Exception as e:
    print(f"Erro Fatal: {e}")
