// Integrated Dashboard with Backend API Connection
class IntegratedFireDetectionDashboard {
    constructor() {
        this.api = window.fireAPI;
        this.cameras = [
            { id: 1, location: "Block A - Lab 3", status: "fire", confidence: 92, people: 3 },
            { id: 2, location: "Block B - Entrance", status: "safe", confidence: 15, people: 0 },
            { id: 3, location: "Block C - Corridor", status: "warning", confidence: 45, people: 2 },
            { id: 4, location: "Block A - Lab 1", status: "safe", confidence: 8, people: 5 },
            { id: 5, location: "Block D - Cafeteria", status: "safe", confidence: 12, people: 15 },
            { id: 6, location: "Block E - Library", status: "safe", confidence: 5, people: 8 }
        ];
        
        this.stats = {
            activeCameras: 12,
            fireIncidentsToday: 3,
            peopleEvacuated: 8,
            responseTime: 45
        };
        
        this.init();
    }

    async init() {
        console.log('🔥 Initializing Integrated Fire Detection Dashboard...');
        
        // Wait for API to be available
        await this.waitForAPI();
        
        // Load backend data
        await this.loadBackendData();
        
        // Setup UI
        this.bindEvents();
        this.updateCameraFeeds();
        this.startRealTimeUpdates();
        
        console.log('✅ Integrated Dashboard ready!');
    }

    async waitForAPI() {
        return new Promise((resolve) => {
            const checkAPI = () => {
                if (window.fireAPI) {
                    this.api = window.fireAPI;
                    resolve();
                } else {
                    console.log('⏳ Waiting for API to initialize...');
                    setTimeout(checkAPI, 500);
                }
            };
            checkAPI();
        });
    }

    async loadBackendData() {
        try {
            console.log('📊 Loading data from backend...');
            
            const [metrics, statistics, incidents] = await Promise.all([
                this.api.getPerformanceMetrics(),
                this.api.getStatistics(),
                this.api.getFireDetectionIncidents()
            ]);

            if (metrics && metrics.data) {
                console.log('📈 Performance metrics loaded:', metrics.data);
                this.updatePerformanceDisplay(metrics.data);
            }

            if (statistics && statistics.data) {
                console.log('📊 Statistics loaded:', statistics.data);
                this.updateStatsFromBackend(statistics.data);
            }

            if (incidents && incidents.data) {
                console.log('🚨 Incidents loaded:', incidents.data);
                this.updateIncidentsDisplay(incidents.data);
            }

        } catch (error) {
            console.error('❌ Failed to load backend data:', error);
            this.showNotification('Backend data unavailable, using mock data', 'Operating in offline mode', 'warning');
        }
    }

    updatePerformanceDisplay(data) {
        // Update performance metrics in the UI
        const performanceContainer = document.querySelector('.performance-metrics');
        if (performanceContainer) {
            performanceContainer.innerHTML = `
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div class="bg-gray-800 p-4 rounded-lg text-center">
                        <div class="text-2xl font-bold text-blue-400">${data.accuracy || 94.2}%</div>
                        <div class="text-sm text-gray-400">Accuracy</div>
                    </div>
                    <div class="bg-gray-800 p-4 rounded-lg text-center">
                        <div class="text-2xl font-bold text-green-400">${data.precision || 92.1}%</div>
                        <div class="text-sm text-gray-400">Precision</div>
                    </div>
                    <div class="bg-gray-800 p-4 rounded-lg text-center">
                        <div class="text-2xl font-bold text-yellow-400">${data.recall || 88.7}%</div>
                        <div class="text-sm text-gray-400">Recall</div>
                    </div>
                    <div class="bg-gray-800 p-4 rounded-lg text-center">
                        <div class="text-2xl font-bold text-purple-400">${data.processing_time || 125}ms</div>
                        <div class="text-sm text-gray-400">Response Time</div>
                    </div>
                </div>
            `;
        }
    }

    updateStatsFromBackend(data) {
        this.stats = {
            activeCameras: data.total_cameras || this.stats.activeCameras,
            fireIncidentsToday: data.incidents_today || this.stats.fireIncidentsToday,
            peopleEvacuated: data.people_evacuated || this.stats.peopleEvacuated,
            responseTime: data.average_response_time || this.stats.responseTime
        };
        this.updateStats();
    }

