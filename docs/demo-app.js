// ============================================================
// 🏠 TENANT SCREENING AI - Demo Interactivo
// ============================================================

let tenantUses = 0;

function initTenantDemo() {
    const container = document.getElementById('tenant-demo');
    if (!container) return;

    container.innerHTML = `
        <style>
            .tenant-demo { background: #0d0d1a; border-radius: 20px; padding: 2rem; margin: 2rem auto; max-width: 800px; border: 1px solid #1a1a3e; }
            .tenant-demo h3 { color: #ff8c00; margin-bottom: 1rem; font-size: 1.3rem; }
            .tenant-form { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 1.5rem; }
            .tenant-field { display: flex; flex-direction: column; gap: 6px; }
            .tenant-field.full { grid-column: span 2; }
            .tenant-field label { color: #888; font-size: 0.85rem; font-weight: 600; }
            .tenant-field input, .tenant-field select { padding: 12px 14px; background: #111122; border: 2px solid #222244; border-radius: 10px; color: #fff; font-size: 0.95rem; transition: border-color 0.3s; }
            .tenant-field input:focus, .tenant-field select:focus { border-color: #ff8c00; outline: none; }
            .tenant-field select option { background: #111122; }
            .tenant-btn { grid-column: span 2; padding: 14px; background: linear-gradient(135deg, #ff8c00, #ff6600); color: #000; border: none; border-radius: 12px; font-weight: 700; font-size: 1rem; cursor: pointer; transition: all 0.3s; }
            .tenant-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,140,0,0.3); }
            .tenant-result { border-radius: 12px; padding: 1.5rem; margin-top: 1rem; display: none; animation: slideDown 0.3s ease; background: #111122; border: 1px solid #222244; }
            .tenant-score-wrap { display: flex; align-items: center; gap: 20px; margin-bottom: 1.5rem; }
            .tenant-score-circle { width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; border: 4px solid; }
            .tenant-score-circle.low { border-color: #00ff88; color: #00ff88; background: rgba(0,255,136,0.1); }
            .tenant-score-circle.medium { border-color: #ffbd2e; color: #ffbd2e; background: rgba(255,189,46,0.1); }
            .tenant-score-circle.high { border-color: #ff4444; color: #ff4444; background: rgba(255,68,68,0.1); }
            .tenant-score-info h4 { font-size: 1.2rem; margin-bottom: 0.3rem; }
            .tenant-score-info p { color: #888; font-size: 0.9rem; }
            .tenant-factors { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
            .tenant-factor { padding: 10px 14px; background: #0a0a15; border-radius: 8px; font-size: 0.85rem; }
            .tenant-factor .label { color: #666; }
            .tenant-factor .value { color: #fff; font-weight: 600; }
            .tenant-factor .status { font-size: 0.8rem; margin-top: 4px; }
            .tenant-uses { text-align: center; color: #666; font-size: 0.8rem; margin-top: 1rem; }
        </style>
        <div class="tenant-demo">
            <h3>🏠 Evalúa a tu Inquilino</h3>
            <p style="color:#666; margin-bottom:1rem;">Ingresa los datos del candidato y recibe un reporte de riesgo completo</p>
            
            <div class="tenant-form">
                <div class="tenant-field">
                    <label>👤 Nombre completo</label>
                    <input type="text" id="t-name" placeholder="Juan Pérez">
                </div>
                <div class="tenant-field">
                    <label>💳 Ingreso mensual ($)</label>
                    <input type="number" id="t-income" placeholder="30000">
                </div>
                <div class="tenant-field">
                    <label>🏠 Renta mensual ($)</label>
                    <input type="number" id="t-rent" placeholder="8000">
                </div>
                <div class="tenant-field">
                    <label>📅 Antigüedad laboral (años)</label>
                    <input type="number" id="t-tenure" placeholder="3">
                </div>
                <div class="tenant-field">
                    <label>💳 Score de crédito</label>
                    <select id="t-credit">
                        <option value="excellent">Excelente (750+)</option>
                        <option value="good">Bueno (650-749)</option>
                        <option value="fair">Regular (550-649)</option>
                        <option value="poor">Malo (menos de 550)</option>
                    </select>
                </div>
                <div class="tenant-field">
                    <label>📋 Historial de alquileres</label>
                    <select id="t-history">
                        <option value="excellent">Sin problemas</option>
                        <option value="good">1-2 problemas menores</option>
                        <option value="fair">Problemas moderados</option>
                        <option value="poor">Desalojos o deudas</option>
                    </select>
                </div>
                <div class="tenant-field full">
                    <label>📝 Notas adicionales</label>
                    <input type="text" id="t-notes" placeholder="Mascotas, garantías, referencias...">
                </div>
                <button class="tenant-btn" onclick="analyzeTenant()">🔍 Analizar Inquilino</button>
            </div>
            
            <div class="tenant-result" id="tenant-result"></div>
            <div class="tenant-uses" id="tenant-uses">Usos: ${tenantUses}/3</div>
        </div>
    `;
}

