// Progressive Fire Detection Dashboard with Automatic Safe/Fire Button Status
class ProgressiveStatusDashboard {
    constructor() {
        this.api = window.fireAPI;
        this.isConnected = false;
        this.currentVideoData = null;
        this.statusButtons = new Map();
        this.alertHistory = [];
        
        // Video monitoring data
        this.videos = [
            {
                id: 'video1',
                name: 'kitchen_fire_scenario_001.mp4',
                location: 'Block A - Kitchen Lab',
                status: 'safe',
                confidence: 5.2,
                buttonElement: null
            },
            {
                id: 'video2', 
                name: 'electrical_fire_scenario_002.mp4',
                location: 'Block B - Electrical Room',
                status: 'safe',
                confidence: 3.8,
                buttonElement: null
            }
        ];
        
        this.init();
    }

    async init() {
        console.log('🔥 Initializing Progressive Status Dashboard...');
        
        // Create status monitoring interface
        this.createStatusInterface();
        
        // Start real-time monitoring
        this.startProgressiveMonitoring();
        
        // Connect to backend API
        await this.connectToBackend();
        
        console.log('✅ Progressive Status Dashboard ready!');
    }

    createStatusInterface() {
        // Find the main content area or create it
        let mainContent = document.querySelector('.flex-1.p-6') || document.querySelector('main') || document.body;
        
        // Create the progressive status interface
        const statusInterface = document.createElement('div');
        statusInterface.id = 'progressive-status-interface';
        statusInterface.className = 'bg-gray-800 p-6 rounded-lg mb-6';
        
        statusInterface.innerHTML = `
            <div class="mb-6">
                <h2 class="text-2xl font-semibold text-white mb-4 flex items-center">
                    <i class="fas fa-video text-blue-500 mr-3"></i>
                    Progressive Fire Detection - Live Video Monitoring
                </h2>
                <div class="bg-gray-700 p-4 rounded-lg">
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
                        <div class="flex items-center">
                            <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                            <span class="text-gray-300">Safe Zone: 0% - 19%</span>
                        </div>
                        <div class="flex items-center">
                            <div class="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                            <span class="text-gray-300">Smoke Alert: 20% - 69%</span>
                        </div>
                        <div class="flex items-center">
                            <div class="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                            <span class="text-gray-300">Fire Emergency: 70% - 100%</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Live Video Status Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                ${this.videos.map(video => this.createVideoStatusCard(video)).join('')}
            </div>

            <!-- System Status Display -->
            <div class="bg-gray-700 p-6 rounded-lg">
                <h3 class="text-xl font-semibold text-white mb-4">System Status</h3>
                <div id="system-status-display" class="space-y-3">
                    <div class="flex items-center justify-between bg-gray-800 p-3 rounded">
                        <span class="text-gray-300">Backend Connection:</span>
                        <span id="backend-status" class="text-yellow-500">
                            <i class="fas fa-circle animate-pulse mr-1"></i>Connecting...
                        </span>
                    </div>
                    <div class="flex items-center justify-between bg-gray-800 p-3 rounded">
                        <span class="text-gray-300">Video Processing:</span>
                        <span id="video-processing-status" class="text-blue-500">
                            <i class="fas fa-play mr-1"></i>Active
                        </span>
                    </div>
                    <div class="flex items-center justify-between bg-gray-800 p-3 rounded">
                        <span class="text-gray-300">Emergency Response:</span>
                        <span id="emergency-status" class="text-green-500">
                            <i class="fas fa-shield-alt mr-1"></i>Ready
                        </span>
                    </div>
                </div>
            </div>

            <!-- Alert History -->
            <div class="mt-6 bg-gray-700 p-6 rounded-lg">
                <h3 class="text-xl font-semibold text-white mb-4">Recent Alerts</h3>
                <div id="alert-history" class="space-y-2">
                    <div class="text-gray-400 text-center py-4">No alerts yet - monitoring in progress...</div>
                </div>
            </div>
        `;

        // Insert the interface at the beginning of main content
        if (mainContent.children.length > 0) {
            mainContent.insertBefore(statusInterface, mainContent.firstChild);
        } else {
            mainContent.appendChild(statusInterface);
        }

        // Store button references
        this.videos.forEach(video => {
            video.buttonElement = document.getElementById(`status-btn-${video.id}`);
        });
    }

