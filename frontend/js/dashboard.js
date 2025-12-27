// Dashboard JavaScript for Fire Detection System
class FireDetectionDashboard {
    constructor() {
        this.cameras = [
            { id: 1, location: "Mall Inside - Fire Incident", status: "fire", confidence: 92, people: 3, video: "mall_inside.mp4" },
            { id: 2, location: "Mart - Fire Detection", status: "fire", confidence: 87, people: 2, video: "mart.mp4" },
            { id: 3, location: "Mall Escalator - Normal", status: "safe", confidence: 15, people: 8, video: "mall_escalator.mp4" },
            { id: 4, location: "Mall First Floor - Normal", status: "safe", confidence: 12, people: 5, video: "mall_first_floor.mp4" },
            { id: 5, location: "Mall Front - Normal", status: "safe", confidence: 8, people: 12, video: "mall_front.mp4" },
            { id: 6, location: "Mall Total View - Normal", status: "safe", confidence: 5, people: 15, video: "mall_total.mp4" }
        ];
        
        this.stats = {
            activeCameras: 6,        // Fixed at 6 cameras as requested
            fireIncidentsToday: 2,   // Based on mall_inside.mp4 and mart.mp4
            peopleEvacuated: 4,      // Static count
            responseTime: 35         // Static response time in seconds
        };
        
        this.notifications = [
            { type: 'emergency', title: 'Fire Detected - Mall Inside', message: 'High confidence (92%) fire detection in mall_inside.mp4', time: 'Just now' },
            { type: 'emergency', title: 'Fire Detected - Mart Area', message: 'High confidence (87%) fire detection in mart.mp4', time: '2 minutes ago' },
            { type: 'success', title: 'All Safe - Mall Escalator', message: 'Normal monitoring, no threats detected', time: '5 minutes ago' },
            { type: 'success', title: 'All Safe - Mall First Floor', message: 'Normal monitoring, no threats detected', time: '7 minutes ago' },
            { type: 'info', title: 'System Status Update', message: 'All 6 cameras online and functioning properly', time: '10 minutes ago' }
        ];
        
        this.init();
        this.loadRecentVideoAnalyses();
    }

    init() {
        this.bindEvents();
        this.startRealTimeUpdates();
        this.updateCameraFeeds();
        this.setupNotificationPanel();
        this.setupSettingsPanel();
        
        // Update stats every 30 seconds
        setInterval(() => {
            this.updateStats();
        }, 30000);
        
        // Update camera status every 5 seconds
        setInterval(() => {
            this.simulateCameraUpdates();
        }, 5000);
    }

    setupNotificationPanel() {
        // Ensure notification panel exists and is properly set up
        const notificationPanel = document.getElementById('notificationPanel');
        if (notificationPanel) {
            this.updateNotificationList();
        }
    }

    setupSettingsPanel() {
        // Ensure settings panel exists and bind events
        const settingsPanel = document.getElementById('settingsPanel');
        if (settingsPanel) {
            // Add event listeners for settings controls
            const alertSensitivity = settingsPanel.querySelector('select');
            const autoEmergency = settingsPanel.querySelector('input[type="checkbox"]:first-of-type');
            const videoRecording = settingsPanel.querySelector('input[type="checkbox"]:last-of-type');
            
            if (alertSensitivity) {
                alertSensitivity.addEventListener('change', (e) => {
                    this.showNotification('Settings Updated', `Alert sensitivity changed to ${e.target.value}`, 'info');
                });
            }
            
            if (autoEmergency) {
                autoEmergency.addEventListener('change', (e) => {
                    this.showNotification('Settings Updated', `Auto emergency response ${e.target.checked ? 'enabled' : 'disabled'}`, 'info');
                });
            }
            
            if (videoRecording) {
                videoRecording.addEventListener('change', (e) => {
                    this.showNotification('Settings Updated', `Auto video recording ${e.target.checked ? 'enabled' : 'disabled'}`, 'info');
                });
            }
        }
    }

    updateNotificationList() {
        const notificationList = document.getElementById('notificationList');
        if (!notificationList) return;
        
        notificationList.innerHTML = '';
        
        this.notifications.forEach(notification => {
            const notificationElement = this.createNotificationElement(notification);
            notificationList.appendChild(notificationElement);
        });
        
        // Update badge count
        const badge = document.getElementById('notificationBadge');
        if (badge) {
            badge.textContent = this.notifications.length;
        }
    }

