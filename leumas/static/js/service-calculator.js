/* Phase 3: Service Calculator JavaScript */

class ServiceCalculator {
    constructor() {
        this.roiData = {
            investment: 5000,
            expectedReturn: 25000,
            timeframe: 12,
            riskLevel: 'medium'
        };

        this.costData = {
            projectScope: 'medium',
            complexity: 'moderate',
            timeline: 8,
            teamSize: 3
        };

        this.scopePrices = {
            small: 5000,
            medium: 15000,
            large: 50000
        };

        this.complexityMultiplier = {
            simple: 1.0,
            moderate: 1.5,
            complex: 2.5,
            veryComplex: 4.0
        };
    }

    /**
     * Calculate ROI percentage
     * @param {number} investment - Initial investment
     * @param {number} expectedReturn - Expected return value
     * @returns {object} ROI data with percentage and efficiency
     */
    calculateROI(investment, expectedReturn) {
        if (investment <= 0) {
            return {
                roiPercentage: 0,
                profit: 0,
                efficiency: 0,
                breakeven: Infinity,
                recommendation: 'Enter a valid investment amount'
            };
        }

        const profit = expectedReturn - investment;
        const roiPercentage = ((profit / investment) * 100).toFixed(2);
        
        // Efficiency score (0-100): How good is the ROI?
        // Perfect efficiency is 100% ROI
        const efficiency = Math.min((roiPercentage / 100) * 100, 100).toFixed(1);

        // Estimat breakeven timeframe (in months)
        const monthlyProfit = (profit / this.roiData.timeframe).toFixed(2);
        const breakeven = monthlyProfit > 0 ? (investment / monthlyProfit).toFixed(1) : Infinity;

        return {
            roiPercentage: parseFloat(roiPercentage),
            profit: profit,
            efficiency: parseFloat(efficiency),
            breakeven: breakeven === Infinity ? '∞' : breakeven,
            recommendation: this.getROIRecommendation(roiPercentage)
        };
    }

    /**
     * Get ROI recommendation based on percentage
     */
    getROIRecommendation(roi) {
        const roiNum = parseFloat(roi);
        
        if (roiNum < 0) return '❌ Not recommended - Negative ROI';
        if (roiNum < 10) return '⚠️ Caution - Low ROI';
        if (roiNum < 50) return '👍 Reasonable - Moderate ROI';
        if (roiNum < 100) return '✅ Good - Strong ROI';
        if (roiNum < 200) return '🚀 Excellent - Exceptional ROI';
        return '💎 Exceptional - Outstanding ROI';
    }

    /**
     * Calculate project cost based on scope and complexity
     * @param {string} scope - 'small', 'medium', 'large'
     * @param {string} complexity - 'simple', 'moderate', 'complex', 'veryComplex'
     * @param {number} teamSize - Number of team members
     * @returns {object} Cost breakdown with total, labor, contingency
     */
    calculateProjectCost(scope, complexity, teamSize) {
        const basePrice = this.scopePrices[scope] || 15000;
        const complexMultiplier = this.complexityMultiplier[complexity] || 1.5;
        
        // Labor cost (assume $150/hour, 8 hours/day, 5 days/week)
        const estimatedDays = (basePrice / (150 * 8)) * complexity.length;
        const laborCost = (estimatedDays * 8 * 150 * teamSize).toFixed(0);
        
        // Calculate adjusted base cost
        const adjustedBaseCost = (basePrice * complexMultiplier).toFixed(0);
        
        // Contingency buffer (15-25% based on complexity)
        const contingencyPercentage = 15 + (complexity.length * 2);
        const contingency = (adjustedBaseCost * (contingencyPercentage / 100)).toFixed(0);
        
        const totalCost = (parseFloat(adjustedBaseCost) + parseFloat(contingency)).toFixed(0);

        return {
            baseCost: parseInt(adjustedBaseCost),
            laborCost: parseInt(laborCost),
            contingency: parseInt(contingency),
            totalCost: parseInt(totalCost),
            estimatedDays: estimatedDays.toFixed(0),
            contingencyPercentage: contingencyPercentage,
            breakdown: {
                'Base Price': `$${parseInt(adjustedBaseCost).toLocaleString()}`,
                'Labor Cost': `$${parseInt(laborCost).toLocaleString()}`,
                'Contingency': `$${parseInt(contingency).toLocaleString()}`,
                'Total Estimate': `$${parseInt(totalCost).toLocaleString()}`
            }
        };
    }

    /**
     * Format currency
     */
    formatCurrency(amount) {
        return `$${parseInt(amount).toLocaleString()}`;
    }

    /**
     * Update ROI calculator display
     */
    updateROIDisplay() {
        const result = this.calculateROI(this.roiData.investment, this.roiData.expectedReturn);
        
        const roiResults = document.querySelector('[data-calculator="roi"] .calculator-results');
        if (!roiResults) return;

        roiResults.innerHTML = `
            <div class="result-card">
                <div class="result-label">ROI Percentage</div>
                <div class="result-value">${result.roiPercentage}%</div>
                <div class="result-subtext">${result.recommendation}</div>
            </div>
            
            <div class="result-card">
                <div class="result-label">Net Profit</div>
                <div class="result-value">${this.formatCurrency(result.profit)}</div>
                <div class="roi-efficiency">
                    <span class="roi-label">Efficiency</span>
                    <div class="roi-bar">
                        <div class="roi-fill" style="width: ${result.efficiency}%"></div>
                    </div>
                    <span class="roi-percentage">${result.efficiency}%</span>
                </div>
            </div>
            
            <div class="result-card">
                <div class="result-label">Breakeven Timeline</div>
                <div class="result-value">${result.breakeven}</div>
                <div class="result-subtext">Months to recover initial investment</div>
            </div>
        `;
    }

