import numpy as np
from typing import Dict, Any

class AdaptationRiskAgent:
    """
    Evaluates industrial asset vulnerability to extreme heat events, thermal stress,
    and grid instability for MSMEs operating in developing regions.
    """
    def __init__(self, mttr_hours: float = 24.0, mtbf_hours: float = 5000.0):
        self.mttr = mttr_hours  # Mean Time To Repair
        self.mtbf = mtbf_hours  # Mean Time Between Failures

    def assess_thermal_vulnerability(
        self, 
        ambient_temp_c: float, 
        threshold_temp_c: float = 38.0, 
        grid_outage_hours_per_month: float = 12.0
    ) -> Dict[str, Any]:
        """
        Calculates equipment failure risk, derating-induced downtime, and climate risk score.
        """
        temp_delta = max(0.0, ambient_temp_c - threshold_temp_c)
        
        # Beta thermal degradation exponent
        beta = 0.08
        failure_rate_multiplier = np.exp(beta * temp_delta)
        
        # Adjusted MTBF under heat stress
        adjusted_mtbf = self.mtbf / failure_rate_multiplier
        
        # Availability Risk Index (0.0 to 1.0)
        availability_index = adjusted_mtbf / (adjusted_mtbf + self.mttr)
        unavailability_risk = 1.0 - availability_index
        
        # Overall Climate Risk Score (1 to 10 scale)
        risk_score = min(10.0, (unavailability_risk * 10) + (grid_outage_hours_per_month / 10.0))
        
        risk_category = "Low"
        if risk_score > 7.0:
            risk_category = "High / Critical"
        elif risk_score > 4.0:
            risk_category = "Moderate"

        return {
            "ambient_temp_c": ambient_temp_c,
            "adjusted_mtbf_hours": round(float(adjusted_mtbf), 1),
            "unavailability_risk_pct": round(float(unavailability_risk * 100), 2),
            "climate_risk_score": round(float(risk_score), 2),
            "vulnerability_category": risk_category
        }

    
