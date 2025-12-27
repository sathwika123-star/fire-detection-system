// Frontend-Backend API Integration for Fire Detection System
class FireDetectionAPI {
    constructor() {
        this.baseURL = 'http://127.0.0.1:8000/api';
        this.endpoints = {
            fireDetection: '/fire-detection/',
            statistics: '/fire-detection/statistics/',
            performanceMetrics: '/fire-detection/performance_metrics/',
            testConnection: '/fire-detection/test_connection/',
            emergencyContacts: '/emergency-contacts/',
            cameras: '/cameras/',
            emergencyAlert: '/fire-detection/emergency_alert/'
        };
        this.isConnected = false;
        this.testConnection();
    }

    // Test backend connection
    async testConnection() {
        try {
            console.log('🔄 Testing backend connection...');
            const response = await fetch(`${this.baseURL}${this.endpoints.testConnection}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('✅ Backend connected successfully:', data);
                this.isConnected = true;
                this.updateConnectionStatus(true);
                return data;
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Backend connection failed:', error);
            this.isConnected = false;
            this.updateConnectionStatus(false);
            return null;
        }
    }

    // Get performance metrics from backend
    async getPerformanceMetrics() {
        try {
            console.log('📊 Fetching performance metrics...');
            const response = await fetch(`${this.baseURL}${this.endpoints.performanceMetrics}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('📈 Performance metrics received:', data);
                return data;
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Failed to fetch performance metrics:', error);
            return this.getMockPerformanceMetrics();
        }
    }

    // Get system statistics
    async getStatistics() {
        try {
            console.log('📊 Fetching system statistics...');
            const response = await fetch(`${this.baseURL}${this.endpoints.statistics}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('📈 Statistics received:', data);
                return data;
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Failed to fetch statistics:', error);
            return this.getMockStatistics();
        }
    }

    // Get fire detection incidents
    async getFireDetectionIncidents() {
        try {
            console.log('🔥 Fetching fire detection incidents...');
            const response = await fetch(`${this.baseURL}${this.endpoints.fireDetection}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('🚨 Fire incidents received:', data);
                return data;
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Failed to fetch fire incidents:', error);
            return this.getMockIncidents();
        }
    }

    // Send emergency alert
    async sendEmergencyAlert(alertData) {
        try {
            console.log('🚨 Sending emergency alert...', alertData);
            const response = await fetch(`${this.baseURL}${this.endpoints.emergencyAlert}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(alertData)
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('✅ Emergency alert sent successfully:', data);
                return data;
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Failed to send emergency alert:', error);
            return null;
        }
    }

    // Update connection status in UI
    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            if (connected) {
                statusElement.innerHTML = `
                    <span class="flex items-center text-green-400">
                        <div class="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                        Backend Connected
                    </span>
                `;
            } else {
                statusElement.innerHTML = `
                    <span class="flex items-center text-red-400">
                        <div class="w-2 h-2 bg-red-400 rounded-full mr-2"></div>
                        Backend Disconnected
                    </span>
                `;
            }
        }
    }

    // Mock data fallbacks when backend is unavailable
    getMockPerformanceMetrics() {
        return {
            status: 'success',
            data: {
                accuracy: 94.2,
                precision: 92.1,
                recall: 88.7,
                f1_score: 90.3,
                average_confidence: 87.5,
                processing_time: 125,
                total_detections: 1247,
                false_alarm_rate: 4.8
            },
            message: 'Mock performance metrics (backend unavailable)'
        };
    }

    getMockStatistics() {
        return {
            status: 'success',
            data: {
                total_cameras: 12,
                active_cameras: 11,
                incidents_today: 3,
                incidents_this_week: 8,
                incidents_this_month: 24,
                people_evacuated: 15,
                average_response_time: 45,
                system_uptime: 99.7
            },
            message: 'Mock statistics (backend unavailable)'
        };
    }

    getMockIncidents() {
        return {
            status: 'success',
            data: [
                {
                    id: 1,
                    timestamp: new Date().toISOString(),
                    location: 'Block A - Lab 3',
                    confidence: 92.5,
                    status: 'resolved',
                    response_time: 43
                },
                {
                    id: 2,
                    timestamp: new Date(Date.now() - 3600000).toISOString(),
                    location: 'Block C - Corridor',
                    confidence: 78.3,
                    status: 'investigating',
                    response_time: 38
                }
            ],
            message: 'Mock incidents (backend unavailable)'
        };
    }

    // Auto-refresh data
    startAutoRefresh() {
        console.log('🔄 Starting auto-refresh...');
        
        // Refresh performance metrics every 30 seconds
        setInterval(async () => {
            const metrics = await this.getPerformanceMetrics();
            if (metrics && window.updatePerformanceMetrics) {
                window.updatePerformanceMetrics(metrics.data);
            }
        }, 30000);

        // Refresh statistics every 15 seconds
        setInterval(async () => {
            const stats = await this.getStatistics();
            if (stats && window.updateStatistics) {
                window.updateStatistics(stats.data);
            }
        }, 15000);

        // Test connection every 60 seconds
        setInterval(() => {
            this.testConnection();
        }, 60000);
    }
}

// Initialize API integration
const fireAPI = new FireDetectionAPI();

// Start auto-refresh when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔥 Fire Detection API Integration initialized');
    fireAPI.startAutoRefresh();
});

// Export for global use
window.FireDetectionAPI = FireDetectionAPI;
window.fireAPI = fireAPI;
