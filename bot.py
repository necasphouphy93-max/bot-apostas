import telebot
import sys

# ==========================================
# 👇 PREENCHE COM MUITO CUIDADO 👇
# ==========================================

# Tem de ter aspas! Ex: "1234..."
TELEGRAM_TOKEN = "8420090733:AAEqYWQrzuNxT6YYwK9XRHB1SKzGjRn-kBE"

# Tem de ter aspas e o sinal menos! Ex: "-100..."
GRUPO_ID = "-1003385933313"

# ==========================================

bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("--- INICIANDO TESTE DE CONEXÃO ---")
print(f"A tentar enviar para o ID: {GRUPO_ID}")

try:
    bot.send_message(GRUPO_ID, "🚀 **TESTE GITHUB:**\nEstou vivo! O Bot está conectado.")
    print("✅ SUCESSO! Mensagem enviada.")
except Exception as e:
    print(f"❌ ERRO GRAVE: {e}")
    sys.exit(1) # Isto força o GitHub a ficar Vermelho se der erro
