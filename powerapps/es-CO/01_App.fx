// =====================================================================
//  App: Inventario de Activos TI - Vías y Explanaciones (Canvas, Power Apps)
//  Origen de datos: Microsoft Lists (SharePoint) -> Sedes, Activos,
//  Asignaciones, Mantenimientos, VerificacionesInventario, UsuariosApp
//  Pegar en: App > OnStart   (y App > Formulas para las fórmulas con nombre)
// =====================================================================

// ---------- App.Formulas (fórmulas con nombre, se recalculan solas) ----------
gUsuario = LookUp(UsuariosApp; Correo = User().Email && Habilitado);;
gRol = Coalesce(gUsuario.Rol.Value; "Consulta");;
gPuedeEditar = gRol in ["Administrador"; "Inventario"];;
gEsAdmin = gRol = "Administrador";;

// Colores corporativos (ajustar a la marca de Vías y Explanaciones)
cPrimario = ColorValue("#1F4E79");;
cAcento   = ColorValue("#F2A900");;
cFondo    = ColorValue("#F5F7FA");;
cOk       = ColorValue("#2E7D32");;
cAlerta   = ColorValue("#C62828");;

// ---------- App.OnStart ----------
Concurrent(
    ClearCollect(colSedes; Sedes);
    Set(varHoy; Today())
);;
// Si el usuario no está registrado, se informa y queda en modo consulta
If(
    IsBlank(gUsuario);
    Notify("Su usuario no tiene rol asignado. Ingresa en modo consulta."; NotificationType.Warning)
);;