    updateIncidentsDisplay(incidents) {
        const incidentsContainer = document.querySelector('.recent-incidents');
        if (incidentsContainer && Array.isArray(incidents)) {
            const incidentsHTML = incidents.map(incident => `
                <div class="bg-gray-800 p-4 rounded-lg border-l-4 ${
                    incident.status === 'resolved' ? 'border-green-500' : 
                    incident.status === 'investigating' ? 'border-yellow-500' : 'border-red-500'
                }">
                    <div class="flex justify-between items-start">
                        <div>
                            <h4 class="font-semibold text-white">${incident.location}</h4>
                            <p class="text-sm text-gray-400">${new Date(incident.timestamp).toLocaleString()}</p>
                            <p class="text-sm text-gray-300">Confidence: ${incident.confidence}%</p>
                        </div>
                        <span class="px-2 py-1 rounded text-xs font-bold ${
                            incident.status === 'resolved' ? 'bg-green-600' : 
                            incident.status === 'investigating' ? 'bg-yellow-600' : 'bg-red-600'
                        }">
                            ${incident.status.toUpperCase()}
                        </span>
                    </div>
                </div>
            `).join('');
            
            incidentsContainer.innerHTML = `
                <h3 class="text-lg font-semibold text-white mb-4">Recent Incidents</h3>
                <div class="space-y-3">${incidentsHTML}</div>
            `;
        }
    }

