"""API e página do Ponto Falante para a entrega de Secure DevOps."""
from pathlib import Path
from time import time
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Ponto Falante", version="1.0.0")
REQUESTS = Counter("http_requests_total", "Requisições HTTP", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Duração das requisições", ["path"])
STARTED = time()

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time()
        response = await call_next(request)
        path = request.url.path
        if path != "/metrics":
            REQUESTS.labels(request.method, path, str(response.status_code)).inc()
            LATENCY.labels(path).observe(time() - start)
        return response

app.add_middleware(MetricsMiddleware)

@app.get("/health")
def health():
    return {"status": "ok", "service": "ponto-falante", "fonte": "simulador"}

@app.get("/api/status")
def status():
    return {"modo": "simulador", "token_sptrans_configurado": False,
            "aviso": "MVP didático: previsões ilustrativas, sem conexão à SPTrans."}

@app.get("/api/pontos")
def pontos(busca: str = ""):
    if busca and "031245" not in busca and "paulista" not in busca.lower():
        return {"itens": [], "fonte": "simulador"}
    return {"itens": [{"codigo": "031245", "nome": "Av. Paulista, 1000", "bairro": "Bela Vista"}],
            "fonte": "simulador"}

@app.get("/api/pontos/{codigo}/previsoes")
def previsoes(codigo: str):
    return {"ponto": codigo, "fonte": "simulador", "simulado": True, "previsoes": [
        {"linha": "875A", "sentido": "Metrô Ana Rosa", "minutos": 3, "acessivel": True},
        {"linha": "875C", "sentido": "Metrô Santa Cruz", "minutos": 8, "acessivel": True},
        {"linha": "857R", "sentido": "Terminal Sacomã", "minutos": 14, "acessivel": False}]}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def home():
    return FileResponse(ROOT / "index.html")

@app.get("/{asset:path}")
def assets(asset: str):
    target = (ROOT / asset).resolve()
    if not target.is_relative_to(ROOT) or not target.is_file():
        return Response(status_code=404)
    return FileResponse(target)
