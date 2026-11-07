// =====================================================================
//  Pantalla: scrVerificacion  (inventario físico en sitio con escáner)
//  Controles: bcrPlaca (Barcode reader, tipos QR + Code128), ddSedeVerif,
//             ddCondicion, chkCustodio, txtNovedad, btnConfirmar
// =====================================================================

// bcrPlaca.OnScan
Set(varEscaneado; LookUp(Activos; Title = First(bcrPlaca.Barcodes).Value));;
If(IsBlank(varEscaneado); Notify("Placa no registrada en el inventario: " & First(bcrPlaca.Barcodes).Value; NotificationType.Error))

// Entrada manual alterna (txtPlacaManual.OnChange) para equipos sin etiqueta legible
Set(varEscaneado; LookUp(Activos; Title = Upper(Trim(txtPlacaManual.Text))))

// lblCoincideSede.Text
If(varEscaneado.Sede.Id = ddSedeVerif.Selected.ID; "✔ Ubicación coincide"; "✖ Ubicación NO coincide")

// btnConfirmar.OnSelect
Patch(
    VerificacionesInventario;
    Defaults(VerificacionesInventario);
    {
        Title: "INV-" & Text(Today(); "yyyy-mm");
        Activo: {Id: varEscaneado.ID; Value: varEscaneado.Title};
        FechaVerificacion: Now();
        Verificador: User().FullName;
        SedeVerificada: {Id: ddSedeVerif.Selected.ID; Value: ddSedeVerif.Selected.Title};
        CoincideUbicacion: varEscaneado.Sede.Id = ddSedeVerif.Selected.ID;
        CoincideCustodio: chkCustodio.Value;
        CondicionObservada: {Value: ddCondicion.Selected.Value};
        Novedad: txtNovedad.Text
    }
);;
Patch(Activos; varEscaneado; {Condicion: {Value: ddCondicion.Selected.Value}});;
Collect(colVerificadosHoy; {Placa: varEscaneado.Title});;
Reset(txtNovedad);; Set(varEscaneado; Blank());;
Notify("Verificado (" & CountRows(colVerificadosHoy) & " en esta jornada)"; NotificationType.Success)

// =====================================================================
//  Pantalla: scrMantenimientos
// =====================================================================
// galMant.Items
SortByColumns(
    Filter(Mantenimientos; EstadoMantenimiento.Value in ["Programado"; "En curso"]);
    "FechaProgramada"; SortOrder.Ascending
)
// lblVencido.Visible
ThisItem.FechaProgramada < Today()

// btnFinalizar.OnSelect   (cierra el mantenimiento y reprograma el siguiente a 6 meses)
Patch(Mantenimientos; ThisItem; {EstadoMantenimiento: {Value: "Finalizado"}; FechaRealizada: Today()});;
Patch(
    Activos;
    LookUp(Activos; ID = ThisItem.Activo.Id);
    {
        Estado: {Value: If(IsBlank(LookUp(Activos; ID = ThisItem.Activo.Id).CustodioCorreo); "Disponible"; "Asignado")};
        UltimoMantenimiento: Today();
        ProximoMantenimiento: DateAdd(Today(); 6; TimeUnit.Months)
    }
)
