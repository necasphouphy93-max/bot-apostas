import telebot
import requests
import time
from datetime import datetime

# ==============================================================================
# 👇👇👇 CONFIGURAÇÕES - PREENCHE AQUI 👇👇👇
# ==============================================================================

# ⚠️ NÃO TE ESQUEÇAS DE COLOCAR O TEU TOKEN E ID AQUI!
TELEGRAM_TOKEN = "COLOCA_O_TEU_TOKEN_AQUI"
GRUPO_ID = "COLOCA_O_ID_AQUI"

# ==============================================================================

RAPIDAPI_KEY = '544d4e147f6767e1a4d8d1b3244347ca'
SEASON = "2025"
# Ligas: Premier, La Liga, PT, Serie A, Bundes, Ligue 1, Eredivisie
LEAGUES = [39, 140, 94, 135, 78, 61, 88]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def analisar_forma_inteligente(team_id):
    # Lógica de Pontos: Vit=3, Emp=1. Precisa de 10pts em 15 possíveis.
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    try:
        data = requests.get(url, headers=headers, params={"team": team_id, "last": "5", "status": "FT"}).json()
        jogos = data.get('response', [])
        if not jogos: return False, 0
        pontos = 0
        derrotas = 0
        for j in jogos:
            home = j['teams']['home']['id'] == team_id
            g_home = j['goals']['home']
            g_away = j['goals']['away']
            if home:
                if g_home > g_away: pontos += 3
                elif g_home == g_away: pontos += 1
                else: derrotas += 1
            else:
                if g_away > g_home: pontos += 3
                elif g_away == g_home: pontos += 1
                else: derrotas += 1
        return (pontos >= 10 and derrotas <= 1), pontos
    except:
        return False, 0

def run():
    print(f"🕵️‍♂️ A analisar o mercado...")
    tips = []
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    for league in LEAGUES:
        if len(tips) >= 3: break
        url_fix = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        try:
            resp = requests.get(url_fix, headers=headers, params={"date": hoje, "league": league, "season": SEASON}).json()
            matches = resp.get('response', [])
            if not matches: continue
            
            for match in matches:
                if len(tips) >= 3: break
                fid = match['fixture']['id']
                home = match['teams']['home']['name']
                hid = match['teams']['home']['id']
                away = match['teams']['away']['name']
                
                url_odds = "https://api-football-v1.p.rapidapi.com/v3/odds"
                ro = requests.get(url_odds, headers=headers, params={"fixture": fid, "bookmaker": "6"}).json()
                
                if ro['response']:
                    bets = ro['response'][0]['bookmakers'][0]['bets']
                    melhor_opcao = None
                    odd_sel = 0
                    
                    # 1. Vencedor
                    m_1x2 = next((b for b in bets if b['id'] == 1), None)
                    if m_1x2:
                        val = next((v for v in m_1x2['values'] if v['value'] == 'Home'), None)
                        if val and 1.20 <= float(val['odd']) <= 1.35:
                            melhor_opcao = "Vencedor (Casa)"
                            odd_sel = float(val['odd'])
                    # 2. Dupla Chance
                    if not melhor_opcao:
                        m_dc = next((b for b in bets if b['id'] == 12), None)
                        if m_dc:
                            val = next((v for v in m_dc['values'] if 'Home' in v['value'] and 'Draw' in v['value']), None)
                            if val and 1.20 <= float(val['odd']) <= 1.35:
                                melhor_opcao = "Casa ou Empate (1X)"
                                odd_sel = float(val['odd'])
                    # 3. Golos
                    if not melhor_opcao:
                        m_gl = next((b for b in bets if b['id'] == 5), None)
                        if m_gl:
                            val = next((v for v in m_gl['values'] if v['value'] == 'Over 1.5'), None)
                            if val and 1.20 <= float(val['odd']) <= 1.35:
                                melhor_opcao = "Over 1.5 Golos"
                                odd_sel = float(val['odd'])
                                
                    if melhor_opcao:
                        ok, pts = analisar_forma_inteligente(hid)
                        if ok:
                            tips.append({'jogo': f"{home} vs {away}", 'mercado': melhor_opcao, 'odd': odd_sel, 'pts': pts})
                time.sleep(0.5)
        except: continue

    # ==========================================================
    # 👇 AQUI ESTÁ A PARTE QUE MUDA (ENVIA SEMPRE MENSAGEM) 👇
    # ==========================================================

    if len(tips) >= 3:
        odd_total = 1.0
        msg = "☁️ **MÚLTIPLA AUTOMÁTICA GITHUB** ☁️\n\n"
        for t in tips:
            odd_total *= t['odd']
            msg += f"⚽ **{t['jogo']}**\n🎯 {t['mercado']}\n📊 Forma: {t['pts']}/15 pts\n💰 Odd: {t['odd']}\n\n"
        msg += f"🚀 **ODD TOTAL: {odd_total:.2f}**"
        try:
            bot.send_message(GRUPO_ID, msg, parse_mode='Markdown')
            print("✅ Múltipla enviada!")
        except Exception as e: print(e)
    else:
        # ESTA É A MENSAGEM DE AVISO
        print("Sem tripla perfeita hoje.")
        msg_vazia = "⚠️ **Relatório Diário:**\n\nO Bot analisou o mercado, mas não encontrou 3 jogos com segurança máxima (Odd 1.20-1.35 + Forma Boa).\n\n🛡️ **Hoje protegemos a banca.**"
        try:
            bot.send_message(GRUPO_ID, msg_vazia, parse_mode='Markdown')
            print("✅ Aviso de 'Sem Jogos' enviado!")
        except Exception as e: print(e)

if __name__ == "__main__":
    run()
