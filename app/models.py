from typing import Optional

from pydantic import BaseModel, Field


class HardFilters(BaseModel):
    manufacturer: str
    model: str
    gearbox: Optional[str] = None
    fuel_type: Optional[str] = None
    engine_volume: Optional[float] = None


class RangeFilters(BaseModel):
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    km_min: Optional[int] = None
    km_max: Optional[int] = None
    owners_max: Optional[int] = None


class Preferences(BaseModel):
    area: Optional[str] = None
    color: Optional[str] = None


class SearchRequest(BaseModel):
    hard_filters: HardFilters
    range_filters: RangeFilters = Field(default_factory=RangeFilters)
    result_limit: int = 10
