# Modelos de datos para la API - Moira
from typing import List, Optional
from pydantic import BaseModel


class Planeta(BaseModel):
    nombre: str
    estrella: Optional[str] = None
    metodo_descubrimiento: Optional[str] = None
    mision: Optional[str] = None
    planetas_en_sistema: Optional[int] = None
    periodo_orbital_dias: Optional[float] = None
    semieje_mayor_au: Optional[float] = None
    excentricidad: Optional[float] = None
    masa_jup: Optional[float] = None
    radio_jup: Optional[float] = None
    densidad: Optional[float] = None
    distancia_pc: Optional[float] = None
    temp_estrella_k: Optional[float] = None
    masa_estrella: Optional[float] = None
    radio_estrella: Optional[float] = None
    planet_type: Optional[str] = None


class PaginaPlanetas(BaseModel):
    total: int
    pagina: int
    tam_pagina: int
    planetas: List[Planeta]


class ConteoTipo(BaseModel):
    planet_type: str
    cantidad: int


class Resumen(BaseModel):
    total_planetas: int
    masa_promedio: Optional[float]
    radio_promedio: Optional[float]
    periodo_promedio: Optional[float]
    por_tipo: List[ConteoTipo]
