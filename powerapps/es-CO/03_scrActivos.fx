// =====================================================================
//  Pantalla: scrActivos  (búsqueda y filtros del inventario)
//  Controles: txtBuscar, ddTipo, ddEstado, ddSede, galActivos
// =====================================================================

// ddTipo.Items      -> Choices(Activos.TipoActivo)      (AllowEmptySelection = true)
// ddEstado.Items    -> Choices(Activos.Estado)
// ddSede.Items      -> colSedes   (Value: Title)

// galActivos.Items  (todas las condiciones son delegables con SharePoint)
SortByColumns(
    Filter(
        Activos;
        (IsBlank(txtBuscar.Text) || StartsWith(Title; txtBuscar.Text)
            || StartsWith(Serial; txtBuscar.Text) || StartsWith(CustodioNombre; txtBuscar.Text));
        (IsBlank(ddTipo.Selected.Value)   || TipoActivo.Value = ddTipo.Selected.Value);
        (IsBlank(ddEstado.Selected.Value) || Estado.Value = ddEstado.Selected.Value);
        (IsBlank(ddSede.Selected.Title)   || Sede.Id = ddSede.Selected.ID)
    );
    "Title"; SortOrder.Ascending
)

// Plantilla de la galería
// lblPlaca.Text      ThisItem.Title & " · " & ThisItem.TipoActivo.Value
// lblDetalle.Text    ThisItem.Marca & " " & ThisItem.Modelo & "  |  " & ThisItem.Sede.Value
// lblCustodio.Text   Coalesce(ThisItem.CustodioNombre, "Sin custodio")
// icoEstado.Color
Switch(
    ThisItem.Estado.Value;
    "Asignado"; cOk;
    "Disponible"; cPrimario;
    "En mantenimiento"; cAcento;
    cAlerta
)
// icoAlertaObsoleto.Visible   (equipo con más de 5 años)
DateDiff(ThisItem.FechaCompra; Today(); TimeUnit.Years) >= 5

// galActivos.OnSelect
Set(varActivoSel; ThisItem);; Navigate(scrDetalleActivo; ScreenTransition.Cover)
