/** @odoo-module **/
const { rpc } = window;
function $(sel){ return document.querySelector(sel); }
async function quote(configId, city, zip, total){
    try { return await rpc('/pos/self_order/delivery/quote', { config_id: configId, city, zip_code: zip, amount_total: total }); }
    catch { return { ok: false, error: 'rpc_failed' }; }
}
function show(text, css='text-body'){ const el = document.querySelector('#so-delivery-result'); if (el){ el.className = `mt-2 ${css}`; el.textContent = text; } }
document.addEventListener('DOMContentLoaded', () => {
    const btn = $('#so-delivery-quote'); if (!btn) return;
    const configId = document.body?.dataset?.posConfigId ? parseInt(document.body.dataset.posConfigId) : null;
    btn.addEventListener('click', async () => {
        const city = $('#so-delivery-city')?.value || ''; const zip = $('#so-delivery-zip')?.value || '';
        const total = window?.oSelfOrder?.cart?.total || 0.0; // placeholder if exposed by self-order
        const res = await quote(configId, city, zip, total);
        if (!res.ok) { show('Entrega no disponible.', 'text-danger'); return; }
        if (!res.matched) { show('Fuera de zona de entrega.', 'text-warning'); return; }
        if (!res.meets_minimum) { show(`Pedido mínimo: ${res.zone.min_order_amount}.`, 'text-warning'); return; }
        if (res.delivery_fee && res.delivery_fee > 0) { show(`Zona: ${res.zone.name}. Envío: ${res.delivery_fee}. ETA: ${res.zone.eta_min}-${res.zone.eta_max} min.`); }
        else { show(`Zona: ${res.zone.name}. ¡Envío gratis! ETA: ${res.zone.eta_min}-${res.zone.eta_max} min.`, 'text-success'); }
    });
});
