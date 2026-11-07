# Product Backlog

Prioridad MoSCoW (M = Must, S = Should, C = Could). Estimación en puntos de historia (Fibonacci).

| ID | Como… | Quiero… | Para… | Prior. | Pts | Sprint |
|----|-------|---------|-------|--------|-----|--------|
| HU-01 | Auxiliar de inventario | registrar un activo con su hoja de vida (placa, serial, especificaciones, compra, garantía) | tener un catálogo único | M | 5 | 1 |
| HU-02 | Usuario de TI | buscar y filtrar activos por placa, serial, custodio, tipo, estado y sede | encontrarlos en segundos | M | 3 | 1 |
| HU-03 | Auxiliar de inventario | editar la información de un activo y validar placas duplicadas | mantener datos confiables | M | 3 | 1 |
| HU-04 | Auxiliar de inventario | asignar, transferir o recibir en devolución un activo | saber siempre quién lo custodia | M | 5 | 2 |
| HU-05 | Custodio | recibir por correo el acta de entrega del equipo | formalizar la custodia | M | 3 | 2 |
| HU-06 | Auxiliar de inventario | escanear la etiqueta QR de un equipo en sitio y registrar la verificación | hacer el inventario físico rápido | M | 8 | 2 |
| HU-07 | Jefe de TI | ver el historial de movimientos y mantenimientos de un activo | tener trazabilidad completa | M | 3 | 2 |
| HU-08 | Técnico de TI | recibir recordatorios de mantenimientos preventivos próximos | evitar fallas | S | 5 | 2 |
| HU-09 | Área financiera | recibir alertas de garantías por vencer | gestionar reclamaciones a tiempo | S | 3 | 3 |
| HU-10 | Dirección | ver un tablero en Power BI con estado, antigüedad, obsolescencia y valor del inventario | decidir compras y presupuesto | M | 8 | 3 |
| HU-11 | Administrador | asignar roles (Administrador, Inventario, Consulta) | que cada quien vea/modifique solo lo suyo | M | 3 | 1 |
| HU-12 | Administrador | dar de baja un activo dejando registro | controlar la disposición final | S | 2 | 3 |
| HU-13 | Usuario | imprimir etiquetas QR por lote | etiquetar equipos nuevos | C | 3 | Futuro |
| HU-14 | Área financiera | integrar el inventario con el ERP | conciliar activos contables | C | 13 | Futuro |

## Criterios de aceptación (ejemplos, formato Dado/Cuando/Entonces)
**HU-01** – *Dado* un usuario con rol Inventario, *cuando* guarda un activo con placa y serial, *entonces* queda en la
lista Activos con estado *Disponible*; *si* la placa ya existe, el sistema rechaza el registro y lo notifica.

**HU-04** – *Dado* un activo Disponible, *cuando* se registra una asignación con custodio y acta aceptada,
*entonces* se crea un registro en Asignaciones, el activo pasa a *Asignado* con el nuevo custodio y se dispara FL01.

**HU-06** – *Dado* un equipo con etiqueta QR, *cuando* se escanea en una sede, *entonces* el sistema muestra el activo,
indica si la ubicación coincide y guarda la verificación con fecha, verificador y condición observada.

**HU-11** – *Dado* un usuario con rol Consulta, *cuando* abre la app, *entonces* no ve los botones de crear, editar,
asignar ni dar de baja.
