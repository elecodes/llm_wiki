#!/bin/bash

# Function to handle script termination
cleanup() {
    echo ""
    echo "Terminando procesos..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servidores detenidos. ¡Hasta luego, loco!"
    exit
}

# Trap Ctrl+C (SIGINT) and other termination signals
trap cleanup SIGINT SIGTERM

echo "🚀 Iniciando el LLM Wiki Dev Stack..."

# 1. Iniciar el Backend
echo "📡 Levantando el Backend (FastAPI)..."
if [ ! -d ".venv" ]; then
    echo "❌ Error: No se encontró la carpeta .venv. Ejecutá primero: python3 -m venv .venv && pip install -r requirements.txt"
    exit 1
fi

source .venv/bin/activate
# Usamos python directamente ya que chat_server.py tiene el bloque uvicorn.run
python scripts/chat_server.py &
BACKEND_PID=$!

# 2. Iniciar el Frontend
echo "💻 Levantando el Frontend (Vite)..."
if [ ! -d "chat-ui/node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    cd chat-ui && npm install && cd ..
fi

cd chat-ui
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Todo en marcha."
echo "   - Backend: http://localhost:8000"
echo "   - Frontend: Mirá los logs arriba para ver el puerto (usualmente 5173 o 5174)"
echo "Presioná Ctrl+C para apagar todo."

# Mantener el script vivo para que el trap funcione
wait
