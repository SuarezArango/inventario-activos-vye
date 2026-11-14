# Inventario de Activos TI – Vías y Explanaciones

Prototipo funcional (**TRL5**) del proyecto de grado de Ingeniería de Sistemas – UNAD (curso 202016907, Fase 4):
*Desarrollo e implementación de una solución de gestión de activos tecnológicos basada en Microsoft Power Platform
para la empresa Vías y Explanaciones.*

**Autores:** Camilo Suárez Arango · Liliana Amparo Viana Londoño · **Tutor:** Orlando Gómez Barboza

Solución *low-code* en Microsoft Power Platform para registrar, asignar, verificar físicamente (QR) y analizar
500 activos tecnológicos en 4 sedes, desarrollada con **Scrum** en tres sprints.

## Qué incluye el prototipo
| Componente | Qué hace | Documentación |
|------------|----------|---------------|
| **Microsoft Lists (SharePoint)** | Base de datos: activos, Asignaciones, Mantenimientos, VerificacionesInventario, UsuariosApp | `lists/modelo_datos.json` |
| **Power Apps** – app *Inventario VYE* | Búsqueda, registro, roles, asignación/transferencia/devolución con historial, baja, inventario físico con QR | `powerapps/` |
| **FL01** – Acta de asignación | Correo HTML al custodio cuando se registra una asignación o transferencia | `flows/flujos_power_automate.md` |
| **FL02** – Mantenimiento preventivo | Correo diario (7:00 a. m.) con los equipos de los próximos 7 días y conteo de vencidos | `flows/flujos_power_automate.md` |
| **FL03** – Garantías por vencer | Correo mensual con garantías que vencen en 30 días | `flows/flujos_power_automate.md` |
| **Power BI** – Tablero | 8 medidas DAX, indicadores por sede, estado, antigüedad y tipo | `powerbi/medidas_dax.md` |

## Arquitectura
```
 Usuarios (web / app móvil Power Apps)
        │
   Power Apps (lienzo)
        │   lectura / escritura
   Microsoft Lists (SharePoint Online)
   activos · Asignaciones · Mantenimientos · VerificacionesInventario · UsuariosApp
        │ disparadores / consultas OData          │ conector SharePoint
   Power Automate (FL01–FL03) ──► Outlook       Power BI Desktop (tablero)
```

## Guía rápida para revisar el repositorio
1. **Evidencias de funcionamiento:** `tests/evidencias/` (pantallazos de la app publicada, flujos, QR y Power BI).
2. **Plan y resultados de pruebas:** `tests/plan_pruebas.md` (PF-04 a PF-11 aprobadas).
3. **Metodología y backlog:** `docs/metodologia_scrum.md`, `docs/product_backlog.md`.
4. **Fórmulas reales de la app (Power Fx):** `powerapps/es-CO/` y la pantalla QR en `powerapps/VerificacionScreen.pa.yaml`.
5. **Presentación paso a paso:** `docs/presentacion/` (fuentes de las diapositivas).

## Estructura del repositorio
| Carpeta | Contenido |
|---------|-----------|
| `docs/` | Metodología Scrum, product backlog, etiquetas QR (`etiquetas_qr.pdf`), presentación |
| `lists/` | Modelo de datos (esquema de las listas) |
| `scripts/` | Generador de datos de prueba y de etiquetas QR (Python), aprovisionamiento (PnP PowerShell), corrección de fechas (JS) |
| `data/` | Datos sintéticos de prueba (CSV) |
| `powerapps/` | Fórmulas Power Fx por pantalla (`es-CO` = separadores en español) y YAML de pantallas |
| `flows/` | Diseño e implementación real de los flujos FL01–FL03 |
| `powerbi/` | Medidas DAX, layout del tablero y archivo `.pbix` |
| `tests/` | Plan y registro de pruebas, evidencias |

## Puesta en marcha (resumen)
1. Crear un equipo de Teams / sitio de SharePoint (zona horaria UTC-05 Bogotá, región Español – Colombia).
2. `python scripts/generar_datos_prueba.py` e importar `data/activos.csv` como lista **activos** (columnas de opción con selección única y fechas *solo fecha*).
3. Crear las demás listas según `lists/modelo_datos.json`.
4. Power Apps: *Comenzar con datos* → lista activos y personalizar con las fórmulas de `powerapps/es-CO/`.
5. Power Automate: crear FL01–FL03 según `flows/flujos_power_automate.md` (ojo con los nombres internos `field_N`).
6. Power BI Desktop: *Lista de SharePoint Online* y medidas de `powerbi/medidas_dax.md`.

## Limitaciones conocidas
- Desplegado en el tenant académico de la UNAD: solo cuentas institucionales entran a la app.
- Datos sintéticos (500 activos) con la estructura de un inventario real.
- Power BI en Desktop: el tenant académico no permite activar Power BI en la web.
