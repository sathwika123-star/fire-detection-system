/**
 * Real AI Fire Detection Integration
 * This file integrates the frontend with the real AI detection backend
 * Replaces JavaScript simulation with actual AI-powered fire detection
 */

class RealAIFireDetection {
    constructor() {
        this.isInitialized = false;
        this.aiCapabilities = null;
        this.monitoringActive = false;
        this.detectionInterval = null;
        this.videoSources = [
            'mall_inside.mp4',
            'mart.mp4',
            'mall escalator.mp4',
            'mall first floor.mp4',
            'mall front.mp4',
            'mall total.mp4'
        ];
        this.lastDetectionResults = {};
        this.detectionHistory = [];
        
        this.init();
    }

    async init() {
        console.log('🤖 Initializing Real AI Fire Detection System...');
        
        try {
            // Check AI detection capabilities
            await this.checkAICapabilities();
            
            // Initialize video monitoring
            await this.initializeVideoMonitoring();
            
            // Start real-time detection
            this.startRealTimeDetection();
            
            this.isInitialized = true;
            console.log('✅ Real AI Fire Detection System initialized successfully');
            
            // Update UI to show AI status
            this.updateAIStatusIndicator(true);
            
        } catch (error) {
            console.error('❌ Failed to initialize AI detection:', error);
            this.fallbackToSimulation();
        }
    }

    async checkAICapabilities() {
        try {
            const response = await fetch('/api/real-ai-detection-live/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`AI capabilities check failed: ${response.status}`);
            }

            this.aiCapabilities = await response.json();
            
            console.log('🤖 AI Detection Capabilities:', this.aiCapabilities);
            
            if (!this.aiCapabilities.capabilities?.ai_available) {
                console.warn('⚠️ AI detection not available, falling back to simulation');
                this.fallbackToSimulation();
                return false;
            }

            return true;

        } catch (error) {
            console.error('❌ AI capabilities check error:', error);
            throw error;
        }
    }

    async initializeVideoMonitoring() {
        console.log('📹 Initializing video monitoring for', this.videoSources.length, 'sources');
        
        // Initialize monitoring for each video source
        for (const videoSource of this.videoSources) {
            await this.setupVideoSourceMonitoring(videoSource);
        }
    }

