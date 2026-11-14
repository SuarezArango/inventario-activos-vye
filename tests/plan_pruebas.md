# Plan y registro de pruebas (TRL5)

Basado en ISO/IEC 25010 (familia ISO/IEC 25000) y documentación de pruebas ISO/IEC/IEEE 29119-3.
Completar las columnas *Resultado* y *Evidencia* durante el Sprint 3.

## 1. Pruebas funcionales
| ID | Historia | Caso | Resultado esperado | Resultado | Evidencia |
|----|----------|------|-------------------|-----------|-----------|
| PF-01 | HU-01 | Crear activo con todos los campos | Se guarda, estado Disponible | | |
| PF-02 | HU-03 | Crear activo con placa duplicada | Mensaje "Ya existe un activo con esa placa" | | |
| PF-03 | HU-02 | Buscar por serial parcial (inicio) | La galería muestra el activo | | |
| PF-04 | HU-04 | Asignar activo disponible | Registro en Asignaciones + activo Asignado | Aprobada (13/11/2026) | sprint2_HU04_confirmacion.jpg |
| PF-05 | HU-04 | Transferir a otra sede | Cambia custodio y sede; historial con 2 movimientos | Aprobada (13/11/2026, VYE-0002) | sprint2_HU04_HU07_movimiento_historial.jpg |
| PF-06 | HU-05 | Verificar correo de acta | Correo recibido por el custodio en < 2 min | Aprobada (13/11/2026, VYE-0020; acta completa tras corregir nombres internos field_N) | pantallazo del correo |
| PF-07 | HU-06 | Escanear QR válido | Muestra activo y coincidencia de ubicación | Aprobada (13/11/2026): entrada manual en Studio (VYE-0001 coincide, VYE-0002 no coincide) y escaneo con cámara desde la app móvil Power Apps | sprint2_HU06_verificacion_coincide.jpg |
| PF-08 | HU-06 | Escanear placa inexistente | Mensaje de placa no registrada | Aprobada (VYE-9999) | sprint2_HU06_jornada_y_placa_inexistente.jpg |
| PF-09 | HU-08 | Ejecutar FL02 manualmente | Envía resumen con los equipos de los próximos 7 días y el conteo de vencidos | Aprobada (13/11/2026): 3 equipos próximos (VYE-0441, VYE-0427, VYE-0300) y conteo de vencidos | historial de ejecución FL02 |
| PF-10 | HU-10 | Actualizar informe Power BI | KPIs coinciden con conteos de la lista | | |
| PF-11 | HU-09 | Ejecutar FL03 manualmente | Correo a financiera con garantías por vencer en 30 días | Aprobada (13/11/2026) | historial de ejecución FL03 |

## 2. Pruebas de seguridad y roles
| ID | Rol | Acción | Esperado | Resultado |
|----|-----|--------|----------|-----------|
| PS-01 | Consulta | Abrir detalle de activo | Ve datos, sin botones de edición | |
| PS-02 | Inventario | Dar de baja | Botón no visible | |
| PS-03 | Administrador | Dar de baja | Permitido y registrado | |
| PS-04 | Usuario sin registro | Abrir app | Aviso y modo consulta | |
| PS-05 | Permisos SharePoint | Usuario Consulta edita la lista directamente | Denegado (grupo Lectores) | |

## 3. Pruebas de confiabilidad
- Pérdida de conexión durante un registro → mensaje de error de `frmActivo.OnFailure`, sin datos corruptos.
- Restauración: exportar listas (plantilla / CSV) e importarlas en un sitio de pruebas.

## 4. Validación con muestra real (inventario físico)
Muestra aleatoria de **20 equipos** de la población de ≈500. Para cada uno: tiempo de verificación con la app vs.
método manual y coincidencia de datos.

| Indicador | Línea base (manual) | Con la app | Meta |
|-----------|--------------------|-----------|------|
| Tiempo promedio por equipo (min) | | | −50 % |
| % registros con datos correctos | | | ≥ 95 % |

## 5. Usabilidad – System Usability Scale (SUS)
Aplicar el cuestionario SUS (10 ítems, escala 1–5) a los usuarios clave después de la demo.
Cálculo: ítems impares (valor − 1), pares (5 − valor); suma × 2,5. Meta: puntaje promedio ≥ 68.
