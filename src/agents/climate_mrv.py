from typing import Dict, Any

class ClimateMRVAgent:
    """
    Computes greenhouse gas (GHG) reductions, avoided emissions, and GEF/GCF 
    Core Indicator metrics in alignment with IEEE P7802 and IPCC Tier-2 frameworks.
    """
    def __init__(self, grid_ef_kg_kwh: float = 0.52):
        self.grid_ef_kg_kwh = grid_ef_kg_kwh  # Grid emission factor (kg CO2e / kWh)

    def compute_avoided_emissions(
        self, 
        baseline_kwh: float, 
        project_kwh: float, 
        refrigerant_leakage_saved_kg: float = 0.0, 
        gwp: float = 1430.0
    ) -> Dict[str, float]:
        """
        Calculates net avoided emissions (tCO2e) combining energy savings 
        and fugitive refrigerant abatement (Kigali Amendment / Low-GWP tracking).
        """
        # Energy savings in kWh
        energy_saved_kwh = max(0.0, baseline_kwh - project_kwh)
        
        # Indirect emissions saved from electricity (tCO2e)
        indirect_avoided_tco2e = (energy_saved_kwh * self.grid_ef_kg_kwh) / 1000.0
        
        # Direct emissions saved from avoided refrigerant leakage (tCO2e)
        direct_avoided_tco2e = (refrigerant_leakage_saved_kg * gwp) / 1000.0
        
        # Total avoided emissions
        total_avoided_tco2e = indirect_avoided_tco2e + direct_avoided_tco2e

        return {
            "energy_saved_kwh": round(float(energy_saved_kwh), 2),
            "indirect_avoided_tco2e": round(float(indirect_avoided_tco2e), 4),
            "direct_avoided_tco2e": round(float(direct_avoided_tco2e), 4),
            "total_avoided_tco2e": round(float(total_avoided_tco2e), 4),
            "gef_indicator_6_2_tco2e": round(float(total_avoided_tco2e), 4)  # GEF Core Indicator 6.2
        }