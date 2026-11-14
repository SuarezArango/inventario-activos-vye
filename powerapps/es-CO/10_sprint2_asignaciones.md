# Sprint 2 – Asignaciones, historial y baja de activos

Construido el 13/11/2026 en la app "Inventario VYE".

## Listas nuevas en SharePoint (sitio Inventario VYE)
| Lista | Columnas (nombre interno = nombre visible) |
|---|---|
| Asignaciones | Title (consecutivo MOV-…), Activo (búsqueda → activos), TipoMovimiento (Asignación/Transferencia/Devolución), CustodioNombre, CustodioCorreo, Area, SedeDestino (opción), FechaMovimiento (solo fecha), RegistradoPor, ActaAceptada (Sí/No), Observaciones |
| Mantenimientos | Title, Activo (búsqueda), TipoMantenimiento, EstadoMantenimiento, FechaProgramada, FechaRealizada, Tecnico, Costo, Descripcion |
| VerificacionesInventario | Title, Activo (búsqueda), FechaVerificacion, Verificador, SedeVerificada, CoincideUbicacion, CoincideCustodio, CondicionObservada, Novedad |

Todas las columnas de opción con selección múltiple = No y opciones definidas.

## Pantalla AsignacionScreen (HU-04 y HU-07)
Controles: ddMovimiento, txtCustNombre, txtCustCorreo, ddArea, ddSede, chkActa, txtObs,
btnRegistrarMov, btnVolverAsig y lblHistorial (historial del activo).
Se creó pegando YAML en Power Apps Studio (formato invariante, separador ",").

### btnRegistrarMov.OnSelect (como se ve en la barra de fórmulas en español)
```
If(
    ddMovimiento.Selected.Value <> "Devolución" && (IsBlank(txtCustNombre.Text) || IsBlank(txtCustCorreo.Text));
    Notify("Ingrese el nombre y el correo del nuevo custodio"; NotificationType.Error);
    !chkActa.Value;
    Notify("El custodio debe aceptar el acta de entrega"; NotificationType.Error);
    With({dev: ddMovimiento.Selected.Value = "Devolución"};
        Patch(Asignaciones; Defaults(Asignaciones); {
            Title: "MOV-" & Text(Now(); "yyyymmddhhmmss");
            Activo: {Id: RecordsGallery1.Selected.ID; Value: RecordsGallery1.Selected.Title};
            TipoMovimiento: {Value: ddMovimiento.Selected.Value};
            CustodioNombre: If(dev; ""; txtCustNombre.Text);
            CustodioCorreo: If(dev; ""; Lower(txtCustCorreo.Text));
            Area: ddArea.Selected.Value;
            SedeDestino: {Value: ddSede.Selected.Value};
            FechaMovimiento: Today();
            RegistradoPor: User().Email;
            ActaAceptada: chkActa.Value;
            Observaciones: txtObs.Text
        });;
        Patch(activos; LookUp(activos; ID = RecordsGallery1.Selected.ID); {
            Estado: {Value: If(dev; "Disponible"; "Asignado")};
            CustodioNombre: If(dev; ""; txtCustNombre.Text);
            CustodioCorreo: If(dev; ""; Lower(txtCustCorreo.Text));
            Area: {Value: ddArea.Selected.Value};
            Sede: {Value: ddSede.Selected.Value}
        })
    );;
    Notify("Movimiento registrado correctamente"; NotificationType.Success);;
    Reset(txtCustNombre);; Reset(txtCustCorreo);; Reset(txtObs);; Reset(chkActa);;
    Navigate(MainScreen1; ScreenTransition.None)
)
```

### lblHistorial.Text
```
With({h: SortByColumns(Filter(Asignaciones; Activo.Id = RecordsGallery1.Selected.ID); "ID"; SortOrder.Descending)};
    If(IsEmpty(h); "Este activo no tiene movimientos registrados.";
        Concat(FirstN(h; 15); Text(FechaMovimiento; "dd/mm/yyyy") & "  ·  " & TipoMovimiento.Value & "  ·  " &
               Coalesce(CustodioNombre; "(devuelto a TI)") & "  ·  " & SedeDestino.Value; Char(10))))
```
Limitación conocida: el filtro por columna de búsqueda muestra advertencia de delegación.
Mejora futura: agregar una columna de texto "Placa" en Asignaciones y filtrar por ella.