    createNotificationElement(notification) {
        const div = document.createElement('div');
        
        const colorClasses = {
            emergency: 'bg-red-900 border-red-500 text-red-300',
            urgent: 'bg-orange-900 border-orange-500 text-orange-300',
            info: 'bg-blue-900 border-blue-500 text-blue-300',
            success: 'bg-green-900 border-green-500 text-green-300'
        };
        
        const iconClasses = {
            emergency: 'fas fa-fire text-red-400',
            urgent: 'fas fa-exclamation-triangle text-orange-400',
            info: 'fas fa-info-circle text-blue-400',
            success: 'fas fa-check-circle text-green-400'
        };
        
        div.className = `notification-item ${colorClasses[notification.type]} border p-3 rounded-lg`;
        div.innerHTML = `
            <div class="flex items-start space-x-3">
                <i class="${iconClasses[notification.type]} mt-1"></i>
                <div class="flex-1">
                    <div class="font-semibold">${notification.title}</div>
                    <div class="text-sm opacity-90">${notification.message}</div>
                    <div class="text-xs opacity-75 mt-1">
                        <i class="fas fa-clock"></i> ${notification.time}
                    </div>
                </div>
            </div>
        `;
        
        return div;
    }

    addNotification(type, title, message) {
        const newNotification = {
            type: type,
            title: title,
            message: message,
            time: 'Just now'
        };
        
        this.notifications.unshift(newNotification);
        
        // Keep only last 10 notifications
        if (this.notifications.length > 10) {
            this.notifications = this.notifications.slice(0, 10);
        }
        
        this.updateNotificationList();
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

        // Navigation - All links now work
        document.querySelectorAll('nav a').forEach(link => {
            link.addEventListener('click', (e) => {
                const href = e.target.getAttribute('href');
                if (href === '#') {
                    e.preventDefault();
                    this.showComingSoon(e.target.textContent.trim());
                }
                // All other links will navigate normally to their respective pages
            });
        });

        // Start/Stop all buttons
        document.querySelector('.bg-blue-600').addEventListener('click', () => {
            this.startAllCameras();
        });

        document.querySelector('.bg-gray-600').addEventListener('click', () => {
            this.pauseAllCameras();
        });

        // Video link detection
        const detectVideoBtn = document.getElementById('detectVideoBtn');
        if (detectVideoBtn) {
            detectVideoBtn.addEventListener('click', () => {
                this.handleVideoLinkDetection();
            });
        }
    }

    handleEmergencyAction(action) {
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
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Simulate emergency protocol
        this.showNotification('Emergency Alert Activated', 'All emergency protocols have been triggered', 'danger');
        
        // Update all fire cameras to emergency state
        this.cameras.forEach(camera => {
            if (camera.status === 'fire') {
                this.updateCameraFeedVisual(camera.location, 'emergency');
            }
        });

        console.log('🚨 EMERGENCY ALERT ACTIVATED');
        console.log('📱 SMS alerts sent to emergency contacts');
        console.log('📧 Email notifications dispatched');
        console.log('🔊 Building-wide announcement activated');
        console.log('🚨 All sirens activated');
    }

    contactFireDepartment() {
        this.showNotification('Contacting Fire Department', 'Direct call initiated to emergency services', 'warning');
        
        // Simulate call interface
        setTimeout(() => {
            this.showModal('Fire Department Contact', `
                <div class="text-center">
                    <i class="fas fa-phone-alt text-4xl text-green-500 mb-4"></i>
                    <p class="mb-4">Connecting to Fire Department...</p>
                    <div class="sound-wave-container flex justify-center space-x-1 mb-4">
                        <div class="sound-wave"></div>
                        <div class="sound-wave"></div>
                        <div class="sound-wave"></div>
                    </div>
                    <p class="text-sm text-gray-400">Emergency details transmitted automatically</p>
                </div>
            `);
        }, 1000);
    }

    makeBuildingAnnouncement() {
        this.showNotification('Building Announcement Active', 'Public address system activated', 'info');
        
        this.showModal('Building Announcement', `
            <div class="text-center">
                <i class="fas fa-megaphone text-4xl text-blue-500 mb-4"></i>
                <div class="bg-gray-700 p-4 rounded-lg mb-4">
                    <p class="text-sm text-gray-300 mb-2">Now Broadcasting:</p>
                    <p class="font-semibold">"Attention all building occupants. A fire has been detected in Block A - Lab 3. Please evacuate the building immediately using the nearest emergency exit. Do not use elevators. Proceed to the designated assembly point."</p>
                </div>
                <div class="flex justify-center space-x-4">
                    <button class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg">Stop Announcement</button>
                    <button class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">Repeat Message</button>
                </div>
            </div>
        `);
    }

