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
