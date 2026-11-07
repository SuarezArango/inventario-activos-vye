// =====================================================================
//  Pantalla: scrAsignacion  (asignar, transferir o devolver un activo)
//  Controles: ddMovimiento, cmbCustodio (Office365Users), ddArea, ddSedeDestino,
//             chkActa, txtObs, btnRegistrar
//  Conector adicional: Office 365 Users
// =====================================================================

// ddMovimiento.Items
If(IsBlank(varActivoSel.CustodioCorreo); ["Asignación"]; ["Transferencia"; "Devolución"])

// cmbCustodio.Items   (busca en el directorio de la empresa)
Office365Users.SearchUser({searchTerm: cmbCustodio.SearchText; top: 15})
// cmbCustodio.DisplayMode
If(ddMovimiento.Selected.Value = "Devolución"; DisplayMode.Disabled; DisplayMode.Edit)

// btnRegistrar.OnSelect
If(
    ddMovimiento.Selected.Value <> "Devolución" && IsBlank(cmbCustodio.Selected);
    Notify("Seleccione el nuevo custodio"; NotificationType.Error);
    !chkActa.Value;
    Notify("El custodio debe aceptar el acta de entrega"; NotificationType.Error);

    // 1) Registrar movimiento (historial / trazabilidad)
    Patch(
        Asignaciones;
        Defaults(Asignaciones);
        {
            Title: "MOV-" & Text(Now(); "yyyymmddhhmmss");
            Activo: {Id: varActivoSel.ID; Value: varActivoSel.Title};
            TipoMovimiento: {Value: ddMovimiento.Selected.Value};
            CustodioNombre: If(ddMovimiento.Selected.Value = "Devolución"; ""; cmbCustodio.Selected.DisplayName);
            CustodioCorreo: If(ddMovimiento.Selected.Value = "Devolución"; ""; cmbCustodio.Selected.Mail);
            Area: ddArea.Selected.Value;
            SedeDestino: {Id: ddSedeDestino.Selected.ID; Value: ddSedeDestino.Selected.Title};
            FechaMovimiento: Now();
            RegistradoPor: User().Email;
            ActaAceptada: chkActa.Value;
            Observaciones: txtObs.Text
        }
    );;
    // 2) Actualizar el estado actual del activo
    Set(
        varActivoSel;
        Patch(
            Activos;
            varActivoSel;
            {
                Estado: {Value: If(ddMovimiento.Selected.Value = "Devolución"; "Disponible"; "Asignado")};
                CustodioNombre: If(ddMovimiento.Selected.Value = "Devolución"; ""; cmbCustodio.Selected.DisplayName);
                CustodioCorreo: If(ddMovimiento.Selected.Value = "Devolución"; ""; cmbCustodio.Selected.Mail);
                Area: {Value: ddArea.Selected.Value};
                Sede: {Id: ddSedeDestino.Selected.ID; Value: ddSedeDestino.Selected.Title}
            }
        )
    );;
    // El flujo "FL01 Notificar asignación" envía el acta por correo al custodio
    Notify("Movimiento registrado"; NotificationType.Success);;
    Back()
)
