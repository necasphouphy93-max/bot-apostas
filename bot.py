import requests
import time
import sys

# O TEU TOKEN (Confirma se é deste bot que está no grupo!)
TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"

print("--- A PROCURAR MENSAGENS RECENTES ---")

# Vamos pedir ao Telegram tudo o que aconteceu com este Bot
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    response = requests.get(url)
    dados = response.json()
    
    if not dados.get("ok"):
        print("❌ O Token está inválido! Verifica no BotFather.")
        sys.exit(1)

    result = dados.get("result", [])

    if len(result) == 0:
        print("⚠️ O Bot está online, mas NÃO VIU nenhuma mensagem.")
        print("MOTIVOS POSSÍVEIS:")
        print("1. O bot que está no grupo NÃO É este do Token.")
        print("2. O bot não é Administrador e não consegue ler.")
        print("3. Ainda não escreveste 'TESTE GITHUB 123' no grupo.")
        sys.exit(1)

    print(f"✅ O Bot encontrou {len(result)} atividades!")
    
    encontrei = False
    for update in result:
        # Tenta encontrar a mensagem de grupo
        if "message" in update:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            tipo = msg["chat"]["type"]
            texto = msg.get("text", "")
            titulo = msg["chat"].get("title", "Privado")
            
            print(f"\n📩 Mensagem: '{texto}'")
            print(f"🏠 Grupo: '{titulo}'")
            print(f"🆔 ID REAL: {chat_id}")
            
            if "TESTE GITHUB" in texto:
                print("🎉 ENCONTREI O TEU GRUPO! O ID CERTO É O DE CIMA!")
                encontrei = True

        # Tenta encontrar quando adicionaste o bot ao grupo
        if "my_chat_member" in update:
            chat_id = update["my_chat_member"]["chat"]["id"]
            nome_grupo = update["my_chat_member"]["chat"]["title"]
            print(f"\n👋 Fui adicionado ao grupo: '{nome_grupo}'")
            print(f"🆔 ID REAL: {chat_id}")
            encontrei = True

    if not encontrei:
        print("\n❌ Li algumas coisas, mas não vi a tua mensagem 'TESTE GITHUB 123'.")

except Exception as e:
    print(f"Erro: {e}")