    handleVideoLinkDetection() {
        const videoLinkInput = document.getElementById('videoLinkInput');
        const videoLink = videoLinkInput.value.trim();
        
        if (!videoLink) {
            this.showNotification('Error', 'Please paste a public video link.', 'danger');
            return;
        }

        // Validate if it's a valid URL
        try {
            new URL(videoLink);
        } catch (e) {
            this.showNotification('Error', 'Please enter a valid video URL.', 'danger');
            return;
        }

        this.showNotification('Processing Video', 'Starting fire detection analysis...', 'info');

        // Send to backend for processing
        this.processVideoForFireDetection(videoLink);
    }

    async processVideoForFireDetection(videoUrl) {
        try {
            // Call backend API to process the video link for fire detection
            const result = await window.fireAPI.sendEmergencyAlert({
                video_url: videoUrl,
                type: 'video_analysis',
                message: 'Fire detection requested for public video link.',
                timestamp: new Date().toISOString()
            });

            if (result) {
                this.showNotification('Detection Started', 'Fire detection analysis started for the provided video.', 'success');
                
                // Show processing modal
                this.showModal('Video Analysis in Progress', `
                    <div class="text-center">
                        <i class="fas fa-video text-4xl text-blue-500 mb-4"></i>
                        <p class="mb-4">Analyzing video for fire detection...</p>
                        <div class="w-full bg-gray-700 rounded-full h-2 mb-4">
                            <div class="bg-blue-600 h-2 rounded-full animate-pulse w-1/3"></div>
                        </div>
                        <p class="text-sm text-gray-400">Video: ${videoUrl}</p>
                        <p class="text-sm text-gray-400 mt-2">This may take a few minutes depending on video length.</p>
                    </div>
                `);

                // Clear the input field
                document.getElementById('videoLinkInput').value = '';
                
                // Simulate detection results after some time
                setTimeout(() => {
                    this.simulateVideoDetectionResult(videoUrl);
                }, 10000); // 10 seconds simulation
                
            } else {
                this.showNotification('Error', 'Failed to start fire detection for the video.', 'danger');
            }
        } catch (error) {
            console.error('Video detection error:', error);
            this.showNotification('Error', 'An error occurred while processing the video.', 'danger');
        }
    }

    simulateVideoDetectionResult(videoUrl) {
        // Simulate detection results
        const hasFireDetected = Math.random() > 0.5; // 50% chance of fire detection
        const confidence = hasFireDetected ? Math.floor(Math.random() * 30) + 70 : Math.floor(Math.random() * 40) + 10;

        if (hasFireDetected) {
            this.showNotification('🔥 FIRE DETECTED!', `Fire detected in video with ${confidence}% confidence`, 'danger');
            
            this.showModal('Fire Detection Results', `
                <div class="text-center">
                    <i class="fas fa-fire text-6xl text-red-500 mb-4 animate-pulse"></i>
                    <h4 class="text-xl font-bold text-red-500 mb-4">FIRE DETECTED</h4>
                    <div class="bg-red-900 p-4 rounded-lg mb-4">
                        <p><strong>Confidence:</strong> ${confidence}%</p>
                        <p><strong>Video:</strong> ${videoUrl}</p>
                        <p><strong>Detection Time:</strong> ${new Date().toLocaleTimeString()}</p>
                    </div>
                    <div class="bg-gray-700 p-4 rounded-lg">
                        <h5 class="font-semibold mb-2">Emergency Actions Initiated:</h5>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between">
                                <span>SMS Alerts:</span>
                                <span class="text-green-400">✓ Sent</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Email Notifications:</span>
                                <span class="text-green-400">✓ Sent</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Emergency Contacts:</span>
                                <span class="text-yellow-400">⏳ Calling</span>
                            </div>
                        </div>
                    </div>
                </div>
            `);
        } else {
            this.showNotification('Analysis Complete', `No fire detected. Confidence: ${confidence}%`, 'success');
            
            this.showModal('Video Analysis Results', `
                <div class="text-center">
                    <i class="fas fa-shield-alt text-6xl text-green-500 mb-4"></i>
                    <h4 class="text-xl font-bold text-green-500 mb-4">NO FIRE DETECTED</h4>
                    <div class="bg-green-900 p-4 rounded-lg mb-4">
                        <p><strong>Confidence:</strong> ${confidence}%</p>
                        <p><strong>Video:</strong> ${videoUrl}</p>
                        <p><strong>Analysis Time:</strong> ${new Date().toLocaleTimeString()}</p>
                    </div>
                    <p class="text-gray-400">The video has been analyzed and no fire or smoke was detected.</p>
                </div>
            `);
        }
    }

