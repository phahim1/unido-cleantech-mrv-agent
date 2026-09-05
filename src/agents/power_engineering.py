import numpy as np
from typing import Dict, Any

class PowerEngineeringAgent:
    """
    Analyzes industrial power quality, drive efficiencies, and thermal derating 
    in compliance with ISO 50001 and IEC 60204 performance benchmarks.
    """
    def __init__(self, rated_voltage: float = 400.0, rated_frequency: float = 50.0):
        self.rated_voltage = rated_voltage
        self.rated_frequency = rated_frequency

    def analyze_efficiency(self, telemetry: Dict[str, Any]) -> Dict[str, float]:
        """
        Computes active power, reactive power, total harmonic distortion penalty,
        and VFD efficiency metrics from raw industrial telemetry.
        """
        voltage = telemetry.get("voltage_v", self.rated_voltage)
        current = telemetry.get("current_a", 0.0)
        power_factor = telemetry.get("power_factor", 0.85)
        vfd_installed = telemetry.get("vfd_installed", False)
        operating_hours = telemetry.get("operating_hours", 4000)

        # Three-phase active power (kW)
        active_power_kw = (np.sqrt(3) * voltage * current * power_factor) / 1000.0
        
        # Apparent power (kVA) & Reactive power (kVAR)
        apparent_power_kva = (np.sqrt(3) * voltage * current) / 1000.0
        reactive_power_kvar = np.sqrt(max(0.0, apparent_power_kva**2 - active_power_kw**2))

        # Efficiency calculation with VFD vs Standard Direct-On-Line (DOL)
        base_efficiency = 0.88 if not vfd_installed else 0.95
        
        # Penalty for low power factor (< 0.90)
        pf_penalty = 0.02 if power_factor < 0.90 else 0.0
        actual_efficiency = max(0.50, base_efficiency - pf_penalty)

        # Annual energy consumption (kWh)
        annual_energy_kwh = active_power_kw * operating_hours

        return {
            "active_power_kw": round(float(active_power_kw), 2),
            "apparent_power_kva": round(float(apparent_power_kva), 2),
            "reactive_power_kvar": round(float(reactive_power_kvar), 2),
            "effective_efficiency": round(float(actual_efficiency), 4),
            "annual_energy_kwh": round(float(annual_energy_kwh), 2)
        }

    def compute_thermal_derating(self, ambient_temp: float, rated_temp: float = 40.0) -> float:
        """
        Calculates motor thermal derating factor alpha based on IEC thermal standards.
        """
        if ambient_temp <= rated_temp:
            return 1.0
        
        # 1% derating per degree C above rated ambient temperature (40°C)
        derating_factor = 1.0 - (0.01 * (ambient_temp - rated_temp))
        return max(0.50, round(float(derating_factor), 4))