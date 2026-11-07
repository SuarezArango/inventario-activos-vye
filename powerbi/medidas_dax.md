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
