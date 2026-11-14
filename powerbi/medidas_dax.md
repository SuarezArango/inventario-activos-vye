# Informe de Power BI – Tablero de activos TI

**Origen:** Power BI Desktop > Obtener datos > *Lista de SharePoint Online* (URL del sitio), tablas
Activos, Asignaciones, Mantenimientos, VerificacionesInventario, Sedes.
**Relaciones:** `Activos[ID]` 1—* `Asignaciones[ActivoId]`, `Mantenimientos[ActivoId]`, `VerificacionesInventario[ActivoId]`;
`Sedes[ID]` 1—* `Activos[SedeId]`. Agregar una tabla calendario `dCalendario` marcada como tabla de fechas.

## Columnas calculadas (tabla Activos)
```DAX
Antiguedad_Anios = DATEDIFF ( Activos[FechaCompra], TODAY (), YEAR )

Rango_Antiguedad =
SWITCH ( TRUE (),
    Activos[Antiguedad_Anios] < 2, "0-2 años",
    Activos[Antiguedad_Anios] < 5, "2-5 años",
    "5+ años (obsolescencia)" )

Garantia_Vigente = IF ( Activos[FechaFinGarantia] >= TODAY (), "Vigente", "Vencida" )
```

## Medidas
```DAX
Total Activos = COUNTROWS ( Activos )
Activos Operativos = CALCULATE ( [Total Activos], Activos[Estado] <> "Dado de baja" )
Activos Asignados = CALCULATE ( [Total Activos], Activos[Estado] = "Asignado" )
% Utilizacion = DIVIDE ( [Activos Asignados], [Activos Operativos] )
Activos Disponibles = CALCULATE ( [Total Activos], Activos[Estado] = "Disponible" )

Equipos Obsoletos =
CALCULATE ( [Total Activos],
    Activos[Antiguedad_Anios] >= 5,
    Activos[Estado] <> "Dado de baja",
    Activos[TipoActivo] IN { "Portátil", "Escritorio" } )

Mantenimientos Vencidos =
CALCULATE ( [Total Activos],
    Activos[ProximoMantenimiento] < TODAY (),
    Activos[Estado] <> "Dado de baja" )

Valor Inventario = SUMX ( FILTER ( Activos, Activos[Estado] <> "Dado de baja" ), Activos[ValorCompra] )
Costo Correctivos = CALCULATE ( SUM ( Mantenimientos[Costo] ), Mantenimientos[TipoMantenimiento] = "Correctivo" )

% Exactitud Inventario =        -- verificaciones físicas que coinciden en ubicación y custodio
DIVIDE (
    CALCULATE ( COUNTROWS ( VerificacionesInventario ),
        VerificacionesInventario[CoincideUbicacion] = TRUE (),
        VerificacionesInventario[CoincideCustodio] = TRUE () ),
    COUNTROWS ( VerificacionesInventario ) )

% Cobertura Verificacion =
DIVIDE ( DISTINCTCOUNT ( VerificacionesInventario[ActivoId] ), [Activos Operativos] )
```

## Páginas del informe
1. **Resumen gerencial:** tarjetas (Total, % Utilización, Obsoletos, Mantenimientos vencidos, Valor inventario),
   barras por Sede y por Área, anillo por Estado.
2. **Ciclo de vida:** histograma por Rango_Antiguedad, tabla de garantías por vencer, matriz Tipo × Antigüedad.
3. **Mantenimiento:** preventivo vs correctivo por mes, costo correctivo, top 10 activos con más correctivos.
4. **Inventario físico:** % Exactitud y % Cobertura por jornada y sede, lista de novedades.

---

## Implementación real (14/11/2026) – Power BI Desktop
El tenant académico de la UNAD no permite activar Power BI en la web (registro en Fabric free: "Cuenta no aprobada"),
por eso el tablero se construyó en **Power BI Desktop** (gratuito), conectado a SharePoint en línea.

- **Origen:** Obtener datos → *Lista de SharePoint Online* (implementación 2.0), sitio
  `https://unadvirtualedu.sharepoint.com/sites/InventarioVYE`, autenticación *Cuenta de Microsoft*.
  Tablas cargadas: activos, Asignaciones, Mantenimientos, VerificacionesInventario.
- **Archivo:** `Tablero_Inventario_VYE.pbix` (carpeta FASE 4 del estudiante en OneDrive). Página 16:9, 1280 × 720.

### Medidas creadas (tabla activos)
```DAX
Total Activos = COUNTROWS(activos)
Activos Operativos = CALCULATE([Total Activos], activos[Estado] <> "Dado de baja")
Utilizacion = DIVIDE(CALCULATE([Total Activos], activos[Estado] = "Asignado"), [Activos Operativos])   -- formato %
Valor Inventario = CALCULATE(SUM(activos[ValorCompra]), activos[Estado] <> "Dado de baja")
Mantenimientos Vencidos = CALCULATE([Total Activos], activos[ProximoMantenimiento] < TODAY(), activos[Estado] <> "Dado de baja")
Garantias por Vencer 30d = CALCULATE([Total Activos], activos[FechaFinGarantia] >= TODAY(), activos[FechaFinGarantia] <= TODAY() + 30, activos[Estado] <> "Dado de baja")
Equipos Obsoletos = CALCULATE([Total Activos], activos[FechaCompra] <= EDATE(TODAY(), -60), activos[Estado] <> "Dado de baja", activos[TipoActivo] IN {"Portátil", "Escritorio"})
Exactitud Inventario = DIVIDE(CALCULATE(COUNTROWS(VerificacionesInventario), VerificacionesInventario[CoincideUbicacion] = TRUE()), COUNTROWS(VerificacionesInventario))   -- formato %
```
### Columna calculada
```DAX
Rango Antiguedad = VAR anios = DATEDIFF(activos[FechaCompra], TODAY(), YEAR)
RETURN SWITCH(TRUE(), ISBLANK(activos[FechaCompra]), "Sin dato", anios < 2, "0-2 años", anios < 5, "2-5 años", "5+ años")
```
### Página "Resumen" (layout)
Título; tarjeta con 6 indicadores (Total Activos, Valor Inventario, Utilización, Mantenimientos vencidos,
Garantías por vencer 30 d, Equipos obsoletos); columnas por Sede; anillo por Estado; columnas por Rango de
antigüedad; columnas por Tipo de activo; segmentador por Sede.

Valores el 14/11/2026 (datos de prueba): 500 activos · $1,22 mil M · 81,12 % de utilización · 431 mantenimientos
vencidos · 6 garantías por vencer en 30 días · 129 equipos obsoletos. Evidencia: `tests/evidencias/sprint3_HU10_tablero_powerbi.jpg`.