    createVideoStatusCard(video) {
        return `
            <div class="bg-gray-900 border border-gray-600 rounded-lg overflow-hidden" id="card-${video.id}">
                <!-- Video Preview Area -->
                <div class="h-48 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center relative">
                    <div class="text-center">
                        <i id="video-icon-${video.id}" class="fas fa-shield-alt text-green-500 text-4xl mb-2"></i>
                        <p id="video-status-text-${video.id}" class="text-green-500 font-bold">SAFE ZONE</p>
                        <p class="text-gray-400 text-sm mt-1">${video.name}</p>
                    </div>
                    
                    <!-- Confidence Level Indicator -->
                    <div class="absolute top-3 right-3 bg-black bg-opacity-70 px-2 py-1 rounded">
                        <span id="confidence-${video.id}" class="text-green-400 text-sm font-bold">${video.confidence}%</span>
                    </div>
                    
                    <!-- Time in Video Indicator -->
                    <div class="absolute bottom-3 left-3 bg-black bg-opacity-70 px-2 py-1 rounded">
                        <span id="video-time-${video.id}" class="text-gray-300 text-xs">00:00:00</span>
                    </div>
                </div>

                <!-- Video Information -->
                <div class="p-4">
                    <h4 class="text-white font-semibold mb-2">${video.location}</h4>
                    <div class="space-y-3">
                        <!-- Status Information -->
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-gray-400">Detection Stage:</span>
                            <span id="detection-stage-${video.id}" class="text-green-500 font-semibold">Safe Zone</span>
                        </div>
                        
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-gray-400">Fire Scenario:</span>
                            <span id="fire-scenario-${video.id}" class="text-gray-300">Monitoring</span>
                        </div>

                        <!-- Confidence Progress Bar -->
                        <div class="space-y-1">
                            <div class="flex justify-between text-xs">
                                <span class="text-gray-400">Confidence Level</span>
                                <span id="confidence-text-${video.id}" class="text-gray-300">${video.confidence}%</span>
                            </div>
                            <div class="w-full bg-gray-700 rounded-full h-2">
                                <div id="confidence-bar-${video.id}" 
                                     class="bg-green-500 h-2 rounded-full transition-all duration-300" 
                                     style="width: ${Math.min(video.confidence, 100)}%"></div>
                            </div>
                        </div>

                        <!-- Status Action Button -->
                        <button id="status-btn-${video.id}" 
                                class="w-full mt-4 px-4 py-3 rounded-lg font-semibold transition-all duration-300 flex items-center justify-center space-x-2 bg-green-600 hover:bg-green-700 text-white"
                                onclick="window.progressiveDashboard.handleStatusButtonClick('${video.id}')">
                            <i class="fas fa-shield-alt"></i>
                            <span>SAFE - No Action Required</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    async connectToBackend() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/confidence-live/');
            if (response.ok) {
                this.isConnected = true;
                this.updateConnectionStatus('connected');
                console.log('✅ Connected to Progressive Fire Detection backend');
            } else {
                throw new Error('Backend not responding');
            }
        } catch (error) {
            console.warn('⚠️ Backend connection failed, using simulation mode');
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
        }
    }

    updateConnectionStatus(status) {
        const statusElement = document.getElementById('backend-status');
        if (statusElement) {
            switch(status) {
                case 'connected':
                    statusElement.innerHTML = '<i class="fas fa-circle text-green-500 mr-1"></i>Connected';
                    statusElement.className = 'text-green-500';
                    break;
                case 'disconnected':
                    statusElement.innerHTML = '<i class="fas fa-circle text-red-500 mr-1"></i>Disconnected - Simulation Mode';
                    statusElement.className = 'text-red-500';
                    break;
                case 'connecting':
                    statusElement.innerHTML = '<i class="fas fa-circle animate-pulse text-yellow-500 mr-1"></i>Connecting...';
                    statusElement.className = 'text-yellow-500';
                    break;
            }
        }
    }

    startProgressiveMonitoring() {
        console.log('🔄 Starting progressive fire detection monitoring...');
        
        // Update every 3 seconds
        setInterval(async () => {
            if (this.isConnected) {
                await this.fetchLiveData();
            } else {
                this.simulateProgressiveDetection();
            }
        }, 3000);
    }

    async fetchLiveData() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/confidence-live/');
            if (response.ok) {
                const data = await response.json();
                this.currentVideoData = data;
                this.updateVideoDisplay(data);
            } else {
                console.warn('Failed to fetch live data, switching to simulation');
                this.isConnected = false;
                this.updateConnectionStatus('disconnected');
            }
        } catch (error) {
            console.error('Error fetching live data:', error);
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
        }
    }

    simulateProgressiveDetection() {
        // Simulate progressive fire detection for demo purposes
        const currentTime = Date.now();
        
        this.videos.forEach(video => {
            // Simulate different fire progression scenarios
            let confidence, stage, scenario;
            
            if (video.id === 'video1') {
                // Kitchen fire scenario
                const elapsed = (currentTime % 900000) / 1000; // 15-minute cycle
                if (elapsed < 120) {
                    confidence = 5 + Math.random() * 10;
                    stage = 'safe';
                    scenario = 'kitchen_fire';
                } else if (elapsed < 180) {
                    confidence = 20 + Math.random() * 20;
                    stage = 'smoke_detected';
                    scenario = 'kitchen_fire';
                } else if (elapsed < 240) {
                    confidence = 45 + Math.random() * 20;
                    stage = 'fire_development';
                    scenario = 'kitchen_fire';
                } else if (elapsed < 300) {
                    confidence = 70 + Math.random() * 15;
                    stage = 'fire_emergency';
                    scenario = 'kitchen_fire';
                } else {
                    confidence = 80 + Math.random() * 15;
                    stage = 'fire_emergency';
                    scenario = 'kitchen_fire';
                }
            } else {
                // Electrical fire scenario
                const elapsed = (currentTime % 1260000) / 1000; // 21-minute cycle
                if (elapsed < 180) {
                    confidence = 2 + Math.random() * 8;
                    stage = 'safe';
                    scenario = 'electrical_fire';
                } else if (elapsed < 300) {
                    confidence = 15 + Math.random() * 20;
                    stage = 'smoke_detected';
                    scenario = 'electrical_fire';
                } else if (elapsed < 360) {
                    confidence = 40 + Math.random() * 25;
                    stage = 'fire_development';
                    scenario = 'electrical_fire';
                } else {
                    confidence = 70 + Math.random() * 20;
                    stage = 'fire_emergency';
                    scenario = 'electrical_fire';
                }
            }

            const simulatedData = {
                video_name: video.name,
                confidence: confidence,
                detection_stage: stage,
                fire_scenario: scenario,
                time_in_video: this.formatElapsedTime(elapsed || 0),
                timestamp: new Date().toISOString()
            };

            this.updateVideoDisplay(simulatedData, video.id);
        });
    }

    updateVideoDisplay(data, targetVideoId = null) {
        // If targetVideoId is specified, update only that video
        let videosToUpdate = targetVideoId ? 
            this.videos.filter(v => v.id === targetVideoId) : 
            this.videos.filter(v => v.name === data.video_name);

        if (videosToUpdate.length === 0 && !targetVideoId) {
            // If no matching video found, update the first one
            videosToUpdate = [this.videos[0]];
        }

        videosToUpdate.forEach(video => {
            const confidence = Math.round(data.confidence * 10) / 10;
            const stage = data.detection_stage;
            const scenario = data.fire_scenario;
            
            // Update confidence display
            this.updateConfidenceDisplay(video.id, confidence);
            
            // Update status based on detection stage
            this.updateStatusDisplay(video.id, stage, confidence);
            
            // Update scenario and time
            this.updateScenarioDisplay(video.id, scenario, data.time_in_video);
            
            // Update status button automatically
            this.updateStatusButton(video.id, stage, confidence);
            
            // Check for alert triggers
            this.checkAlertTriggers(video, stage, confidence);
        });
    }

    updateConfidenceDisplay(videoId, confidence) {
        const confidenceElement = document.getElementById(`confidence-${videoId}`);
        const confidenceTextElement = document.getElementById(`confidence-text-${videoId}`);
        const confidenceBarElement = document.getElementById(`confidence-bar-${videoId}`);
        
        if (confidenceElement) confidenceElement.textContent = `${confidence}%`;
        if (confidenceTextElement) confidenceTextElement.textContent = `${confidence}%`;
        
        if (confidenceBarElement) {
            confidenceBarElement.style.width = `${Math.min(confidence, 100)}%`;
            
            // Update bar color based on confidence level
            if (confidence < 20) {
                confidenceBarElement.className = 'bg-green-500 h-2 rounded-full transition-all duration-300';
                confidenceElement.className = 'text-green-400 text-sm font-bold';
            } else if (confidence < 70) {
                confidenceBarElement.className = 'bg-yellow-500 h-2 rounded-full transition-all duration-300';
                confidenceElement.className = 'text-yellow-400 text-sm font-bold';
            } else {
                confidenceBarElement.className = 'bg-red-500 h-2 rounded-full transition-all duration-300';
                confidenceElement.className = 'text-red-400 text-sm font-bold';
            }
        }
    }

    updateStatusDisplay(videoId, stage, confidence) {
        const iconElement = document.getElementById(`video-icon-${videoId}`);
        const textElement = document.getElementById(`video-status-text-${videoId}`);
        const stageElement = document.getElementById(`detection-stage-${videoId}`);
        
        switch(stage) {
            case 'safe':
                if (iconElement) {
                    iconElement.className = 'fas fa-shield-alt text-green-500 text-4xl mb-2';
                }
                if (textElement) {
                    textElement.textContent = 'SAFE ZONE';
                    textElement.className = 'text-green-500 font-bold';
                }
                if (stageElement) {
                    stageElement.textContent = 'Safe Zone';
                    stageElement.className = 'text-green-500 font-semibold';
                }
                break;
                
            case 'smoke_detected':
                if (iconElement) {
                    iconElement.className = 'fas fa-cloud text-yellow-500 text-4xl mb-2';
                }
                if (textElement) {
                    textElement.textContent = 'SMOKE DETECTED';
                    textElement.className = 'text-yellow-500 font-bold';
                }
                if (stageElement) {
                    stageElement.textContent = 'Smoke Alert';
                    stageElement.className = 'text-yellow-500 font-semibold';
                }
                break;
                
            case 'fire_development':
                if (iconElement) {
                    iconElement.className = 'fas fa-exclamation-triangle text-orange-500 text-4xl mb-2';
                }
                if (textElement) {
                    textElement.textContent = 'FIRE DEVELOPING';
                    textElement.className = 'text-orange-500 font-bold';
                }
                if (stageElement) {
                    stageElement.textContent = 'Fire Development';
                    stageElement.className = 'text-orange-500 font-semibold';
                }
                break;
                
            case 'fire_emergency':
                if (iconElement) {
                    iconElement.className = 'fas fa-fire text-red-500 text-4xl mb-2 animate-pulse';
                }
                if (textElement) {
                    textElement.textContent = 'FIRE EMERGENCY';
                    textElement.className = 'text-red-500 font-bold animate-pulse';
                }
                if (stageElement) {
                    stageElement.textContent = 'Fire Emergency';
                    stageElement.className = 'text-red-500 font-semibold animate-pulse';
                }
                break;
        }
    }

    updateScenarioDisplay(videoId, scenario, timeInVideo) {
        const scenarioElement = document.getElementById(`fire-scenario-${videoId}`);
        const timeElement = document.getElementById(`video-time-${videoId}`);
        
        if (scenarioElement) {
            const scenarioText = {
                'kitchen_fire': 'Kitchen Fire',
                'electrical_fire': 'Electrical Fire',
                'monitoring': 'Monitoring'
            }[scenario] || 'Unknown';
            scenarioElement.textContent = scenarioText;
        }
        
        if (timeElement && timeInVideo) {
            timeElement.textContent = timeInVideo;
        }
    }

    updateStatusButton(videoId, stage, confidence) {
        const button = document.getElementById(`status-btn-${videoId}`);
        if (!button) return;

        const video = this.videos.find(v => v.id === videoId);
        if (!video) return;

        // Update button based on detection stage
        switch(stage) {
            case 'safe':
                button.className = 'w-full mt-4 px-4 py-3 rounded-lg font-semibold transition-all duration-300 flex items-center justify-center space-x-2 bg-green-600 hover:bg-green-700 text-white';
                button.innerHTML = `
                    <i class="fas fa-shield-alt"></i>
                    <span>SAFE - No Action Required</span>
                `;
                video.status = 'safe';
                break;
                
            case 'smoke_detected':
                button.className = 'w-full mt-4 px-4 py-3 rounded-lg font-semibold transition-all duration-300 flex items-center justify-center space-x-2 bg-yellow-600 hover:bg-yellow-700 text-white animate-pulse';
                button.innerHTML = `
                    <i class="fas fa-cloud"></i>
                    <span>SMOKE ALERT - Investigation Required</span>
                `;
                video.status = 'smoke_alert';
                break;
                
            case 'fire_development':
                button.className = 'w-full mt-4 px-4 py-3 rounded-lg font-semibold transition-all duration-300 flex items-center justify-center space-x-2 bg-orange-600 hover:bg-orange-700 text-white animate-pulse';
                button.innerHTML = `
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>FIRE DEVELOPING - Prepare Response</span>
                `;
                video.status = 'fire_development';
                break;
                
            case 'fire_emergency':
                button.className = 'w-full mt-4 px-4 py-3 rounded-lg font-semibold transition-all duration-300 flex items-center justify-center space-x-2 bg-red-600 hover:bg-red-700 text-white animate-pulse';
                button.innerHTML = `
                    <i class="fas fa-fire"></i>
                    <span>FIRE ACCIDENT - Emergency Response Active</span>
                `;
                video.status = 'fire_accident';
                break;
        }
    }

    checkAlertTriggers(video, stage, confidence) {
        const lastAlert = this.alertHistory[this.alertHistory.length - 1];
        const currentTime = Date.now();
        
        // Avoid duplicate alerts within 30 seconds
        if (lastAlert && (currentTime - lastAlert.timestamp) < 30000 && 
            lastAlert.videoId === video.id && lastAlert.stage === stage) {
            return;
        }
        
        let alertTriggered = false;
        let alertType = '';
        let alertMessage = '';
        
        if (stage === 'smoke_detected' && confidence >= 20) {
            alertType = 'smoke_alert';
            alertMessage = `💨 Smoke detected in ${video.location} (${confidence}% confidence)`;
            alertTriggered = true;
        } else if (stage === 'fire_emergency' && confidence >= 70) {
            alertType = 'fire_emergency';
            alertMessage = `🔥 FIRE EMERGENCY in ${video.location} (${confidence}% confidence)`;
            alertTriggered = true;
        }
        
        if (alertTriggered) {
            const alert = {
                videoId: video.id,
                location: video.location,
                stage: stage,
                confidence: confidence,
                message: alertMessage,
                type: alertType,
                timestamp: currentTime
            };
            
            this.alertHistory.push(alert);
            this.displayAlert(alert);
            
            // Update emergency status
            if (alertType === 'fire_emergency') {
                const emergencyStatus = document.getElementById('emergency-status');
                if (emergencyStatus) {
                    emergencyStatus.innerHTML = '<i class="fas fa-exclamation-triangle text-red-500 mr-1"></i>EMERGENCY ACTIVE';
                    emergencyStatus.className = 'text-red-500 animate-pulse';
                }
            }
            
            console.log(`🚨 ALERT TRIGGERED: ${alertMessage}`);
        }
    }

    displayAlert(alert) {
        const alertHistory = document.getElementById('alert-history');
        if (!alertHistory) return;
        
        // Remove "no alerts" message if present
        const noAlerts = alertHistory.querySelector('.text-gray-400');
        if (noAlerts) noAlerts.remove();
        
        const alertElement = document.createElement('div');
        alertElement.className = `p-3 rounded-lg border-l-4 ${
            alert.type === 'fire_emergency' ? 'bg-red-900 border-red-500' : 'bg-yellow-900 border-yellow-500'
        } animate-pulse`;
        
        alertElement.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <p class="font-semibold ${alert.type === 'fire_emergency' ? 'text-red-400' : 'text-yellow-400'}">
                        ${alert.message}
                    </p>
                    <p class="text-sm text-gray-400 mt-1">
                        ${new Date(alert.timestamp).toLocaleString()}
                    </p>
                </div>
                <span class="px-2 py-1 rounded text-xs font-bold ${
                    alert.type === 'fire_emergency' ? 'bg-red-600' : 'bg-yellow-600'
                }">
                    ${alert.type.toUpperCase().replace('_', ' ')}
                </span>
            </div>
        `;
        
        // Insert at the beginning of alert history
        alertHistory.insertBefore(alertElement, alertHistory.firstChild);
        
        // Remove animation after 3 seconds
        setTimeout(() => {
            alertElement.classList.remove('animate-pulse');
        }, 3000);
        
        // Keep only last 10 alerts in the display
        const alerts = alertHistory.querySelectorAll('.p-3.rounded-lg');
        if (alerts.length > 10) {
            alerts[alerts.length - 1].remove();
        }
    }

