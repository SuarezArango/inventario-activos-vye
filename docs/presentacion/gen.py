B={'sp_activos':'1b472256af2eaaddc5e3bf8e56e4ba71','app_principal':'ab0bb46dc6ee76144362e57cdeb8f8d7','app_busqueda':'a9fd4cb1a7768433b0db35844f422189','app_movimiento':'9eae8c2b796cf353adefaa5264cda9d9','fl01':'8776de638a6f992fe7e2f526f06ffb78','fl02':'88606bc91472b3f7f6f82822f0eaad91','flujos':'115c2627cc25e02789872b4d5b65658e','asig_ok':'0cc79326d4e45172fad854f773ded150','qr_coincide':'9532d3b579e0b88bb0a3c4f9796cf7c2','qr_jornada':'9fc093121d8749f06584b6d593cbf4f3','powerbi':'dd8db73f2754d98f48f59c21b8e0e528','app_generada':'87fdc06de120bd0a97d6a8a949a8974b','acta':'d0531afa12ade731267b94ff26a5b3ca','regional':'84f7a7ceaa39d2217932ffc49d245b36','teams':'402ecfd3a50450e18ff2cf58a30fc656','tipos_col':'eb09710d59528a22d28732d4f5a7ec1d','arquitectura':'3e39371ed6d69925f647e37d8da55c7f','modelo':'98f8ed1f5b843290e3dbf53770a70b74','etiquetas':'8ec7fac280e8763e042c77d291871524','app_fechas':'c464c9c310ea58416e88435713213591'}
def img(k,cls,alt): return f'<img src="/_blob/{B[k]}" class="{cls}" alt="{alt}">'
def head(eb,title): return f'<div class="head rise"><p class="eyebrow">{eb}</p><h2>{title}</h2></div>'
def steps(items): return '<div class="steps">'+''.join(f'<div class="step"><div class="n">{i+1}</div><p class="t">{t}</p></div>' for i,t in enumerate(items))+'</div>'
def split(eb,title,items,pic,cap,notes,cls='',extra=''):
    return f'''<section id="{{id}}" class="stack {cls}">
{head(eb,title)}
<div class="split rise2"><div class="txt">{steps(items)}{extra}</div><div class="pic">{pic}<p class="cap">{cap}</p></div></div>
<aside>{notes}</aside>
</section>'''
S={}
S['cover']=f'''<section id="cover" class="dark stack center">
<div class="head rise"><p class="eyebrow">Proyecto de grado · Fase 4 · UNAD</p><h1>Inventario de activos TI<br>con Microsoft Power Platform</h1></div>
<p class="lead rise2" style="width:1300px">Cómo construimos, paso a paso, el prototipo funcional (TRL5) para la empresa Vías y Explanaciones</p>
<div class="cover-names rise3"><p class="body">Camilo Suárez Arango · Liliana Amparo Viana Londoño</p><p class="small">Curso 202016907 · Tutor: Orlando Gómez Barboza · Noviembre de 2026</p></div>
<aside>Presentación de repaso para el video de la Fase 4. Cada diapositiva tiene notas con lo que se puede decir. Saludo: nombres de los dos, curso y el título del proyecto.</aside>
</section>'''
S['agenda']=f'''<section id="agenda" class="stack">
{head("Ruta de la presentación","Qué vamos a recorrer")}
<div class="cards rise2">
<div class="card"><p class="tag">1 · Contexto</p><h3>Problema, objetivo y metodología Scrum</h3></div>
<div class="card"><p class="tag">2 · Diseño</p><h3>Arquitectura y modelo de datos</h3></div>
<div class="card"><p class="tag">3 · Construcción</p><h3>10 pasos, de SharePoint a Power BI</h3></div>
<div class="card"><p class="tag">4 · Resultados</p><h3>Problemas, pruebas, TRL5 y guion del video</h3></div>
</div>
<aside>Mostrar la ruta: primero el contexto, luego el diseño, después cómo se construyó el prototipo desde cero y al final los resultados y lo que va en el video.</aside>
</section>'''
S['problema']=f'''<section id="problema" class="stack alt">
{head("Contexto","El problema en Vías y Explanaciones")}
<div class="cards rise2">
<div class="card"><h3>¿Quién tiene qué equipo?</h3><p class="body">Sin un registro central es difícil saber el custodio, la sede y el estado de cada activo tecnológico.</p></div>
<div class="card"><h3>¿Qué se le debe hacer?</h3><p class="body">Mantenimientos preventivos y garantías que vencen sin que nadie lo note a tiempo.</p></div>
<div class="card"><h3>¿Sigue donde dice el registro?</h3><p class="body">El inventario físico en las sedes se hace a mano y sin trazabilidad de las novedades.</p></div>
</div>
<p class="lead rise3">Necesidad: centralizar el inventario, dejar trazabilidad de cada movimiento y automatizar los avisos.</p>
<aside>Explicar la empresa: obras viales y operación minera con varias sedes. El problema no es solo tecnológico: es de control y trazabilidad. Estas tres preguntas guían todo el prototipo.</aside>
</section>'''
S['objetivo']=f'''<section id="objetivo" class="stack">
{head("Objetivo","Una solución de gestión de activos sobre Power Platform")}
<div class="cards rise2">
<div class="card"><p class="big">1</p><h3>App en Power Apps</h3><p class="body">Registro, búsqueda, roles, asignaciones, baja e inventario con QR.</p></div>
<div class="card"><p class="big">3</p><h3>Flujos en Power Automate</h3><p class="body">Acta de entrega, recordatorio de mantenimiento y alerta de garantías.</p></div>
<div class="card"><p class="big">1</p><h3>Tablero en Power BI</h3><p class="body">Indicadores de estado, antigüedad, valor y obsolescencia del inventario.</p></div>
</div>
<p class="body rise3">Alcance: prototipo funcional validado en un entorno relevante (TRL5), con datos de prueba de 500 activos y 4 sedes.</p>
<aside>Objetivo general: desarrollar e implementar una solución de gestión de activos tecnológicos basada en Microsoft Power Platform para Vías y Explanaciones. Resaltar que el resultado es un prototipo funcional: una app, tres flujos y un tablero, todos sobre la misma fuente de datos.</aside>
</section>'''
S['metodologia']=f'''<section id="metodologia" class="stack alt">
{head("Metodología","Scrum en tres sprints, articulado con CDIO")}
<table class="rise2">
<tr><th>Sprint</th><th>Historias de usuario</th><th>Entregable</th><th>Estado</th></tr>
<tr><td class="k">Sprint 1</td><td>HU-01 Registrar activo · HU-02 Buscar · HU-03 Placa única · HU-11 Roles</td><td>Listas en SharePoint y app base</td><td class="ok">Terminado</td></tr>
<tr><td class="k">Sprint 2</td><td>HU-04 Asignar · HU-05 Acta · HU-06 Inventario QR · HU-07 Historial · HU-08 Mantenimiento · HU-12 Baja</td><td>Movimientos, QR y flujos FL01–FL02</td><td class="ok">Terminado</td></tr>
<tr><td class="k">Sprint 3</td><td>HU-09 Garantías · HU-10 Tablero Power BI · ajustes y pruebas</td><td>FL03, tablero y validación</td><td>En cierre</td></tr>
</table>
<p class="body rise3">CDIO: <b>Concebir</b> (backlog de 14 historias) → <b>Diseñar</b> (arquitectura y datos) → <b>Implementar</b> (sprints) → <b>Operar</b> (pruebas en el tenant real).</p>
<aside>Cada sprint terminó con una revisión y pruebas registradas en el plan de pruebas (PF-01 a PF-11). Las historias HU-13 y HU-14 quedaron como trabajo futuro.</aside>
</section>'''
S['arquitectura']=f'''<section id="arquitectura" class="stack">
{head("Diseño","Arquitectura: todo dentro de Microsoft 365")}
<div class="rise2">{img("arquitectura","diagram","Diagrama de arquitectura: Power Apps y Power Automate leen y escriben en Microsoft Lists; Power BI se conecta a las listas; los custodios reciben correos de Outlook")}</div>
<aside>SharePoint (Microsoft Lists) es la base de datos. Power Apps es la interfaz para registrar y consultar. Power Automate escucha las listas y envía correos. Power BI lee las mismas listas para los indicadores. La autenticación y los permisos los da Microsoft Entra ID, sin servidores propios.</aside>
</section>'''
S['modelo']=f'''<section id="modelo" class="stack alt">
{head("Diseño","Modelo de datos: cinco listas relacionadas")}
<div class="rise2">{img("modelo","diagram","Modelo de datos con las listas activos, Asignaciones, Mantenimientos, VerificacionesInventario y UsuariosApp")}</div>
<aside>La lista activos es el centro. Asignaciones, Mantenimientos y VerificacionesInventario tienen una columna de búsqueda (Activo) que apunta a activos: así se conserva el historial. UsuariosApp define el rol de cada persona en la app.</aside>
</section>'''
S['p1-sitio']=split("Paso 1 de 10 · SharePoint","Crear el espacio de trabajo",
["Crear el equipo <b>Inventario VYE</b> en Microsoft Teams.","Teams crea automáticamente el <b>sitio de SharePoint</b> y el grupo de Microsoft 365.","Los dos integrantes quedan como miembros con permisos de edición."],
img("teams","shot","Equipo Inventario VYE creado en Microsoft Teams"),"Equipo de Teams que da origen al sitio de SharePoint del proyecto.",
"Primer paso: con la cuenta UNAD creamos un equipo en Teams. Eso genera el sitio de SharePoint donde viven todas las listas. Ventaja: no se necesita servidor ni base de datos aparte.")
S['p2-lista']=split("Paso 2 de 10 · Datos","La lista activos con 500 equipos de prueba",
["Script en Python que genera <b>500 activos sintéticos</b> en 4 sedes (CSV).","Importar el CSV como lista <b>activos</b>: placa, serial, tipo, marca, sede, custodio, fechas…","Crear por API REST las listas Asignaciones, Mantenimientos, Verificaciones y UsuariosApp."],
img("sp_activos","shot","Lista activos en SharePoint con placas VYE-0001 a VYE-0008"),"Lista activos en SharePoint: cada fila es un equipo identificado por su placa.",
"Los datos son de prueba pero con la estructura real de un inventario. El script está en el repositorio (generar_datos_prueba.py). Las otras listas se crearon con la API de SharePoint para dejar nombres internos limpios.",cls='alt')
S['p3-config']=f'''<section id="p3-config" class="stack">
{head("Paso 3 de 10 · Configuración","Ajustar columnas y región antes de la app")}
<div class="split rise2"><div class="txt">{steps(["Columnas de opción con valores definidos y <b>selección única</b> (Estado, Tipo, Sede…).","Fechas como <b>solo fecha</b>, sin hora.","Sitio en zona <b>UTC-05 Bogotá</b> y región <b>Español (Colombia)</b>."])}</div>
<div class="pic"><div class="pic-row">{img("tipos_col","qr","Menú de tipos de columna en SharePoint")}{img("regional","qr-shot","Configuración regional del sitio en Español (Colombia)")}</div><p class="cap">Tipos de columna y configuración regional del sitio.</p></div></div>
<aside>Este paso parece menor pero evitó varios errores: al importar el CSV las columnas quedaron como selección múltiple y la app las leía como tablas. También ajustamos la zona horaria para que las fechas no salieran un día antes.</aside>
</section>'''
S['p4-app']=split("Paso 4 de 10 · Power Apps","Generar la app a partir de la lista",
["En Power Apps: <b>Comenzar con datos</b> → lista activos.","Power Apps crea una app con galería, búsqueda y formulario.","Es solo el punto de partida: nombres técnicos, hora en las fechas y sin roles."],
img("app_generada","shot","App generada automáticamente en Power Apps Studio"),"Primera versión generada automáticamente en Power Apps Studio.",
"Mostrar que la app generada sirve como base, pero no está lista: por ejemplo, las fechas tenían selectores de hora y minutos, y no había control de quién puede editar.",cls='alt')
S['p5-personaliza']=split("Paso 5 de 10 · Power Apps","Personalizar: búsqueda, roles y validaciones",
["Búsqueda por <b>placa, serial o custodio</b> (delegable a SharePoint).","Roles con la lista UsuariosApp: Administrador, Inventario, Consulta.","Placa única, mensajes claros y fechas sin hora."],
img("app_busqueda","shot","App publicada filtrando las placas que empiezan por VYE-002"),"App publicada: búsqueda por placa “VYE-002”.",
"Fórmula de roles en App.Formulas: quien no está registrado en UsuariosApp entra como Consulta. Los botones de editar y dar de baja se muestran según el rol. La búsqueda usa StartsWith porque SharePoint la resuelve en el servidor (delegación), así funciona con miles de registros.",
extra='<p class="code">gRol = Coalesce(<br>LookUp(UsuariosApp;<br>Correo = Lower(User().Email)<br>).Rol.Value; "Consulta")</p>')
S['p6-movimientos']=split("Paso 6 de 10 · Trazabilidad","Asignar, transferir y devolver con historial",
["Pantalla <b>Movimiento del activo</b>: tipo, nuevo custodio, área y sede.","Cada movimiento queda en <b>Asignaciones</b> y actualiza el activo.","Dar de baja: solo Administrador y <b>sin borrar el historial</b>."],
img("app_movimiento","shot","Pantalla de movimiento del activo VYE-0020 con su historial"),"Movimiento de VYE-0020: formulario a la izquierda, historial a la derecha.",
"Demostración en vivo para el video: transferir un equipo a otra persona y mostrar cómo aparece en el historial. El custodio debe aceptar el acta (casilla) para registrar el movimiento.",cls='alt')
S['p7-acta']=f'''<section id="p7-acta" class="stack">
{head("Paso 7 de 10 · Power Automate","FL01: acta de entrega automática por correo")}
<div class="pair rise2"><div class="pic">{img("fl01","half","Flujo FL01 en Power Automate con la acción Enviar correo")}<p class="cap">FL01: nuevo registro en Asignaciones → leer el activo → enviar correo.</p></div>
<div class="pic">{img("acta","half","Correo de acta de entrega del activo VYE-0020")}<p class="cap">Correo que recibe el custodio (prueba PF-06).</p></div></div>
<aside>El flujo se dispara solo cuando se registra una asignación o transferencia (no en devoluciones). Detalle técnico para la sustentación: Power Automate usa los nombres internos de las columnas (field_1, field_2…), por eso al principio el correo salía sin tipo ni serial.</aside>
</section>'''
S['p8-qr']=f'''<section id="p8-qr" class="stack alt">
{head("Paso 8 de 10 · Inventario físico","Verificar equipos en sitio con código QR")}
<div class="split rise2"><div class="txt">{steps(["Etiquetas QR generadas con Python: el QR contiene la <b>placa</b>.","En el celular se escanea y la app compara la <b>sede registrada</b> con la real.","Cada verificación queda en <b>VerificacionesInventario</b> con su novedad."])}</div>
<div class="pic"><div class="pic-row">{img("etiquetas","qr","Hoja de etiquetas QR de VYE-0001 a VYE-0020")}{img("qr_coincide","qr-shot","Pantalla de verificación: VYE-0001 con ubicación coincidente")}</div><p class="cap">Etiquetas QR y verificación de VYE-0001: “La ubicación coincide”.</p></div></div>
<aside>Para el video: escanear una etiqueta con la app de Power Apps en el celular. La verificación no modifica el inventario: deja la novedad registrada para que el responsable decida, en línea con la ISO/IEC 19770-1.</aside>
</section>'''
S['p9-flujos']=split("Paso 9 de 10 · Power Automate","FL02 y FL03: recordatorios programados",
["<b>FL02</b> (diario, 7:00 a. m.): mantenimientos de los próximos 7 días y conteo de vencidos.","<b>FL03</b> (mensual, día 1): garantías que vencen en 30 días, con valor de compra.","Consultas OData a la lista activos y tabla HTML en el correo."],
img("fl02","shot","Flujo FL02 con el filtro OData de la acción Proximos"),"FL02: filtro de los mantenimientos de los próximos 7 días.",
"Los dos flujos se probaron con ejecución manual (PF-09 y PF-11). FL03 se creó copiando FL02 con Guardar como y cambiando filtros y columnas: reutilización.")
S['p10-powerbi']=f'''<section id="p10-powerbi" class="stack alt">
{head("Paso 10 de 10 · Power BI","Tablero de indicadores conectado a SharePoint")}
<div class="split rise2"><div class="txt">{steps(["Power BI Desktop → <b>Lista de SharePoint Online</b>.","8 medidas DAX: total, utilización, valor, vencidos, garantías, obsoletos…","Gráficos por sede, estado, antigüedad y tipo, con filtro por sede."])}</div>
<div class="pic">{img("powerbi","shot","Tablero de Power BI con 500 activos y 81,12 % de utilización")}<p class="cap">500 activos · $1,22 mil M · 81,12 % de utilización · 129 obsoletos.</p></div></div>
<aside>Se hizo en Power BI Desktop porque la UNAD no permite activar Power BI en la web con cuenta de estudiante. En la empresa se publicaría en el servicio con licencia corporativa. Equipos obsoletos: portátiles y escritorios con 5 años o más.</aside>
</section>'''
S['problemas']=f'''<section id="problemas" class="stack">
{head("Lecciones aprendidas","Problemas que encontramos y cómo los resolvimos")}
<table class="rise2">
<tr><th>Problema</th><th>Causa</th><th>Solución</th></tr>
<tr><td class="k">La app mostraba “Tabla” en Estado y Tipo</td><td>El CSV creó columnas de selección múltiple</td><td>Opciones definidas y selección única</td></tr>
<tr><td class="k">Fechas un día antes</td><td>Medianoche UTC vista en zona Bogotá</td><td>Región Colombia, solo fecha y script que corrigió 500 registros</td></tr>
<tr><td class="k">Correo sin tipo, marca ni serial</td><td>Power Automate usa nombres internos field_N</td><td>Mapa de field_1 a field_20 en el flujo</td></tr>
<tr><td class="k">Power BI web no disponible</td><td>El tenant UNAD no aprueba Fabric free</td><td>Tablero en Power BI Desktop</td></tr>
<tr><td class="k">App en solo lectura</td><td>Otra sesión de Studio abierta</td><td>Cerrar o invalidar el bloqueo de edición</td></tr>
</table>
<aside>Esta diapositiva es muy útil para la sustentación: muestra que entendimos la plataforma y no solo seguimos un tutorial. Elegir dos de estos casos para contarlos en el video.</aside>
</section>'''
S['pruebas']=f'''<section id="pruebas" class="stack alt">
{head("Validación","Pruebas funcionales ejecutadas")}
<table class="rise2">
<tr><th>Prueba</th><th>Historia</th><th>Caso</th><th>Resultado</th></tr>
<tr><td class="k">PF-04 / PF-05</td><td>HU-04</td><td>Asignar y transferir un activo con historial</td><td class="ok">Aprobada</td></tr>
<tr><td class="k">PF-06</td><td>HU-05</td><td>Correo de acta con datos completos</td><td class="ok">Aprobada</td></tr>
<tr><td class="k">PF-07 / PF-08</td><td>HU-06</td><td>Escaneo QR en el celular y placa inexistente</td><td class="ok">Aprobada</td></tr>
<tr><td class="k">PF-09</td><td>HU-08</td><td>FL02: recordatorio de mantenimiento</td><td class="ok">Aprobada</td></tr>
<tr><td class="k">PF-10</td><td>HU-10</td><td>Tablero: el total coincide con la lista (500)</td><td class="ok">Aprobada</td></tr>
<tr><td class="k">PF-11</td><td>HU-09</td><td>FL03: alerta de garantías por vencer</td><td class="ok">Aprobada</td></tr>
</table>
<p class="small rise3">Plan de pruebas basado en ISO/IEC 25010 e ISO/IEC/IEEE 29119-3; evidencias en el repositorio (tests/evidencias).</p>
<aside>Cada prueba tiene su pantallazo. Pendiente para cerrar el Sprint 3: encuesta de usabilidad SUS y verificación de 20 equipos con las etiquetas QR.</aside>
</section>'''
S['trl5']=f'''<section id="trl5" class="stack">
{head("Nivel de madurez","¿Por qué decimos que es TRL5?")}
<div class="cards rise2">
<div class="card"><p class="tag">Entorno relevante</p><p class="body">Tenant real de Microsoft 365, SharePoint en línea, correos reales y app móvil con cámara.</p></div>
<div class="card"><p class="tag">Datos representativos</p><p class="body">500 activos con la estructura de un inventario real, 4 sedes y varios tipos de equipo.</p></div>
<div class="card"><p class="tag">Componentes integrados</p><p class="body">App, flujos y tablero funcionando sobre la misma fuente de datos.</p></div>
</div>
<p class="body rise3"><b>Limitaciones:</b> tenant académico (solo cuentas UNAD entran a la app), datos sintéticos y Power BI en Desktop. En la empresa se migraría a su tenant con un buzón compartido.</p>
<aside>TRL5 de MinCiencias: validación en un entorno relevante. No es el entorno final de la empresa, pero sí la misma plataforma que usaría. Por eso la migración es directa.</aside>
</section>'''
S['guion']=f'''<section id="guion" class="stack alt">
{head("Para el video (máx. 10 min)","Guion sugerido y reparto")}
<table class="rise2">
<tr><th>Tiempo</th><th>Quién</th><th>Qué se muestra</th></tr>
<tr><td class="k">0:00 – 0:45</td><td>Ambos</td><td>Presentación y problema de la empresa</td></tr>
<tr><td class="k">0:45 – 2:00</td><td>Liliana</td><td>Objetivo, Scrum y arquitectura</td></tr>
<tr><td class="k">2:00 – 4:00</td><td>Camilo</td><td>SharePoint y app: búsqueda, roles y formulario</td></tr>
<tr><td class="k">4:00 – 5:30</td><td>Liliana</td><td>Transferencia en vivo y correo del acta</td></tr>
<tr><td class="k">5:30 – 7:00</td><td>Camilo</td><td>Inventario físico: escaneo QR en el celular</td></tr>
<tr><td class="k">7:00 – 8:15</td><td>Liliana</td><td>Flujos FL02 y FL03</td></tr>
<tr><td class="k">8:15 – 9:15</td><td>Camilo</td><td>Tablero de Power BI</td></tr>
<tr><td class="k">9:15 – 10:00</td><td>Ambos</td><td>Resultados, TRL5 y conclusiones</td></tr>
</table>
<aside>Recordatorio de la guía: las dos cámaras encendidas todo el tiempo y máximo 10 minutos. El video debe mostrar el PROTOTIPO funcionando, no el documento. Ensayar una vez con cronómetro.</aside>
</section>'''
S['cierre']=f'''<section id="cierre" class="dark stack center">
<div class="head rise"><p class="eyebrow">Cierre</p><h2>Un prototipo que ya responde las tres preguntas</h2></div>
<div class="steps rise2" style="width:1500px">
<p class="lead">¿Quién tiene qué? → app con roles, movimientos e historial.</p>
<p class="lead">¿Qué se le debe hacer? → avisos de mantenimiento y garantía.</p>
<p class="lead">¿Sigue donde dice el registro? → inventario con QR y tablero.</p>
</div>
<p class="body rise3">Trabajo futuro: obsolescencia (FL04), mantenimientos automáticos, etiquetas QR por lote e integración con el ERP.</p>
<aside>Cerrar volviendo a las tres preguntas del inicio. Agradecer al tutor. Mencionar el repositorio de GitHub con el código y las evidencias.</aside>
</section>'''
for k,v in S.items():
    v=v.replace('{id}',k)
    open(f'/home/claude/deck/root/project/slides/{k}.html','w',encoding='utf-8').write(v)
print(len(S))
