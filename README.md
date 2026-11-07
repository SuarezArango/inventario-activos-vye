# Software de Inventariado Físico de Activos Tecnológicos – Vías y Explanaciones

Prototipo funcional (TRL5) del proyecto de grado – Ingeniería de Sistemas, UNAD (202016907).
**Autores:** Camilo Suárez Arnago · Liliana Amparo Viana Londoño · **Tutor:** Orlando Gómez Barboza

Solución *low-code* en Microsoft Power Platform para registrar, asignar, verificar físicamente y analizar
≈500 activos tecnológicos, desarrollada con **Scrum**.

## Arquitectura
```
 Usuarios (web / móvil)
        │
   Power Apps (Canvas) ──► Office 365 Users (directorio)
        │   lectura/escritura
   Microsoft Lists (SharePoint Online)
   Sedes · Activos · Asignaciones · Mantenimientos · VerificacionesInventario · UsuariosApp
        │ disparadores / consultas             │ conector SharePoint
   Power Automate (FL01–FL04) ──► Outlook   Power BI (tablero gerencial)
```

## Estructura del repositorio
| Carpeta | Contenido |
|---------|-----------|
| `docs/` | Metodología Scrum, product backlog |
| `lists/` | Modelo de datos (esquema de las listas) |
| `scripts/` | Aprovisionamiento de listas (PnP PowerShell) y generador de datos de prueba (Python) |
| `data/` | Datos sintéticos de prueba (CSV) |
| `powerapps/` | Fórmulas Power Fx por pantalla y, al exportar, el paquete `.msapp` de la app |
| `flows/` | Diseño de los flujos y paquetes exportados (.zip) |
| `powerbi/` | Modelo, medidas DAX y archivo `.pbix` |
| `tests/` | Plan y registro de pruebas, SUS |

## Puesta en marcha
1. Crear un sitio de SharePoint (ej. `InventarioTI`).
2. `python scripts/generar_datos_prueba.py --activos 500`
3. `./scripts/aprovisionar_listas.ps1 -SiteUrl <url-del-sitio> -ClientId <guid> -CargarDatos`
4. En Power Apps: *Crear > Aplicación de lienzo en blanco*, agregar las 6 listas y Office 365 Users como orígenes
   de datos y construir las pantallas pegando las fórmulas de `powerapps/` (ver el orden 01–06).
5. Crear los flujos según `flows/flujos_power_automate.md`.
6. Power BI Desktop: conectar a las listas y crear las medidas de `powerbi/medidas_dax.md`.
7. Exportar la app (`Archivo > Guardar como > Este equipo`, .msapp), los flujos (.zip) y el .pbix a sus carpetas y hacer *commit*.

## Versionado
`main` = versión estable · ramas `sprint-N` · etiquetas `v0.1` (Sprint 1), `v0.2` (Sprint 2), `v1.0` (TRL5).
