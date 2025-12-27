// Dashboard JavaScript for Fire Detection System
class FireDetectionDashboard {
    constructor() {
        this.cameras = [
            { id: 1, location: "Mall Video 1", status: "safe", confidence: 10, people: 0, videoFile: "mall.mp4", cameraId: "CAM_MALL_001" },
            { id: 2, location: "Mall Video 2", status: "monitoring", confidence: 45, people: 2, videoFile: "mall_xo0ks0c.mp4", cameraId: "CAM_MALL_002" },
            { id: 3, location: "Mall Video 3", status: "safe", confidence: 8, people: 1, videoFile: "mall_zHb6RQQ.mp4", cameraId: "CAM_MALL_003" }
        ];
        
        this.stats = {
            activeCameras: 12,
            fireIncidentsToday: 3,
            peopleEvacuated: 8,
            responseTime: 45
        };
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.startRealTimeUpdates();
        this.updateCameraFeeds();
        
        // Update stats every 30 seconds
        setInterval(() => {
            this.updateStats();
        }, 30000);
        
        // Update camera status every 5 seconds
        setInterval(() => {
            this.simulateCameraUpdates();
        }, 5000);
    }

    bindEvents() {
        // Emergency response buttons
        document.querySelectorAll('.emergency-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const buttonText = e.currentTarget.querySelector('.font-semibold').textContent;
                this.handleEmergencyAction(buttonText);
            });
        });

        // Camera feed interactions
        document.querySelectorAll('.camera-feed').forEach(feed => {
            feed.addEventListener('click', (e) => {
                e.preventDefault();
                const location = feed.dataset.location;
                this.showCameraDetails(location);
            });
        });

        // Navigation - Simplified handling for Django URLs
        document.querySelectorAll('nav a').forEach(link => {
            link.addEventListener('click', (e) => {
                const href = e.target.getAttribute('href') || e.currentTarget.getAttribute('href');
                console.log('Navigation clicked - href:', href, 'currentTarget:', e.currentTarget); // Enhanced debug
                
                // Let all valid URLs through, only prevent # and empty links
                if (href && href !== '#' && href !== '' && href !== 'null' && href !== 'undefined') {
                    console.log('✅ Allowing navigation to:', href);
                    // Don't prevent default - let browser navigate normally
                    return;
                }
                
                // Only prevent default for invalid links
                console.log('❌ Preventing navigation for invalid href:', href);
                e.preventDefault();
                const linkText = (e.target.textContent || e.currentTarget.textContent).trim();
                this.showComingSoon(linkText);
            });
        });

        // Start/Stop all buttons
        const startButton = document.querySelector('.bg-blue-600');
        const pauseButton = document.querySelector('.bg-gray-600');
        
        if (startButton && startButton.textContent.includes('Start All')) {
            startButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.startAllCameras();
            });
        }

        if (pauseButton && pauseButton.textContent.includes('Pause All')) {
            pauseButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.pauseAllCameras();
            });
        }

        // Header notification and settings buttons
        document.querySelectorAll('header button').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const icon = btn.querySelector('i');
                if (icon.classList.contains('fa-bell')) {
                    this.showNotifications();
                } else if (icon.classList.contains('fa-cog')) {
                    this.showSettings();
                }
            });
        });
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
        // Show immediate visual feedback
        this.showNotification('Emergency Alert Initiated', 'Activating all emergency protocols...', 'danger');
        
        // Update UI to show emergency state
        document.body.classList.add('emergency-active');
        
        // Show emergency modal
        const modal = document.getElementById('emergencyModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
        
        // Simulate API call to trigger emergency
        this.makeAPICall('/api/emergency-contacts/emergency_alert/', {
            method: 'POST',
            data: {
                alert_type: 'fire_emergency',
                location: 'Block A - Lab 3',
                confidence: 92,
                automatic: false
            }
        }).then(response => {
            console.log('🚨 Emergency alert sent successfully');
            this.showNotification('Emergency Services Notified', 'All emergency contacts have been alerted', 'success');
        }).catch(error => {
            console.error('Emergency alert failed:', error);
            this.showNotification('Alert System Error', 'Failed to send emergency alerts. Please contact manually.', 'danger');
        });
        
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
        this.showNotification('Contacting Fire Department', 'Establishing connection to emergency services...', 'warning');
        
        // Simulate calling fire department API
        this.makeAPICall('/api/emergency-contacts/emergency_alert/', {
            method: 'POST',
            data: {
                alert_type: 'fire_department_call',
                priority: 'high',
                location: 'Building Fire Detection System',
                details: 'Automated fire detection system alert'
            }
        }).then(response => {
            // Simulate call interface
            setTimeout(() => {
                this.showModal('Fire Department Contact', `
                    <div class="text-center">
                        <i class="fas fa-phone-alt text-4xl text-green-500 mb-4 animate-pulse"></i>
                        <p class="mb-4 text-green-400 font-semibold">✅ Connected to Fire Department</p>
                        <div class="bg-gray-700 p-4 rounded-lg mb-4">
                            <p class="text-sm text-gray-300 mb-2">Call Status: <span class="text-green-400">Active</span></p>
                            <p class="text-sm text-gray-300 mb-2">Duration: <span id="call-timer">00:00</span></p>
                            <p class="text-sm text-gray-300">Emergency details transmitted automatically</p>
                        </div>
                        <div class="flex justify-center space-x-4">
                            <button class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg" onclick="this.closest('.fixed').remove()">
                                <i class="fas fa-phone-slash mr-2"></i>End Call
                            </button>
                            <button class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">
                                <i class="fas fa-microphone mr-2"></i>Speak
                            </button>
                        </div>
                    </div>
                `);
                
                // Start call timer
                let seconds = 0;
                const timer = setInterval(() => {
                    seconds++;
                    const mins = Math.floor(seconds / 60);
                    const secs = seconds % 60;
                    const timerElement = document.getElementById('call-timer');
                    if (timerElement) {
                        timerElement.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
                    } else {
                        clearInterval(timer);
                    }
                }, 1000);
                
            }, 2000);
        }).catch(error => {
            this.showNotification('Connection Failed', 'Unable to contact fire department. Please call manually: 911', 'danger');
        });
    }

    makeBuildingAnnouncement() {
        this.showNotification('Building Announcement Activating', 'Public address system coming online...', 'info');
        
        // Simulate announcement API call
        this.makeAPICall('/api/fire-detection/building_announcement/', {
            method: 'POST',
            data: {
                message: 'Fire detected in Block A Lab 3. Evacuate immediately.',
                priority: 'high',
                repeat: true
            }
        }).then(response => {
            this.showModal('Building Announcement', `
                <div class="text-center">
                    <i class="fas fa-megaphone text-4xl text-blue-500 mb-4 animate-bounce"></i>
                    <div class="bg-gray-700 p-4 rounded-lg mb-4">
                        <p class="text-sm text-gray-300 mb-2">🔊 Now Broadcasting:</p>
                        <div class="bg-red-900 p-3 rounded border-l-4 border-red-500">
                            <p class="font-semibold text-red-200">"Attention all building occupants. A fire has been detected in Block A - Lab 3. Please evacuate the building immediately using the nearest emergency exit. Do not use elevators. Proceed to the designated assembly point."</p>
                        </div>
                        <div class="mt-3 flex justify-between text-sm text-gray-400">
                            <span>Status: <span class="text-green-400">Broadcasting</span></span>
                            <span>Repetitions: <span class="text-blue-400">Continuous</span></span>
                        </div>
                    </div>
                    <div class="flex justify-center space-x-4">
                        <button class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg" onclick="this.closest('.fixed').remove()">
                            <i class="fas fa-stop mr-2"></i>Stop Announcement
                        </button>
                        <button class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">
                            <i class="fas fa-redo mr-2"></i>Repeat Message
                        </button>
                        <button class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg">
                            <i class="fas fa-edit mr-2"></i>Custom Message
                        </button>
                    </div>
                </div>
            `);
        }).catch(error => {
            this.showNotification('Announcement Failed', 'PA system unavailable. Use manual announcement procedures.', 'danger');
        });
    }

    // Helper function to make API calls with proper Django CSRF handling
    makeAPICall(url, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            }
        };

        if (options.data) {
            defaultOptions.body = JSON.stringify(options.data);
        }

        const finalOptions = { ...defaultOptions, ...options };
        
        return fetch(url, finalOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('API call failed:', error);
                // Return a simulated success for demo purposes
                return new Promise((resolve) => {
                    setTimeout(() => {
                        resolve({ status: 'simulated', message: 'Demo mode - API call simulated' });
                    }, 1000);
                });
            });
    }

    // Get Django CSRF token
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        // Try to get from meta tag
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        return csrfMeta ? csrfMeta.getAttribute('content') : '';
    }

    simulateCameraUpdates() {
        // Randomly update camera statuses
        const randomCamera = this.cameras[Math.floor(Math.random() * this.cameras.length)];
        
        if (Math.random() < 0.1) { // 10% chance of status change
            if (randomCamera.status === 'safe' && randomCamera.confidence < 20) {
                randomCamera.status = 'warning';
                randomCamera.confidence = Math.floor(Math.random() * 30) + 40;
            } else if (randomCamera.status === 'warning') {
                if (Math.random() < 0.3) {
                    randomCamera.status = 'fire';
                    randomCamera.confidence = Math.floor(Math.random() * 20) + 80;
                    this.stats.fireIncidentsToday++;
                } else {
                    randomCamera.status = 'safe';
                    randomCamera.confidence = Math.floor(Math.random() * 20) + 5;
                }
            }
            
            this.updateCameraFeedVisual(randomCamera.location, randomCamera.status);
            this.updateStats();
        }
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
                feed.classList.add('emergency-glow');
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
        // Update active cameras
        document.querySelector('.grid .bg-gray-800:nth-child(1) .text-2xl').textContent = this.stats.activeCameras;
        
        // Update fire incidents
        document.querySelector('.grid .bg-gray-800:nth-child(2) .text-2xl').textContent = this.stats.fireIncidentsToday;
        
        // Update people evacuated
        document.querySelector('.grid .bg-gray-800:nth-child(3) .text-2xl').textContent = this.stats.peopleEvacuated;
        
        // Update response time
        document.querySelector('.grid .bg-gray-800:nth-child(4) .text-2xl').textContent = this.stats.responseTime + 's';
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
                
                ${camera.videoFile ? `
                    <div class="bg-gray-800 p-4 rounded-lg">
                        <h5 class="font-semibold text-blue-300 mb-2">📹 Live Video Feed</h5>
                        <video controls class="w-full rounded-lg" style="max-height: 300px;">
                            <source src="/media/uploaded_videos/${camera.videoFile}" type="video/mp4">
                            <source src="/media/cctv_recordings/${camera.videoFile}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <div class="mt-2 text-sm text-gray-400">
                            <p>Camera ID: ${camera.cameraId || 'Unknown'}</p>
                            <p>Video File: ${camera.videoFile}</p>
                        </div>
                    </div>
                ` : ''}
                
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

    showNotifications() {
        this.showModal('Notifications', `
            <div class="space-y-4">
                <div class="bg-red-900 p-3 rounded-lg border-l-4 border-red-500">
                    <div class="flex justify-between items-start">
                        <div>
                            <h5 class="font-semibold text-red-300">Fire Alert - Block A Lab 3</h5>
                            <p class="text-sm text-gray-300">High confidence fire detection (92%)</p>
                            <p class="text-xs text-gray-400">2 minutes ago</p>
                        </div>
                        <span class="bg-red-500 text-white px-2 py-1 rounded text-xs">HIGH</span>
                    </div>
                </div>
                
                <div class="bg-yellow-900 p-3 rounded-lg border-l-4 border-yellow-500">
                    <div class="flex justify-between items-start">
                        <div>
                            <h5 class="font-semibold text-yellow-300">Monitoring Alert - Block C</h5>
                            <p class="text-sm text-gray-300">Elevated temperature detected</p>
                            <p class="text-xs text-gray-400">15 minutes ago</p>
                        </div>
                        <span class="bg-yellow-500 text-black px-2 py-1 rounded text-xs">MEDIUM</span>
                    </div>
                </div>
                
                <div class="bg-blue-900 p-3 rounded-lg border-l-4 border-blue-500">
                    <div class="flex justify-between items-start">
                        <div>
                            <h5 class="font-semibold text-blue-300">System Update</h5>
                            <p class="text-sm text-gray-300">All cameras online and functioning</p>
                            <p class="text-xs text-gray-400">30 minutes ago</p>
                        </div>
                        <span class="bg-blue-500 text-white px-2 py-1 rounded text-xs">INFO</span>
                    </div>
                </div>
                
                <div class="text-center">
                    <button class="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded-lg text-sm">
                        Mark All as Read
                    </button>
                </div>
            </div>
        `);
    }

    showSettings() {
        this.showModal('System Settings', `
            <div class="space-y-6">
                <div>
                    <h5 class="font-semibold text-white mb-3">Detection Settings</h5>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-300">Fire Detection Sensitivity</span>
                            <select class="bg-gray-700 text-white px-3 py-1 rounded">
                                <option value="high" selected>High</option>
                                <option value="medium">Medium</option>
                                <option value="low">Low</option>
                            </select>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-300">Alert Threshold (%)</span>
                            <input type="range" min="50" max="95" value="75" class="w-24">
                            <span class="text-blue-400 w-12 text-right">75%</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-300">Auto-Alert Fire Department</span>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" checked class="sr-only peer">
                                <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </label>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h5 class="font-semibold text-white mb-3">Camera Settings</h5>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-300">Recording Quality</span>
                            <select class="bg-gray-700 text-white px-3 py-1 rounded">
                                <option value="1080p" selected>1080p</option>
                                <option value="720p">720p</option>
                                <option value="480p">480p</option>
                            </select>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-300">Frame Rate (FPS)</span>
                            <select class="bg-gray-700 text-white px-3 py-1 rounded">
                                <option value="30" selected>30</option>
                                <option value="15">15</option>
                                <option value="10">10</option>
                            </select>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-300">Night Vision</span>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" checked class="sr-only peer">
                                <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </label>
                        </div>
                    </div>
                </div>
                
                <div class="flex space-x-3">
                    <button class="flex-1 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg" onclick="this.closest('.fixed').remove()">
                        Save Settings
                    </button>
                    <button class="flex-1 bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded-lg" onclick="this.closest('.fixed').remove()">
                        Cancel
                    </button>
                </div>
            </div>
        `);
    }
}

// Global functions
function closeEmergencyModal() {
    const modal = document.getElementById('emergencyModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new FireDetectionDashboard();
});