    /**
     * Update Cost Estimator display
     */
    updateCostDisplay() {
        const result = this.calculateProjectCost(
            this.costData.projectScope,
            this.costData.complexity,
            this.costData.teamSize
        );
        
        const costResults = document.querySelector('[data-calculator="cost"] .calculator-results');
        if (!costResults) return;

        const breakdownHTML = Object.entries(result.breakdown)
            .map(([label, value]) => `
                <div class="breakdown-item ${label.includes('Total') ? 'total-item' : ''}">
                    <span class="breakdown-label">${label}</span>
                    <span class="breakdown-amount">${value}</span>
                </div>
            `).join('');

        costResults.innerHTML = `
            <div class="result-card">
                <div class="result-label">Estimated Total Cost</div>
                <div class="result-value">${this.formatCurrency(result.totalCost)}</div>
                <div class="result-subtext">Includes ${result.contingencyPercentage}% contingency buffer</div>
            </div>
            
            <div class="cost-breakdown">
                <div class="breakdown-title">Cost Breakdown</div>
                ${breakdownHTML}
            </div>
            
            <div class="result-card">
                <div class="result-label">Project Timeline</div>
                <div class="result-value">${result.estimatedDays}</div>
                <div class="result-subtext">Estimated working days (8 hours/day)</div>
            </div>
        `;
    }

    /**
     * Update both calculator displays
     */
    updateAllDisplays() {
        this.updateROIDisplay();
        this.updateCostDisplay();
    }

    /**
     * Reset ROI calculator to defaults
     */
    resetROI() {
        this.roiData = {
            investment: 5000,
            expectedReturn: 25000,
            timeframe: 12,
            riskLevel: 'medium'
        };
        this.updateROIDisplay();
        this.updateROIInputs();
    }

    /**
     * Reset Cost calculator to defaults
     */
    resetCost() {
        this.costData = {
            projectScope: 'medium',
            complexity: 'moderate',
            timeline: 8,
            teamSize: 3
        };
        this.updateCostDisplay();
        this.updateCostInputs();
    }

    /**
     * Update input field values from data
     */
    updateROIInputs() {
        document.querySelectorAll('[data-calculator="roi"] input, [data-calculator="roi"] select').forEach(el => {
            const key = el.dataset.key;
            if (key && this.roiData[key] !== undefined) {
                el.value = this.roiData[key];
                // Update range slider display
                if (el.type === 'range') {
                    const display = el.closest('.input-group')?.querySelector('.range-display');
                    if (display) {
                        if (key === 'investment' || key === 'expectedReturn') {
                            display.textContent = this.formatCurrency(el.value);
                        } else {
                            display.textContent = el.value;
                        }
                    }
                }
            }
        });
    }

    /**
     * Update cost input field values
     */
    updateCostInputs() {
        document.querySelectorAll('[data-calculator="cost"] input, [data-calculator="cost"] select').forEach(el => {
            const key = el.dataset.key;
            if (key && this.costData[key] !== undefined) {
                el.value = this.costData[key];
                // Update range slider display
                if (el.type === 'range') {
                    const display = el.closest('.input-group')?.querySelector('.range-display');
                    if (display) {
                        display.textContent = el.value;
                    }
                }
            }
        });
    }

    /**
     * Initialize event listeners
     */
    init() {
        // ROI Calculator listeners
        document.querySelectorAll('[data-calculator="roi"] input, [data-calculator="roi"] select').forEach(el => {
            el.addEventListener('input', (e) => {
                const key = e.target.dataset.key;
                let value = e.target.value;
                
                // Update range display
                if (e.target.type === 'range') {
                    const display = e.target.closest('.input-group')?.querySelector('.range-display');
                    if (display) {
                        if (key === 'investment' || key === 'expectedReturn') {
                            display.textContent = this.formatCurrency(value);
                        } else {
                            display.textContent = value;
                        }
                    }
                    value = parseInt(value);
                } else {
                    value = isNaN(value) ? value : parseFloat(value);
                }
                
                if (key) {
                    this.roiData[key] = value;
                    this.updateROIDisplay();
                }
            });
        });

        // Cost Calculator listeners
        document.querySelectorAll('[data-calculator="cost"] input, [data-calculator="cost"] select').forEach(el => {
            el.addEventListener('input', (e) => {
                const key = e.target.dataset.key;
                let value = e.target.value;
                
                // Update range display
                if (e.target.type === 'range') {
                    const display = e.target.closest('.input-group')?.querySelector('.range-display');
                    if (display) {
                        if (key === 'teamSize') {
                            display.textContent = `${value} team members`;
                        } else {
                            display.textContent = `${value} weeks`;
                        }
                    }
                    value = parseInt(value);
                }
                
                if (key) {
                    this.costData[key] = value;
                    this.updateCostDisplay();
                }
            });
        });

        // Reset button listeners
        const roiResetBtn = document.querySelector('[data-calculator="roi"] .calculator-btn:last-child');
        const costResetBtn = document.querySelector('[data-calculator="cost"] .calculator-btn:last-child');
        
        if (roiResetBtn) {
            roiResetBtn.addEventListener('click', () => this.resetROI());
        }
        if (costResetBtn) {
            costResetBtn.addEventListener('click', () => this.resetCost());
        }

        // Initial display
        this.updateAllDisplays();
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const calculator = new ServiceCalculator();
        calculator.init();
        
        // Export to window for external access
        window.serviceCalculator = calculator;
    });
} else {
    const calculator = new ServiceCalculator();
    calculator.init();
    window.serviceCalculator = calculator;
}
