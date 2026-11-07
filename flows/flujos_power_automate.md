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
