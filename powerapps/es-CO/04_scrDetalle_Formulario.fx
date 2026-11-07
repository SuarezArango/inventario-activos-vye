// =====================================================================
//  Pantalla: scrDetalleActivo  (hoja de vida + historial)
// =====================================================================
// frmVerActivo.DataSource = Activos ; Item = varActivoSel ; DefaultMode = FormMode.View

// galHistorial.Items  (trazabilidad: movimientos del activo)
SortByColumns(
    Filter(Asignaciones; Activo.Id = varActivoSel.ID);
    "FechaMovimiento"; SortOrder.Descending
)
// galMantActivo.Items
SortByColumns(
    Filter(Mantenimientos; Activo.Id = varActivoSel.ID);
    "FechaProgramada"; SortOrder.Descending
)
// imgQR.Image  -> código QR de la placa (para imprimir la etiqueta)
"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" & EncodeUrl(varActivoSel.Title)

// btnEditar.OnSelect   (Visible: gPuedeEditar)
EditForm(frmActivo);; Navigate(scrFormularioActivo; ScreenTransition.Fade)
// btnAsignar.OnSelect  (Visible: gPuedeEditar && varActivoSel.Estado.Value <> "Dado de baja")
Navigate(scrAsignacion; ScreenTransition.Fade)
// btnBaja.OnSelect     (Visible: gEsAdmin)
Patch(Activos; varActivoSel; {Estado: {Value: "Dado de baja"}; CustodioNombre: ""; CustodioCorreo: ""});;
Notify("Activo dado de baja"; NotificationType.Success);; Back()

// =====================================================================
//  Pantalla: scrFormularioActivo  (crear / editar)
// =====================================================================
// frmActivo.DataSource = Activos ; Item = varActivoSel

// Validación antes de guardar (btnGuardar.OnSelect)
If(
    IsBlank(DataCardValue_Placa.Text) || IsBlank(DataCardValue_Serial.Text);
    Notify("Placa y serial son obligatorios"; NotificationType.Error);
    frmActivo.Mode = FormMode.New
        && !IsBlank(LookUp(Activos; Title = DataCardValue_Placa.Text));
    Notify("Ya existe un activo con esa placa"; NotificationType.Error);
    SubmitForm(frmActivo)
)
// frmActivo.OnSuccess
Set(varActivoSel; frmActivo.LastSubmit);;
Notify("Activo guardado correctamente"; NotificationType.Success);;
Navigate(scrDetalleActivo; ScreenTransition.Fade)
// frmActivo.OnFailure
Notify("No se pudo guardar: " & frmActivo.Error; NotificationType.Error)
