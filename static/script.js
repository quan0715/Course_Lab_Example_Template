    let problems = [];
    let currentProb = null;

    async function init() {
        // Load theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }

        const res = await fetch('/api/problems');
        const data = await res.json();
        document.title = data.app_title;
        document.getElementById('page-title').textContent = data.app_title;
        document.getElementById('app-description').textContent = data.app_description;
        let metaDesc = document.querySelector('meta[name="description"]');
        if (!metaDesc) {
            metaDesc = document.createElement('meta');
            metaDesc.name = 'description';
            document.head.appendChild(metaDesc);
        }
        metaDesc.content = data.app_description;
        problems = data.problems;
        renderTable();
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-theme');
        const isDark = document.body.classList.contains('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        
        // Update editor theme if it exists
        if (editor && window.monaco) {
            monaco.editor.setTheme(isDark ? 'vs-dark' : 'vs');
        }
    }



    function renderTable() {
    const tbody = document.getElementById('problem-table-body');
    if (!tbody) return;
    
    let html = '';
    problems.forEach((p, idx) => {
        const hasRun = p.has_run;
        const isPass = p.passed === p.total_tests && p.total_tests > 0;
        const pct = p.total_tests > 0 ? (p.passed / p.total_tests) * 100 : 0;
        
        let statusIcon = '';
        if (!hasRun) {
            statusIcon = '<div class="table-status-icon pending" title="未執行"><svg viewBox="0 0 32 32" fill="currentColor"><circle cx="16" cy="16" r="8"/></svg></div>';
        } else if (isPass) {
            statusIcon = '<div class="table-status-icon pass" title="通過"><svg viewBox="0 0 32 32" fill="currentColor"><path d="M14 21.414L9 16.414 10.414 15 14 18.586 21.586 11 23 12.414z"/></svg></div>';
        } else {
            statusIcon = '<div class="table-status-icon fail" title="失敗"><svg viewBox="0 0 32 32" fill="currentColor"><path d="M16 2C8.2 2 2 8.2 2 16s6.2 14 14 14 14-6.2 14-14S23.8 2 16 2zm5.4 19L16 15.6 10.6 21 9.2 19.6 14.6 14.2 9.2 8.8 10.6 7.4 16 12.8 21.4 7.4 22.8 8.8 17.4 14.2 22.8 19.6 21.4 21z"/></svg></div>';
        }
        
        const barClass = isPass ? 'table-progress-bar' : 'table-progress-bar fail';
        
        html += `
            <tr class="table-row-clickable" onclick="openModal('${p.name}')">
                <td id="status-${p.name}">${statusIcon}</td>
                <td>
                    <div style="font-weight: 500; font-size: 0.875rem;">${p.display_name || p.name}</div>
                    <div style="font-size: 0.75rem; color: var(--cds-text-secondary); margin-top: 2px;">${p.name}</div>
                </td>
                <td style="font-family: 'IBM Plex Mono', monospace;" id="score-${p.name}">${p.score} / ${p.total_points}</td>
                <td>
                    <div style="display: flex; flex-direction: column;">
                        <span style="font-size: 0.75rem;" id="tests-${p.name}">${p.passed} / ${p.total_tests}</span>
                        <div class="table-progress">
                            <div id="bar-${p.name}" class="${barClass}" style="width: ${pct}%"></div>
                        </div>
                    </div>
                </td>
                <td style="text-align: right;">
                    <button class="table-action-btn" onclick="runProblem(event, '${p.name}')" title="執行測試">
                        <svg viewBox="0 0 32 32"><path d="M7,28a1,1,0,0,1-1-1V5a1,1,0,0,1,1.4819-.8763l20,11a1,1,0,0,1,0,1.7525l-20,11A1.0005,1.0005,0,0,1,7,28Z"/></svg>
                    </button>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    
    // Update progress indicator
    updateProgressIndicator();
}

function updateProgressIndicator() {
    const container = document.getElementById('progress-indicator');
    if (!container) return;
    
    let totalPassed = 0;
    let totalProblems = problems.length;
    let totalScore = 0;
    let maxScore = 0;
    
    problems.forEach(p => {
        if (p.has_run && p.passed === p.total_tests && p.total_tests > 0) {
            totalPassed++;
        }
        totalScore += p.score || 0;
        maxScore += p.total_points || 0;
    });
    
    const percentage = totalProblems > 0 ? (totalPassed / totalProblems) * 100 : 0;
    
    container.innerHTML = `
        <div class="progress-circle" style="--progress: ${percentage}">
            <svg width="36" height="36" viewBox="0 0 36 36">
                <circle class="progress-bg" cx="18" cy="18" r="15"/>
                <circle class="progress-bar" cx="18" cy="18" r="15"/>
            </svg>
        </div>
        <div class="progress-text">
            <span style="font-size: 0.9375rem; font-weight: 500; color: var(--cds-text-primary);">${totalPassed}/${totalProblems} Solved</span>
            <span style="font-size: 0.9375rem; font-weight: 400; color: var(--cds-text-secondary);">Score: ${totalScore}/${maxScore}</span>
        </div>
    `;
}

    async function runProblem(e, probName) {
        if (e) e.stopPropagation();
            const status = document.getElementById(`status-${probName}`);
        if (status) {
            status.innerHTML = '<div class="table-status-icon running"><svg viewBox="0 0 32 32" fill="currentColor"><path d="M16 2C8.2 2 2 8.2 2 16s6.2 14 14 14 14-6.2 14-14S23.8 2 16 2zm0 26C9.4 28 4 22.6 4 16S9.4 4 16 4s12 5.4 12 12-5.4 12-12 12z" opacity="0.2"/><path d="M16 4C9.4 4 4 9.4 4 16" fill="none" stroke="currentColor" stroke-width="4"/></svg></div>';
        }
        
        // If currently viewing this problem, show loading in results
        if (currentProb === probName && document.getElementById('problem-view').classList.contains('is-visible')) {
             document.getElementById('results-container-view').innerHTML = `
                <div class="loading-container">
                    <div class="spinner"></div>
                    <p>執行測試中...</p>
                </div>`;
        }
        
        try {
            const res = await fetch(`/api/run/${probName}`, { method: 'POST' });
            const data = await res.json();
            const idx = problems.findIndex(p => p.name === probName);
            if (idx !== -1) {
                problems[idx].score = data.score;
                problems[idx].passed = data.passed_count;
                problems[idx].total_tests = data.total_count;
                problems[idx].has_run = true;
                problems[idx].details = data.details;
            }
            
            renderTable();
            updateStats();
            
            // If currently viewing this problem, update results
            if (currentProb === probName && document.getElementById('problem-view').classList.contains('is-visible')) {
                if (data.details && data.details.length > 0) {
                    document.getElementById('results-container-view').innerHTML = renderTestResults(data.details);
                } else {
                    document.getElementById('results-container-view').innerHTML = '<div style="text-align:center; padding: 32px; color: var(--cds-text-secondary);">沒有測試結果</div>';
                }
            }
        } catch (err) {
            console.error(err);
            if (status) status.className = 'status-indicator fail';
        }
    }

    async function runAll() {
        for (const p of problems) {
            await runProblem(null, p.name);
        }
    }

    // Global variable for current language
    let currentLang = '';

    // Replaces openModal
    async function openProblemView(probName, lang = '') { // Was openModal
        currentProb = probName;
        if (lang !== undefined) currentLang = lang;
        
        const p = problems.find(x => x.name === probName);
        const displayName = p ? (p.display_name || p.name) : probName;
        document.getElementById('problem-view-title').textContent = displayName;
        document.getElementById('problem-view').classList.add('is-visible');
        
        // Update navigation buttons
        updateNavButtons(probName);
        
        // Reset save button
        const btnSave = document.getElementById('btn-save-view');
        btnSave.disabled = true;
        
        // Reset results
        document.getElementById('results-container-view').innerHTML = '<div style="text-align:center; color: var(--cds-text-secondary); padding: 20px;">尚未執行測試</div>';
        
        // Show loading for description
        document.getElementById('problem-description-content').innerHTML = `
            <div class="loading-container">
                <div class="spinner"></div>
                <p>載入中...</p>
            </div>`;
        
        // Initialize Editor if needed
        if (!editorLoaded && !editorInitializing) {
            initEditor();
        } else if (editorLoaded && editor) {
            // Need to wait for view to be visible for layout to work correctly?
            setTimeout(() => {
                editor.layout();
                loadCode(currentProb);
            }, 50);
        }

        try {
            const langParam = currentLang ? `?lang=${currentLang}` : '';
            const infoRes = await fetch(`/api/problem/${probName}/info${langParam}`);
            const info = await infoRes.json();
            
            // Render language selector
            renderLanguageSelector(info.available_langs || []);    
            // Render Info in Header
            const infoContainer = document.getElementById('problem-header-info');
            
            // Calculate status
            let statusHtml = '';
            if (p && p.has_run) {
                const isPass = p.passed === p.total_tests && p.total_tests > 0;
                const statusText = isPass ? 'PASS' : 'FAIL';
                const statusColor = isPass ? 'var(--cds-success)' : 'var(--cds-danger)';
                statusHtml = `<span class="header-badge" style="background-color: ${statusColor}; color: #fff;">${statusText}</span>`;
            } else {
                statusHtml = `<span class="header-badge" style="background-color: var(--cds-border-subtle); color: var(--cds-text-primary);">PENDING</span>`;
            }

            infoContainer.innerHTML = `
                <span class="header-info-item">Points: ${info.points}</span>
                <span class="header-info-item">Timeout: ${info.timeout || 1}s</span>
                ${statusHtml}
            `;

            // Render Description
            let html = '';
            
            if ((info.forbidden && info.forbidden.length > 0) || (info.required && info.required.length > 0)) {
                html += '<div class="keywords-section" style="margin-top: 0; margin-bottom: 24px;">';
                if (info.forbidden && info.forbidden.length > 0) {
                    html += '<div class="keywords-group"><span class="keywords-label">禁止使用的關鍵字 (Forbidden)</span><div class="keyword-tags">';
                    info.forbidden.forEach(kw => { html += `<span class="keyword-tag forbidden">${kw}</span>`; });
                    html += '</div></div>';
                }
                if (info.required && info.required.length > 0) {
                    html += '<div class="keywords-group"><span class="keywords-label">必須使用的關鍵字 (Required)</span><div class="keyword-tags">';
                    info.required.forEach(kw => { html += `<span class="keyword-tag required">${kw}</span>`; });
                    html += '</div></div>';
                }
                html += '</div>';
            }
            
            if (info.description_html) {
                html += '<div class="problem-description" style="border-bottom: none; padding: 0;">' + info.description_html + '</div>';
            }
            
            // Wrap description in padding container
            document.getElementById('problem-description-content').innerHTML = `<div style="padding: 24px;">${html}</div>`;
            
            // Initialize Cases from API response
        currentProblemCases = info.test_cases || [];
        renderPendingCases();
            
        } catch (err) {
            console.error(err);
            document.getElementById('problem-description-content').innerHTML = '<div style="text-align:center; padding: 32px;"><p>無法載入題目資訊。</p></div>';
        }
    }
    
    // Replaces openModal call in renderGrid
    function openModal(probName) {
        openProblemView(probName);
    }

    function renderMarkdown(md) {
        let html = md;
        html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
        html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.split('\n\n').map(p => {
            if (p.startsWith('<h') || p.startsWith('<pre') || p.trim() === '') return p;
            return '<p>' + p.replace(/\n/g, '<br>') + '</p>';
        }).join('\n');
        return html;
    }

    function renderTestResults(details) {
        if (!details || details.length === 0) return '<p style="padding:16px">無測試資料。</p>';
        return details.map((d, i) => {
            const statusClass = d.status.toLowerCase();
            let content = '';
            if (d.status === 'PASS') {
                content = `<div class="diff-block"><div class="diff-col"><h5>輸入 (Input)</h5><div class="diff-box">${d.input}</div></div><div class="diff-col"><h5>輸出 (Output)</h5><div class="diff-box">${d.output}</div></div></div>`;
            } else if (d.status === 'FAIL' && d.case === 'Keyword Check') {
                const forbiddenList = d.forbidden ? d.forbidden.join(', ') : '無';
                const requiredList = d.required ? d.required.join(', ') : '無';
                const violations = d.violations ? d.violations.join('<br>') : d.msg;
                content = `<div class="keyword-info"><div><strong>禁止關鍵字:</strong> ${forbiddenList}</div><div><strong>必須關鍵字:</strong> ${requiredList}</div><div style="margin-top:8px"><strong>違規項目:</strong><br>${violations}</div></div>`;
            } else if (d.status === 'FAIL' && d.case === 'Compilation') {
                content = `<div class="compile-log"><strong>編譯錯誤日誌:</strong><br><br>${d.log || '無日誌'}</div>`;
            } else if (d.status === 'FAIL') {
                content = `<div class="diff-block"><div class="diff-col"><h5>預期輸出 (Expected)</h5><div class="diff-box">${d.expected}</div></div><div class="diff-col"><h5>實際輸出 (Got)</h5><div class="diff-box">${d.got}</div></div></div><div class="mt-1"><h5>輸入 (Input)</h5><div class="diff-box">${d.input}</div></div>`;
            } else if (d.status === 'TLE') {
                content = `<div>時間限制: ${d.timeout}s</div><div class="mt-1"><h5>輸入 (Input)</h5><div class="diff-box">${d.input}</div></div>`;
            } else if (d.status === 'ERROR') {
                content = `<div class="keyword-info"><strong>執行錯誤:</strong> ${d.msg}</div>`;
            }
            return `<div class="result-item"><div class="result-summary ${statusClass}" onclick="this.nextElementSibling.classList.toggle('is-open')">測試 #${i+1}: ${d.status}</div><div class="result-details">${content}</div></div>`;
        }).join('');
    }

    function rerunCurrent() {
        if (currentProb) runProblem(null, currentProb);
    }

    function closeProblemView() { // Was closeModal
        document.getElementById('problem-view').classList.remove('is-visible');
        // Refresh table when closing to show updated stats
        renderTable();
    }
    
    function renderLanguageSelector(availableLangs) {
        const container = document.getElementById('lang-selector-container');
        if (!container) return;
        
        if (!availableLangs || availableLangs.length <= 1) {
            container.style.display = 'none';
            return;
        }
        
        container.style.display = 'flex';
        
        const langNames = {
            '': '中文',
            'en': 'English',
            'zh': '中文',
            'zh-tw': '繁中',
            'zh-cn': '簡中',
            'ja': '日本語',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch'
        };
        
        let html = '';
        availableLangs.forEach(lang => {
            const isActive = lang === currentLang;
            const displayName = langNames[lang] || lang.toUpperCase();
            const activeClass = isActive ? 'active' : '';
            html += `<button class="lang-btn ${activeClass}" onclick="switchLanguage('${lang}')">${displayName}</button>`;
        });
        
        container.innerHTML = html;
    }
    
    function switchLanguage(lang) {
        currentLang = lang;
        openProblemView(currentProb, lang);
    }
    
    // --- Problem List Navigation Logic ---
    function toggleProblemList() {
        const dropdown = document.getElementById('problem-list-dropdown');
        if (dropdown.classList.contains('is-visible')) {
            dropdown.classList.remove('is-visible');
        } else {
            renderProblemList();
            dropdown.classList.add('is-visible');
        }
    }
    
    function renderProblemList() {
        const dropdown = document.getElementById('problem-list-dropdown');
        dropdown.innerHTML = problems.map((p, idx) => {
            const isActive = p.name === currentProb ? 'active' : '';
            let statusIcon = '<svg class="status-icon none" viewBox="0 0 32 32" fill="currentColor"><circle cx="16" cy="16" r="8"/></svg>';
            
            if (p.has_run) {
                if (p.passed === p.total_tests && p.total_tests > 0) {
                    statusIcon = '<svg class="status-icon pass" viewBox="0 0 32 32" fill="currentColor"><path d="M14 21.414L9 16.414 10.414 15 14 18.586 21.586 11 23 12.414z"/></svg>';
                } else {
                    statusIcon = '<svg class="status-icon fail" viewBox="0 0 32 32" fill="currentColor"><path d="M16 2C8.2 2 2 8.2 2 16s6.2 14 14 14 14-6.2 14-14S23.8 2 16 2zm5.4 19L16 15.6 10.6 21 9.2 19.6 14.6 14.2 9.2 8.8 10.6 7.4 16 12.8 21.4 7.4 22.8 8.8 17.4 14.2 22.8 19.6 21.4 21z"/></svg>';
                }
            }
            
            return `
                <div class="problem-list-item ${isActive}" onclick="openProblemView('${p.name}'); toggleProblemList();">
                    <div class="problem-list-item-title">${idx + 1}. ${p.display_name || p.name}</div>
                    <div class="problem-list-item-status">${statusIcon}</div>
                </div>
            `;
        }).join('');
    }
    
    function prevProblem() {
        const idx = problems.findIndex(p => p.name === currentProb);
        if (idx > 0) {
            openProblemView(problems[idx - 1].name);
        }
    }
    
    function nextProblem() {
        const idx = problems.findIndex(p => p.name === currentProb);
        if (idx !== -1 && idx < problems.length - 1) {
            openProblemView(problems[idx + 1].name);
        }
    }
    
    // Close dropdown when clicking outside
    window.addEventListener('click', function(e) {
        const dropdown = document.getElementById('problem-list-dropdown');
        const btn = document.querySelector('button[onclick="toggleProblemList()"]');
        if (dropdown.classList.contains('is-visible') && !dropdown.contains(e.target) && !btn.contains(e.target)) {
            dropdown.classList.remove('is-visible');
        }
    });

    // Update navigation buttons state
    function updateNavButtons(probName) {
        const idx = problems.findIndex(p => p.name === probName);
        document.getElementById('btn-prev-prob').disabled = (idx <= 0);
        document.getElementById('btn-next-prob').disabled = (idx === -1 || idx >= problems.length - 1);
    }

    // Keep for compatibility if called elsewhere
    function closeModal() {
        closeProblemView();
    }

    function openHelpModal() {
        document.getElementById('help-modal-overlay').classList.add('is-visible');
        // Load markdown content
        fetch('/static/help.md')
            .then(res => res.text())
            .then(md => {
                const html = renderMarkdown(md);
                document.getElementById('help-modal-body').innerHTML = `<div class="help-content">${html}</div>`;
            })
            .catch(err => {
                console.error(err);
                document.getElementById('help-modal-body').innerHTML = '<p>Failed to load help.</p>';
            });
    }

    function closeHelpModal() {
        document.getElementById('help-modal-overlay').classList.remove('is-visible');
    }

    // Editor variables
    let editor = null;
    let editorLoaded = false;
    let editorInitializing = false;

    function initEditor() {
        if (editorLoaded || editorInitializing) return;
        editorInitializing = true;
        
        const isDark = document.body.classList.contains('dark-theme');
        
        require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
        require(['vs/editor/editor.main'], function() {
            // Updated ID: editor-container-view
            editor = monaco.editor.create(document.getElementById('editor-container-view'), {
                value: '// Loading...',
                language: 'cpp',
                theme: isDark ? 'vs-dark' : 'vs',
                automaticLayout: true,
                minimap: { enabled: false }
            });
            
            // Enable save button on change
            editor.onDidChangeModelContent(() => {
                const btnSave = document.getElementById('btn-save-view');
                if (btnSave) btnSave.disabled = false;
            });
            
            // Mark editor as loaded FIRST
            editorLoaded = true;
            editorInitializing = false;
            
            // Then load code
            if (currentProb) {
                console.log('Editor initialized, loading code for:', currentProb);
                loadCode(currentProb);
            }
        });
    }

    async function loadCode(probName) {
        if (!editor) {
            console.error('Editor not ready yet');
            return;
        }
        try {
            console.log('Fetching code for:', probName);
            const res = await fetch(`/api/code/${probName}`);
            const data = await res.json();
            console.log('Code fetched, length:', data.content ? data.content.length : 0);
            if (data.content) {
                editor.setValue(data.content);
                // Reset save button
                const btnSave = document.getElementById('btn-save-view');
                if (btnSave) btnSave.disabled = true;
                console.log('Code loaded successfully');
            }
        } catch (err) {
            console.error('Failed to load code:', err);
            editor.setValue('// Failed to load code');
        }
    }

    async function saveCode() {
        if (!editor || !currentProb) return;
        const content = editor.getValue();
        try {
            const res = await fetch(`/api/code/${currentProb}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: content })
            });
            const data = await res.json();
            if (data.success) {
                // Disable save button
                const btnSave = document.getElementById('btn-save-view');
                if (btnSave) btnSave.disabled = true;
            } else {
                alert('儲存失敗: ' + data.error);
            }
        } catch (err) {
            alert('儲存失敗: ' + err);
        }
    }
    
    async function runFromEditor() {
        const btnSave = document.getElementById('btn-save-view');
        if (!btnSave.disabled) {
            await saveCode();
        }
        
        // Switch to result tab
    // switchTab('test-result'); // Removed tab switching
    
    document.getElementById('results-container-view').innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>執行測試中...</p>
        </div>`;
            
        try {
            // Add timeout to prevent indefinite loading
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
            
            const res = await fetch(`/api/run/${currentProb}`, { 
                method: 'POST',
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            
            const data = await res.json();
            
            // Update the problem data
            const p = problems.find(x => x.name === currentProb);
            if (p) {
                p.score = data.score;
                p.total_points = data.total_points;
                p.passed = data.passed_count;
                p.total_tests = data.total_count;
                p.has_run = true;
                p.details = data.details;
            }
            
            // Update stats
            renderTable();
            
            // Render results in Results View
            if (data.details && data.details.length > 0) {
                document.getElementById('results-container-view').innerHTML = renderTestResults(data.details);
            } else {
                document.getElementById('results-container-view').innerHTML = '<div style="text-align:center; padding: 32px; color: var(--cds-text-secondary);">沒有測試結果</div>';
            }
            
        } catch (err) {
            console.error(err);
            let errorMsg = '執行失敗';
            if (err.name === 'AbortError') {
                errorMsg = '執行逾時（超過30秒）';
            } else if (err.message) {
                errorMsg = '執行失敗: ' + err.message;
            }
            document.getElementById('results-container-view').innerHTML = '<p style="color:var(--cds-danger); text-align:center; padding: 32px;">' + errorMsg + '</p>';
        }
    }

    // Git Push function - 顯示確認 Modal
    function pushToGitHub() {
        openPushConfirmModal();
    }
    
    // 開啟 Push 確認 Modal
    function openPushConfirmModal() {
        const modal = document.getElementById('push-confirm-modal');
        modal.classList.add('is-visible');
    }
    
    // 關閉 Push 確認 Modal
    function closePushConfirmModal() {
        const modal = document.getElementById('push-confirm-modal');
        modal.classList.remove('is-visible');
    }
    
    // 實際執行 Push
    async function confirmPushToGitHub() {
        // 關閉 Modal
        closePushConfirmModal();
        
        // 找到 Push 按鈕
        const btn = document.querySelector('.btn-git');
        const originalHTML = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `
            <div class="spinner" style="width: 16px; height: 16px; border-width: 2px; margin-right: 8px;"></div>
            推送中...
        `;
        
        try {
            const response = await fetch('/api/git_push', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    commit_message: 'GUI 自動提交'
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert(`✅ 成功！\n\n${result.message}\n\n詳細資訊:\n${result.details || ''}`);
            } else {
                alert(`❌ 失敗\n\n${result.error}\n\n${result.details || ''}\n\n請檢查:\n1. 是否已設定 git remote\n2. 是否有網路連線\n3. 是否有權限 push 到遠端`);
            }
        } catch (error) {
            alert(`❌ 錯誤\n\n無法連接到伺服器: ${error.message}`);
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHTML;
        }
    }

    // Tab Switching Logic
    let currentProblemCases = []; 

    function renderPendingCases() {
    const container = document.getElementById('results-container-view');
    if (!container) return;
    
    if (!currentProblemCases || currentProblemCases.length === 0) {
        container.innerHTML = '<p style="color: var(--cds-text-secondary); padding: 20px; text-align: center;">No test cases available.</p>';
        return;
    }

    let html = '';
    
    currentProblemCases.forEach((caseData, idx) => {
        // Format input: remove outer brackets if present
        let displayInput = caseData.input || '';
        displayInput = displayInput.replace(/^\[|\]$/g, ''); 
        displayInput = displayInput.split('\n').map(line => line.replace(/^\[|\]$/g, '')).join('\n');
        
        let displayExpected = caseData.expected || '';
        displayExpected = displayExpected.replace(/^\[|\]$/g, '');

        // Use the same structure as renderTestResults for PASS cases
        const content = `<div class="diff-col"><h5>輸入 (Input)</h5><div class="diff-box">${displayInput}</div></div><div class="diff-col"><h5>輸出 (Output)</h5><div class="diff-box">${displayExpected}</div></div>`;

        html += `
            <div class="result-item">
                <div class="result-summary" onclick="this.nextElementSibling.classList.toggle('is-open')" style="color: var(--cds-text-primary);">
                    測試 #${idx + 1} (Pending)
                </div>
                <div class="result-details">
                    ${content}
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}    

    function addTestCase() {
        // Disabled
    }

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', init);
    
    // Handle resize
    window.addEventListener('resize', () => {
        if (editor) editor.layout();
    });
