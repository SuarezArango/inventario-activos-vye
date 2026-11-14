# Flujos de Power Automate

Los flujos se construyen en Power Automate (nube) sobre el mismo sitio de SharePoint. Al terminarlos se exportan
como paquete (`Exportar > Paquete (.zip)`) y el .zip se guarda en esta carpeta para el repositorio.

| ID | Nombre | Disparador | Historia de usuario |
|----|--------|-----------|---------------------|
| FL01 | Notificar asignación | SharePoint – *Cuando se crea un elemento* en **Asignaciones** | HU-05 |
| FL02 | Recordatorio de mantenimiento preventivo | *Periodicidad* diaria 7:00 a. m. | HU-08 |
| FL03 | Alerta de garantías por vencer | *Periodicidad* mensual, día 1 | HU-09 |
| FL04 | Reporte de obsolescencia | *Periodicidad* mensual, día 1 | HU-10 |

## FL01 – Notificar asignación
1. **Disparador:** Cuando se crea un elemento (lista *Asignaciones*).
2. **Condición:** `TipoMovimiento` es distinto de *Devolución*.
3. **Obtener elemento** (lista *Activos*, Id = `Activo Id`).
4. **Enviar correo (V2)** a `CustodioCorreo`, CC mesa de ayuda TI:
   - Asunto: `Acta de entrega del activo @{triggerBody()?['Activo']?['Value']}`
   - Cuerpo HTML: placa, serial, tipo, marca/modelo, sede, fecha y cláusula de custodia.
5. **Sí no (rama Devolución):** correo de confirmación de devolución al custodio anterior.

## FL02 – Recordatorio de mantenimiento preventivo
1. **Periodicidad:** 1 día.
2. **Obtener elementos** (*Activos*) con Consulta de filtro OData:
   `ProximoMantenimiento le '@{addDays(utcNow(),7,'yyyy-MM-dd')}' and Estado ne 'Dado de baja'`
3. **Aplicar a cada uno:** si no existe un mantenimiento *Programado* para ese activo (Obtener elementos en
   *Mantenimientos* con `Activo/Id eq @{items('Aplicar_a_cada_uno')?['ID']} and EstadoMantenimiento eq 'Programado'`),
   **Crear elemento** en *Mantenimientos* (Preventivo, Programado, FechaProgramada = ProximoMantenimiento).
4. **Crear tabla HTML** con los activos y **Enviar correo** resumen al equipo de TI.

## FL03 – Alerta de garantías por vencer
1. **Periodicidad:** mensual.
2. **Obtener elementos** (*Activos*): `FechaFinGarantia ge '@{utcNow('yyyy-MM-dd')}' and FechaFinGarantia le '@{addDays(utcNow(),30,'yyyy-MM-dd')}'`
3. **Crear tabla HTML** (Placa, Tipo, Marca, FechaFinGarantia) y **Enviar correo** al área administrativa/financiera.

## FL04 – Reporte de obsolescencia
1. **Periodicidad:** mensual.
2. **Obtener elementos** (*Activos*): `FechaCompra le '@{addDays(utcNow(),-1825,'yyyy-MM-dd')}' and Estado ne 'Dado de baja'`
   (equipos con 5 años o más).
3. **Filtrar matriz** a Portátil/Escritorio, **Crear tabla CSV**, **Crear archivo** en la biblioteca *Reportes*
   y **Enviar correo** a Dirección con el enlace (insumo para el presupuesto de renovación).

> Nota: en las consultas OData de SharePoint las columnas de elección se filtran por su texto (`Estado ne 'Dado de baja'`)
> y las de búsqueda por `Columna/Id`. Si un filtro falla, aplicar el filtro con la acción *Filtrar matriz*.

---

## Implementación real de FL01 (13/11/2026)
Flujo **"FL01 Notificar asignacion de activo"** (flujo de nube automatizado, conexión Outlook UNAD).

1. **Desencadenador:** SharePoint – *Cuando se crea un elemento* (sitio Inventario VYE, lista **Asignaciones**).
   Condición del desencadenador: `@not(equals(triggerOutputs()?['body/TipoMovimiento/Value'], 'Devolución'))`
2. **Obtener elemento** (lista **activos**), Id = `@{triggerOutputs()?['body/Activo/Id']}`
3. **Enviar correo electrónico (V2)**
   - Para: `@{triggerOutputs()?['body/CustodioCorreo']}`
   - Asunto: `Acta de entrega del activo @{triggerOutputs()?['body/Activo/Value']} - Vias y Explanaciones`
   - Cuerpo HTML: saludo, tabla (placa, tipo, marca y modelo, serial, sede, área, fecha, registrado por),
     cláusula de custodia y observaciones.

### Nombres internos de la lista `activos`
La lista se creó importando un CSV, por eso sus columnas tienen nombres internos `field_N`.
Power Automate usa los nombres internos:

| Columna | Interno | Columna | Interno |
|---|---|---|---|
| Serial | field_1 | Estado | field_12 |
| TipoActivo | field_2 | Condicion | field_13 |
| Marca | field_3 | Sede | field_14 |
| Modelo | field_4 | Area | field_15 |
| Procesador | field_5 | CustodioNombre | field_16 |
| RAM_GB | field_6 | CustodioCorreo | field_17 |
| Almacenamiento_GB | field_7 | UltimoMantenimiento | field_18 |
| SistemaOperativo | field_8 | ProximoMantenimiento | field_19 |
| FechaCompra | field_9 | Observaciones | field_20 |
| FechaFinGarantia | field_10 | ValorCompra | field_11 |

