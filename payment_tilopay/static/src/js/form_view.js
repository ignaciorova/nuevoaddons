/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const actionRegistry = registry.category("actions");

actionRegistry.add("tilopay_fetch_methods", async function (env, action) {
    const orm = env.services.orm;
    const notification = env.services.notification;
    const currentAction = env.services.action;

    try {
        // 👉 1. Llamas tu SDK o simulas lógica JS
        console.log("Ejecutando Tilopay SDK...");
        let resultado = await new Promise((resolve) =>
            setTimeout(() => resolve({ api_key: "123", metodo: "tarjeta" }), 2000)
        );

        // 👉 2. Actualizamos el registro actual
        let activeId = action.res_id || action.context.active_id;
        await orm.write("payment.provider", [activeId], {
            tilopay_api_key: resultado.api_key,
            tilopay_method: resultado.metodo,
        });

        notification.add("Registro actualizado con éxito ✅", { type: "success" });

        // 👉 3. Refrescamos el formulario
        return currentAction.doAction({
            type: "ir.actions.act_window",
            res_model: "payment.provider",
            res_id: activeId,
            views: [[false, "form"]],
            target: "current",
        });

    } catch (error) {
        console.error(error);
        notification.add("Error ejecutando Tilopay ❌", { type: "danger" });
    }
});