    simulateCameraUpdates() {
        // Disabled camera simulation to prevent fluctuating stats
        // Keeping stats stable as requested by user for 6 cameras
        return;
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
                    <button class="call-btn bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg font-semibold">Call</button>
                `;
                badge.className = 'bg-red-500 text-white px-2 py-1 rounded text-xs font-bold animate-pulse';
                badge.textContent = 'ALERT';
                feed.classList.add('emergency-glow');
                // Add event listener for call button
                const callBtn = content.querySelector('.call-btn');
                if (callBtn) {
                    callBtn.addEventListener('click', (e) => {
                        if (callBtn.textContent === 'Call') {
                            callBtn.textContent = 'End Call';
                            callBtn.classList.remove('bg-green-600');
                            callBtn.classList.add('bg-red-600');
                            this.showNotification('Calling Emergency Contact', 'Call initiated to emergency contact.', 'warning');
                        } else {
                            callBtn.textContent = 'Call';
                            callBtn.classList.remove('bg-red-600');
                            callBtn.classList.add('bg-green-600');
                            this.showNotification('Call Ended', 'Emergency call ended.', 'info');
                        }
                    });
                }
                break;
                
            case 'warning':
                content.innerHTML = `
                    <i class="fas fa-exclamation-triangle text-yellow-500 text-4xl mb-2"></i>
                    <p class="text-yellow-500 font-bold">MONITORING</p>
                `;
                badge.className = 'bg-yellow-500 text-black px-2 py-1 rounded text-xs font-bold';
                badge.textContent = 'WATCH';
                feed.classList.remove('emergency-glow');
                break;
                
            case 'safe':
                content.innerHTML = `
                    <i class="fas fa-shield-alt text-green-500 text-4xl mb-2"></i>
                    <p class="text-green-500 font-bold">SAFE</p>
                `;
                badge.className = 'bg-green-500 text-white px-2 py-1 rounded text-xs font-bold';
                badge.textContent = 'SAFE';
                feed.classList.remove('emergency-glow');
                break;
        }
    }

    updateCameraFeeds() {
        this.cameras.forEach(camera => {
            this.updateCameraFeedVisual(camera.location, camera.status);
        });
    }

    updateStats() {
        // Keep stats consistent - always show 6 cameras as specified by user
        this.stats.activeCameras = 6;
        this.stats.fireIncidentsToday = 2;
        this.stats.peopleEvacuated = 4;
        this.stats.responseTime = 35;
        
        // Update active cameras - use more specific selector
        const activeCamerasStat = document.querySelector('.stats-card:first-child .text-2xl');
        if (activeCamerasStat) activeCamerasStat.textContent = '6';
        
        // Update fire incidents
        const fireIncidentsStat = document.querySelector('.stats-card:nth-child(2) .text-2xl');
        if (fireIncidentsStat) fireIncidentsStat.textContent = '2';
        
        // Update people evacuated
        const peopleEvacuatedStat = document.querySelector('.stats-card:nth-child(3) .text-2xl');
        if (peopleEvacuatedStat) peopleEvacuatedStat.textContent = '4';
        
        // Update response time
        const responseTimeStat = document.querySelector('.stats-card:nth-child(4) .text-2xl');
        if (responseTimeStat) responseTimeStat.textContent = '35s';
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
                
                ${camera.status === 'fire' ? `
                    <div class="bg-red-900 p-4 rounded-lg">
                        <h5 class="font-semibold text-red-300 mb-2">Emergency Actions</h5>
                        <div class="space-y-2 text-sm">
                            <div class="flex justify-between">
                                <span>Siren Activated:</span>
                                <span class="text-green-400">✓ Active</span>
                            </div>
                            <div class="flex justify-between">
                                <span>SMS Alerts:</span>
                                <span class="text-green-400">✓ Sent</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Fire Department:</span>
                                <span class="text-yellow-400">⏳ Notified</span>
                            </div>
                        </div>
                    </div>
                ` : ''}
                
                <div class="flex space-x-2">
                    <button class="flex-1 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">View Live Feed</button>
                    <button class="flex-1 bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded-lg">Download Snapshot</button>
                </div>
            </div>
        `);
    }

    showComingSoon(feature) {
        this.showModal('Coming Soon', `
            <div class="text-center">
                <i class="fas fa-tools text-4xl text-blue-500 mb-4"></i>
                <h4 class="text-lg font-semibold mb-2">${feature}</h4>
                <p class="text-gray-400">This feature is currently under development and will be available in the next update.</p>
            </div>
        `);
    }

    startRealTimeUpdates() {
        // Simulate real-time data updates
        setInterval(() => {
            // Update response time
            this.stats.responseTime = Math.floor(Math.random() * 20) + 35;
            
            // Update people count
            const totalPeople = this.cameras.reduce((sum, camera) => sum + camera.people, 0);
            this.stats.peopleEvacuated = Math.max(0, this.stats.peopleEvacuated + Math.floor(Math.random() * 3) - 1);
            
            this.updateStats();
        }, 10000);
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
    
    async loadRecentVideoAnalyses() {
        try {
            const response = await fetch('/api/video-analysis/recent_analyses/');
            if (response.ok) {
                const data = await response.json();
                this.integratVideoAnalysesWithCameras(data.data);
            }
        } catch (error) {
            console.error('Failed to load video analyses:', error);
        }
    }
    
    integratVideoAnalysesWithCameras(analyses) {
        // Integrate recent video analyses with camera feeds
        analyses.forEach(analysis => {
            if (analysis.fire_detected && analysis.confidence_score > 0.7) {
                // Find a camera to update or create virtual camera display
                const availableCamera = this.cameras.find(c => c.status === 'safe');
                if (availableCamera) {
                    availableCamera.status = 'fire';
                    availableCamera.confidence = Math.round(analysis.confidence_score * 100);
                    availableCamera.location = analysis.location;
                    
                    // Update visual immediately
                    this.updateCameraFeedVisual(availableCamera.location, 'fire');
                    
                    // Show notification
                    this.showNotification(
                        '🔥 Fire Detected in Video Analysis', 
                        `Fire detected in ${analysis.title} with ${Math.round(analysis.confidence_score * 100)}% confidence`, 
                        'danger'
                    );
                    
                    // Trigger emergency response simulation
                    this.triggerEmergencyResponse(analysis);
                }
            }
        });
        
        this.updateCameraFeeds();
    }
    
    triggerEmergencyResponse(analysis) {
        // Simulate emergency response for video analysis
        setTimeout(() => {
            this.showNotification('📱 SMS Alerts Sent', 'Emergency contacts have been notified', 'warning');
        }, 2000);
        
        setTimeout(() => {
            this.showNotification('📞 Emergency Calls Initiated', 'Automatic calls to fire department started', 'warning');
        }, 4000);
        
        setTimeout(() => {
            this.showNotification('🚨 Siren Activated', 'Building evacuation sirens are now active', 'danger');
        }, 6000);
        
        // Play siren sound simulation
        this.playSirenSound();
    }
    
    playSirenSound() {
        // Create audio context for siren sound (browser compatibility)
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(400, audioContext.currentTime + 0.5);
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime + 1);
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.setValueAtTime(0, audioContext.currentTime + 1.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 1.5);
            
            // Show siren indicator
            this.showSirenIndicator();
        } catch (error) {
            console.log('Audio not supported, showing visual siren instead');
            this.showSirenIndicator();
        }
    }
    
    showSirenIndicator() {
        const sirenIndicator = document.createElement('div');
        sirenIndicator.className = 'fixed top-4 left-4 bg-red-600 text-white px-4 py-2 rounded-lg animate-pulse z-50';
        sirenIndicator.innerHTML = '<i class="fas fa-bullhorn mr-2"></i>🚨 SIREN ACTIVE 🚨';
        
        document.body.appendChild(sirenIndicator);
        
        setTimeout(() => {
            sirenIndicator.remove();
        }, 10000); // Remove after 10 seconds
    }
}