function analyzeTenant() {
    if (!DemoSystem.use()) return;
    tenantUses++;
    
    const name = document.getElementById('t-name').value || 'Sin nombre';
    const income = parseFloat(document.getElementById('t-income').value) || 25000;
    const rent = parseFloat(document.getElementById('t-rent').value) || 8000;
    const tenure = parseInt(document.getElementById('t-tenure').value) || 2;
    const credit = document.getElementById('t-credit').value;
    const history = document.getElementById('t-history').value;
    
    // Calcular score
    let score = 50;
    const factors = [];
    
    // Ratio ingreso/renta
    const ratio = income / rent;
    if (ratio >= 3) { score += 20; factors.push({ name: 'Ingreso/Renta', value: `${ratio.toFixed(1)}x`, status: '✅ Excelente', color: '#00ff88' }); }
    else if (ratio >= 2) { score += 10; factors.push({ name: 'Ingreso/Renta', value: `${ratio.toFixed(1)}x`, status: '✅ Bueno', color: '#00ff88' }); }
    else if (ratio >= 1.5) { factors.push({ name: 'Ingreso/Renta', value: `${ratio.toFixed(1)}x`, status: '⚠️ Regular', color: '#ffbd2e' }); }
    else { score -= 15; factors.push({ name: 'Ingreso/Renta', value: `${ratio.toFixed(1)}x`, status: '❌ Bajo', color: '#ff4444' }); }
    
    // Antigüedad
    if (tenure >= 5) { score += 15; factors.push({ name: 'Antigüedad', value: `${tenure} años`, status: '✅ Estable', color: '#00ff88' }); }
    else if (tenure >= 2) { score += 5; factors.push({ name: 'Antigüedad', value: `${tenure} años`, status: '✅ Adecuado', color: '#00ff88' }); }
    else { score -= 5; factors.push({ name: 'Antigüedad', value: `${tenure} años`, status: '⚠️ Reciente', color: '#ffbd2e' }); }
    
    // Crédito
    const creditScores = { excellent: 20, good: 10, fair: -5, poor: -20 };
    const creditLabels = { excellent: 'Excelente (750+)', good: 'Bueno (650-749)', fair: 'Regular (550-649)', poor: 'Malo (<550)' };
    score += creditScores[credit];
    const creditColor = credit === 'excellent' || credit === 'good' ? '#00ff88' : credit === 'fair' ? '#ffbd2e' : '#ff4444';
    factors.push({ name: 'Crédito', value: creditLabels[credit], status: credit === 'poor' ? '❌ Riesgo alto' : credit === 'fair' ? '⚠️ Atención' : '✅ Aceptable', color: creditColor });
    
    // Historial
    const historyScores = { excellent: 15, good: 5, fair: -10, poor: -25 };
    const historyLabels = { excellent: 'Sin problemas', good: '1-2 menores', fair: 'Moderados', poor: 'Desalojos/deudas' };
    score += historyScores[history];
    const historyColor = history === 'excellent' || history === 'good' ? '#00ff88' : history === 'fair' ? '#ffbd2e' : '#ff4444';
    factors.push({ name: 'Historial', value: historyLabels[history], status: history === 'poor' ? '❌ Riesgo crítico' : history === 'fair' ? '⚠️ Revisar' : '✅ Limpio', color: historyColor });
    
    // Limitar score
    score = Math.max(0, Math.min(100, score));
    
    const scoreClass = score >= 70 ? 'low' : score >= 40 ? 'medium' : 'high';
    const recommendation = score >= 70 ? '✅ APROBAR' : score >= 40 ? '⚠️ REVISAR CON CAUTELA' : '❌ RECHAZAR';
    const recColor = score >= 70 ? '#00ff88' : score >= 40 ? '#ffbd2e' : '#ff4444';
    
    const result = document.getElementById('tenant-result');
    result.style.display = 'block';
    result.innerHTML = `
        <div class="tenant-score-wrap">
            <div class="tenant-score-circle ${scoreClass}">${score}</div>
            <div class="tenant-score-info">
                <h4 style="color:${recColor}">${recommendation}</h4>
                <p>Score de riesgo para <strong>${name}</strong></p>
            </div>
        </div>
        <div class="tenant-factors">
            ${factors.map(f => `
                <div class="tenant-factor">
                    <div class="label">${f.name}</div>
                    <div class="value">${f.value}</div>
                    <div class="status" style="color:${f.color}">${f.status}</div>
                </div>
            `).join('')}
        </div>
    `;
    
    document.getElementById('tenant-uses').textContent = `Usos: ${tenantUses}/3`;
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initTenantDemo, 100);
});
