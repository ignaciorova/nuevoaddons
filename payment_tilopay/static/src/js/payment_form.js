/** @odoo-module **/
/* global Accept */

import { _t } from '@web/core/l10n/translation';
import { loadJS } from '@web/core/assets';

import paymentForm from '@payment/js/payment_form';
import { rpc, RPCError } from '@web/core/network/rpc';

paymentForm.include({

    tilopayData: undefined,

    // #=== DOM MANIPULATION ===#

    /**
     * Prepare the inline form of Tilopay for direct payment.
     *
     * @private
     * @param {number} providerId - The id of the selected payment option's provider.
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The online payment flow of the selected payment option.
     * @return {void}
     */
    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'tilopay') {
            this._super(...arguments);
            return;
        }

        // Check if the inline form values were already extracted.
        this.tilopayData ??= {}; // Store the form data of each instantiated payment method.
        if (flow === 'token') {
            return; // Don't show the form for tokens.
        } else if (this.tilopayData[paymentOptionId]) {
            this._setPaymentFlow('direct'); // Overwrite the flow even if no re-instantiation.
            loadJS(this.tilopayData[paymentOptionId]['acceptJSUrl']); // Reload the SDK.
            return; // Don't re-extract the data if already done for this payment method.
        }

        // Overwrite the flow of the selected payment method.
        this._setPaymentFlow('direct');

        // Extract and deserialize the inline form values.
        const radio = document.querySelector('input[name="o_payment_radio"]:checked');
        const inlineForm = this._getInlineForm(radio);
        const tilopayForm = inlineForm.querySelector('[name="o_tilopay_form"]');
        this.tilopayData[paymentOptionId] = JSON.parse(tilopayForm.dataset['tilopayInlineFormValues']);
        var tilopayJson = JSON.parse(tilopayForm.dataset['tilopayInlineFormValues']);
        let acceptJSUrl = 'https://app.tilopay.com/sdk/v2/sdk_tpay.min.js';
        if (this.tilopayData[paymentOptionId].state !== 'enabled') {
            acceptJSUrl = 'https://app.tilopay.com/sdk/v2/sdk_tpay.min.js';
        }
        this.tilopayData[paymentOptionId].form = tilopayForm;
        this.tilopayData[paymentOptionId].acceptJSUrl = acceptJSUrl;

        // Load the SDK.
        loadJS(acceptJSUrl).then(() => {
            // Init Tilopay:
            this.Tilopay(tilopayJson);
        }).catch((error) => {
            console.error("Error to load Tilopay Script:", error);
        });;
    },

    // #=== PAYMENT FLOW ===#

    /**
     * Trigger the payment processing by submitting the data.
     *
     * @override method from payment.payment_form
     * @private
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The payment flow of the selected payment option.
     * @return {void}
     */
    async _initiatePaymentFlow(providerCode, paymentOptionId, paymentMethodCode, flow) {
        //Set value to 0
        if (providerCode !== 'tilopay' || flow === 'token') {
            this._super(...arguments); // Tokens are handled by the generic flow
            return;
        }

        const inputs = Object.values(
            this._tilopayGetInlineFormInputs(paymentOptionId, paymentMethodCode)
        );
        if (!inputs.every(element => element.reportValidity())) {
            this._enableButton(); // The submit button is disabled at this point, enable it
            return;
        }

        await this._super(...arguments);
    },

    /**
     * Process the direct payment flow.
     *
     * @override method from payment.payment_form
     * @private
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {object} processingValues - The processing values of the transaction.
     * @return {void}
     */
    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'tilopay') {
            this._super(...arguments);
            return;
        }

        // Build the authentication and card data objects to be dispatched to Authorized.Net
        const secureData = {
            authData: {
                apiLoginID: this.tilopayData[paymentOptionId]['login_id'],
                clientKey: this.tilopayData[paymentOptionId]['client_key'],
            },
            ...this._tilopayGetPaymentDetails(paymentOptionId, paymentMethodCode),
        };

        this.TilopayUpdateOptions({
                returnData: '{"reference":"'+processingValues.reference+'","amount":'+processingValues.amount+',"currency":'+processingValues.currency_id+'}' // base 64 array [custom_parameter_a => "valor de a",custom_parameter_b => "valor de b"]
        });
        var payment = await this.tiloMakePay();

        this._tilopayHandleResponse(payment,processingValues)
    },

    /**
     * Handle the response from tilopay and initiate the payment.
     *
     * @private
     * @param {object} response - The payment nonce returned by tilopay
     * @param {object} processingValues - The processing values of the transaction.
     * @return {void}
     */
    _tilopayHandleResponse(response,processingValues) {
        if (response.message !== "Success" & response.message !== "") {
            let error = '';
            this._displayErrorDialog(_t("Payment Tilopay processing failed"), response.message);
            this._enableButton();
            return;
        }
    },

    // #=== GETTERS ===#

    /**
     * Return all relevant inline form inputs based on the payment method type of the provider.
     *
     * @private
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @return {Object} - An object mapping the name of inline form inputs to their DOM element
     */
    _tilopayGetInlineFormInputs(paymentOptionId, paymentMethodCode) {
        const form = this.tilopayData[paymentOptionId]['form'];
        return {
            card: form.querySelector('#tlpy_cc_number'),
            expiration: form.querySelector('#tlpy_cc_expiration_date'),
            cvv: form.querySelector('#tlpy_cvv'),
        };
    },

    /**
     * Return the credit card or bank data to pass to the Accept.dispatch request.
     *
     * @private
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @return {Object} - Data to pass to the Accept.dispatch request
     */
    _tilopayGetPaymentDetails(paymentOptionId, paymentMethodCode) {
        const inputs = this._tilopayGetInlineFormInputs(paymentOptionId, paymentMethodCode);
        return {
            cardData: {
                cardNumber: inputs.card.value.replace(/ /g, ''),
                expiration: inputs.expiration.value,
                cardCode: inputs.cvv.value,
            },
        };
    },

    /**
    * TILOPAY METHODS
    */

    async Tilopay(values){
        var initialize = await Tilopay.Init(values);
        //Charge Methods
        await this.tilopayChargeMethods(initialize.methods);
    },

    async tilopayChargeMethods(methods) {
        methods.forEach(function (method) {
            var option = document.createElement("option");
            option.value = method.id;
            option.text = method.name;
            document.getElementById("tlpy_payment_method").appendChild(option);
        });
    },

    async getSinpeMovil() {
        var sinpe = await Tilopay.getSinpeMovil();
        //console.log(sinpe);
    },

    async tiloMakePay() {
        var payment = await Tilopay.startPayment();
        return payment
    },

    async TilopayUpdateOptions(values){
        var update = await Tilopay.updateOptions(values);
    },
});