## Cambios en MainScreen1
| Control | Propiedad | Fórmula |
|---|---|---|
| MoveIconButton1 (nuevo, ícono Personas) | OnSelect | `Navigate(AsignacionScreen; ScreenTransition.None)` |
| MoveIconButton1 | Visible | `And(gPuedeEditar; !editMode; !newMode; !deleteMode; RecordsGallery1.Selected.Estado.Value <> "Dado de baja")` |
| EditIconButton1 | Visible | `And(gPuedeEditar; !editMode; !newMode; !deleteMode)` |
| DeleteIconButton1 (HU-12) | OnSelect | `Patch(activos; LookUp(activos; ID = RecordsGallery1.Selected.ID); {Estado: {Value: "Dado de baja"}; CustodioNombre: ""; CustodioCorreo: ""});; Notify("Activo dado de baja. Su historial se conserva."; NotificationType.Success)` |
| DeleteIconButton1 | Visible | `And(gEsAdmin; !editMode; !newMode; !deleteMode; RecordsGallery1.Selected.Estado.Value <> "Dado de baja")` |
| DeleteIconButton1 | Tooltip | `"Dar de baja (solo Administrador)"` |

## Prueba ejecutada
PF-05: transferencia de VYE-0002 de Camila Muñoz a Luis Restrepo (custodio ficticio).
Resultado: registro MOV creado en Asignaciones, activo actualizado y visible en el historial. Aprobada.

## Pantalla VerificacionScreen (HU-06, inventario físico con QR)
YAML completo en `powerapps/VerificacionScreen.pa.yaml` (formato invariante). Se pegó en Studio y luego se
insertó el control **Lector de código de barras** (BarcodeReader1, tipo Auto: QR y Code128).

- Entrada: escaneo del QR de la placa o digitación manual (`txtPlacaManual` + `btnBuscarPlaca`).
- `BarcodeReader1.OnScan` (barra de fórmulas en español):
```
Set(varVerif; LookUp(activos; Title = Upper(Trim(First(BarcodeReader1.Barcodes).Value))));;
If(IsBlank(varVerif); Notify("Placa no registrada en el inventario: " & First(BarcodeReader1.Barcodes).Value; NotificationType.Error);
   varVerif.Estado.Value = "Dado de baja"; Notify("Atención: el activo " & varVerif.Title & " figura como dado de baja"; NotificationType.Warning);
   !IsBlank(LookUp(colVerificados; Placa = varVerif.Title)); Notify("El activo " & varVerif.Title & " ya fue verificado en esta jornada"; NotificationType.Warning);
   Notify("Activo leído: " & varVerif.Title; NotificationType.Information))
```
- Compara la sede registrada con la sede donde se encuentra (`ddSedeVerif`) y muestra ✔/✖.
- `btnConfirmarVerif` hace Patch a VerificacionesInventario (Title INV-aaaa-mm, Activo, FechaVerificacion,
  Verificador, SedeVerificada, CoincideUbicacion, CoincideCustodio, CondicionObservada, Novedad) y acumula
  `colVerificados` para el resumen de la jornada. La verificación no modifica el maestro de activos:
  las novedades quedan como registro de auditoría para que el responsable de inventario decida.
- Acceso: botón `btnIrVerificacion` "Inventario físico (QR)" en el encabezado de MainScreen1, visible con `gPuedeEditar`.
- Nota: la columna Area de activos es de opción, por eso en el texto se usa `varVerif.Area.Value`.
- Etiquetas de prueba: `python scripts/generar_etiquetas_qr.py` → `docs/etiquetas_qr.pdf` (QR = placa).
