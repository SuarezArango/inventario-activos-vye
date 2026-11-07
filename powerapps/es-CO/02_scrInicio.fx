// =====================================================================
//  Pantalla: scrInicio  (tablero resumido + menú)
// =====================================================================

// lblBienvenida.Text
"Hola, " & User().FullName & "  ·  Rol: " & gRol

// Tarjetas KPI (Label.Text). CountIf sobre Choice es delegable en SharePoint.
// lblTotal.Text
CountRows(Activos)          // Nota: en listas > 2000 usar la columna de conteo de Power BI o un flujo
// lblAsignados.Text
CountIf(Activos; Estado.Value = "Asignado")
// lblDisponibles.Text
CountIf(Activos; Estado.Value = "Disponible")
// lblEnMantenimiento.Text
CountIf(Activos; Estado.Value = "En mantenimiento")
// lblMantVencidos.Text   (mantenimiento preventivo vencido)
CountIf(Activos; ProximoMantenimiento < Today() && Estado.Value <> "Dado de baja")

// Botones de menú (OnSelect)
// btnActivos
Navigate(scrActivos; ScreenTransition.Fade)
// btnNuevo  (Visible: gPuedeEditar)
Set(varActivoSel; Blank());; NewForm(frmActivo);; Navigate(scrFormularioActivo; ScreenTransition.Fade)
// btnVerificar  (Visible: gPuedeEditar)
Navigate(scrVerificacion; ScreenTransition.Fade)
// btnMantenimientos
Navigate(scrMantenimientos; ScreenTransition.Fade)
// btnReportes -> abre el informe de Power BI publicado
Launch("https://app.powerbi.com/groups/me/reports/<ID_DEL_INFORME>")
