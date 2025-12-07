<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>Tuga Tips Pro</title>
    
    <!-- PWA Settings -->
    <meta name="theme-color" content="#15803d" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    
    <!-- Ícone -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚽</text></svg>">

    <!-- Bibliotecas Externas (CDN) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    
    <!-- Babel para compilar JSX no navegador -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- Import Map para Módulos (Links Públicos e Seguros) -->
    <script type="importmap">
{
  "imports": {
    "react": "https://esm.sh/react@18.2.0",
    "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
    "lucide-react": "https://esm.sh/lucide-react@0.330.0",
    "@google/genai": "https://esm.run/@google/genai",
    "react-dom/": "https://aistudiocdn.com/react-dom@^19.2.0/",
    "react/": "https://aistudiocdn.com/react@^19.2.0/"
  }
}
</script>

    <style>
      body { 
        font-family: 'Inter', sans-serif; 
        -webkit-tap-highlight-color: transparent; 
        /* Fundo de Futebol com Bola e Taça */
        background: 
            linear-gradient(to bottom, rgba(240, 253, 244, 0.85), rgba(255, 255, 255, 0.95)),
            url('https://images.unsplash.com/photo-1551958219-acbc608c6377?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
      }
      
      /* Animações */
      @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
      .animate-fade-in { animation: fadeIn 0.6s ease-out forwards; }
      
      .slide-in-from-bottom-4 { animation: slideInBottom4 0.7s ease-out forwards; }
      @keyframes slideInBottom4 { from { transform: translateY(1rem); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
      
      /* Skeleton Loading Animation */
      .skeleton {
        background: linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
        background-size: 200% 100%;
        animation: 1.5s shine linear infinite;
      }
      @keyframes shine { to { background-position-x: -200%; } }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel" data-type="module">
        import React, { useState, useEffect, useCallback } from "react";
        import { createRoot } from "react-dom/client";
        import { GoogleGenAI } from "@google/genai";
        import { 
            Bell, BellOff, Trophy, Clock, CheckCircle, XCircle, SearchCheck, 
            ChevronDown, ChevronUp, BarChart2, Loader2, AlertCircle, 
            TrendingUp, History, LockKeyhole, Percent 
        } from "lucide-react";

        // CONFIGURAÇÃO
        const API_KEY = "AIzaSyAIotZ_PncE9SHxhARqh2RvBVhNSFXlNhw"; 
        const START_HOUR = 8; 
        const STORAGE_KEY = 'tuga_tips_betclic_v7';
        const NOTIF_KEY = 'tuga_tips_notif';

        // Extração JSON Robusta
        const extractJson = (text) => {
            const jsonMatch = text.match(/```json\s*([\s\S]*?)\s*```/);
            if (jsonMatch && jsonMatch[1]) return jsonMatch[1];
            const firstBrace = text.indexOf('[');
            const lastBrace = text.lastIndexOf(']');
            if (firstBrace !== -1 && lastBrace !== -1) return text.substring(firstBrace, lastBrace + 1);
            return text;
        };

        // Serviço IA
        const fetchDailyBets = async () => {
            try {
                const ai = new GoogleGenAI({ apiKey: API_KEY });
                const today = new Date().toLocaleDateString('pt-PT');
                
                const prompt = `
                  Atue como um especialista em apostas desportivas focado no mercado Português (Betclic). Hoje é ${today}.
                  
                  TAREFA:
                  Encontre 3 dicas de aposta para jogos REAIS de HOJE ou AMANHÃ.
                  
                  REGRAS ESTRITAS (BETCLIC):
                  1. **FONTE DE ODDS**: Pesquise especificamente por odds da **Betclic Portugal**.
                  2. **MERCADOS**: Use a terminologia da Betclic (ex: "Resultado Final", "Total de Golos", "Hipótese Dupla").
                  3. **VALORES**: As odds devem estar entre 1.25 e 1.35.
                  4. **DESPORTOS**: Futebol ou Basquetebol (NBA/Euroliga).
                  
                  ANÁLISE OBRIGATÓRIA:
                  Para cada jogo, analise os últimos 5 jogos de ambas as equipas. A justificação tem de citar essa forma recente (ex: "Venceu 4 dos últimos 5").
                  
                  OUTPUT JSON ARRAY:
                  [{ 
                    "sport": "Futebol", 
                    "league": "Liga", 
                    "match": "Casa vs Fora", 
                    "selection": "Aposta (Termo Betclic)", 
                    "odd": 1.30, 
                    "startTime": "HH:MM", 
                    "rationale": "Análise da forma recente..." 
                  }]
                `;

                const response = await ai.models.generateContent({
                    model: "gemini-2.5-flash",
                    contents: prompt,
                    config: { tools: [{ googleSearch: {} }], temperature: 0.3 },
                });

                const parsedData = JSON.parse(extractJson(response.text || ""));
                if (!Array.isArray(parsedData) || parsedData.length < 3) throw new Error("Dados inválidos");

                const selections = parsedData.slice(0, 3).map((item, index) => ({
                    id: `bet-${Date.now()}-${index}`,
                    sport: item.sport,
                    match: item.match,
                    league: item.league,
                    selection: item.selection,
                    odd: parseFloat(item.odd),
                    rationale: item.rationale,
                    startTime: item.startTime,
                    outcome: 'pending'
                }));

                const totalOdd = selections.reduce((acc, curr) => acc * curr.odd, 1);

                return {
                    id: `slip-${Date.now()}`,
                    date: new Date().toISOString(),
                    selections,
                    totalOdd: parseFloat(totalOdd.toFixed(2)),
                    status: 'pending'
                };
            } catch (error) {
                console.error(error);
                return null;
            }
        };

        const checkSlipStatus = async (slip) => {
            try {
                const ai = new GoogleGenAI({ apiKey: API_KEY });
                const prompt = `Verifique resultados finais dos jogos: ${JSON.stringify(slip.selections.map(s => ({ match: s.match, selection: s.selection })))}. Retorne JSON array strings: ["won", "lost", "pending"].`;
                const response = await ai.models.generateContent({
                    model: "gemini-2.5-flash",
                    contents: prompt,
                    config: { tools: [{ googleSearch: {} }] },
                });
                const results = JSON.parse(extractJson(response.text || ""));
                let anyLost = false, allWon = true, anyPending = false;
                const updatedSelections = slip.selections.map((sel, i) => {
                    const res = results[i] || 'pending';
                    if (res === 'lost') anyLost = true;
                    if (res === 'pending') anyPending = true;
                    if (res !== 'won') allWon = false;
                    return { ...sel, outcome: res };
                });
                let newStatus = 'pending';
                if (anyLost) newStatus = 'lost';
                else if (!anyPending && allWon) newStatus = 'won';
                return { ...slip, selections: updatedSelections, status: newStatus, checkedAt: new Date().toISOString() };
            } catch (e) { return slip; }
        };

        // Componentes UI
        const Header = ({ notificationsEnabled, onToggle }) => (
            <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md shadow-md border-b-4 border-green-700">
                <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
                    <div className="flex items-center space-x-2">
                        <div className="bg-gradient-to-br from-red-600 to-red-700 p-2 rounded-lg text-white shadow-sm">
                            <Trophy size={24} />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-slate-900 leading-none">Tuga Tips Pro</h1>
                            <p className="text-xs text-green-700 font-bold uppercase tracking-wider">Boletim Diário</p>
                        </div>
                    </div>
                    <button onClick={onToggle} className={`p-2 rounded-full shadow-sm border border-slate-100 ${notificationsEnabled ? 'bg-green-100 text-green-700' : 'bg-white/50 text-slate-400'}`}>
                        {notificationsEnabled ? <Bell size={20} /> : <BellOff size={20} />}
                    </button>
                </div>
            </header>
        );

        const BetCard = ({ selection }) => {
            const [expanded, setExpanded] = useState(false);
            return (
                <div className="bg-white/90 backdrop-blur-md rounded-xl shadow-sm border border-white/40 overflow-hidden mb-4 transition-all hover:shadow-lg">
                    <div className="p-4 cursor-pointer" onClick={() => setExpanded(!expanded)}>
                        <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center space-x-2 text-sm text-slate-600 font-medium">
                                <span>{selection.sport && selection.sport.includes('Fut') ? '⚽' : '🏀'}</span>
                                <span className="uppercase tracking-wide text-xs">{selection.league}</span>
                            </div>
                            <div className="flex items-center text-xs text-slate-400">
                                <Clock size={12} className="mr-1" />
                                {selection.startTime}
                            </div>
                        </div>
                        <div className="flex justify-between items-center">
                            <div>
                                <h3 className="text-lg font-bold text-slate-800">{selection.match}</h3>
                                <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-sm font-medium border border-slate-200 mt-1 inline-block">
                                    {selection.selection}
                                </span>
                            </div>
                            <div className="text-right">
                                <span className="text-2xl font-bold text-green-700">{selection.odd.toFixed(2)}</span>
                                <div className="text-[10px] text-red-500 font-bold uppercase mt-1 flex items-center justify-end">
                                    <Percent size={10} className="mr-1"/>Ref. Betclic
                                </div>
                            </div>
                        </div>
                        {/* Indicador de expansão sutil */}
                        <div className="flex justify-center mt-2">
                             {expanded ? <ChevronUp size={16} className="text-slate-300" /> : <ChevronDown size={16} className="text-slate-300" />}
                        </div>
                    </div>
                    {expanded && (
                        <div className="px-4 pb-4 pt-0 bg-slate-50/80 border-t border-slate-100">
                            <div className="mt-3">
                                <h4 className="text-xs font-bold text-red-600 uppercase mb-2 flex items-center">
                                    <BarChart2 size={12} className="mr-1"/> Forma (Últimos 5 Jogos)
                                </h4>
                                <p className="text-sm text-slate-600 leading-relaxed whitespace-pre-line text-justify">
                                    {selection.rationale}
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            );
        };

        const SkeletonCard = () => (
            <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-white/20 p-4 mb-4">
                <div className="flex justify-between mb-3">
                    <div className="skeleton h-4 w-20 rounded"></div>
                    <div className="skeleton h-4 w-12 rounded"></div>
                </div>
                <div className="flex justify-between items-center">
                    <div className="space-y-2 w-2/3">
                        <div className="skeleton h-6 w-3/4 rounded"></div>
                        <div className="skeleton h-5 w-1/2 rounded"></div>
                    </div>
                    <div className="skeleton h-8 w-16 rounded"></div>
                </div>
            </div>
        );

        const HistoryList = ({ history, onCheck, checkingId }) => (
            <div className="space-y-4">
                {history.length === 0 ? <div className="text-center py-8 text-slate-500 text-sm bg-white/60 backdrop-blur-sm rounded-xl">Sem histórico recente.</div> :
                history.map(slip => (
                    <div key={slip.id} className={`relative rounded-xl border-l-4 overflow-hidden shadow-sm backdrop-blur-sm ${
                        slip.status === 'won' ? 'bg-green-50/95 border-green-500' :
                        slip.status === 'lost' ? 'bg-red-50/95 border-red-500' : 'bg-white/95 border-yellow-400'
                    }`}>
                        <div className="p-4">
                            <div className="flex justify-between items-start mb-3">
                                <div>
                                    <div className="text-xs text-slate-500 uppercase font-semibold">{new Date(slip.date).toLocaleDateString('pt-PT')}</div>
                                    <div className="text-sm font-bold text-slate-800 mt-1">{slip.status === 'won' ? 'GREEN ✅' : slip.status === 'lost' ? 'RED ❌' : 'Pendente'}</div>
                                </div>
                                <div className="text-right">
                                    <div className="text-xs text-slate-500">Odd Total</div>
                                    <div className="font-bold text-xl text-slate-900">{slip.totalOdd.toFixed(2)}</div>
                                </div>
                            </div>
                            <div className="space-y-2 mb-3">
                                {slip.selections.map((sel, i) => (
                                    <div key={i} className="flex justify-between items-center text-sm border-b border-black/5 pb-1 last:border-0">
                                        <span className="truncate max-w-[60%] text-slate-700">{sel.match}</span>
                                        <div className="flex items-center space-x-2">
                                            <span className="font-medium text-slate-600">{sel.odd.toFixed(2)}</span>
                                            {sel.outcome === 'won' ? <CheckCircle size={14} className="text-green-600"/> :
                                             sel.outcome === 'lost' ? <XCircle size={14} className="text-red-600"/> :
                                             <Clock size={14} className="text-yellow-500"/>}
                                        </div>
                                    </div>
                                ))}
                            </div>
                            {slip.status === 'pending' && (
                                <button onClick={() => onCheck(slip.id)} disabled={checkingId === slip.id}
                                    className="flex items-center space-x-1 bg-white border border-slate-200 px-3 py-1.5 rounded-full text-xs font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50 shadow-sm">
                                    {checkingId === slip.id ? <Loader2 size={14} className="animate-spin text-blue-600" /> : <SearchCheck size={14} className="text-blue-600" />}
                                    <span>{checkingId === slip.id ? 'Verificando...' : 'Verificar'}</span>
                                </button>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        );

        const App = () => {
            const [currentSlip, setCurrentSlip] = useState(null);
            const [history, setHistory] = useState([]);
            const [appStatus, setAppStatus] = useState('idle'); 
            const [timeMsg, setTimeMsg] = useState('');
            const [activeTab, setActiveTab] = useState('daily');
            const [checkingId, setCheckingId] = useState(null);
            const [notificationsEnabled, setNotificationsEnabled] = useState(false);

            const runLogic = useCallback(async () => {
                const storedDataStr = localStorage.getItem(STORAGE_KEY);
                let localHistory = [], localSlip = null;
                const now = new Date();
                const todayStr = now.toLocaleDateString('pt-PT');

                if (storedDataStr) {
                    const parsed = JSON.parse(storedDataStr);
                    localHistory = parsed.history || [];
                    localSlip = parsed.currentSlip;
                    // Limpar histórico antigo (>10 dias)
                    const tenDaysAgo = new Date(); tenDaysAgo.setDate(tenDaysAgo.getDate() - 10);
                    localHistory = localHistory.filter(s => new Date(s.date) > tenDaysAgo);

                    if (localSlip) {
                        const slipDate = new Date(localSlip.date).toLocaleDateString('pt-PT');
                        // PERSISTÊNCIA RÍGIDA: Se tem slip de hoje, usa-o e pronto.
                        if (slipDate === todayStr) {
                            setAppStatus('success'); setCurrentSlip(localSlip); setHistory(localHistory);
                            return;
                        }
                        if (slipDate !== todayStr) {
                            if (!localHistory.find(h => h.id === localSlip.id)) localHistory.unshift(localSlip);
                            localSlip = null;
                        }
                    }
                }
                
                if (now.getHours() < START_HOUR) {
                    setAppStatus('waiting_time');
                    const target = new Date(); target.setHours(START_HOUR, 0, 0, 0);
                    const diff = target - now;
                    const h = Math.floor(diff / 3600000); const m = Math.floor((diff % 3600000) / 60000);
                    setTimeMsg(`${h}h ${m}m`); setHistory(localHistory);
                    return;
                }

                setAppStatus('generating'); setHistory(localHistory);
                await new Promise(r => setTimeout(r, 100)); // UI delay

                const newSlip = await fetchDailyBets();
                if (newSlip) {
                    setCurrentSlip(newSlip); setAppStatus('success');
                    localStorage.setItem(STORAGE_KEY, JSON.stringify({ history: localHistory, currentSlip: newSlip }));
                } else {
                    setAppStatus('error');
                }
            }, []);

            useEffect(() => {
                if (localStorage.getItem(NOTIF_KEY) === 'true') setNotificationsEnabled(true);
                runLogic();
                const interval = setInterval(() => runLogic(), 60000);
                return () => clearInterval(interval);
            }, [runLogic]);

            const handleCheckHistory = async (id) => {
                setCheckingId(id);
                const slip = history.find(s => s.id === id);
                if (slip) {
                    const updated = await checkSlipStatus(slip);
                    const newHistory = history.map(s => s.id === id ? updated : s);
                    setHistory(newHistory);
                    localStorage.setItem(STORAGE_KEY, JSON.stringify({ history: newHistory, currentSlip }));
                }
                setCheckingId(null);
            };

            const toggleNotifications = async () => {
                if (!notificationsEnabled) {
                    if (await Notification.requestPermission() === 'granted') {
                        setNotificationsEnabled(true); localStorage.setItem(NOTIF_KEY, 'true');
                    }
                } else {
                    setNotificationsEnabled(false); localStorage.setItem(NOTIF_KEY, 'false');
                }
            };

            return (
                <div className="min-h-screen pb-24 bg-transparent">
                    <Header notificationsEnabled={notificationsEnabled} onToggle={toggleNotifications} />
                    <main className="max-w-4xl mx-auto px-4 pt-6">
                        <div className="flex space-x-4 mb-6 border-b border-slate-200/60 bg-white/60 backdrop-blur-sm rounded-t-lg p-1">
                            <button onClick={() => setActiveTab('daily')} className={`flex-1 pb-2 text-sm font-bold border-b-2 transition-colors ${activeTab === 'daily' ? 'border-red-600 text-red-600' : 'border-transparent text-slate-500'}`}>Tripla do Dia</button>
                            <button onClick={() => setActiveTab('history')} className={`flex-1 pb-2 text-sm font-bold border-b-2 transition-colors ${activeTab === 'history' ? 'border-red-600 text-red-600' : 'border-transparent text-slate-500'}`}>Histórico</button>
                        </div>

                        {activeTab === 'daily' && (
                            <div className="animate-fade-in space-y-6">
                                {appStatus === 'waiting_time' && (
                                    <div className="text-center py-12 bg-white/90 backdrop-blur-sm rounded-xl shadow border border-slate-200">
                                        <div className="bg-blue-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"><Clock className="text-blue-600" /></div>
                                        <h2 className="text-xl font-bold text-slate-800">Boletim em Preparação</h2>
                                        <p className="text-slate-500 text-sm mt-2">Disponível em: <span className="font-mono font-bold text-slate-800">{timeMsg}</span></p>
                                        <p className="text-xs text-slate-400 mt-4">Diariamente às {START_HOUR}:00</p>
                                    </div>
                                )}
                                {appStatus === 'generating' && (
                                    <div className="space-y-6">
                                        <div className="bg-gradient-to-r from-green-700/80 to-green-600/80 backdrop-blur-sm rounded-xl p-6 h-32 w-full animate-pulse border border-white/20">
                                           <div className="h-6 bg-white/20 rounded w-1/3 mb-4"></div><div className="h-8 bg-white/30 rounded w-2/3"></div>
                                        </div>
                                        <div><SkeletonCard /><SkeletonCard /><SkeletonCard /></div>
                                    </div>
                                )}
                                {appStatus === 'error' && (
                                    <div className="text-center py-12 bg-white/90 backdrop-blur-sm rounded-xl shadow border border-red-100">
                                        <AlertCircle size={48} className="mx-auto text-red-500 mb-4" />
                                        <p className="text-slate-600 font-bold">Falha na conexão.</p>
                                        <button onClick={() => runLogic()} className="mt-4 bg-red-600 text-white px-6 py-2 rounded-full font-bold shadow hover:bg-red-700 transition">Recarregar</button>
                                    </div>
                                )}
                                {appStatus === 'success' && currentSlip && (
                                    <>
                                        <div className="bg-gradient-to-r from-green-700/95 to-green-600/95 backdrop-blur-sm rounded-xl p-6 text-white shadow-lg relative overflow-hidden animate-in slide-in-from-bottom-4 border border-green-800/20">
                                            <div className="relative z-10">
                                                <div className="flex items-center space-x-2 mb-1"><span className="bg-red-600 text-[10px] font-bold px-2 py-0.5 rounded uppercase">Oficial</span><p className="text-green-100 text-xs">{new Date(currentSlip.date).toLocaleDateString('pt-PT')}</p></div>
                                                <h2 className="text-3xl font-bold text-white">Odd Total: <span className="text-yellow-300">{currentSlip.totalOdd.toFixed(2)}</span></h2>
                                            </div>
                                            <div className="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-yellow-400 opacity-20 rounded-full blur-xl"></div>
                                        </div>
                                        <div className="animate-in slide-in-from-bottom-4" style={{animationDelay: '100ms'}}>{currentSlip.selections.map((sel, idx) => <BetCard key={idx} selection={sel} />)}</div>
                                        <div className="text-center p-4 bg-yellow-50/90 backdrop-blur-sm rounded-lg border border-yellow-100 text-xs text-yellow-900 font-bold shadow-sm">
                                            <TrendingUp size={14} className="inline mr-1" />Gestão recomendada: 1-2% da banca.
                                        </div>
                                    </>
                                )}
                            </div>
                        )}
                        {activeTab === 'history' && (
                            <div className="bg-white/90 backdrop-blur-md rounded-xl shadow-sm border border-slate-200 p-4 animate-fade-in">
                                <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2"><History className="text-red-600" size={20}/> Histórico (10 Dias)</h2>
                                <HistoryList history={history} onCheck={handleCheckHistory} checkingId={checkingId} />
                            </div>
                        )}
                    </main>
                </div>
            );
        };

        const root = createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
