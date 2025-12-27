// Fire Detection System JavaScript
class FireDetectionSystem {
    constructor() {
        this.isFireDetected = false;
        this.currentLocation = "Block A – Lab 3";
        this.severityLevel = 0.92;
        this.peopleCount = 3;
        this.sirenActive = false;
        this.init();
    }

    init() {
        this.updateDateTime();
        this.startSimulation();
        this.bindEvents();
        
        // Update time every second
        setInterval(() => {
            this.updateDateTime();
        }, 1000);
        
        // Simulate real-time updates every 5 seconds
        setInterval(() => {
            this.simulateDetection();
        }, 5000);
    }

    bindEvents() {
        // SMS Button
        document.querySelector('.bg-blue-600').addEventListener('click', () => {
            this.sendSMS();
        });

        // Email Button
        document.querySelector('.bg-gray-600').addEventListener('click', () => {
            this.sendEmail();
        });

        // Alert Button
        document.querySelector('.bg-yellow-600').addEventListener('click', () => {
            this.triggerSiren();
        });

        // Header buttons
        document.querySelector('.fa-bell').parentElement.addEventListener('click', () => {
            this.showNotifications();
        });

        document.querySelector('.fa-sync-alt').parentElement.addEventListener('click', () => {
            this.refreshFeeds();
        });
    }

    updateDateTime() {
        const now = new Date();
        const formatted = now.toLocaleDateString('en-GB') + ' ' + 
                         now.toLocaleTimeString('en-US', { 
                             hour: '2-digit', 
                             minute: '2-digit',
                             hour12: true 
                         });
        
        // Update all time displays
        document.getElementById('snapshotTime').textContent = formatted;
        document.getElementById('snapshotDate').textContent = formatted;
        document.getElementById('alertTime').textContent = formatted;
    }

    simulateDetection() {
        // Randomly simulate fire detection or safe status
        const scenarios = [
            {
                fire: true,
                location: "Block A – Lab 3",
                severity: 0.92,
                people: 3
            },
            {
                fire: false,
                location: "Block B – Entrance",
                severity: 0.15,
                people: 0
            },
            {
                fire: true,
                location: "Block C – Corridor",
                severity: 0.87,
                people: 5
            },
            {
                fire: false,
                location: "Block A – Lab 1",
                severity: 0.08,
                people: 2
            }
        ];

        const scenario = scenarios[Math.floor(Math.random() * scenarios.length)];
        this.updateDetectionStatus(scenario);
    }

    updateDetectionStatus(scenario) {
        this.isFireDetected = scenario.fire;
        this.currentLocation = scenario.location;
        this.severityLevel = scenario.severity;
        this.peopleCount = scenario.people;

        // Update UI elements
        const statusBadge = document.getElementById('statusBadge');
        const locationTitle = document.getElementById('locationTitle');
        const alertLocation = document.getElementById('alertLocation');
        const severityBar = document.getElementById('severityBar');
        const severityValue = document.getElementById('severityValue');
        const peopleCountElement = document.getElementById('peopleCount');
        const mainFeedImage = document.getElementById('mainFeedImage');

        if (this.isFireDetected) {
            statusBadge.textContent = 'Fire Detected';
            statusBadge.className = 'bg-red-500 text-white px-3 py-1 rounded-lg font-medium fire-detected';
            mainFeedImage.parentElement.classList.add('fire-border', 'emergency-glow');
            
            // Auto-trigger siren for high severity
            if (this.severityLevel > 0.8) {
                setTimeout(() => this.triggerSiren(), 1000);
            }
        } else {
            statusBadge.textContent = 'Safe';
            statusBadge.className = 'bg-green-500 text-white px-3 py-1 rounded-lg font-medium';
            mainFeedImage.parentElement.classList.remove('fire-border', 'emergency-glow');
        }

        locationTitle.textContent = this.currentLocation;
        alertLocation.textContent = this.currentLocation;
        severityBar.style.width = (this.severityLevel * 100) + '%';
        severityValue.textContent = this.severityLevel.toFixed(2);
        peopleCountElement.textContent = this.peopleCount;

        // Update severity bar color based on level
        if (this.severityLevel > 0.8) {
            severityBar.className = 'h-2 bg-red-500 rounded-full';
        } else if (this.severityLevel > 0.5) {
            severityBar.className = 'h-2 bg-orange-500 rounded-full';
        } else {
            severityBar.className = 'h-2 bg-yellow-500 rounded-full';
        }

        // Add new incident to recent incidents
        this.addRecentIncident(scenario);

        // Log detection event
        console.log(`Detection Update: ${scenario.fire ? 'FIRE' : 'SAFE'} at ${this.currentLocation} - Severity: ${this.severityLevel}`);
    }