Ejemplo: tipo de activo = `body('Obtener_elemento')?['field_2']?['Value']`.
Las listas Asignaciones, Mantenimientos y VerificacionesInventario se crearon por API y sí tienen nombres internos legibles.

### Prueba PF-06
Asignación de VYE-0010 con el correo del estudiante como custodio: el acta llegó en menos de 5 minutos (13/11/2026 20:23).
Primera ejecución sin tipo, marca y serial (nombres internos); corregido el mismo día.

---

## Implementación real de FL02 (13/11/2026)
Flujo **"FL02 Recordatorio de mantenimiento preventivo"** (flujo de nube programado, todos los días 12:00 UTC = 7:00 a. m. hora Colombia).

1. **Recurrence**: intervalo 1 día, hora de inicio 2026-11-13T12:00:00Z.
2. **Proximos** – SharePoint *Obtener elementos* (lista activos), orden `field_19 asc`, filtro:
   `field_19 ge '@{formatDateTime(convertFromUtc(utcNow(),'SA Pacific Standard Time'),'yyyy-MM-dd')}' and field_19 le '@{formatDateTime(addDays(convertFromUtc(utcNow(),'SA Pacific Standard Time'),7),'yyyy-MM-dd')}' and field_12 ne 'Dado de baja'`
3. **Vencidos** – *Obtener elementos* (activos), primeros 5000, filtro:
   `field_19 lt '@{formatDateTime(convertFromUtc(utcNow(),'SA Pacific Standard Time'),'yyyy-MM-dd')}' and field_12 ne 'Dado de baja'`
4. **Seleccionar** desde `body('Proximos')?['value']`, mapa (modo texto):
   Placa = Title, Tipo = field_2/Value, Marca y modelo = field_3 + field_4, Sede = field_14/Value,
   Custodio = coalesce(field_16,'Sin custodio'), Mantenimiento programado = formatDateTime(field_19,'dd-MM-yyyy').
5. **Crear tabla HTML** desde `body('Seleccionar')`.
6. **Enviar correo electrónico (V2)** al equipo de TI (en el prototipo, la cuenta UNAD del estudiante):
   asunto con `length(body('Proximos')?['value'])` equipos; cuerpo HTML con estilos de tabla, la tabla y el
   conteo `length(body('Vencidos')?['value'])` de mantenimientos vencidos.

Prueba PF-09 (13/11/2026, ejecución manual): todas las acciones correctas; 3 equipos en los próximos 7 días.
La consulta OData se validó antes contra la API REST de SharePoint (3 próximos, 234 vencidos).

**Hallazgo (datos):** las fechas importadas desde el CSV quedaron guardadas como medianoche UTC; con la zona
horaria del sitio (UTC-05 Bogotá) se muestran un día antes (p. ej. VYE-0441: 14-11-2026 en el CSV, 13-11-2026
en SharePoint). Afecta solo a los datos sintéticos de la carga inicial; los registros creados desde la app
guardan la fecha correcta. Corrección propuesta: sumar 5 horas a las columnas de fecha con un script por la API REST.

**Mejora futura:** crear automáticamente un registro *Programado* en la lista Mantenimientos por cada equipo próximo
(si no existe), y omitir el correo cuando no haya equipos.

---

## Implementación real de FL03 (13/11/2026)
Flujo **"FL03 Alerta de garantias por vencer"** (copia de FL02 con *Guardar como*; las copias quedan desactivadas y hay que activarlas).

1. **Recurrence**: cada 1 mes desde 2026-12-01T12:00:00Z (día 1, 7:00 a. m. hora Colombia).
2. **GarantiasPorVencer** – *Obtener elementos* (activos), orden `field_10 asc`, filtro:
   `field_10 ge '@{formatDateTime(convertFromUtc(utcNow(),'SA Pacific Standard Time'),'yyyy-MM-dd')}' and field_10 le '@{formatDateTime(addDays(convertFromUtc(utcNow(),'SA Pacific Standard Time'),30),'yyyy-MM-dd')}' and field_12 ne 'Dado de baja'`
3. **SinGarantia** – *Obtener elementos* (activos), primeros 5000, filtro `field_10 lt '<hoy>' and field_12 ne 'Dado de baja'`.
4. **Seleccionar** desde `body('GarantiasPorVencer')?['value']`: Placa, Tipo, Marca y modelo, Serial (field_1), Sede,
   Fin de garantía (field_10, dd-MM-yyyy) y Valor de compra (`formatNumber(field_11,'C0','es-CO')`).
5. **Crear tabla HTML** y **Enviar correo (V2)** al área administrativa y financiera (en el prototipo, la cuenta UNAD
   del estudiante), con la tabla y el conteo de equipos activos sin garantía vigente.

Prueba PF-11 (13/11/2026, ejecución manual): estado *Correcto*. Con los datos de prueba hay 6 equipos con garantía por vencer en 30 días.
