// =====================================================================
//  Fórmulas REALES de la app "Inventario VYE" al cierre del Sprint 1
//  (app generada desde la lista con Integrar > Power Apps > Crear una aplicación)
//  Configuración regional en español: separador de argumentos ";" y de fórmulas ";;"
//  Orígenes de datos: activos, UsuariosApp (SharePoint, sitio Inventario VYE)
// =====================================================================

// ---------- App.Formulas (HU-11: roles) ----------
gRol = Coalesce(LookUp(UsuariosApp; Correo = Lower(User().Email)).Rol.Value; "Consulta");;
gPuedeEditar = gRol = "Administrador" || gRol = "Inventario";;
gEsAdmin = gRol = "Administrador";;

// ---------- TableNameLabel1.Text (barra superior con el rol) ----------
"Inventario VYE · " & gRol

// ---------- RecordsGallery1.Items (HU-02: búsqueda delegable por placa, serial o custodio) ----------
SortByColumns(
    Filter([@activos];
        IsBlank(SearchInput1.Text)
        || StartsWith(Title; SearchInput1.Text)
        || StartsWith(Serial; SearchInput1.Text)
        || StartsWith(CustodioNombre; SearchInput1.Text)
    );
    "Title"; SortOrder.Ascending
)

// ---------- Plantilla de la galería ----------
// Title1.Text      (sin cambios)  ThisItem.Title
// Subtitle1.Text
ThisItem.TipoActivo.Value & " · " & ThisItem.Estado.Value
// Body1.Text
Coalesce(ThisItem.CustodioNombre; "Sin custodio")

// ---------- Visibilidad por rol (HU-11) ----------
// NewRecordButtonBarContainer1.Visible   gPuedeEditar
// Ícono lápiz (editar).Visible            gPuedeEditar
// Ícono caneca (eliminar).Visible         gEsAdmin

// ---------- Form1.OnFailure (HU-03: mensaje claro ante placa duplicada) ----------
Notify("No se pudo guardar. Verifique que la placa no exista ya en el inventario y que los campos obligatorios estén completos."; NotificationType.Error)

// ---------- Reglas configuradas en SharePoint (no son fórmulas) ----------
// activos.Title (Placa): Exigir valores únicos = Sí (columna indexada)        -> HU-03
// TipoActivo, Estado, Condicion, Sede, Area: Opción, selección múltiple = No
// Columnas de fecha: solo fecha; sitio en zona (UTC-05:00) Bogotá, región Español (Colombia)
