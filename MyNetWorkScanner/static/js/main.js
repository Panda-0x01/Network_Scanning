 document.getElementById('scanForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const scanBtn = document.getElementById('scanBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Show loading, hide results
            scanBtn.disabled = true;
            scanBtn.textContent = '⏳ Scanning...';
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                const response = await fetch('/scan', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    displayResults(data);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            } finally {
                scanBtn.disabled = false;
                scanBtn.textContent = '🚀 Start Scan';
                loading.style.display = 'none';
            }
        });
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            
            let html = `
                <div class="result-section">
                    <div class="result-header">📊 Scan Summary</div>
                    <div class="result-content">
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>Target:</strong> ${data.url}
                            </div>
                            <div class="info-item">
                                <strong>Hostname:</strong> ${data.hostname}
                            </div>
                            <div class="info-item">
                                <strong>IP Address:</strong> ${data.ip}
                            </div>
                            <div class="info-item">
                                <strong>Status:</strong> 
                                <span class="status-badge ${data.ping ? 'status-online' : 'status-offline'}">
                                    ${data.ping ? '🟢 Online' : '🔴 Offline/Filtered'}
                                </span>
                            </div>
                            <div class="info-item">
                                <strong>Scan Duration:</strong> ${data.scan_duration}s
                            </div>
                            <div class="info-item">
                                <strong>Ports Scanned:</strong> ${data.total_ports_scanned}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            if (data.open_ports && data.open_ports.length > 0) {
                html += `
                    <div class="result-section">
                        <div class="result-header">🔓 Open Ports (${data.open_ports.length})</div>
                        <div class="result-content">
                            <div class="ports-grid">
                `;
                
                data.open_ports.forEach(port => {
                    html += `
                        <div class="port-item">
                            <div class="port-number">Port ${port.port}</div>
                            <div class="port-service">${port.service}</div>
                        </div>
                    `;
                });
                
                html += `
                            </div>
                        </div>
                    </div>
                `;
            }
            
            if (data.http_info && !data.http_info.error) {
                html += `
                    <div class="result-section">
                        <div class="result-header">🌐 HTTP Information</div>
                        <div class="result-content">
                            <div class="info-grid">
                                <div class="info-item">
                                    <strong>Status Code:</strong> ${data.http_info.status_code}
                                </div>
                                <div class="info-item">
                                    <strong>Server:</strong> ${data.http_info.server}
                                </div>
                                <div class="info-item">
                                    <strong>Content Length:</strong> ${data.http_info.content_length} bytes
                                </div>
                                <div class="info-item">
                                    <strong>Page Title:</strong> ${data.http_info.title || 'N/A'}
                                </div>
                            </div>
                            <h4 style="margin: 20px 0 10px 0;">Response Headers:</h4>
                            <div class="http-headers">
                                ${Object.entries(data.http_info.headers).map(([key, value]) => 
                                    `${key}: ${value}`
                                ).join('\\n')}
                            </div>
                        </div>
                    </div>
                `;
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }