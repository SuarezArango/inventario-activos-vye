// Corrige el desfase de un día en las fechas importadas desde CSV a la lista "activos".
// Las fechas quedaron como medianoche UTC (T00:00:00Z); en la zona del sitio (UTC-05 Bogotá) se mostraban un día antes.
// Se ejecuta en la consola del navegador estando en https://<tenant>.sharepoint.com/sites/InventarioVYE (sesión iniciada).
(async () => {
  const site = "/sites/InventarioVYE/_api";
  const h = { Accept: "application/json;odata=nometadata" };
  const digest = (await (await fetch(site + "/contextinfo", { method: "POST", headers: h })).json()).FormDigestValue;
  const items = (await (await fetch(site + "/web/lists/getbytitle('activos')/items?$top=5000&$select=Id,field_9,field_10,field_18,field_19", { headers: h })).json()).value;
  const campos = ["field_9", "field_10", "field_18", "field_19"]; // FechaCompra, FechaFinGarantia, UltimoMantenimiento, ProximoMantenimiento
  let cambiados = 0, errores = 0;
  for (const it of items) {
    const body = {};
    for (const f of campos) if (it[f] && it[f].endsWith("T00:00:00Z")) body[f] = it[f].replace("T00:00:00Z", "T05:00:00Z");
    if (!Object.keys(body).length) continue;
    const r = await fetch(site + `/web/lists/getbytitle('activos')/items(${it.Id})`, {
      method: "POST",
      headers: { ...h, "Content-Type": "application/json;odata=nometadata", "X-RequestDigest": digest, "IF-MATCH": "*", "X-HTTP-Method": "MERGE" },
      body: JSON.stringify(body),
    });
    r.ok ? cambiados++ : errores++;
  }
  console.log({ total: items.length, cambiados, errores });
})();
