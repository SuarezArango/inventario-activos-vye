# Metodología de desarrollo ágil – Scrum

Se reemplaza el modelo en cascada de la Fase 3 por **Scrum**, como exige la Fase 4 (RA3: metodologías ágiles,
prototipo TRL5). Scrum encaja porque el producto se construye por incrementos funcionales que los usuarios
clave de Vías y Explanaciones pueden probar y retroalimentar en cada sprint.

## 1. Roles
| Rol Scrum | Responsable | Funciones |
|-----------|-------------|-----------|
| Product Owner | Jefe/Coordinador de TI de Vías y Explanaciones *(confirmar nombre)* | Prioriza el backlog, acepta historias |
| Scrum Master | Liliana Amparo Viana Londoño *(propuesto)* | Facilita eventos, retira impedimentos, controla el tablero |
| Equipo de desarrollo | Camilo Suárez Arnago y Liliana Amparo Viana Londoño | Diseño, desarrollo, pruebas y documentación |
| Usuarios clave | Auxiliar de inventario, área administrativa, dirección | Validación en cada Sprint Review |

## 2. Artefactos
- **Product Backlog:** `docs/product_backlog.md` (historias de usuario con criterios de aceptación y puntos).
- **Sprint Backlog:** tareas de cada sprint en el tablero (Microsoft Planner o GitHub Projects).
- **Incremento:** versión publicada de la app + listas + flujos al cierre de cada sprint (etiqueta `v0.x` en GitHub).
- **Definición de Terminado (DoD):** la historia cumple sus criterios de aceptación, se probó con datos de prueba,
  respeta los permisos por rol, está documentada y su código/fórmulas están en GitHub.

## 3. Eventos
| Evento | Duración | Frecuencia |
|--------|----------|-----------|
| Sprint Planning | 1 h | Inicio de cada sprint |
| Daily Scrum (virtual, Teams/WhatsApp) | 15 min | Diario |
| Sprint Review con usuarios clave | 45 min | Fin de sprint |
| Sprint Retrospective | 30 min | Fin de sprint |

## 4. Plan de sprints
Para el periodo académico de la Fase 4 se usan **sprints de una semana** (cronograma comprimido); en la
ejecución completa del proyecto (6 meses) los sprints serían de dos semanas.

| Sprint | Fechas | Objetivo (meta del sprint) | Historias |
|--------|--------|---------------------------|-----------|
| 0 | 25 oct – 31 oct 2026 | Ajustes Fase 3, backlog, arquitectura, entorno M365 y GitHub | — |
| 1 | 1 nov – 8 nov | Modelo de datos en Lists y carga de datos; CRUD de activos | HU-01, HU-02, HU-03, HU-11 |
| 2 | 9 nov – 15 nov | Asignaciones/trazabilidad, inventario físico con QR, flujos | HU-04, HU-05, HU-06, HU-07, HU-08 |
| 3 | 16 nov – 22 nov | Power BI, alertas, pruebas TRL5, video y entrega | HU-09, HU-10, HU-12 |

## 5. Métricas ágiles
- **Velocidad** (puntos terminados por sprint) y **burndown** del sprint.
- Cumplimiento de la DoD (% historias aceptadas en la Review).
- Defectos abiertos / cerrados por sprint (meta: < 5 % críticos sin corregir, Tabla 3 del documento).

## 6. Nivel de madurez TRL5
TRL5 = *validación de la tecnología en un entorno relevante*. Evidencias que se presentarán:
1. Prototipo integrado (Power Apps + Lists + Power Automate + Power BI) funcionando en un tenant de Microsoft 365.
2. Datos de prueba representativos (500 activos, 4 sedes) y verificación física con una muestra de 20 equipos reales.
3. Pruebas funcionales, de roles y de usabilidad (SUS) con usuarios clave; resultados en `tests/plan_pruebas.md`.
4. Video de demostración (< 10 min) y código en GitHub.