    async setupVideoSourceMonitoring(videoSource) {
        try {
            // Start continuous monitoring for this video source
            const response = await fetch('/api/real-ai-detection-live/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    video_source: videoSource,
                    mode: 'continuous'
                })
            });

            if (response.ok) {
                const result = await response.json();
                console.log(`✅ Continuous monitoring started for ${videoSource}:`, result);
            } else {
                console.warn(`⚠️ Failed to start monitoring for ${videoSource}`);
            }

        } catch (error) {
            console.error(`❌ Error setting up monitoring for ${videoSource}:`, error);
        }
    }

    startRealTimeDetection() {
        console.log('🚀 Starting real-time AI detection...');
        
        this.monitoringActive = true;
        
        // Analyze each video source periodically
        this.detectionInterval = setInterval(async () => {
            if (this.monitoringActive) {
                await this.performBatchDetection();
            }
        }, 3000); // Check every 3 seconds

        // Also perform enhanced analysis less frequently
        setInterval(async () => {
            if (this.monitoringActive) {
                await this.performEnhancedAnalysis();
            }
        }, 10000); // Enhanced analysis every 10 seconds
    }

    async performBatchDetection() {
        const promises = this.videoSources.map(videoSource => 
            this.analyzeVideoSource(videoSource, 'standard')
        );

        try {
            const results = await Promise.all(promises);
            this.processDetectionResults(results);
        } catch (error) {
            console.error('❌ Batch detection error:', error);
        }
    }

    async analyzeVideoSource(videoSource, mode = 'standard') {
        try {
            const response = await fetch('/api/real-ai-detection-live/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    video_source: videoSource,
                    mode: mode
                })
            });

            if (!response.ok) {
                throw new Error(`Detection failed for ${videoSource}: ${response.status}`);
            }

            const result = await response.json();
            result.video_source = videoSource;
            result.analysis_time = new Date().toISOString();
            
            return result;

        } catch (error) {
            console.error(`❌ Analysis error for ${videoSource}:`, error);
            return {
                video_source: videoSource,
                error: error.message,
                analysis: { fire_detected: false, smoke_detected: false, confidence: 0 }
            };
        }
    }

    async performEnhancedAnalysis() {
        // Perform enhanced analysis on a rotating basis
        const sourceIndex = Math.floor(Date.now() / 10000) % this.videoSources.length;
        const videoSource = this.videoSources[sourceIndex];
        
        console.log(`🔍 Performing enhanced analysis on ${videoSource}`);
        
        try {
            const result = await this.analyzeVideoSource(videoSource, 'enhanced');
            this.processEnhancedResult(result);
        } catch (error) {
            console.error('❌ Enhanced analysis error:', error);
        }
    }

    processDetectionResults(results) {
        const timestamp = new Date().toISOString();
        
        results.forEach((result, index) => {
            if (result.error) {
                console.warn(`⚠️ Detection error for ${result.video_source}:`, result.error);
                return;
            }

            const analysis = result.analysis;
            const videoSource = result.video_source;
            
            // Store last detection result
            this.lastDetectionResults[videoSource] = {
                ...analysis,
                timestamp: timestamp,
                enhanced: false
            };

            // Update UI for this video source
            this.updateVideoSourceUI(videoSource, analysis, index);
            
            // Handle alerts
            if (analysis.fire_detected || analysis.smoke_detected) {
                this.handleDetectionAlert(videoSource, analysis);
            }
        });

        // Update global statistics
        this.updateGlobalStatistics();
    }

    processEnhancedResult(result) {
        if (result.error) {
            console.warn('⚠️ Enhanced analysis error:', result.error);
            return;
        }

        const analysis = result.analysis;
        const videoSource = result.video_source;
        
        console.log(`🔍 Enhanced analysis results for ${videoSource}:`, analysis);
        
        // Store enhanced result
        this.lastDetectionResults[videoSource] = {
            ...analysis,
            timestamp: new Date().toISOString(),
            enhanced: true
        };

        // Update UI with enhanced insights
        this.updateEnhancedUI(videoSource, analysis);
        
        // Log enhanced insights if available
        if (analysis.enhanced_insights) {
            console.log(`💡 Enhanced insights for ${videoSource}:`, analysis.enhanced_insights);
            this.displayEnhancedInsights(videoSource, analysis.enhanced_insights);
        }
    }

    updateVideoSourceUI(videoSource, analysis, index) {
        // Update dashboard video display
        const videoElement = document.querySelector(`#video-${index + 1}`);
        const statusElement = document.querySelector(`#status-${index + 1}`);
        const confidenceElement = document.querySelector(`#confidence-${index + 1}`);
        const alertElement = document.querySelector(`#alert-${index + 1}`);

        if (statusElement) {
            let status = '✅ Safe';
            let statusClass = 'safe';
            
            if (analysis.fire_detected) {
                status = '🔥 FIRE DETECTED';
                statusClass = 'fire';
            } else if (analysis.smoke_detected) {
                status = '💨 Smoke Detected';
                statusClass = 'smoke';
            }
            
            statusElement.textContent = status;
            statusElement.className = `status ${statusClass}`;
        }

        if (confidenceElement) {
            confidenceElement.textContent = `${analysis.confidence.toFixed(1)}%`;
            confidenceElement.className = `confidence confidence-${this.getConfidenceLevel(analysis.confidence)}`;
        }

        if (alertElement) {
            if (analysis.fire_detected || analysis.smoke_detected) {
                alertElement.style.display = 'block';
                alertElement.className = `alert ${analysis.fire_detected ? 'fire' : 'smoke'}`;
                alertElement.textContent = analysis.fire_detected ? '🚨 FIRE ALERT' : '⚠️ SMOKE ALERT';
            } else {
                alertElement.style.display = 'none';
            }
        }

        // Update camera feeds interface if present
        this.updateCameraFeedUI(videoSource, analysis, index);
    }

    updateCameraFeedUI(videoSource, analysis, index) {
        const cameraContainer = document.querySelector(`#camera-${index + 1}`);
        if (!cameraContainer) return;

        const statusIndicator = cameraContainer.querySelector('.status-indicator');
        const confidenceDisplay = cameraContainer.querySelector('.confidence-display');
        const alertOverlay = cameraContainer.querySelector('.alert-overlay');

        if (statusIndicator) {
            if (analysis.fire_detected) {
                statusIndicator.className = 'status-indicator fire';
                statusIndicator.textContent = '🔥 FIRE';
            } else if (analysis.smoke_detected) {
                statusIndicator.className = 'status-indicator smoke';
                statusIndicator.textContent = '💨 SMOKE';
            } else {
                statusIndicator.className = 'status-indicator safe';
                statusIndicator.textContent = '✅ SAFE';
            }
        }

        if (confidenceDisplay) {
            confidenceDisplay.textContent = `AI: ${analysis.confidence.toFixed(1)}%`;
            confidenceDisplay.className = `confidence-display level-${this.getConfidenceLevel(analysis.confidence)}`;
        }

        if (alertOverlay) {
            if (analysis.fire_detected || analysis.smoke_detected) {
                alertOverlay.style.display = 'flex';
                alertOverlay.className = `alert-overlay ${analysis.fire_detected ? 'fire' : 'smoke'}`;
            } else {
                alertOverlay.style.display = 'none';
            }
        }
    }

    updateEnhancedUI(videoSource, analysis) {
        // Create or update enhanced insights panel
        const insightsPanel = document.getElementById('enhanced-insights') || this.createEnhancedInsightsPanel();
        
        if (analysis.enhanced_insights) {
            const insights = analysis.enhanced_insights;
            
            let insightsHTML = `
                <div class="enhanced-insight-item">
                    <h4>🎯 ${videoSource} - Enhanced AI Analysis</h4>
                    <div class="insight-grid">
                        <div class="insight-card">
                            <h5>🔥 Flame Analysis</h5>
                            <p>Intensity: ${insights.flame_characteristics?.flame_intensity_percentage || 0}%</p>
                            <p>Coverage: ${insights.flame_characteristics?.flame_coverage || 'None'}</p>
                        </div>
                        <div class="insight-card">
                            <h5>💨 Smoke Analysis</h5>
                            <p>Density: ${insights.smoke_density?.smoke_density_score || 0}%</p>
                            <p>Impact: ${insights.smoke_density?.visibility_impact || 'None'}</p>
                        </div>
                        <div class="insight-card">
                            <h5>🌡️ Heat Signature</h5>
                            <p>Temperature: ${insights.heat_signature?.temperature_estimate || 'Normal'}</p>
                            <p>Hot Spots: ${insights.heat_signature?.hot_spots_count || 0}</p>
                        </div>
                    </div>
                </div>
            `;
            
            insightsPanel.innerHTML = insightsHTML;
        }
    }

    createEnhancedInsightsPanel() {
        const panel = document.createElement('div');
        panel.id = 'enhanced-insights';
        panel.className = 'enhanced-insights-panel';
        
        // Try to append to dashboard or create floating panel
        const dashboard = document.querySelector('.dashboard-container') || document.body;
        dashboard.appendChild(panel);
        
        return panel;
    }

    handleDetectionAlert(videoSource, analysis) {
        const alertLevel = analysis.fire_detected ? 'CRITICAL' : 'WARNING';
        const alertType = analysis.fire_detected ? 'FIRE' : 'SMOKE';
        
        console.log(`🚨 ${alertLevel} ALERT: ${alertType} detected in ${videoSource} with ${analysis.confidence.toFixed(1)}% confidence`);
        
        // Add to detection history
        this.detectionHistory.unshift({
            timestamp: new Date().toISOString(),
            videoSource: videoSource,
            alertType: alertType,
            confidence: analysis.confidence,
            severity: alertLevel
        });

        // Keep only last 50 detections
        if (this.detectionHistory.length > 50) {
            this.detectionHistory = this.detectionHistory.slice(0, 50);
        }

        // Show browser notification if supported
        this.showBrowserNotification(alertType, videoSource, analysis.confidence);
        
        // Play alert sound
        this.playAlertSound(alertType);
        
        // Update alert statistics
        this.updateAlertStatistics(alertType);
    }

    showBrowserNotification(alertType, videoSource, confidence) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(`🚨 ${alertType} DETECTED`, {
                body: `${alertType} detected in ${videoSource} with ${confidence.toFixed(1)}% confidence`,
                icon: '/static/images/fire-icon.png',
                tag: `fire-alert-${videoSource}`,
                requireInteraction: true
            });
        } else if ('Notification' in window && Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    this.showBrowserNotification(alertType, videoSource, confidence);
                }
            });
        }
    }

    playAlertSound(alertType) {
        try {
            const audio = new Audio(alertType === 'FIRE' ? '/static/sounds/fire-alarm.mp3' : '/static/sounds/smoke-alarm.mp3');
            audio.volume = 0.5;
            audio.play().catch(e => console.log('Audio play failed:', e));
        } catch (error) {
            console.log('Alert sound not available:', error);
        }
    }

    updateGlobalStatistics() {
        const totalSources = this.videoSources.length;
        let fireDetections = 0;
        let smokeDetections = 0;
        let safeCount = 0;
        let totalConfidence = 0;

        Object.values(this.lastDetectionResults).forEach(result => {
            if (result.fire_detected) fireDetections++;
            else if (result.smoke_detected) smokeDetections++;
            else safeCount++;
            
            totalConfidence += result.confidence || 0;
        });

        const avgConfidence = totalConfidence / totalSources;
        
        // Update statistics display
        this.updateStatisticsUI({
            totalSources,
            fireDetections,
            smokeDetections,
            safeCount,
            avgConfidence,
            aiActive: true
        });
    }

    updateStatisticsUI(stats) {
        // Update various statistics elements
        const elements = {
            'total-cameras': stats.totalSources,
            'fire-alerts': stats.fireDetections,
            'smoke-alerts': stats.smokeDetections,
            'safe-cameras': stats.safeCount,
            'avg-confidence': `${stats.avgConfidence.toFixed(1)}%`,
            'ai-status': stats.aiActive ? '🤖 AI Active' : '❌ AI Offline'
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    updateAIStatusIndicator(active) {
        const indicator = document.getElementById('ai-status-indicator') || this.createAIStatusIndicator();
        
        if (active) {
            indicator.className = 'ai-status active';
            indicator.innerHTML = '🤖 Real AI Detection Active';
        } else {
            indicator.className = 'ai-status inactive';
            indicator.innerHTML = '❌ AI Detection Offline';
        }
    }

    createAIStatusIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'ai-status-indicator';
        indicator.className = 'ai-status';
        
        // Add to top of dashboard
        const dashboard = document.querySelector('.dashboard-header') || document.body;
        dashboard.appendChild(indicator);
        
        return indicator;
    }

    getConfidenceLevel(confidence) {
        if (confidence >= 80) return 'high';
        if (confidence >= 60) return 'medium';
        if (confidence >= 40) return 'low';
        return 'very-low';
    }

    displayEnhancedInsights(videoSource, insights) {
        console.log(`💡 Enhanced AI Insights for ${videoSource}:`);
        
        if (insights.evacuation_recommendations) {
            console.log('🚨 Evacuation Recommendations:');
            insights.evacuation_recommendations.forEach(recommendation => {
                console.log(`  ${recommendation}`);
            });
        }
        
        // Show recommendations in UI if fire detected
        if (insights.evacuation_recommendations && insights.evacuation_recommendations.length > 0) {
            this.showEvacuationRecommendations(insights.evacuation_recommendations);
        }
    }

    showEvacuationRecommendations(recommendations) {
        // Create or update recommendations panel
        let panel = document.getElementById('evacuation-recommendations');
        if (!panel) {
            panel = document.createElement('div');
            panel.id = 'evacuation-recommendations';
            panel.className = 'evacuation-panel';
            document.body.appendChild(panel);
        }

        const recommendationsHTML = `
            <div class="evacuation-content">
                <h3>🚨 EVACUATION RECOMMENDATIONS</h3>
                <ul>
                    ${recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
                <button onclick="this.parentElement.parentElement.style.display='none'">Close</button>
            </div>
        `;
        
        panel.innerHTML = recommendationsHTML;
        panel.style.display = 'block';
    }

    fallbackToSimulation() {
        console.warn('⚠️ Falling back to JavaScript simulation');
        
        // Initialize the original simulation system
        if (window.originalFireDetection) {
            window.originalFireDetection.init();
        }
        
        this.updateAIStatusIndicator(false);
    }

    stop() {
        console.log('⏹️ Stopping Real AI Fire Detection');
        
        this.monitoringActive = false;
        
        if (this.detectionInterval) {
            clearInterval(this.detectionInterval);
            this.detectionInterval = null;
        }
        
        this.isInitialized = false;
    }

    // Public API methods
    getDetectionHistory() {
        return this.detectionHistory;
    }

    getLastResults() {
        return this.lastDetectionResults;
    }

    getAICapabilities() {
        return this.aiCapabilities;
    }

    isAIActive() {
        return this.isInitialized && this.monitoringActive;
    }
}

