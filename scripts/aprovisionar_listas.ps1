<#
.SYNOPSIS
  Crea en un sitio de SharePoint Online las listas del prototipo (lists/modelo_datos.json)
  y opcionalmente carga los datos de prueba de la carpeta data/.

.REQUISITOS
  - PowerShell 7+
  - Módulo PnP.PowerShell:  Install-Module PnP.PowerShell -Scope CurrentUser
  - Un registro de aplicación (ClientId) habilitado para PnP en el tenant:
      Register-PnPEntraIDAppForInteractiveLogin -ApplicationName "PnP-VYE" -Tenant tu-tenant.onmicrosoft.com
  - Permisos de propietario sobre el sitio.

.EJEMPLO
  ./scripts/aprovisionar_listas.ps1 -SiteUrl https://tutenant.sharepoint.com/sites/InventarioTI -ClientId <guid> -CargarDatos
#>
param(
    [Parameter(Mandatory)] [string] $SiteUrl,
    [Parameter(Mandatory)] [string] $ClientId,
    [switch] $CargarDatos
)

$ErrorActionPreference = "Stop"
$raiz   = Split-Path $PSScriptRoot -Parent
$modelo = Get-Content (Join-Path $raiz "lists/modelo_datos.json") -Raw -Encoding utf8 | ConvertFrom-Json

Connect-PnPOnline -Url $SiteUrl -ClientId $ClientId -Interactive

# ---------- 1. Crear listas y columnas ----------
foreach ($lista in $modelo.listas) {
    if (-not (Get-PnPList -Identity $lista.nombre -ErrorAction SilentlyContinue)) {
        New-PnPList -Title $lista.nombre -Template GenericList -OnQuickLaunch | Out-Null
        Write-Host "Lista creada: $($lista.nombre)" -ForegroundColor Green
    }
    foreach ($col in $lista.columnas) {
        if ($col.nombre -eq "Title") {
            if ($col.mostrar) { Set-PnPField -List $lista.nombre -Identity "Title" -Values @{ Title = $col.mostrar } }
            continue
        }
        if (Get-PnPField -List $lista.nombre -Identity $col.nombre -ErrorAction SilentlyContinue) { continue }

        switch ($col.tipo) {
            "Choice" {
                Add-PnPField -List $lista.nombre -DisplayName $col.nombre -InternalName $col.nombre `
                    -Type Choice -Choices $col.opciones -AddToDefaultView | Out-Null
            }
            "Lookup" {
                $origen = Get-PnPList -Identity $col.lista
                $xml = "<Field Type='Lookup' DisplayName='$($col.nombre)' Name='$($col.nombre)' " +
                       "List='{$($origen.Id)}' ShowField='Title' />"
                Add-PnPFieldFromXml -List $lista.nombre -FieldXml $xml | Out-Null
            }
            default {
                Add-PnPField -List $lista.nombre -DisplayName $col.nombre -InternalName $col.nombre `
                    -Type $col.tipo -AddToDefaultView | Out-Null
            }
        }
        if ($col.obligatorio) { Set-PnPField -List $lista.nombre -Identity $col.nombre -Values @{ Required = $true } }
    }
}
# Placa única en Activos
Set-PnPField -List "Activos" -Identity "Title" -Values @{ EnforceUniqueValues = $true; Indexed = $true }

if (-not $CargarDatos) { Write-Host "Listas listas. Use -CargarDatos para importar data/*.csv"; return }

# ---------- 2. Cargar datos de prueba ----------
function Convertir-Valor($valor, $tipo) {
    if ([string]::IsNullOrWhiteSpace($valor)) { return $null }
    switch ($tipo) {
        "Boolean"  { return ($valor -in @("Sí", "Si", "True", "1")) }
        "Number"   { return [double]$valor }
        "Currency" { return [double]$valor }
        default    { return $valor }
    }
}

$cacheIds = @{}   # lista -> (Title -> Id) para resolver búsquedas
function Obtener-Id($lista, $titulo) {
    if (-not $cacheIds.ContainsKey($lista)) {
        $cacheIds[$lista] = @{}
        Get-PnPListItem -List $lista -PageSize 500 -Fields "Title" | ForEach-Object {
            $cacheIds[$lista][$_["Title"]] = $_.Id
        }
    }
    return $cacheIds[$lista][$titulo]
}

$cargas = [ordered]@{
    "Sedes"          = "sedes.csv"
    "Activos"        = "activos.csv"
    "Asignaciones"   = "asignaciones.csv"
    "Mantenimientos" = "mantenimientos.csv"
    "UsuariosApp"    = "usuarios_app.csv"
}
foreach ($nombreLista in $cargas.Keys) {
    $def   = $modelo.listas | Where-Object nombre -eq $nombreLista
    $filas = Import-Csv (Join-Path $raiz "data/$($cargas[$nombreLista])") -Encoding utf8
    $batch = New-PnPBatch
    foreach ($fila in $filas) {
        $valores = @{}
        foreach ($col in $def.columnas) {
            $v = $fila.($col.nombre)
            if ($col.tipo -eq "Lookup") { $v = Obtener-Id $col.lista $v }
            else { $v = Convertir-Valor $v $col.tipo }
            if ($null -ne $v) { $valores[$col.nombre] = $v }
        }
        Add-PnPListItem -List $nombreLista -Values $valores -Batch $batch | Out-Null
    }
    Invoke-PnPBatch -Batch $batch
    $cacheIds.Remove($nombreLista) | Out-Null
    Write-Host "$nombreLista: $($filas.Count) registros cargados" -ForegroundColor Cyan
}
