/**
 * VAT Refund Predictor - JavaScript Integration Module
 * 
 * This file can be included in any website to add VAT refund prediction functionality.
 * 
 * Usage:
 * 1. Include this file in your HTML: <script src="vat_predictor.js"></script>
 * 2. Call VATPredictor.predict(data) with your form data
 * 3. Handle the response
 */

const VATPredictor = (function() {
    'use strict';

    // Configuration
    const CONFIG = {
        API_URL: 'http://localhost:5001',  // Change this to your production API URL
        TIMEOUT: 30000  // 30 seconds timeout
    };

    // State to Region mapping (for API compatibility)
    const STATE_TO_REGION = {
        // North
        'Delhi': 'North',
        'Haryana': 'North',
        'Himachal Pradesh': 'North',
        'Jammu and Kashmir': 'North',
        'Ladakh': 'North',
        'Punjab': 'North',
        'Rajasthan': 'North',
        'Uttar Pradesh': 'North',
        'Uttarakhand': 'North',
        'Chandigarh': 'North',
        
        // South
        'Andhra Pradesh': 'South',
        'Karnataka': 'South',
        'Kerala': 'South',
        'Tamil Nadu': 'South',
        'Telangana': 'South',
        'Puducherry': 'South',
        'Lakshadweep': 'South',
        'Andaman and Nicobar Islands': 'South',
        
        // East
        'Bihar': 'East',
        'Jharkhand': 'East',
        'Odisha': 'East',
        'West Bengal': 'East',
        'Assam': 'East',
        'Arunachal Pradesh': 'East',
        'Manipur': 'East',
        'Meghalaya': 'East',
        'Mizoram': 'East',
        'Nagaland': 'East',
        'Sikkim': 'East',
        'Tripura': 'East',
        
        // West
        'Goa': 'West',
        'Gujarat': 'West',
        'Maharashtra': 'West',
        'Chhattisgarh': 'West',
        'Madhya Pradesh': 'West',
        'Dadra and Nagar Haveli and Daman and Diu': 'West'
    };

    // All Indian states and UTs
    const INDIAN_STATES = [
        'Andhra Pradesh',
        'Arunachal Pradesh',
        'Assam',
        'Bihar',
        'Chhattisgarh',
        'Goa',
        'Gujarat',
        'Haryana',
        'Himachal Pradesh',
        'Jharkhand',
        'Karnataka',
        'Kerala',
        'Madhya Pradesh',
        'Maharashtra',
        'Manipur',
        'Meghalaya',
        'Mizoram',
        'Nagaland',
        'Odisha',
        'Punjab',
        'Rajasthan',
        'Sikkim',
        'Tamil Nadu',
        'Telangana',
        'Tripura',
        'Uttar Pradesh',
        'Uttarakhand',
        'West Bengal',
        'Andaman and Nicobar Islands',
        'Chandigarh',
        'Dadra and Nagar Haveli and Daman and Diu',
        'Delhi',
        'Jammu and Kashmir',
        'Ladakh',
        'Lakshadweep',
        'Puducherry'
    ];

    /**
     * Convert state name to region
     * @param {string} state - State name
     * @returns {string} Region (North/South/East/West)
     */
    function stateToRegion(state) {
        return STATE_TO_REGION[state] || 'North';
    }

    /**
     * Check if API is healthy
     * @returns {Promise<Object>} Health status
     */
    async function checkHealth() {
        try {
            const response = await fetch(`${CONFIG.API_URL}/health`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            return await response.json();
        } catch (error) {
            throw new Error(`API health check failed: ${error.message}`);
        }
    }

    /**
     * Predict VAT refund amount
     * @param {Object} data - Input data
     * @param {number} data.amount - Transaction amount
     * @param {number} data.vatRate - VAT rate (5, 12, 18, or 28)
     * @param {string} data.category - Business category
     * @param {string} data.state - Indian state name
     * @param {number} data.annualTurnover - Annual turnover
     * @param {number} [data.riskScore=0.2] - Risk score (0.0 to 1.0)
     * @param {string} [data.compliance='Compliant'] - Compliance status
     * @returns {Promise<Object>} Prediction result
     */
    async function predict(data) {
        // Validate required fields
        if (!data.amount || !data.vatRate || !data.category || !data.state || !data.annualTurnover) {
            throw new Error('Missing required fields: amount, vatRate, category, state, annualTurnover');
        }

        // Convert state to region
        const region = stateToRegion(data.state);

        // Prepare API request data
        const apiData = {
            Amount: parseFloat(data.amount),
            VAT_Rate: parseFloat(data.vatRate),
            Category: data.category,
            Region: region,
            Filing_Status: 'Filed',
            Compliance_Flag: data.compliance || 'Compliant',
            Refund_Eligible: 'Yes',
            Is_Anomaly: 'No',
            Risk_Score: parseFloat(data.riskScore || 0.2),
            Annual_Turnover: parseFloat(data.annualTurnover)
        };

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), CONFIG.TIMEOUT);

            const response = await fetch(`${CONFIG.API_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(apiData),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Prediction failed');
            }

            return result;
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout - API took too long to respond');
            }
            throw new Error(`Prediction failed: ${error.message}`);
        }
    }

    /**
     * Batch predict multiple VAT refunds
     * @param {Array<Object>} dataArray - Array of input data objects
     * @returns {Promise<Array<Object>>} Array of prediction results
     */
    async function batchPredict(dataArray) {
        const predictions = dataArray.map(data => {
            const region = stateToRegion(data.state);
            return {
                Amount: parseFloat(data.amount),
                VAT_Rate: parseFloat(data.vatRate),
                Category: data.category,
                Region: region,
                Filing_Status: 'Filed',
                Compliance_Flag: data.compliance || 'Compliant',
                Refund_Eligible: 'Yes',
                Is_Anomaly: 'No',
                Risk_Score: parseFloat(data.riskScore || 0.2),
                Annual_Turnover: parseFloat(data.annualTurnover)
            };
        });

        try {
            const response = await fetch(`${CONFIG.API_URL}/batch-predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ predictions })
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Batch prediction failed');
            }

            return result.predictions;
        } catch (error) {
            throw new Error(`Batch prediction failed: ${error.message}`);
        }
    }

    /**
     * Get model information
     * @returns {Promise<Object>} Model metadata
     */
    async function getModelInfo() {
        try {
            const response = await fetch(`${CONFIG.API_URL}/model-info`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            return await response.json();
        } catch (error) {
            throw new Error(`Failed to get model info: ${error.message}`);
        }
    }

    /**
     * Get API statistics
     * @returns {Promise<Object>} API usage statistics
     */
    async function getStats() {
        try {
            const response = await fetch(`${CONFIG.API_URL}/stats`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            return await response.json();
        } catch (error) {
            throw new Error(`Failed to get stats: ${error.message}`);
        }
    }

    /**
     * Format currency in Indian Rupees
     * @param {number} amount - Amount to format
     * @returns {string} Formatted currency string
     */
    function formatCurrency(amount) {
        return '₹' + amount.toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    /**
     * Get all Indian states
     * @returns {Array<string>} List of all states
     */
    function getStates() {
        return [...INDIAN_STATES];
    }

    /**
     * Set API URL (useful for switching between dev/prod)
     * @param {string} url - New API URL
     */
    function setApiUrl(url) {
        CONFIG.API_URL = url;
    }

    // Public API
    return {
        predict,
        batchPredict,
        checkHealth,
        getModelInfo,
        getStats,
        formatCurrency,
        getStates,
        stateToRegion,
        setApiUrl,
        version: '1.0.0'
    };
})();

// Export for Node.js/CommonJS
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VATPredictor;
}