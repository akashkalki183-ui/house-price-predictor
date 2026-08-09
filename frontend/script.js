// script.js
// Website logic and interaction with backend

const API_URL = 'http://localhost:5000';

// ==================
// MAIN FUNCTIONS
// ==================

/**
 * Make a prediction
 */
async function predictPrice() {
    // Get input values
    const sqft = document.getElementById('sqft').value;
    const bedrooms = document.getElementById('bedrooms').value;
    const bathrooms = document.getElementById('bathrooms').value;

    // Validate
    if (!sqft || !bedrooms || !bathrooms) {
        showError('❌ Please fill in all fields!');
        return;
    }

    if (sqft < 100 || sqft > 10000) {
        showError('❌ Square feet should be between 100-10000');
        return;
    }

    // Show loading
    showLoading(true);
    hideError();

    try {
        // Send request to backend
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                square_feet: parseFloat(sqft),
                bedrooms: parseInt(bedrooms),
                bathrooms: parseFloat(bathrooms)
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Format price with commas
            const price = new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(data.predicted_price);

            // Display result
            document.getElementById('predictedPrice').textContent = price;
            document.getElementById('inputDetails').innerHTML = `
                <strong>Input Details:</strong><br>
                📏 Square Feet: ${sqft} sq ft<br>
                🛏️ Bedrooms: ${bedrooms}<br>
                🚿 Bathrooms: ${bathrooms}
            `;
            document.getElementById('result').style.display = 'block';

            // Scroll to result
            setTimeout(() => {
                document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
            }, 300);

            console.log('✅ Prediction successful:', data);
        } else {
            showError('❌ ' + (data.error || 'Prediction failed!'));
        }
    } catch (error) {
        showError('❌ Error: Could not connect to server. Make sure backend is running!');
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

/**
 * Load prediction history
 */
async function loadHistory() {
    try {
        showLoading(true);
        
        const response = await fetch(`${API_URL}/history`);
        const data = await response.json();

        const historyList = document.getElementById('historyList');
        historyList.innerHTML = '';

        if (!data.predictions || data.predictions.length === 0) {
            historyList.innerHTML = '<div class="empty-history">📭 No predictions yet</div>';
            return;
        }

        // Display each prediction
        data.predictions.forEach((pred, index) => {
            const price = new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR',
                minimumFractionDigits: 0
            }).format(pred.predicted_price);

            const date = new Date(pred.date).toLocaleString();

            const html = `
                <div class="history-item">
                    <strong>#${data.predictions.length - index}: ${price}</strong>
                    <p>📏 ${pred.square_feet} sq ft | 🛏️ ${pred.bedrooms} bed | 🚿 ${pred.bathrooms} bath</p>
                    <div class="history-date">${date}</div>
                </div>
            `;
            historyList.innerHTML += html;
        });

        console.log('✅ History loaded:', data.count, 'predictions');
    } catch (error) {
        showError('❌ Failed to load history: ' + error.message);
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

/**
 * Clear all predictions
 */
async function clearAllHistory() {
    if (!confirm('⚠️ Are you sure you want to delete all predictions? This cannot be undone!')) {
        return;
    }

    try {
        showLoading(true);
        
        const response = await fetch(`${API_URL}/clear_history`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('historyList').innerHTML = '<div class="empty-history">📭 History cleared</div>';
            showError('✅ All predictions cleared!');
            setTimeout(() => hideError(), 2000);
            console.log('✅ History cleared');
        } else {
            showError('❌ Failed to clear history');
        }
    } catch (error) {
        showError('❌ Error clearing history: ' + error.message);
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

/**
 * Clear result and reset form
 */
function clearResult() {
    document.getElementById('result').style.display = 'none';
    document.getElementById('sqft').value = '';
    document.getElementById('bedrooms').value = '';
    document.getElementById('bathrooms').value = '';
    document.getElementById('sqft').focus();
}

// ==================
// HELPER FUNCTIONS
// ==================

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('error').style.display = 'none';
}

/**
 * Show/hide loading spinner
 */
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

// ==================
// EVENT LISTENERS
// ==================

// Allow Enter key to submit
document.addEventListener('DOMContentLoaded', function() {
    const inputs = ['sqft', 'bedrooms', 'bathrooms'];
    
    inputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    predictPrice();
                }
            });
        }
    });

    console.log('✅ Page loaded successfully!');
    console.log('🔗 API URL:', API_URL);
});