    bindEvents() {
        // Emergency response buttons
        document.querySelectorAll('.emergency-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const buttonText = e.currentTarget.querySelector('.font-semibold').textContent;
                this.handleEmergencyAction(buttonText);
            });
        });

        // Camera feed interactions
        document.querySelectorAll('.camera-feed').forEach(feed => {
            feed.addEventListener('click', () => {
                const location = feed.dataset.location;
                this.showCameraDetails(location);
            });
        });

        // Test backend connection button
        this.addTestConnectionButton();

        // Start/Stop all buttons
        const startBtn = document.querySelector('.bg-blue-600');
        const pauseBtn = document.querySelector('.bg-gray-600');
        
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startAllCameras());
        }
        
        if (pauseBtn) {
            pauseBtn.addEventListener('click', () => this.pauseAllCameras());
        }
    }

    addTestConnectionButton() {
        const controlsContainer = document.querySelector('.bg-blue-600').parentElement;
        if (controlsContainer) {
            const testBtn = document.createElement('button');
            testBtn.className = 'bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg';
            testBtn.innerHTML = '<i class="fas fa-wifi mr-2"></i>Test Backend';
            testBtn.addEventListener('click', () => this.testBackendConnection());
            controlsContainer.appendChild(testBtn);
        }
    }

    async testBackendConnection() {
        this.showNotification('Testing Connection', 'Checking backend API connection...', 'info');
        
        if (this.api) {
            const result = await this.api.testConnection();
            if (result) {
                this.showNotification('Connection Success', 'Backend API is responsive', 'success');
                await this.loadBackendData(); // Refresh data
            } else {
                this.showNotification('Connection Failed', 'Backend API is not responding', 'danger');
            }
        } else {
            this.showNotification('API Error', 'API client not initialized', 'danger');
        }
    }

    async handleEmergencyAction(action) {
        console.log(`🚨 Emergency action triggered: ${action}`);
        
        const alertData = {
            type: 'manual_trigger',
            action: action,
            location: 'Dashboard Control',
            timestamp: new Date().toISOString(),
            severity: 'high'
        };

        // Send to backend if available
        if (this.api && this.api.isConnected) {
            try {
                await this.api.sendEmergencyAlert(alertData);
                console.log('✅ Emergency alert sent to backend');
            } catch (error) {
                console.error('❌ Failed to send emergency alert to backend:', error);
            }
        }

        switch(action) {
            case 'Trigger Emergency Alert':
                this.triggerEmergencyAlert();
                break;
            case 'Contact Fire Department':
                this.contactFireDepartment();
                break;
            case 'Building Announcement':
                this.makeBuildingAnnouncement();
                break;
        }
    }

    triggerEmergencyAlert() {
        const modal = document.getElementById('emergencyModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
        
        this.showNotification('Emergency Alert Activated', 'All emergency protocols triggered', 'danger');
        this.simulateEmergencyProcedures();
    }

    simulateEmergencyProcedures() {
        const procedures = [
            '🚨 Activating all fire alarms...',
            '📱 Sending SMS alerts to emergency contacts...',
            '📧 Dispatching email notifications...',
            '🔊 Broadcasting evacuation announcements...',
            '🚪 Unlocking emergency exits...',
            '🚒 Contacting fire department...'
        ];

        procedures.forEach((procedure, index) => {
            setTimeout(() => {
                console.log(procedure);
                this.showSystemMessage(procedure);
            }, index * 1000);
        });
    }

    showSystemMessage(message) {
        const messagesContainer = document.querySelector('.system-messages') || this.createMessagesContainer();
        const messageElement = document.createElement('div');
        messageElement.className = 'bg-red-900 border border-red-600 p-2 rounded mb-2 text-sm animate-pulse';
        messageElement.textContent = message;
        messagesContainer.appendChild(messageElement);
        
        // Remove after 10 seconds
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 10000);
    }

    createMessagesContainer() {
        const container = document.createElement('div');
        container.className = 'system-messages fixed bottom-4 left-4 w-80 z-50';
        document.body.appendChild(container);
        return container;
    }

    contactFireDepartment() {
        this.showNotification('Contacting Fire Department', 'Emergency call initiated', 'warning');
        
        setTimeout(() => {
            this.showModal('Fire Department Contact', `
                <div class="text-center">
                    <i class="fas fa-phone-alt text-4xl text-green-500 mb-4"></i>
                    <p class="mb-4">🔊 Connected to Emergency Services</p>
                    <div class="bg-gray-700 p-4 rounded-lg mb-4">
                        <p class="text-sm">"Fire Department dispatch, we have your emergency alert. Units are being dispatched to your location. ETA: 4-6 minutes."</p>
                    </div>
                    <p class="text-sm text-gray-400">Location and incident details transmitted automatically</p>
                </div>
            `);
        }, 2000);
    }

    makeBuildingAnnouncement() {
        this.showNotification('Building Announcement Active', 'PA system broadcasting evacuation notice', 'info');
        
        this.showModal('Building Announcement System', `
            <div class="text-center">
                <i class="fas fa-megaphone text-4xl text-blue-500 mb-4"></i>
                <div class="bg-gray-700 p-4 rounded-lg mb-4">
                    <p class="text-sm text-gray-300 mb-2">🔊 Now Broadcasting:</p>
                    <p class="font-semibold italic">"Attention all building occupants. A fire emergency has been detected. Please evacuate the building immediately using the nearest emergency exit. Do not use elevators. Proceed to the designated assembly point in the parking area."</p>
                </div>
                <div class="flex justify-center space-x-4">
                    <button onclick="this.closest('.fixed').remove()" class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg">Stop Announcement</button>
                    <button class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">Repeat Message</button>
                </div>
            </div>
        `);
    }

    updateCameraFeeds() {
        this.cameras.forEach(camera => {
            this.updateCameraFeedVisual(camera.location, camera.status);
        });
    }

    updateCameraFeedVisual(location, status) {
        const feed = document.querySelector(`[data-location="${location}"]`);
        if (!feed) return;

        const content = feed.querySelector('.w-full.h-48 > div');
        const badge = feed.querySelector('.absolute.top-2.right-2 span');
        
        switch(status) {
            case 'fire':
            case 'emergency':
                content.innerHTML = `
                    <i class="fas fa-fire text-red-500 text-4xl mb-2 fire-icon"></i>
                    <p class="text-red-500 font-bold">FIRE DETECTED</p>
                `;
                badge.className = 'bg-red-500 text-white px-2 py-1 rounded text-xs font-bold animate-pulse';
                badge.textContent = 'ALERT';
                break;
                
            case 'warning':
                content.innerHTML = `
                    <i class="fas fa-exclamation-triangle text-yellow-500 text-4xl mb-2"></i>
                    <p class="text-yellow-500 font-bold">MONITORING</p>
                `;
                badge.className = 'bg-yellow-500 text-black px-2 py-1 rounded text-xs font-bold';
                badge.textContent = 'WATCH';
                break;
                
            case 'safe':
                content.innerHTML = `
                    <i class="fas fa-shield-alt text-green-500 text-4xl mb-2"></i>
                    <p class="text-green-500 font-bold">SAFE</p>
                `;
                badge.className = 'bg-green-500 text-white px-2 py-1 rounded text-xs font-bold';
                badge.textContent = 'SAFE';
                break;
        }
    }

    updateStats() {
        const statElements = document.querySelectorAll('.grid .bg-gray-800 .text-2xl');
        if (statElements.length >= 4) {
            statElements[0].textContent = this.stats.activeCameras;
            statElements[1].textContent = this.stats.fireIncidentsToday;
            statElements[2].textContent = this.stats.peopleEvacuated;
            statElements[3].textContent = this.stats.responseTime + 's';
        }
    }

    startAllCameras() {
        this.showNotification('Cameras Started', 'All camera feeds are now active', 'success');
        document.querySelectorAll('.camera-feed').forEach(feed => {
            feed.classList.remove('opacity-50');
        });
    }

    pauseAllCameras() {
        this.showNotification('Cameras Paused', 'All camera feeds have been paused', 'warning');
        document.querySelectorAll('.camera-feed').forEach(feed => {
            feed.classList.add('opacity-50');
        });
    }

    showCameraDetails(location) {
        const camera = this.cameras.find(c => c.location === location);
        if (!camera) return;

        const statusText = {
            'fire': 'Fire Detected',
            'warning': 'Under Monitoring', 
            'safe': 'Safe'
        }[camera.status];

        const statusColor = {
            'fire': 'text-red-500',
            'warning': 'text-yellow-500',
            'safe': 'text-green-500'
        }[camera.status];

        this.showModal(`Camera Details - ${location}`, `
            <div class="space-y-4">
                <div class="text-center">
                    <h4 class="font-semibold text-lg">${location}</h4>
                    <p class="${statusColor} font-bold">${statusText}</p>
                    <p class="text-sm text-gray-400">Backend Status: ${this.api?.isConnected ? '🟢 Connected' : '🔴 Disconnected'}</p>
                </div>
                
                <div class="grid grid-cols-2 gap-4 text-sm">
                    <div>
                        <span class="text-gray-400">Status:</span>
                        <span class="ml-2 ${statusColor}">${statusText}</span>
                    </div>
                    <div>
                        <span class="text-gray-400">Confidence:</span>
                        <span class="ml-2">${camera.confidence}%</span>
                    </div>
                    <div>
                        <span class="text-gray-400">People Count:</span>
                        <span class="ml-2">${camera.people}</span>
                    </div>
                    <div>
                        <span class="text-gray-400">Last Update:</span>
                        <span class="ml-2">${new Date().toLocaleTimeString()}</span>
                    </div>
                </div>
                
                <div class="flex space-x-2">
                    <button class="flex-1 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">View Live Feed</button>
                    <button class="flex-1 bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg" onclick="window.integratedDashboard.refreshCameraData('${location}')">Refresh Data</button>
                </div>
            </div>
        `);
    }

    async refreshCameraData(location) {
        this.showNotification('Refreshing Data', `Updating camera data for ${location}`, 'info');
        
        if (this.api && this.api.isConnected) {
            try {
                await this.loadBackendData();
                this.showNotification('Data Updated', 'Camera data refreshed from backend', 'success');
            } catch (error) {
                this.showNotification('Refresh Failed', 'Could not update from backend', 'warning');
            }
        } else {
            this.showNotification('Offline Mode', 'Backend not available for refresh', 'warning');
        }
    }

    startRealTimeUpdates() {
        console.log('🔄 Starting real-time updates...');
        
        // Update from backend every 30 seconds
        setInterval(async () => {
            if (this.api && this.api.isConnected) {
                try {
                    await this.loadBackendData();
                    console.log('🔄 Data refreshed from backend');
                } catch (error) {
                    console.error('❌ Real-time update failed:', error);
                }
            }
        }, 30000);

        // Simulate camera updates every 10 seconds
        setInterval(() => {
            this.simulateCameraUpdates();
        }, 10000);
    }

    simulateCameraUpdates() {
        const randomCamera = this.cameras[Math.floor(Math.random() * this.cameras.length)];
        
        if (Math.random() < 0.15) { // 15% chance of status change
            if (randomCamera.status === 'safe' && randomCamera.confidence < 25) {
                randomCamera.status = 'warning';
                randomCamera.confidence = Math.floor(Math.random() * 30) + 40;
                this.showNotification('Status Change', `${randomCamera.location} is now under monitoring`, 'warning');
            } else if (randomCamera.status === 'warning') {
                if (Math.random() < 0.3) {
                    randomCamera.status = 'fire';
                    randomCamera.confidence = Math.floor(Math.random() * 20) + 80;
                    this.stats.fireIncidentsToday++;
                    this.showNotification('FIRE DETECTED', `Emergency at ${randomCamera.location}`, 'danger');
                } else {
                    randomCamera.status = 'safe';
                    randomCamera.confidence = Math.floor(Math.random() * 20) + 5;
                    this.showNotification('All Clear', `${randomCamera.location} is now safe`, 'success');
                }
            }
            
            this.updateCameraFeedVisual(randomCamera.location, randomCamera.status);
            this.updateStats();
        }
    }

    showNotification(title, message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 max-w-sm transform translate-x-full transition-transform duration-300`;
        
        const bgColor = {
            'success': 'bg-green-600',
            'warning': 'bg-yellow-600',
            'danger': 'bg-red-600',
            'info': 'bg-blue-600'
        }[type] || 'bg-gray-600';
        
        notification.classList.add(bgColor);
        
        notification.innerHTML = `
            <div class="flex items-start">
                <div class="flex-1">
                    <h4 class="font-semibold text-white">${title}</h4>
                    <p class="text-sm text-gray-100 mt-1">${message}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.remove('translate-x-full'), 100);
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    showModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-gray-800 p-6 rounded-lg max-w-lg w-full mx-4 max-h-96 overflow-y-auto">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-semibold text-white">${title}</h3>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-white">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="text-gray-300">
                    ${content}
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
}

// Global functions
function closeEmergencyModal() {
    const modal = document.getElementById('emergencyModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// Initialize integrated dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔥 Starting Integrated Fire Detection Dashboard...');
    window.integratedDashboard = new IntegratedFireDetectionDashboard();
});
