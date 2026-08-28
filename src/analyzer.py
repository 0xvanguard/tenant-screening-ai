"""
Tenant Screening AI - Motor de Análisis
Analiza y evalúa inquilinos potenciales automáticamente
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Recommendation(Enum):
    APPROVE = "approve"
    APPROVE_WITH_CONDITIONS = "approve_with_conditions"
    REVIEW = "review"
    DECLINE = "decline"


@dataclass
class TenantProfile:
    name: str
    email: str
    phone: str
    monthly_income: float
    monthly_rent: float
    employment_status: str
    employer: Optional[str] = None
    employment_duration_months: Optional[int] = None
    previous_address: Optional[str] = None
    references: List[str] = field(default_factory=list)
    has_pets: bool = False
    pet_type: Optional[str] = None
    has_children: bool = False
    credit_score: Optional[int] = None
    criminal_record: Optional[bool] = None
    eviction_history: Optional[bool] = None


@dataclass
class ScreeningResult:
    risk_score: float  # 0-100 (0=bajo riesgo, 100=alto riesgo)
    risk_level: RiskLevel
    recommendation: Recommendation
    income_to_rent_ratio: float
    stability_score: float
    red_flags: List[str]
    positive_factors: List[str]
    conditions: List[str]
    summary: str
    estimated_approval: str


class TenantAnalyzer:
    """Analizador inteligente de inquilinos"""
    
    # Empleos considerados estables
    STABLE_EMPLOYMENT = [
        "government", "governmental", "federal", "state", "municipal",
        "teacher", "professor", "university", "hospital", "medical",
        "engineer", "software", "developer", "bank", "finance",
        "military", "army", "navy", "air force", "police", "firefighter",
        "permanent", "full-time", "contractor", "self-employed"
    ]
    
    # Empleos considerados inestables
    UNSTABLE_EMPLOYMENT = [
        "freelance", "gig", "uber", "lyft", "delivery", "seasonal",
        "temporary", "temp", "part-time", "intern", "unemployed",
        "student", "retired"
    ]
    
    def __init__(self):
        pass
    
    def analyze(self, profile: TenantProfile) -> ScreeningResult:
        """
        Analiza un perfil de inquilino y retorna recomendación
        
        Args:
            profile: Perfil del inquilino a analizar
            
        Returns:
            ScreeningResult con el análisis completo
        """
        
        # Calcular ratio ingreso/renta
        income_ratio = self._calculate_income_ratio(profile)
        
        # Calcular score de estabilidad
        stability_score = self._calculate_stability_score(profile)
        
        # Detectar red flags
        red_flags = self._detect_red_flags(profile)
        
        # Detectar factores positivos
        positive_factors = self._detect_positive_factors(profile)
        
        # Calcular score de riesgo
        risk_score = self._calculate_risk_score(
            income_ratio, stability_score, red_flags, positive_factors, profile
        )
        
        # Determinar nivel de riesgo
        risk_level = self._get_risk_level(risk_score)
        
        # Generar condiciones
        conditions = self._generate_conditions(profile, risk_level)
        
        # Determinar recomendación
        recommendation = self._get_recommendation(risk_level, conditions)
        
        # Generar resumen
        summary = self._generate_summary(profile, risk_level, recommendation, red_flags, positive_factors)
        
        # Estimar probabilidad de aprobación
        approval = self._estimate_approval(risk_score)
        
        return ScreeningResult(
            risk_score=risk_score,
            risk_level=risk_level,
            recommendation=recommendation,
            income_to_rent_ratio=income_ratio,
            stability_score=stability_score,
            red_flags=red_flags,
            positive_factors=positive_factors,
            conditions=conditions,
            summary=summary,
            estimated_approval=approval
        )
    
    def _calculate_income_ratio(self, profile: TenantProfile) -> float:
        """Calcula ratio ingreso/renta"""
        if profile.monthly_rent <= 0:
            return 0
        return profile.monthly_income / profile.monthly_rent
    
    def _calculate_stability_score(self, profile: TenantProfile) -> float:
        """Calcula score de estabilidad laboral"""
        score = 50  # Base neutral
        
        # Tipo de empleo
        employment_lower = profile.employment_status.lower()
        
        for keyword in self.STABLE_EMPLOYMENT:
            if keyword in employment_lower:
                score += 20
                break
        
        for keyword in self.UNSTABLE_EMPLOYMENT:
            if keyword in employment_lower:
                score -= 15
                break
        
        # Duración del empleo
        if profile.employment_duration_months:
            if profile.employment_duration_months >= 24:
                score += 15
            elif profile.employment_duration_months >= 12:
                score += 10
            elif profile.employment_duration_months >= 6:
                score += 5
            elif profile.employment_duration_months < 3:
                score -= 10
        
        # Empleador reconocido
        if profile.employer:
            employer_lower = profile.employer.lower()
            recognized_employers = ["google", "microsoft", "apple", "amazon", "meta", 
                                   "hospital", "university", "bank", "government"]
            for emp in recognized_employers:
                if emp in employer_lower:
                    score += 10
                    break
        
        return max(0, min(100, score))
    
    def _detect_red_flags(self, profile: TenantProfile) -> List[str]:
        """Detecta señales de alerta"""
        flags = []
        
        # Ratio ingreso/renta bajo
        ratio = self._calculate_income_ratio(profile)
        if ratio < 2:
            flags.append(f"Ratio ingreso/renta bajo ({ratio:.1f}x)")
        elif ratio < 2.5:
            flags.append(f"Ratio ingreso/renta justo ({ratio:.1f}x)")
        
        # Historial de desalojo
        if profile.eviction_history:
            flags.append("Historial de desalojo previo")
        
        # Record criminal
        if profile.criminal_record:
            flags.append("Antecedentes penales")
        
        # Crédito bajo
        if profile.credit_score and profile.credit_score < 600:
            flags.append(f"Score crediticio bajo ({profile.credit_score})")
        
        # Empleo inestable
        employment_lower = profile.employment_status.lower()
        if any(word in employment_lower for word in ["unemployed", "temp", "seasonal"]):
            flags.append("Empleo inestable o temporal")
        
        # Sin referencias
        if not profile.references or len(profile.references) == 0:
            flags.append("Sin referencias proporcionadas")
        
        # Empleo muy reciente
        if profile.employment_duration_months and profile.employment_duration_months < 3:
            flags.append("Empleo reciente (menos de 3 meses)")
        
        return flags
    
    def _detect_positive_factors(self, profile: TenantProfile) -> List[str]:
        """Detecta factores positivos"""
        factors = []
        
        # Ratio ingreso/renta alto
        ratio = self._calculate_income_ratio(profile)
        if ratio >= 4:
            factors.append(f"Excelente ratio ingreso/renta ({ratio:.1f}x)")
        elif ratio >= 3:
            factors.append(f"Buen ratio ingreso/renta ({ratio:.1f}x)")
        
        # Crédito alto
        if profile.credit_score and profile.credit_score >= 750:
            factors.append(f"Excelente score crediticio ({profile.credit_score})")
        elif profile.credit_score and profile.credit_score >= 700:
            factors.append(f"Buen score crediticio ({profile.credit_score})")
        
        # Empleo estable largo
        if profile.employment_duration_months and profile.employment_duration_months >= 36:
            factors.append(f"Empleo estable ({profile.employment_duration_months} meses)")
        
        # Sin mascotas (algunos propietarios prefieren)
        if not profile.has_pets:
            factors.append("Sin mascotas")
        
        # Referencias
        if profile.references and len(profile.references) >= 2:
            factors.append(f"{len(profile.references)} referencias proporcionadas")
        
        # Empleador reconocido
        if profile.employer:
            employer_lower = profile.employer.lower()
            recognized = ["google", "microsoft", "apple", "amazon", "meta", "hospital", "university"]
            if any(emp in employer_lower for emp in recognized):
                factors.append(f"Empleador reconocido: {profile.employer}")
        
        return factors
    
    def _calculate_risk_score(self, income_ratio: float, stability_score: float,
                               red_flags: List, positive_factors: List,
                               profile: TenantProfile) -> float:
        """Calcula el score final de riesgo"""
        score = 50  # Base neutral
        
        # Factor ingreso/renta (peso: 30%)
        if income_ratio >= 4:
            score -= 20
        elif income_ratio >= 3:
            score -= 10
        elif income_ratio >= 2:
            score += 0
        elif income_ratio >= 1.5:
            score += 15
        else:
            score += 30
        
        # Factor estabilidad (peso: 25%)
        stability_impact = (50 - stability_score) * 0.3
        score += stability_impact
        
        # Red flags (peso: 30%)
        score += len(red_flags) * 8
        
        # Factores positivos (peso: 15%)
        score -= len(positive_factors) * 5
        
        return max(0, min(100, score))
    
    def _get_risk_level(self, score: float) -> RiskLevel:
        """Convierte score a nivel de riesgo"""
        if score < 25:
            return RiskLevel.LOW
        elif score < 50:
            return RiskLevel.MEDIUM
        elif score < 75:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _generate_conditions(self, profile: TenantProfile, risk_level: RiskLevel) -> List[str]:
        """Genera condiciones basadas en el análisis"""
        conditions = []
        
        if risk_level == RiskLevel.HIGH:
            conditions.append("Requiere depósito adicional (2 meses)")
            conditions.append("Requiere fiador o co-signer")
        
        if risk_level == RiskLevel.CRITICAL:
            conditions.append("Requiere depósito de 3 meses")
            conditions.append("Requiere fiador con comprobante de ingresos")
            conditions.append("Requiere verificación adicional de empleo")
        
        if profile.credit_score and profile.credit_score < 650:
            conditions.append("Requiere seguro de renta")
        
        if profile.eviction_history:
            conditions.append("Requiere referencia de propietario anterior")
        
        if profile.has_pets:
            conditions.append("Requiere depósito adicional por mascota")
        
        return conditions
    
    def _get_recommendation(self, risk_level: RiskLevel, conditions: List[str]) -> Recommendation:
        """Determina recomendación"""
        if risk_level == RiskLevel.LOW:
            return Recommendation.APPROVE
        elif risk_level == RiskLevel.MEDIUM:
            if len(conditions) <= 1:
                return Recommendation.APPROVE_WITH_CONDITIONS
            else:
                return Recommendation.REVIEW
        elif risk_level == RiskLevel.HIGH:
            return Recommendation.REVIEW
        else:
            return Recommendation.DECLINE
    
    def _generate_summary(self, profile: TenantProfile, risk_level: RiskLevel,
                          recommendation: Recommendation, red_flags: List,
                          positive_factors: List) -> str:
        """Genera resumen del análisis"""
        ratio = self._calculate_income_ratio(profile)
        
        summaries = {
            Recommendation.APPROVE: f"✅ APROBADO - {profile.name} califica con good credit y ingresos estables.",
            Recommendation.APPROVE_WITH_CONDITIONS: f"⚠️ APROBADO CON CONDICIONES - {profile.name} califica pero requiere condiciones adicionales.",
            Recommendation.REVIEW: f"🔍 REVISIÓN REQUERIDA - {profile.name} tiene factores de riesgo que requieren análisis manual.",
            Recommendation.DECLINE: f"❌ RECHAZADO - {profile.name} no cumple con los requisitos mínimos."
        }
        
        base = summaries.get(recommendation, "Análisis inconcluso.")
        
        base += f"\n\n📊 Ratio ingreso/renta: {ratio:.1f}x"
        
        if red_flags:
            base += f"\n⚠️ Señales de alerta: {len(red_flags)}"
        
        if positive_factors:
            base += f"\n✅ Factores positivos: {len(positive_factors)}"
        
        return base
    
    def _estimate_approval(self, risk_score: float) -> str:
        """Estima probabilidad de aprobación"""
        if risk_score < 25:
            return "95%+ Probable"
        elif risk_score < 50:
            return "75-95% Probable"
        elif risk_score < 75:
            return "50-75% Posible"
        else:
            return "<50% Improbable"
    
    def batch_analyze(self, profiles: List[TenantProfile]) -> List[ScreeningResult]:
        """Analiza múltiples perfiles"""
        return [self.analyze(profile) for profile in profiles]
    
    def get_stats(self) -> Dict:
        """Retorna estadísticas del analizador"""
        return {
            "stable_employment_keywords": len(self.STABLE_EMPLOYMENT),
            "unstable_employment_keywords": len(self.UNSTABLE_EMPLOYMENT),
            "risk_levels": ["low", "medium", "high", "critical"],
            "recommendations": ["approve", "approve_with_conditions", "review", "decline"],
            "version": "1.0.0"
        }


# Instancia global del analizador
analyzer = TenantAnalyzer()


def screen_tenant(profile_dict: Dict) -> ScreeningResult:
    """Función de conveniencia para analizar un inquilino"""
    profile = TenantProfile(**profile_dict)
    return analyzer.analyze(profile)