    handleStatusButtonClick(videoId) {
        const video = this.videos.find(v => v.id === videoId);
        if (!video) return;
        
        const button = document.getElementById(`status-btn-${videoId}`);
        if (!button) return;
        
        // Provide user feedback based on current status
        switch(video.status) {
            case 'safe':
                this.showNotification('Safe Status', `${video.location} is in safe zone. Continue monitoring.`, 'info');
                break;
            case 'smoke_alert':
                this.showNotification('Smoke Alert', `Investigation required at ${video.location}. Check for smoke sources.`, 'warning');
                break;
            case 'fire_development':
                this.showNotification('Fire Development', `Fire developing at ${video.location}. Prepare emergency response.`, 'warning');
                break;
            case 'fire_accident':
                this.showNotification('Fire Emergency', `Emergency response active for ${video.location}. Evacuate immediately!`, 'danger');
                break;
        }
    }

    showNotification(title, message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 max-w-sm transform translate-x-full transition-transform duration-300`;
        
        const bgColor = {
            'info': 'bg-blue-600',
            'warning': 'bg-yellow-600', 
            'danger': 'bg-red-600',
            'success': 'bg-green-600'
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
        }, 8000);
    }

    formatElapsedTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
}

// Initialize the progressive status dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔥 Starting Progressive Status Dashboard...');
    window.progressiveDashboard = new ProgressiveStatusDashboard();
});
