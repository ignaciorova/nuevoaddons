/** @odoo-module **/
import { registry } from '@web/core/registry';
const { rpc } = window;

function $(sel) { return document.querySelector(sel); }
async function detectLoop(video, onCode) {
    if (!('BarcodeDetector' in window)) return;
    const detector = new window.BarcodeDetector({ formats: ['qr_code', 'code_128', 'ean_13', 'ean_8', 'code_39'] });
    let active = true;
    async function tick() {
        if (!active) return;
        try {
            const barcodes = await detector.detect(video);
            if (barcodes && barcodes.length) {
                const raw = barcodes[0].rawValue;
                onCode(raw);
                return;
            }
        } catch (e) { /* ignore frame errors */ }
        requestAnimationFrame(tick);
    }
    tick();
    return () => { active = false; };
}
async function queryPartnerByCode(code, configId) {
    try { return await rpc('/pos/self_order/barcode/search', { barcode: code, config_id: configId }); }
    catch { return { ok: false, error: 'rpc_failed' }; }
}
function showResult(text, cssClass='text-success') {
    const el = $('#so-scan-result'); if (!el) return;
    el.className = `mt-3 ${cssClass}`; el.textContent = text;
}
function bindToOrder(partner) {
    window.dispatchEvent(new CustomEvent('so:barcodePartnerSelected', { detail: { partner } }));
}
registry.category('public.root').add('selforder_barcode_init_o18', {
    start() {
        const video = $('#so-scan-video');
        const btnStart = $('#so-scan-start');
        const btnStop = $('#so-scan-stop');
        const manual = $('#so-manual-submit');
        const input = $('#so-manual-code');
        let stopLoop = null, stream = null;
        const configId = document.body?.dataset?.posConfigId ? parseInt(document.body.dataset.posConfigId) : null;
        async function startScan() {
            if (!navigator.mediaDevices?.getUserMedia) { showResult('Cámara no disponible; use ingreso manual.', 'text-warning'); return; }
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
                video.srcObject = stream; await video.play();
                stopLoop = await detectLoop(video, async (code) => {
                    btnStop?.click(); showResult('Código detectado. Buscando cliente...');
                    const res = await queryPartnerByCode(code, configId);
                    if (res.ok && res.found) { showResult(`Cliente: ${res.partner.name}`); bindToOrder(res.partner); }
                    else { showResult('Cliente no encontrado.', 'text-danger'); }
                });
                btnStart.disabled = true; btnStop.disabled = False;
            } catch { showResult('No se pudo iniciar la cámara.', 'text-danger'); }
        }
        function stopScan() {
            try { stopLoop && stopLoop(); if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; } if (video) { video.pause(); video.srcObject = null; } }
            finally { btnStart && (btnStart.disabled = false); btnStop && (btnStop.disabled = true); }
        }
        btnStart?.addEventListener('click', startScan);
        btnStop?.addEventListener('click', stopScan);
        manual?.addEventListener('click', async () => {
            const code = (input?.value || '').trim(); if (!code) return;
            showResult('Buscando cliente...'); const res = await queryPartnerByCode(code, configId);
            if (res.ok && res.found) { showResult(`Cliente: ${res.partner.name}`); bindToOrder(res.partner); }
            else { showResult('Cliente no encontrado.', 'text-danger'); }
        });
        window.addEventListener('so:checkoutBindCustomer', () => {});
    }
});