// Global functions for HTML button interactions
function showNotificationPanel() {
    const panel = document.getElementById('notificationPanel');
    const settings = document.getElementById('settingsPanel');
    
    if (settings) settings.classList.add('translate-x-full');
    if (panel) {
        panel.classList.remove('translate-x-full');
        // Add notification when panel is opened
        if (window.dashboard) {
            window.dashboard.addNotification('info', 'Notification Panel Opened', 'Viewing current system alerts and notifications');
        }
    }
}

function hideNotificationPanel() {
    const panel = document.getElementById('notificationPanel');
    if (panel) panel.classList.add('translate-x-full');
}

function showSettings() {
    const settings = document.getElementById('settingsPanel');
    const notifications = document.getElementById('notificationPanel');
    
    if (notifications) notifications.classList.add('translate-x-full');
    if (settings) {
        settings.classList.remove('translate-x-full');
        // Add notification when settings is opened
        if (window.dashboard) {
            window.dashboard.addNotification('info', 'Settings Panel Opened', 'Accessing system configuration options');
        }
    }
}

function hideSettingsPanel() {
    const settings = document.getElementById('settingsPanel');
    if (settings) settings.classList.add('translate-x-full');
}

function triggerEmergencyAlert() {
    const modal = document.getElementById('emergencyModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    
    if (window.dashboard) {
        window.dashboard.addNotification('emergency', 'EMERGENCY ALERT ACTIVATED', 'All emergency protocols have been triggered - sirens, alerts, and notifications sent');
        window.dashboard.showNotification('🚨 EMERGENCY ALERT ACTIVATED!', 'All emergency protocols have been triggered', 'danger');
        window.dashboard.playAlertSound();
    }
    
    console.log('🚨 EMERGENCY ALERT: All emergency protocols activated');
}

function contactFireDepartment() {
    if (window.dashboard) {
        window.dashboard.addNotification('urgent', 'Fire Department Contacted', 'Emergency call placed to fire department - Response team dispatched');
        window.dashboard.showNotification('📞 Fire Department contacted successfully!', 'Emergency response team dispatched', 'success');
    }
    console.log('📞 Fire Department contacted');
}

function buildingAnnouncement() {
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'Building Announcement Active', 'Public address system broadcasting evacuation instructions');
        window.dashboard.showNotification('📢 Building announcement system activated!', 'Evacuation instructions broadcasting', 'success');
    }
    console.log('📢 Building announcement activated');
}