    addRecentIncident(scenario) {
        const incidentsContainer = document.querySelector('.space-y-3');
        const incidents = incidentsContainer.querySelectorAll('.incident-row');
        
        // Remove oldest incident if we have more than 5
        if (incidents.length >= 5) {
            incidents[incidents.length - 1].remove();
        }

        // Create new incident row
        const newIncident = document.createElement('div');
        newIncident.className = 'incident-row flex justify-between items-center py-2 text-sm';
        
        const now = new Date();
        const dateStr = now.toLocaleDateString('en-GB');
        const severityColor = scenario.severity > 0.8 ? 'bg-red-500' : 
                             scenario.severity > 0.5 ? 'bg-orange-500' : 'bg-yellow-500';
        const statusText = scenario.fire ? 'Fire' : 'Safe';
        const statusColor = scenario.fire ? 'text-red-400' : 'text-green-400';

        newIncident.innerHTML = `
            <span class="text-gray-300">${dateStr}</span>
            <span class="text-gray-300">${scenario.location}</span>
            <div class="w-4 h-2 ${severityColor} rounded-full"></div>
            <span class="${statusColor}">${statusText}</span>
        `;

        // Insert at the beginning (after the header)
        const header = incidentsContainer.querySelector('.border-b');
        header.insertAdjacentElement('afterend', newIncident);
    }

    sendSMS() {
        this.showNotification('SMS Alert Sent', `Emergency SMS sent to fire department and safety team for ${this.currentLocation}`, 'success');
        console.log('SMS sent to emergency contacts');
    }

    sendEmail() {
        this.showNotification('Email Alert Sent', `Detailed incident report emailed with snapshot attachment for ${this.currentLocation}`, 'success');
        console.log('Email sent to emergency contacts');
    }

    triggerSiren() {
        if (this.sirenActive) return;
        
        this.sirenActive = true;
        const modal = document.getElementById('sirenModal');
        const emergencyLocation = document.getElementById('emergencyLocation');
        
        emergencyLocation.textContent = this.currentLocation;
        modal.classList.add('show');
        
        // Play siren sound (if audio file available)
        this.playSirenSound();
        
        this.showNotification('Emergency Siren Activated', `Long beep siren triggered for ${this.currentLocation}`, 'warning');
        console.log('Emergency siren activated');
    }

    closeSiren() {
        this.sirenActive = false;
        const modal = document.getElementById('sirenModal');
        modal.classList.remove('show');
        this.stopSirenSound();
    }

    playSirenSound() {
        // Create audio context for siren sound
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.5);
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime + 1);
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            
            oscillator.start();
            oscillator.stop(audioContext.currentTime + 3);
            
            this.currentSiren = { oscillator, audioContext };
        } catch (error) {
            console.log('Audio not supported or permission denied');
        }
    }

    stopSirenSound() {
        if (this.currentSiren) {
            try {
                this.currentSiren.oscillator.stop();
                this.currentSiren.audioContext.close();
            } catch (error) {
                console.log('Error stopping siren sound');
            }
        }
    }

    showNotifications() {
        const notifications = [
            { text: 'Fire detected in Block A – Lab 3', time: '2 min ago', type: 'danger' },
            { text: 'SMS alerts sent successfully', time: '3 min ago', type: 'success' },
            { text: 'System status: Online', time: '5 min ago', type: 'info' }
        ];
        
        this.showModal('Notifications', notifications.map(n => 
            `<div class="p-2 border-b border-gray-600 last:border-b-0">
                <div class="flex justify-between">
                    <span class="text-sm">${n.text}</span>
                    <span class="text-xs text-gray-400">${n.time}</span>
                </div>
            </div>`
        ).join(''));
    }

    refreshFeeds() {
        this.showNotification('Feeds Refreshed', 'All camera feeds have been refreshed', 'info');
        
        // Add loading animation
        const mainFeed = document.getElementById('mainFeedImage');
        mainFeed.parentElement.classList.add('loading');
        
        setTimeout(() => {
            mainFeed.parentElement.classList.remove('loading');
            this.simulateDetection();
        }, 2000);
    }

    showNotification(title, message, type = 'info') {
        // Create notification element
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
        
        // Slide in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    showModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-gray-800 p-6 rounded-lg max-w-md w-full mx-4">
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

// Global function for closing siren (called from HTML)
function closeSiren() {
    if (window.fireSystem) {
        window.fireSystem.closeSiren();
    }
}

// Initialize the system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.fireSystem = new FireDetectionSystem();
    
    // Add some sample data on load
    setTimeout(() => {
        window.fireSystem.updateDetectionStatus({
            fire: true,
            location: "Block A – Lab 3",
            severity: 0.92,
            people: 3
        });
    }, 1000);
});

// Export for module use if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FireDetectionSystem;
}
