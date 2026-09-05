from fastapi import FastAPI, HTTPException
from src.ingestion.schema import TelemetryPayload
from src.agents.power_engineering import PowerEngineeringAgent
from src.agents.climate_mrv import ClimateMRVAgent
from src.agents.adaptation_risk import AdaptationRiskAgent

app = FastAPI(
    title="UNIDO Cleantech dMRV Ingestion Engine",
    version="1.0.0",
    description="ISO/IEC 17025 compliant telemetry pipeline and multi-agent MRV orchestrator."
)

power_agent = PowerEngineeringAgent()
mrv_agent = ClimateMRVAgent()
adaptation_agent = AdaptationRiskAgent()

@app.get("/")
def read_root():
    return {"status": "online", "system": "UNIDO Cleantech MRV Agent API"}

@app.post("/api/v1/analyze")
def process_telemetry(payload: TelemetryPayload):
    try:
        telemetry_dict = payload.model_dump()
        
        # Execute Agents
        power_results = power_agent.analyze_efficiency(telemetry_dict)
        
        mrv_results = mrv_agent.compute_avoided_emissions(
            baseline_kwh=payload.baseline_kwh,
            project_kwh=payload.project_kwh
        )
        
        adaptation_results = adaptation_agent.assess_thermal_vulnerability(
            ambient_temp_c=payload.ambient_temp_c
        )

        return {
            "device_id": payload.device_id,
            "power_engineering": power_results,
            "climate_mrv": mrv_results,
            "adaptation_risk": adaptation_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    