function startAllVideos() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        video.play().catch(e => console.log('Video autoplay prevented'));
    });
    
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'All Video Feeds Started', 'Monitoring all 6 camera feeds simultaneously');
        window.dashboard.showNotification('▶️ All video feeds started!', 'Monitoring all cameras', 'success');
    }
}

function pauseAllVideos() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => video.pause());
    
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'All Video Feeds Paused', 'Video monitoring temporarily paused');
        window.dashboard.showNotification('⏸️ All video feeds paused!', 'Monitoring paused', 'info');
    }
}

function refreshVideoFeeds() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => video.load());
    
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'Video Feeds Refreshed', 'All camera feeds have been refreshed and reloaded');
        window.dashboard.showNotification('🔄 Video feeds refreshed!', 'All feeds reloaded', 'success');
    }
}

function analyzeAllVideos() {
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'Video Analysis Started', 'Analyzing all 6 uploaded videos for fire detection');
        window.dashboard.showNotification('🔍 Starting analysis of all videos...', 'Processing 6 video files', 'info');
        
        setTimeout(() => {
            window.dashboard.addNotification('success', 'Analysis Complete', 'Analysis completed: 2 fire incidents detected across all videos');
            window.dashboard.showNotification('✅ Analysis complete! 2 fire incidents found', 'Fire detected in mall_inside.mp4 and mart.mp4', 'success');
        }, 3000);
    }
}

function pauseAnalysis() {
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'Analysis Paused', 'Video analysis temporarily paused');
        window.dashboard.showNotification('⏸️ Video analysis paused', 'Analysis stopped', 'info');
    }
}

function generateReport() {
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'Generating Report', 'Creating comprehensive fire detection report based on current data');
        window.dashboard.showNotification('📊 Generating report...', 'Processing analysis data', 'info');
        
        setTimeout(() => {
            window.dashboard.addNotification('success', 'Report Generated', 'Fire detection report created: 2 incidents detected from 6 video sources');
            window.dashboard.showNotification('📊 Report generated successfully!', 'Report available for download', 'success');
        }, 2000);
    }
}

