// Configuration file for Fire Detection System
const CONFIG = {
    // System Settings
    SYSTEM: {
        NAME: "Fire Detection & Emergency Response System",
        VERSION: "1.0.0",
        UPDATE_INTERVAL: 5000, // milliseconds
        STATS_UPDATE_INTERVAL: 30000, // milliseconds
    },

    // Detection Thresholds
    DETECTION: {
        HIGH_SEVERITY_THRESHOLD: 0.8,  // 80% confidence for auto-alert
        MEDIUM_SEVERITY_THRESHOLD: 0.5, // 50% confidence for warning
        LOW_SEVERITY_THRESHOLD: 0.2,   // 20% confidence minimum
        AUTO_SIREN_DELAY: 1000,        // milliseconds before auto-siren
    },

    // Emergency Contacts
    EMERGENCY_CONTACTS: {
        FIRE_DEPARTMENT: "9908339450",
        EMERGENCY_MEDICAL_SERVICES: "9989647221",
        METRO_POLICE_DEPARTMENT: "9866406226",
        SECURITY_MANAGER: "9908339450",
        FACILITY_MANAGER: "9989647221"
    },

    // Email Configuration
    EMAIL: {
        FIRE_DEPARTMENT: "padirishitha13@gmail.com",
        EMERGENCY_MEDICAL_SERVICES: "bellalasathwika2@gmail.com",
        METRO_POLICE_DEPARTMENT: "muppidojuspoorthi921@gmail.com",
        SECURITY_MANAGER: "padirishitha13@gmail.com",
        FACILITY_MANAGER: "bellalasathwika2@gmail.com"
    },

    // Camera Configuration
    CAMERAS: [
        {
            id: 1,
            name: "Block A - Lab 3",
            location: { x: 100, y: 150 },
            rtsp_url: "rtsp://camera1.local:554/stream",
            priority: "high"
        },
        {
            id: 2,
            name: "Block B - Entrance",
            location: { x: 200, y: 100 },
            rtsp_url: "rtsp://camera2.local:554/stream",
            priority: "high"
        },
        {
            id: 3,
            name: "Block C - Corridor",
            location: { x: 300, y: 200 },
            rtsp_url: "rtsp://camera3.local:554/stream",
            priority: "medium"
        },
        {
            id: 4,
            name: "Block A - Lab 1",
            location: { x: 120, y: 120 },
            rtsp_url: "rtsp://camera4.local:554/stream",
            priority: "medium"
        },
        {
            id: 5,
            name: "Block D - Cafeteria",
            location: { x: 400, y: 250 },
            rtsp_url: "rtsp://camera5.local:554/stream",
            priority: "low"
        },
        {
            id: 6,
            name: "Block E - Library",
            location: { x: 500, y: 300 },
            rtsp_url: "rtsp://camera6.local:554/stream",
            priority: "low"
        }
    ],

    // UI Configuration
    UI: {
        THEME: "dark",
        SIDEBAR_WIDTH: "256px",
        NOTIFICATION_DURATION: 5000,
        ANIMATION_DURATION: 300,
        REFRESH_BUTTON_COOLDOWN: 2000,
    },

    // Color Schemes
    COLORS: {
        SAFE: {
            PRIMARY: "#10b981",    // green-500
            BACKGROUND: "#064e3b", // green-900
            TEXT: "#6ee7b7"        // green-300
        },
        WARNING: {
            PRIMARY: "#f59e0b",    // yellow-500
            BACKGROUND: "#78350f", // yellow-900
            TEXT: "#fcd34d"        // yellow-300
        },
        DANGER: {
            PRIMARY: "#ef4444",    // red-500
            BACKGROUND: "#7f1d1d", // red-900
            TEXT: "#fca5a5"        // red-300
        },
        INFO: {
            PRIMARY: "#3b82f6",    // blue-500
            BACKGROUND: "#1e3a8a", // blue-900
            TEXT: "#93c5fd"        // blue-300
        }
    },

    // Sound Configuration
    SOUNDS: {
        ENABLE_AUDIO: true,
        SIREN_FREQUENCY: 800,      // Hz
        SIREN_DURATION: 3000,      // milliseconds
        SIREN_VOLUME: 0.3,         // 0.0 to 1.0
        NOTIFICATION_VOLUME: 0.5,
    },

    // API Endpoints (for backend integration)
    API: {
        BASE_URL: "http://127.0.0.1:8000/api",
        ENDPOINTS: {
            CAMERAS: "/cameras/",
            DETECTION: "/fire-detection/",
            INCIDENTS: "/fire-detection/",
            ALERTS: "/fire-detection/emergency_alert/",
            STATS: "/fire-detection/statistics/",
            PERFORMANCE: "/fire-detection/performance_metrics/",
            TEST_CONNECTION: "/fire-detection/test_connection/",
            EMERGENCY: "/emergency-contacts/"
        },
        TIMEOUT: 10000, // milliseconds
        RETRY_ATTEMPTS: 3
    },

    // WebSocket Configuration (for real-time updates)
    WEBSOCKET: {
        URL: "ws://localhost:8000/ws/fire-detection/",
        RECONNECT_INTERVAL: 5000,
        MAX_RECONNECT_ATTEMPTS: 10,
        HEARTBEAT_INTERVAL: 30000
    },

    // Storage Configuration
    STORAGE: {
        INCIDENT_IMAGES_PATH: "/uploads/incidents/",
        SNAPSHOTS_PATH: "/uploads/snapshots/",
        REPORTS_PATH: "/uploads/reports/",
        MAX_IMAGE_SIZE: 5242880, // 5MB in bytes
    },

    // Building Layout Configuration
    BUILDING: {
        FLOORS: [
            {
                id: 1,
                name: "Ground Floor",
                areas: ["Entrance", "Reception", "Cafeteria", "Security Office"]
            },
            {
                id: 2,
                name: "First Floor",
                areas: ["Lab 1", "Lab 2", "Lab 3", "Office Block A"]
            },
            {
                id: 3,
                name: "Second Floor",
                areas: ["Library", "Auditorium", "Office Block B", "Server Room"]
            }
        ],
        EVACUATION_ROUTES: [
            {
                from: "Block A - Lab 3",
                to: "Main Exit",
                route: ["Corridor A", "Staircase 1", "Ground Floor", "Main Exit"]
            },
            {
                from: "Block B - Entrance",
                to: "Emergency Exit",
                route: ["Emergency Exit B"]
            }
        ]
    },

    // Reporting Configuration
    REPORTS: {
        AUTO_GENERATE: true,
        FORMATS: ["PDF", "CSV", "JSON"],
        SCHEDULE: "daily", // daily, weekly, monthly
        RECIPIENTS: [
            "admin@company.com",
            "safety@company.com",
            "security@company.com"
        ]
    },

    // Advanced Features
    FEATURES: {
        ENABLE_ANALYTICS: true,
        ENABLE_PREDICTIONS: true,
        ENABLE_VOICE_ALERTS: true,
        ENABLE_MOBILE_PUSH: true,
        ENABLE_CLOUD_BACKUP: true,
        ENABLE_FACIAL_RECOGNITION: false, // For people counting accuracy
        ENABLE_SMOKE_ANALYSIS: true,
        ENABLE_HEAT_DETECTION: true
    },

    // Development Settings
    DEBUG: {
        ENABLE_CONSOLE_LOGS: true,
        ENABLE_SIMULATION: true,
        SIMULATION_INTERVAL: 10000,
        MOCK_DATA: true
    }
};

// Export configuration for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

// Make configuration available globally
if (typeof window !== 'undefined') {
    window.FIRE_DETECTION_CONFIG = CONFIG;
}
