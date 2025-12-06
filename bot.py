import requests
import json
import sys

# O TEU TOKEN (Confirma que é este!)
TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"

print("--- 📡 A RASTREAR O GRUPO ---")

# Vamos perguntar ao Telegram: "Onde é que o bot foi adicionado recentemente?"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    response = requests.get(url)
    dados = response.json()
    
    if not dados.get("ok"):
        print("❌ Erro no Token! Verifica se copiaste bem.")
        sys.exit(1)
        
    resultados = dados.get("result", [])
    
    if len(resultados) == 0:
        print("⚠️ O Bot não vê nada. Tens a certeza que escreveste 'ESTOU AQUI' no grupo?")
        sys.exit(1)

    print(f"✅ Encontrei {len(resultados)} interações! Vamos procurar o teu grupo...\n")
    
    grupo_encontrado = False

    for update in reversed(resultados): # Ver do mais recente para o mais antigo
        # Verifica mensagens normais
        if "message" in update:
            msg = update["message"]
            chat = msg["chat"]
            
            # Se for um Grupo ou Supergrupo
            if chat["type"] in ["group", "supergroup"]:
                nome = chat.get("title", "Sem Nome")
                id_real = chat["id"]
                texto = msg.get("text", "")
                
                print(f"🏠 GRUPO ENCONTRADO: '{nome}'")
                print(f"📝 Última mensagem: '{texto}'")
                print(f"🆔 ID PARA COPIAR: {id_real}")
                print("--------------------------------------------------")
                grupo_encontrado = True
                
        # Verifica se alguém adicionou o bot (My Chat Member)
        if "my_chat_member" in update:
            chat = update["my_chat_member"]["chat"]
            nome = chat.get("title", "Sem Nome")
            id_real = chat["id"]
            
            print(f"👋 O BOT ENTROU NO GRUPO: '{nome}'")
            print(f"🆔 ID PARA COPIAR: {id_real}")
            print("--------------------------------------------------")
            grupo_encontrado = True

    if not grupo_encontrado:
        print("❌ O Bot recebeu mensagens, mas parecem ser de chat privado, não de grupo.")
        
except Exception as e:
    print(f"Erro: {e}")