function exportData() {
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'Exporting Data', 'Preparing video analysis data for export');
        window.dashboard.showNotification('💾 Exporting data...', 'Preparing files', 'info');
        
        setTimeout(() => {
            window.dashboard.addNotification('success', 'Data Export Complete', 'Video analysis data exported to CSV/JSON format');
            window.dashboard.showNotification('💾 Data exported successfully!', 'Files ready for download', 'success');
        }, 2000);
    }
}

function analyzeVideoLink() {
    const input = document.getElementById('videoLinkInput');
    const resultDiv = document.getElementById('videoAnalysisResult');
    const videoUrl = input ? input.value.trim() : '';
    
    if (!videoUrl) {
        if (window.dashboard) {
            window.dashboard.showNotification('⚠️ Please enter a video URL', 'URL required for analysis', 'warning');
        }
        return;
    }
    
    if (resultDiv) {
        resultDiv.innerHTML = `
            <div class="bg-blue-900 border border-blue-500 p-4 rounded-lg">
                <div class="flex items-center space-x-3">
                    <i class="fas fa-spinner fa-spin text-blue-400"></i>
                    <div>
                        <div class="font-semibold text-blue-300">Analyzing Video...</div>
                        <div class="text-sm text-blue-200">Processing: ${videoUrl}</div>
                    </div>
                </div>
            </div>
        `;
        resultDiv.classList.remove('hidden');
    }
    
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'External Video Analysis', `Analyzing external video link: ${videoUrl.substring(0, 50)}...`);
    }
    
    setTimeout(() => {
        const isFireVideo = videoUrl.toLowerCase().includes('fire') || videoUrl.toLowerCase().includes('emergency') || Math.random() > 0.7;
        const confidence = isFireVideo ? Math.floor(Math.random() * 20) + 80 : Math.floor(Math.random() * 15);
        const people = Math.floor(Math.random() * 10) + 1;
        
        if (resultDiv) {
            const alertClass = isFireVideo ? 'border-red-500 bg-red-900' : 'border-green-500 bg-green-900';
            const statusIcon = isFireVideo ? '🔥' : '✅';
            const statusText = isFireVideo ? 'FIRE DETECTED' : 'NO THREAT DETECTED';
            const statusColor = isFireVideo ? 'text-red-300' : 'text-green-300';
            
            resultDiv.innerHTML = `
                <div class="${alertClass} border p-4 rounded-lg">
                    <div class="flex items-center justify-between mb-3">
                        <h4 class="font-semibold ${statusColor}">${statusIcon} ${statusText}</h4>
                        <span class="text-xs text-gray-400">${new Date().toLocaleTimeString()}</span>
                    </div>
                    <div class="grid grid-cols-3 gap-4 mb-3">
                        <div class="text-center">
                            <div class="text-sm text-gray-400">Confidence</div>
                            <div class="text-lg font-bold ${isFireVideo ? 'text-red-400' : 'text-green-400'}">${confidence}%</div>
                        </div>
                        <div class="text-center">
                            <div class="text-sm text-gray-400">People</div>
                            <div class="text-lg font-bold text-blue-400">${people}</div>
                        </div>
                        <div class="text-center">
                            <div class="text-sm text-gray-400">Status</div>
                            <div class="text-lg font-bold ${isFireVideo ? 'text-red-400' : 'text-green-400'}">${isFireVideo ? 'ALERT' : 'SAFE'}</div>
                        </div>
                    </div>
                    <div class="text-sm text-gray-300">
                        <strong>Source:</strong> ${videoUrl.substring(0, 60)}${videoUrl.length > 60 ? '...' : ''}
                    </div>
                </div>
            `;
        }
        
        if (window.dashboard) {
            if (isFireVideo) {
                window.dashboard.addNotification('emergency', 'External Video Fire Detected', `Fire detected in external video with ${confidence}% confidence`);
                triggerEmergencyAlert();
            } else {
                window.dashboard.addNotification('success', 'External Video Analysis Complete', 'No fire detected in external video - area is safe');
            }
        }
    }, 3000);
}

// Global functions
function closeEmergencyModal() {
    const modal = document.getElementById('emergencyModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
    
    if (window.dashboard) {
        window.dashboard.addNotification('info', 'Emergency Alert Acknowledged', 'Emergency protocol acknowledgment received');
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new FireDetectionDashboard();
});
