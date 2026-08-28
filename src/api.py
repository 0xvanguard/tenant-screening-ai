"""
Tenant Screening AI - API REST
Analiza y evalúa inquilinos potenciales automáticamente
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from analyzer import TenantAnalyzer, TenantProfile, RiskLevel, Recommendation


# Modelos de datos
class TenantRequest(BaseModel):
    name: str
    email: str
    phone: str
    monthly_income: float
    monthly_rent: float
    employment_status: str
    employer: Optional[str] = None
    employment_duration_months: Optional[int] = None
    previous_address: Optional[str] = None
    references: List[str] = []
    has_pets: bool = False
    pet_type: Optional[str] = None
    has_children: bool = False
    credit_score: Optional[int] = None
    criminal_record: Optional[bool] = None
    eviction_history: Optional[bool] = None


class ScreeningResponse(BaseModel):
    risk_score: float
    risk_level: str
    recommendation: str
    income_to_rent_ratio: float
    stability_score: float
    red_flags: List[str]
    positive_factors: List[str]
    conditions: List[str]
    summary: str
    estimated_approval: str


class StatsResponse(BaseModel):
    stable_employment_keywords: int
    unstable_employment_keywords: int
    risk_levels: List[str]
    recommendations: List[str]
    version: str


# App FastAPI
app = FastAPI(
    title="Tenant Screening AI API",
    description="Analiza y evalúa inquilinos potenciales automáticamente",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = TenantAnalyzer()


@app.get("/")
async def root():
    """Web UI principal"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🏠 Tenant Screening AI</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: system-ui; background: #0a0a0f; color: #fff; }
            .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
            h1 { color: #ff6b35; font-size: 2.5em; margin-bottom: 10px; }
            .subtitle { color: #888; margin-bottom: 30px; }
            .card { background: #1a1a2e; border-radius: 12px; padding: 24px; margin-bottom: 20px; border: 1px solid #333; }
            .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
            .form-group { margin-bottom: 16px; }
            .form-group.full { grid-column: span 2; }
            label { display: block; margin-bottom: 6px; color: #aaa; font-size: 13px; }
            input, select { width: 100%; padding: 12px; background: #0d0d1a; border: 1px solid #444; border-radius: 8px; color: #fff; font-size: 14px; }
            input:focus, select:focus { outline: none; border-color: #ff6b35; }
            .btn { background: linear-gradient(135deg, #ff6b35, #ff8c5a); color: #000; border: none; padding: 14px 32px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 16px; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(255,107,53,0.3); }
            .result { margin-top: 20px; padding: 24px; border-radius: 12px; display: none; }
            .low-risk { background: #0d2818; border: 1px solid #00ff88; }
            .medium-risk { background: #2d2d0d; border: 1px solid #ffaa00; }
            .high-risk { background: #2d1a0d; border: 1px solid #ff6b35; }
            .critical-risk { background: #2d0d0d; border: 1px solid #ff4444; }
            .score-container { display: flex; gap: 30px; margin-bottom: 20px; flex-wrap: wrap; }
            .score-box { text-align: center; min-width: 100px; }
            .score { font-size: 42px; font-weight: bold; }
            .score.low { color: #00ff88; }
            .score.medium { color: #ffaa00; }
            .score.high { color: #ff6b35; }
            .score.critical { color: #ff4444; }
            .score-label { font-size: 12px; color: #888; margin-top: 4px; }
            .recommendation { font-size: 20px; font-weight: bold; margin: 16px 0; }
            .flags { margin-top: 16px; }
            .flag { background: rgba(255,68,68,0.1); border-left: 3px solid #ff4444; padding: 8px 12px; margin: 6px 0; border-radius: 4px; font-size: 13px; }
            .positive { background: rgba(0,255,136,0.1); border-left: 3px solid #00ff88; padding: 8px 12px; margin: 6px 0; border-radius: 4px; font-size: 13px; }
            .conditions { margin-top: 16px; }
            .condition { background: rgba(255,170,0,0.1); border-left: 3px solid #ffaa00; padding: 8px 12px; margin: 6px 0; border-radius: 4px; font-size: 13px; }
            .summary { margin-top: 16px; padding: 16px; background: #0d0d1a; border-radius: 8px; white-space: pre-line; }
            .examples { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 16px; }
            .example-btn { background: #2a2a4a; border: 1px solid #444; color: #fff; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; }
            .example-btn:hover { border-color: #ff6b35; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏠 Tenant Screening AI</h1>
            <p class="subtitle">Analiza y evalúa inquilinos potenciales automáticamente</p>
            
            <div class="card">
                <h3>📝 Datos del Inquilino</h3>
                
                <div class="examples">
                    <span style="color:#888;font-size:12px;">Ejemplos:</span>
                    <button class="example-btn" onclick="loadExample('good')">✅ Buen inquilino</button>
                    <button class="example-btn" onclick="loadExample('medium')">⚠️ Riesgo medio</button>
                    <button class="example-btn" onclick="loadExample('bad')">❌ Alto riesgo</button>
                </div>
                
                <form id="tenantForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Nombre completo</label>
                            <input type="text" id="name" required>
                        </div>
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" id="email" required>
                        </div>
                        <div class="form-group">
                            <label>Teléfono</label>
                            <input type="tel" id="phone" required>
                        </div>
                        <div class="form-group">
                            <label>Score crediticio</label>
                            <input type="number" id="credit_score" min="300" max="850">
                        </div>
                        <div class="form-group">
                            <label>Ingreso mensual ($)</label>
                            <input type="number" id="income" required>
                        </div>
                        <div class="form-group">
                            <label>Renta mensual ($)</label>
                            <input type="number" id="rent" required>
                        </div>
                        <div class="form-group">
                            <label>Estado laboral</label>
                            <select id="employment">
                                <option value="employed">Empleo full-time</option>
                                <option value="self-employed">Autónomo</option>
                                <option value="contract">Contrato</option>
                                <option value="temporary">Temporal</option>
                                <option value="unemployed">Desempleado</option>
                                <option value="retired">Jubilado</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Empleador</label>
                            <input type="text" id="employer">
                        </div>
                        <div class="form-group">
                            <label>Meses en empleo actual</label>
                            <input type="number" id="employment_months" min="0">
                        </div>
                        <div class="form-group">
                            <label>¿Tiene mascotas?</label>
                            <select id="pets">
                                <option value="false">No</option>
                                <option value="true">Sí</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Historial de desalojo</label>
                            <select id="eviction">
                                <option value="false">No</option>
                                <option value="true">Sí</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Antecedentes penales</label>
                            <select id="criminal">
                                <option value="false">No</option>
                                <option value="true">Sí</option>
                            </select>
                        </div>
                    </div>
                </form>
                
                <button class="btn" onclick="analyze()">🔍 Analizar Inquilino</button>
                
                <div id="result" class="result">
                    <div class="score-container">
                        <div class="score-box">
                            <div class="score" id="risk-score">0</div>
                            <div class="score-label">Riesgo</div>
                        </div>
                        <div class="score-box">
                            <div class="score" id="income-ratio" style="color:#00d4ff;">0x</div>
                            <div class="score-label">Ratio Ingreso/Renta</div>
                        </div>
                        <div class="score-box">
                            <div class="score" id="stability" style="color:#aa88ff;">0</div>
                            <div class="score-label">Estabilidad</div>
                        </div>
                    </div>
                    <div id="recommendation" class="recommendation"></div>
                    <div id="approval" style="color:#888;margin-bottom:16px;"></div>
                    <div id="flags" class="flags"></div>
                    <div id="positives" class="flags"></div>
                    <div id="conditions-section" class="conditions"></div>
                    <div id="summary" class="summary"></div>
                </div>
            </div>
        </div>
        
        <script>
            const examples = {
                good: {
                    name: "María García López", email: "maria.garcia@email.com", phone: "+52 55 1234 5678",
                    income: 6000, rent: 1500, employment: "employed", employer: "Google México",
                    employment_months: 36, credit_score: 780, pets: "false", eviction: "false", criminal: "false"
                },
                medium: {
                    name: "Carlos Mendoza", email: "carlos.m@email.com", phone: "+52 55 9876 5432",
                    income: 4000, rent: 1800, employment: "contract", employer: "Freelance Developer",
                    employment_months: 8, credit_score: 680, pets: "true", eviction: "false", criminal: "false"
                },
                bad: {
                    name: "Juan Pérez", email: "juan.p@email.com", phone: "+52 55 5555 5555",
                    income: 2500, rent: 1500, employment: "temporary", employer: "Uber",
                    employment_months: 2, credit_score: 520, pets: "false", eviction: "true", criminal: "true"
                }
            };
            
            function loadExample(type) {
                const ex = examples[type];
                document.getElementById('name').value = ex.name;
                document.getElementById('email').value = ex.email;
                document.getElementById('phone').value = ex.phone;
                document.getElementById('income').value = ex.income;
                document.getElementById('rent').value = ex.rent;
                document.getElementById('employment').value = ex.employment;
                document.getElementById('employer').value = ex.employer;
                document.getElementById('employment_months').value = ex.employment_months;
                document.getElementById('credit_score').value = ex.credit_score;
                document.getElementById('pets').value = ex.pets;
                document.getElementById('eviction').value = ex.eviction;
                document.getElementById('criminal').value = ex.criminal;
            }
            
            async function analyze() {
                const data = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    monthly_income: parseFloat(document.getElementById('income').value),
                    monthly_rent: parseFloat(document.getElementById('rent').value),
                    employment_status: document.getElementById('employment').value,
                    employer: document.getElementById('employer').value || null,
                    employment_duration_months: parseInt(document.getElementById('employment_months').value) || null,
                    credit_score: parseInt(document.getElementById('credit_score').value) || null,
                    has_pets: document.getElementById('pets').value === 'true',
                    eviction_history: document.getElementById('eviction').value === 'true',
                    criminal_record: document.getElementById('criminal').value === 'true',
                    references: []
                };
                
                const response = await fetch('/api/screen', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('result');
                
                resultDiv.style.display = 'block';
                
                // Clasificar por nivel
                const riskClasses = { low: 'low-risk', medium: 'medium-risk', high: 'high-risk', critical: 'critical-risk' };
                resultDiv.className = 'result ' + (riskClasses[result.risk_level] || 'medium-risk');
                
                // Scores
                const riskScore = document.getElementById('risk-score');
                riskScore.textContent = Math.round(result.risk_score);
                riskScore.className = 'score ' + result.risk_level;
                
                document.getElementById('income-ratio').textContent = result.income_to_rent_ratio.toFixed(1) + 'x';
                document.getElementById('stability').textContent = Math.round(result.stability_score);
                
                // Recomendación
                const recNames = {
                    'approve': '✅ APROBADO',
                    'approve_with_conditions': '⚠️ APROBADO CON CONDICIONES',
                    'review': '🔍 REVISIÓN REQUERIDA',
                    'decline': '❌ RECHAZADO'
                };
                document.getElementById('recommendation').textContent = recNames[result.recommendation] || result.recommendation;
                document.getElementById('approval').textContent = 'Probabilidad: ' + result.estimated_approval;
                
                // Red flags
                const flagsDiv = document.getElementById('flags');
                if (result.red_flags.length > 0) {
                    flagsDiv.innerHTML = '<strong style="color:#ff4444;">⚠️ Señales de alerta:</strong>' +
                        result.red_flags.map(f => '<div class="flag">' + f + '</div>').join('');
                } else {
                    flagsDiv.innerHTML = '<span style="color:#00ff88;">✅ Sin señales de alerta</span>';
                }
                
                // Positive factors
                const posDiv = document.getElementById('positives');
                if (result.positive_factors.length > 0) {
                    posDiv.innerHTML = '<strong style="color:#00ff88;">✅ Factores positivos:</strong>' +
                        result.positive_factors.map(f => '<div class="positive">' + f + '</div>').join('');
                }
                
                // Conditions
                const condDiv = document.getElementById('conditions-section');
                if (result.conditions.length > 0) {
                    condDiv.innerHTML = '<strong style="color:#ffaa00;">📋 Condiciones:</strong>' +
                        result.conditions.map(c => '<div class="condition">' + c + '</div>').join('');
                } else {
                    condDiv.innerHTML = '';
                }
                
                // Summary
                document.getElementById('summary').textContent = result.summary;
            }
        </script>
    </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/api/screen", response_model=ScreeningResponse)
async def screen_tenant(request: TenantRequest):
    """Analiza un inquilino y retorna recomendación"""
    if not request.name.strip():
        raise HTTPException(status_code=400, detail="El nombre es requerido")
    if request.monthly_rent <= 0:
        raise HTTPException(status_code=400, detail="La renta debe ser mayor a 0")
    
    profile = TenantProfile(
        name=request.name,
        email=request.email,
        phone=request.phone,
        monthly_income=request.monthly_income,
        monthly_rent=request.monthly_rent,
        employment_status=request.employment_status,
        employer=request.employer,
        employment_duration_months=request.employment_duration_months,
        previous_address=request.previous_address,
        references=request.references,
        has_pets=request.has_pets,
        pet_type=request.pet_type,
        has_children=request.has_children,
        credit_score=request.credit_score,
        criminal_record=request.criminal_record,
        eviction_history=request.eviction_history
    )
    
    result = analyzer.analyze(profile)
    
    return ScreeningResponse(
        risk_score=result.risk_score,
        risk_level=result.risk_level.value,
        recommendation=result.recommendation.value,
        income_to_rent_ratio=result.income_to_rent_ratio,
        stability_score=result.stability_score,
        red_flags=result.red_flags,
        positive_factors=result.positive_factors,
        conditions=result.conditions,
        summary=result.summary,
        estimated_approval=result.estimated_approval
    )


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    return StatsResponse(**analyzer.get_stats())


if __name__ == "__main__":
    print("🏠 Iniciando Tenant Screening AI...")
    print("📡 API: http://localhost:9002")
    print("📖 Docs: http://localhost:9002/docs")
    uvicorn.run(app, host="0.0.0.0", port=9002)
