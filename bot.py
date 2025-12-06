import telebot
import requests
import sys

# ==========================================
# 👇 DADOS DO TEU BOT 👇
# ==========================================
TOKEN = "8420090733:AAEqYwQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"
ID_GRUPO = "-1003385933313" 
# ==========================================

print("--- 🚀 INICIANDO TESTE DE FORÇA ---")

bot = telebot.TeleBot(TOKEN)

# 1. TENTAR ENVIAR MENSAGEM IMEDIATA
try:
    print(f"A tentar enviar 'Olá' para o grupo {ID_GRUPO}...")
    bot.send_message(ID_GRUPO, "👋 **OLÁ! SOU O BOT DO GITHUB!**\n\nSe estás a ler isto, a configuração está 100% correta.\nVou começar a analisar os jogos agora...")
    print("✅ MENSAGEM ENVIADA COM SUCESSO!")
except Exception as e:
    print(f"❌ ERRO GRAVE AO ENVIAR: {e}")
    # Se falhar aqui, o GitHub vai ficar VERMELHO e tu vais saber porquê
    sys.exit(1)

# 2. CONTINUAR COM A ANÁLISE NORMAL (Se a mensagem acima funcionou)
print("A analisar o mercado...")
# (Aqui ele finge que analisa só para terminar o processo bem)
print("Análise concluída.")
