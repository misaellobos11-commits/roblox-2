# Recetas actuales — Matterloom 8.20

Datos extraídos del catálogo Luau del archivo entregado. Todas las cantidades actuales son una unidad.

| Máquina · nivel | Entradas | Salida | Intervalo nominal | Venta entradas → salida | Diferencia |
|---|---|---|---:|---:|---:|
| Separador de carbono · N1 | Materia base ×1 | Carbono ×1 | 2 s | $1 → $8 | +$7 |
| Generador de oxígeno · N2 | Materia base ×1 | Oxígeno ×1 | 2.2 s | $1 → $10 | +$9 |
| Procesador de silicio · N3 | Materia base ×1 | Silicio ×1 | 2.6 s | $1 → $12 | +$11 |
| Formador de hierro · N4 | Materia base ×1 | Hierro ×1 | 2.7 s | $1 → $12 | +$11 |
| Procesador de cobre · N3 | Materia base ×1 | Cobre ×1 | 2.8 s | $1 → $14 | +$13 |
| Generador de hidrógeno · N3 | Materia base ×1 | Hidrógeno ×1 | 2.5 s | $1 → $11 | +$10 |
| Cámara de fusión · N3 | Carbono ×1 + Oxígeno ×1 | Compuesto de carbono ×1 | 3 s | $18 → $24 | +$6 |
| Cámara de fusión · N3 | Oxígeno ×1 + Silicio ×1 | Silicato ×1 | 3 s | $22 → $26 | +$4 |
| Sintetizador elemental · N4 | Carbono ×1 + Hierro ×1 | Compuesto metálico ×1 | 3.2 s | $20 → $30 | +$10 |
| Sintetizador elemental · N4 | Cobre ×1 + Silicio ×1 | Mezcla conductiva ×1 | 3.2 s | $26 → $34 | +$8 |
| Cristalizador · N4 | Silicato ×1 | Cristal básico ×1 | 3.5 s | $26 → $55 | +$29 |
| Formador mineral · N5 | Compuesto metálico ×1 | Mineral sintético ×1 | 3.5 s | $30 → $62 | +$32 |
| Fundidora · N5 | Mineral sintético ×1 | Lingote ×1 | 4 s | $62 → $95 | +$33 |

La diferencia compara el valor de venta del producto con el de sus ingredientes. No es beneficio por segundo: no descuenta maquinaria, cintas, esperas ni cuellos de botella.

Los tiempos son intervalos mínimos entre producciones de una máquina. La simulación revisa cada 0,6 s; en condiciones ideales los intervalos se redondean al siguiente tick y la ejecución real puede demorarse más.
