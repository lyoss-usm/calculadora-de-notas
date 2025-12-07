# core/analisis/__init__.py
"""
Módulo de análisis de notas.
"""
from .roots import plot_notas, obtener_notas
from .simulation import montecarlo, plot_histogram

__all__ = ['plot_notas', 'obtener_notas', 'montecarlo', 'plot_histogram']
