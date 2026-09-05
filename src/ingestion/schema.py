from pydantic import BaseModel, Field
from typing import Optional

class TelemetryPayload(BaseModel):
    device_id: str = Field(..., example="DEV-MSME-001")
    voltage_v: float = Field(..., ge=0.0, le=1000.0, example=400.0)
    current_a: float = Field(..., ge=0.0, le=5000.0, example=120.0)
    power_factor: float = Field(..., ge=0.0, le=1.0, example=0.85)
    ambient_temp_c: float = Field(..., ge=-20.0, le=80.0, example=42.5)
    vfd_installed: bool = Field(default=False)
    operating_hours: float = Field(default=4000.0, ge=0.0)
    baseline_kwh: Optional[float] = Field(default=315000.0)
    project_kwh: Optional[float] = Field(default=220500.0)