// Initialize Real AI Fire Detection when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Store reference to original system if it exists
    if (window.fireDetection) {
        window.originalFireDetection = window.fireDetection;
    }
    
    // Initialize Real AI Detection
    window.realAIFireDetection = new RealAIFireDetection();
    
    // Make it available globally
    window.fireDetection = window.realAIFireDetection;
});

// CSS Styles for AI Detection UI
const aiDetectionStyles = `
<style>
.ai-status {
    position: fixed;
    top: 10px;
    right: 10px;
    padding: 10px 15px;
    border-radius: 5px;
    font-weight: bold;
    z-index: 1000;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.ai-status.active {
    background-color: #10b981;
    color: white;
}

.ai-status.inactive {
    background-color: #ef4444;
    color: white;
}

.enhanced-insights-panel {
    position: fixed;
    bottom: 20px;
    left: 20px;
    width: 600px;
    max-height: 300px;
    overflow-y: auto;
    background: rgba(0,0,0,0.9);
    color: white;
    padding: 15px;
    border-radius: 10px;
    z-index: 999;
}

.insight-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 10px;
}

.insight-card {
    background: rgba(255,255,255,0.1);
    padding: 10px;
    border-radius: 5px;
}

.insight-card h5 {
    margin: 0 0 5px 0;
    font-size: 14px;
}

.insight-card p {
    margin: 2px 0;
    font-size: 12px;
}

.evacuation-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #dc2626;
    color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    z-index: 2000;
    max-width: 500px;
    display: none;
}

.evacuation-content h3 {
    margin: 0 0 15px 0;
    text-align: center;
}

.evacuation-content ul {
    margin: 15px 0;
    padding-left: 20px;
}

.evacuation-content li {
    margin: 5px 0;
}

.evacuation-content button {
    background: white;
    color: #dc2626;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    margin-top: 15px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}

.confidence-display {
    font-size: 12px;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 3px;
    margin-top: 5px;
}

.confidence-display.level-high {
    background: #dc2626;
    color: white;
}

.confidence-display.level-medium {
    background: #f59e0b;
    color: white;
}

.confidence-display.level-low {
    background: #6b7280;
    color: white;
}

.confidence-display.level-very-low {
    background: #10b981;
    color: white;
}
</style>
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', aiDetectionStyles);
