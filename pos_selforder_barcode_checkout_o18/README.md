# POS Self-Order: Barcode Checkout, Custom UI & Delivery Zones (Odoo 18)

Módulo para Odoo 18 Enterprise que añade:
- **Identificación por código** (barcode/QR) en checkout de Self-Order.
- **Vista de checkout** mobile-first con panel de escaneo.
- **Zonas de entrega** con mínima, envío gratis desde, fee y ETA.

> Requisitos: `point_of_sale`, `pos_self_order`, `website`. POS Kitchen Screen es opcional pero recomendado.

## Configuración
1. En **POS → Configuración** activa *Self-Order: Barcode Checkout* y/o *Delivery Options*.
2. Elige **Match Field** (por defecto `selforder_barcode` en `res.partner`).
3. Define **Zonas de Entrega** y el **producto de fee** si corresponde.
4. Publica el **Self-Order (Mobile Menu)**.

## API públicas
- `/pos/self_order/barcode/search` → busca partner por código.
- `/pos/self_order/delivery/quote` → cotiza zona, ETA y fee según ciudad/ZIP y total del carrito.

## Próximos pasos sugeridos
- Agregar **biblioteca de escaneo** (ZXing/Quagga) como fallback.
- Añadir **time slots** de retiro/entrega y validaciones de capacidad.
- Calcular y **agregar automáticamente la línea de fee** en la orden con `so_delivery_fee_product_id`.
- Integrar con **Kitchen Screen** y estados “En preparación/En camino”.
- Hacer el self-order **PWA** con service worker y atajos.
- Validar **consentimiento de datos** y mostrar aviso de privacidad.
