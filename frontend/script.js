const API_BASE_URL = 'http://localhost:5001';

// Get all elements
const codeInput = document.getElementById('code-input');
const analyzeBtn = document.getElementById('analyze-btn');
const clearBtn = document.getElementById('clear-btn');
const languageSelect = document.getElementById('language-select');
const analysisResultsPanel = document.getElementById('analysis-results-panel');
const statsPanel = document.getElementById('statistics-panel');
const statusMsg = document.getElementById('status-message');
const loadingSpinner = document.getElementById('loading-spinner');

function showStatus(msg, type = 'info') {
    if (statusMsg) {
        statusMsg.textContent = msg;
        statusMsg.className = `status-message show ${type}`;
        setTimeout(() => statusMsg.classList.remove('show'), 4000);
    }
}

function showLoading(show = true) {
    if (loadingSpinner) {
        loadingSpinner.style.display = show ? 'flex' : 'none';
    }
}

async function analyzeCode() {
    const code = codeInput.value.trim();
    const language = languageSelect.value;
    
    console.log("Analyzing code...");
    console.log("Language:", language);
    console.log("Code length:", code.length);
    
    if (!code) {
        showStatus('Enter code to analyze', 'info');
        return;
    }
    
    showLoading(true);
    analyzeBtn.disabled = true;
    
    try {
        console.log("Sending request to:", `${API_BASE_URL}/analyze`);
        
        const res = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language })
        });
        
        console.log("Response status:", res.status);
        
        const data = await res.json();
        console.log("Response data:", data);
        
        if (!data.success) {
            showStatus('Error: ' + data.error, 'error');
            console.error('Error from server:', data.error);
            showLoading(false);
            analyzeBtn.disabled = false;
            return;
        }
        
        // Display analysis results
        displayAnalysisResults(data.issues);
        
        // Display optimization techniques to apply
        displayStatistics(data.statistics, data.issues);
        
        showStatus('✨ Analysis complete!', 'success');
        
    } catch (error) {
        console.error('Fetch error:', error);
        showStatus('Error: ' + error.message, 'error');
    } finally {
        showLoading(false);
        analyzeBtn.disabled = false;
    }
}

function displayAnalysisResults(issues) {
    if (!analysisResultsPanel) return;

    analysisResultsPanel.innerHTML = '';

    if (issues.length === 0) {
        const p = document.createElement('p');
        p.textContent = 'No inefficiencies or errors found.';
        p.style.color = 'green';
        analysisResultsPanel.appendChild(p);
        return;
    }

    issues.forEach(issue => {
        const div = document.createElement('div');

        let colors = {
            bg: '#e6f2ff',
            border: '#3498db',
            text: '#333'
        };

        if (issue.severity === 'error') {
            colors = { bg: '#ffe6e6', border: '#e74c3c', text: '#333' };
        } else if (issue.severity === 'warning') {
            colors = { bg: '#fff9e6', border: '#f39c12', text: '#333' };
        }

        div.style.cssText = `padding: 8px; margin: 8px 0; background: ${colors.bg}; border-left: 4px solid ${colors.border}; border-radius: 3px; color: ${colors.text};`;
        div.innerHTML = `<strong>Line ${issue.line}:</strong> ${issue.issue}`;
        analysisResultsPanel.appendChild(div);
    });
}

function displayStatistics(stats, issues = []) {
    if (!statsPanel) return;

    const issueTypes = new Set((issues || []).map(issue => issue.type));

    const applicableTechniques = [];

    if ((stats.constant_folding || 0) > 0 || issueTypes.has('constant_folding')) {
        applicableTechniques.push('Constant Folding');
    }
    if ((stats.dead_code || 0) > 0 || issueTypes.has('dead_code')) {
        applicableTechniques.push('Dead Code Elimination');
    }
    if ((stats.redundant_assignment || 0) > 0 || issueTypes.has('redundant')) {
        applicableTechniques.push('Redundant Assignment Removal');
    }
    if ((stats.expression_simplify || 0) > 0 || issueTypes.has('simplify')) {
        applicableTechniques.push('Expression Simplification');
    }

    statsPanel.innerHTML = '<h3>Optimization Techniques To Apply</h3>';

    if (applicableTechniques.length === 0) {
        const p = document.createElement('p');
        p.style.color = '#999';
        p.textContent = 'No optimization techniques need to be applied.';
        statsPanel.appendChild(p);
        return;
    }

    const list = document.createElement('ul');
    list.style.listStyle = 'none';
    list.style.padding = '0';

    applicableTechniques.forEach(name => {
        const item = document.createElement('li');
        item.style.cssText = 'padding: 8px; margin: 6px 0; background: #f0f0f0; border-left: 4px solid #667eea; border-radius: 3px;';
        item.textContent = name;
        list.appendChild(item);
    });

    statsPanel.appendChild(list);
}

function clearCode() {
    if (codeInput) codeInput.value = '';
    if (analysisResultsPanel) {
        analysisResultsPanel.innerHTML = 'Analysis results will appear here...';
    }
    if (statsPanel) {
        statsPanel.innerHTML = `
            <h3>Optimization Techniques To Apply</h3>
            <p style="color: #999;">Click Analyze to see required optimization techniques...</p>
        `;
    }
    showStatus('Code cleared', 'info');
}

// Event listeners
if (analyzeBtn) {
    analyzeBtn.addEventListener('click', analyzeCode);
}

if (clearBtn) {
    clearBtn.addEventListener('click', clearCode);
}

if (codeInput) {
    codeInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            analyzeCode();
        }
    });
}

// Check backend health
document.addEventListener('DOMContentLoaded', () => {
    console.log("Page loaded");
    fetch(`${API_BASE_URL}/health`)
        .then(res => res.json())
        .then(data => {
            console.log("Backend is healthy:", data);
            showStatus('✓ Backend connected', 'success');
        })
        .catch(err => {
            console.error('Backend health check failed:', err);
            showStatus('⚠️ Backend not running on port 5001', 'error');
        });
});