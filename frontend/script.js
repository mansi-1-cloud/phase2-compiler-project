const API_BASE_URL = 'http://localhost:5001';

// Get all elements
const codeInput = document.getElementById('code-input');
const analyzeBtn = document.getElementById('analyze-btn');
const clearBtn = document.getElementById('clear-btn');
const languageSelect = document.getElementById('language-select');
const issuesPanel = document.getElementById('issues-panel');
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
        
        // Display issues
        displayIssues(data.issues);
        
        // Display statistics
        displayStatistics(data.statistics);
        
        showStatus(`✨ Analysis complete! Found ${data.issues.length} issues.`, 'success');
        
    } catch (error) {
        console.error('Fetch error:', error);
        showStatus('Error: ' + error.message, 'error');
    } finally {
        showLoading(false);
        analyzeBtn.disabled = false;
    }
}

function displayIssues(issues) {
    if (!issuesPanel) return;
    
    issuesPanel.innerHTML = '';
    
    const heading = document.createElement('h3');
    heading.textContent = `Issues Found (${issues.length})`;
    issuesPanel.appendChild(heading);
    
    if (issues.length === 0) {
        const p = document.createElement('p');
        p.textContent = '✨ No issues found!';
        p.style.color = 'green';
        issuesPanel.appendChild(p);
        return;
    }
    
    // Group by severity
    const errors = issues.filter(i => i.severity === 'error');
    const warnings = issues.filter(i => i.severity === 'warning');
    const infos = issues.filter(i => i.severity === 'info');
    
    // Show errors
    if (errors.length > 0) {
        const section = document.createElement('div');
        section.style.marginTop = '10px';
        const title = document.createElement('h4');
        title.textContent = `❌ ERRORS (${errors.length})`;
        title.style.color = '#e74c3c';
        section.appendChild(title);
        
        errors.forEach(issue => {
            const div = document.createElement('div');
            div.style.cssText = 'padding: 8px; margin: 5px 0; background: #ffe6e6; border-left: 4px solid #e74c3c; border-radius: 3px;';
            div.innerHTML = `<strong>Line ${issue.line}:</strong> ${issue.issue}`;
            section.appendChild(div);
        });
        issuesPanel.appendChild(section);
    }
    
    // Show warnings
    if (warnings.length > 0) {
        const section = document.createElement('div');
        section.style.marginTop = '10px';
        const title = document.createElement('h4');
        title.textContent = `⚠️ WARNINGS (${warnings.length})`;
        title.style.color = '#f39c12';
        section.appendChild(title);
        
        warnings.forEach(issue => {
            const div = document.createElement('div');
            div.style.cssText = 'padding: 8px; margin: 5px 0; background: #fff9e6; border-left: 4px solid #f39c12; border-radius: 3px;';
            div.innerHTML = `<strong>Line ${issue.line}:</strong> ${issue.issue}`;
            section.appendChild(div);
        });
        issuesPanel.appendChild(section);
    }
    
    // Show infos
    if (infos.length > 0) {
        const section = document.createElement('div');
        section.style.marginTop = '10px';
        const title = document.createElement('h4');
        title.textContent = `ℹ️ INFO (${infos.length})`;
        title.style.color = '#3498db';
        section.appendChild(title);
        
        infos.forEach(issue => {
            const div = document.createElement('div');
            div.style.cssText = 'padding: 8px; margin: 5px 0; background: #e6f2ff; border-left: 4px solid #3498db; border-radius: 3px;';
            div.innerHTML = `<strong>Line ${issue.line}:</strong> ${issue.issue}`;
            section.appendChild(div);
        });
        issuesPanel.appendChild(section);
    }
}

function displayStatistics(stats) {
    if (!statsPanel) return;
    
    statsPanel.innerHTML = `
        <h3>Statistics</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0;">
            <div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">
                <p><strong>Original Lines:</strong> ${stats.original_lines}</p>
            </div>
            <div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">
                <p><strong>Optimized Lines:</strong> ${stats.optimized_lines}</p>
            </div>
            <div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">
                <p><strong>Lines Saved:</strong> ${stats.lines_saved}</p>
            </div>
            <div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">
                <p><strong>Total Optimizations:</strong> ${stats.total_optimizations}</p>
            </div>
        </div>
        
        <h4>Optimization Breakdown:</h4>
        <ul style="list-style: none; padding: 0;">
            <li>🔢 Constant Folding: <strong>${stats.constant_folding}</strong></li>
            <li>🗑️ Dead Code: <strong>${stats.dead_code}</strong></li>
            <li>♻️ Redundant Assignment: <strong>${stats.redundant_assignment}</strong></li>
            <li>🔁 Expression Simplify: <strong>${stats.expression_simplify}</strong></li>
            <li>🔍 Unused Variables: <strong>${stats.unused_variables}</strong></li>
        </ul>
    `;
}

function clearCode() {
    if (codeInput) codeInput.value = '';
    if (issuesPanel) issuesPanel.innerHTML = '';
    if (statsPanel) statsPanel.innerHTML = '';
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