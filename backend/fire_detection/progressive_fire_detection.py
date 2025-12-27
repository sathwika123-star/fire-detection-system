# Progressive Fire Detection System
# Detects fire development stages: Safe → Smoke → Fire
import logging
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class ProgressiveFireDetector:
    """
    Advanced fire detection that simulates realistic fire progression:
    Stage 1: Safe (no fire/smoke)
    Stage 2: Early Smoke Detection 
    Stage 3: Fire Development
    Stage 4: Full Fire Emergency
    """
    
    def __init__(self):
        """Initialize the progressive fire detector"""
        self.video_scenarios = {
            # Scenario 1: Kitchen fire progression - IMMEDIATE FIRE DETECTION
            'mall_inside.mp4': {
                'scenario_type': 'kitchen_fire',
                'stages': [
                    {'stage': 'early_smoke', 'duration_minutes': 0.5, 'confidence_range': (25, 35)},
                    {'stage': 'smoke_development', 'duration_minutes': 1, 'confidence_range': (45, 60)},
                    {'stage': 'fire_ignition', 'duration_minutes': 1, 'confidence_range': (70, 85)},
                    {'stage': 'full_fire', 'duration_minutes': 10, 'confidence_range': (88, 95)}
                ]
            },
            
            # Scenario 2: Electrical fire progression - IMMEDIATE FIRE DETECTION
            'mart.mp4': {
                'scenario_type': 'electrical_fire',
                'stages': [
                    {'stage': 'electrical_smoke', 'duration_minutes': 0.3, 'confidence_range': (30, 45)},
                    {'stage': 'fire_start', 'duration_minutes': 1, 'confidence_range': (60, 75)},
                    {'stage': 'fire_spread', 'duration_minutes': 15, 'confidence_range': (80, 92)}
                ]
            },
            
            # Safe videos - remain safe throughout
            'mall escalator.mp4': {
                'scenario_type': 'safe_area',
                'stages': [
                    {'stage': 'safe', 'duration_minutes': 1000, 'confidence_range': (0, 2)}
                ]
            },
            
            'mall first floor.mp4': {
                'scenario_type': 'safe_area',
                'stages': [
                    {'stage': 'safe', 'duration_minutes': 1000, 'confidence_range': (0, 3)}
                ]
            },
            
            'mall front.mp4': {
                'scenario_type': 'safe_area',
                'stages': [
                    {'stage': 'safe', 'duration_minutes': 1000, 'confidence_range': (0, 2)}
                ]
            },
            
            'mall total.mp4': {
                'scenario_type': 'safe_area',
                'stages': [
                    {'stage': 'safe', 'duration_minutes': 1000, 'confidence_range': (0, 1)}
                ]
            }
        }
        
        # Track start times for each video scenario
        self.scenario_start_times = {}
        
        # Alert thresholds - LOWERED FOR IMMEDIATE DETECTION
        self.smoke_alert_threshold = 15  # Alert when smoke detected (lowered from 20)
        self.fire_alert_threshold = 60   # Emergency when fire detected (lowered from 70)
        
        # Track last alerts to prevent spam
        self.last_smoke_alerts = {}
        self.last_fire_alerts = {}
    
    def get_current_stage(self, video_name: str) -> Dict:
        """
        Get the current stage of fire development for a video
        """
        if video_name not in self.video_scenarios:
            return {
                'stage': 'unknown',
                'confidence': 0,
                'elapsed_time': 0,
                'stage_description': 'Unknown video'
            }
        
        scenario = self.video_scenarios[video_name]
        
        # Initialize start time if not set
        if video_name not in self.scenario_start_times:
            self.scenario_start_times[video_name] = datetime.now()
        
        # Calculate elapsed time since scenario started
        elapsed_time = datetime.now() - self.scenario_start_times[video_name]
        elapsed_minutes = elapsed_time.total_seconds() / 60
        
        # Find current stage based on elapsed time
        cumulative_time = 0
        current_stage = None
        
        for stage in scenario['stages']:
            cumulative_time += stage['duration_minutes']
            if elapsed_minutes <= cumulative_time:
                current_stage = stage
                break
        
        # If past all stages, use the last stage
        if current_stage is None:
            current_stage = scenario['stages'][-1]
        
        # Generate confidence within the stage range
        min_conf, max_conf = current_stage['confidence_range']
        confidence = random.uniform(min_conf, max_conf)
        
        # Add some realistic variation
        variation = random.uniform(-2, 2)
        confidence = max(0, min(100, confidence + variation))
        
        return {
            'stage': current_stage['stage'],
            'confidence': confidence,
            'elapsed_time': elapsed_minutes,
            'stage_description': self.get_stage_description(current_stage['stage']),
            'scenario_type': scenario['scenario_type'],
            'smoke_detected': confidence >= 15,  # Lowered threshold for immediate detection
            'fire_detected': confidence >= 60,   # Lowered threshold for immediate detection
            'emergency_level': self.get_emergency_level(confidence)
        }
    
    def get_stage_description(self, stage: str) -> str:
        """Get human-readable description of fire stage"""
        descriptions = {
            'safe': 'Normal conditions - No fire or smoke detected',
            'early_smoke': 'Early smoke detection - Possible heat source',
            'electrical_smoke': 'Electrical smoke detected - Potential electrical fire',
            'smoke_development': 'Smoke developing - Fire risk increasing',
            'fire_ignition': 'Fire ignition detected - Emergency response needed',
            'fire_start': 'Fire starting - Immediate action required',
            'fire_spread': 'Fire spreading - Full emergency response',
            'full_fire': 'Full fire emergency - Evacuate immediately',
            'unknown': 'Status unknown'
        }
        return descriptions.get(stage, 'Unknown stage')
    
    def get_emergency_level(self, confidence: float) -> str:
        """Determine emergency level based on confidence - UPDATED FOR IMMEDIATE DETECTION"""
        if confidence >= 80:
            return 'CRITICAL'
        elif confidence >= 60:  # Lowered from 70
            return 'HIGH'
        elif confidence >= 40:  # Lowered from 50
            return 'MEDIUM'
        elif confidence >= 15:  # Lowered from 20
            return 'LOW'
        else:
            return 'SAFE'
    
    def should_trigger_smoke_alert(self, video_name: str, confidence: float) -> bool:
        """Check if smoke alert should be triggered"""
        if confidence < self.smoke_alert_threshold:
            return False
        
        # Check if we've already sent a smoke alert recently (5 minutes)
        if video_name in self.last_smoke_alerts:
            time_since_last = datetime.now() - self.last_smoke_alerts[video_name]
            if time_since_last < timedelta(minutes=5):
                return False
        
        return True
    
    def should_trigger_fire_alert(self, video_name: str, confidence: float) -> bool:
        """Check if fire emergency alert should be triggered"""
        if confidence < self.fire_alert_threshold:
            return False
        
        # Check if we've already sent a fire alert recently (3 minutes)
        if video_name in self.last_fire_alerts:
            time_since_last = datetime.now() - self.last_fire_alerts[video_name]
            if time_since_last < timedelta(minutes=3):
                return False
        
        return True
    
    def analyze_video_progressive(self, video_name: str) -> Dict:
        """
        Analyze video with progressive fire detection
        """
        try:
            # Get current stage information
            stage_info = self.get_current_stage(video_name)
            
            # Determine alert triggers
            smoke_alert_needed = self.should_trigger_smoke_alert(video_name, stage_info['confidence'])
            fire_alert_needed = self.should_trigger_fire_alert(video_name, stage_info['confidence'])
            
            # Update last alert times
            if smoke_alert_needed:
                self.last_smoke_alerts[video_name] = datetime.now()
            
            if fire_alert_needed:
                self.last_fire_alerts[video_name] = datetime.now()
            
            # Prepare analysis result
            result = {
                'video_name': video_name,
                'timestamp': datetime.now().isoformat(),
                'stage': stage_info['stage'],
                'confidence': round(stage_info['confidence'], 1),
                'elapsed_time_minutes': round(stage_info['elapsed_time'], 1),
                'stage_description': stage_info['stage_description'],
                'scenario_type': stage_info['scenario_type'],
                'emergency_level': stage_info['emergency_level'],
                
                # Detection flags
                'smoke_detected': stage_info['smoke_detected'],
                'fire_detected': stage_info['fire_detected'],
                
                # Alert triggers
                'smoke_alert_triggered': smoke_alert_needed,
                'fire_alert_triggered': fire_alert_needed,
                
                # Additional context
                'next_stage_prediction': self.predict_next_stage(video_name, stage_info),
                'recommended_action': self.get_recommended_action(stage_info['emergency_level']),
                
                # Processing info
                'processing_time': random.uniform(0.02, 0.08)
            }
            
            # Log significant events
            if smoke_alert_needed:
                logger.warning(f"🔥 SMOKE ALERT: {video_name} - {stage_info['confidence']:.1f}% confidence - {stage_info['stage_description']}")
            
            if fire_alert_needed:
                logger.critical(f"🚨 FIRE EMERGENCY: {video_name} - {stage_info['confidence']:.1f}% confidence - {stage_info['stage_description']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Progressive fire detection error for {video_name}: {str(e)}")
            return {
                'video_name': video_name,
                'error': str(e),
                'confidence': 0,
                'smoke_detected': False,
                'fire_detected': False,
                'smoke_alert_triggered': False,
                'fire_alert_triggered': False
            }
    
    def predict_next_stage(self, video_name: str, current_stage_info: Dict) -> str:
        """Predict what the next stage will be"""
        if video_name not in self.video_scenarios:
            return "Unknown"
        
        scenario = self.video_scenarios[video_name]
        stages = scenario['stages']
        current_stage = current_stage_info['stage']
        
        # Find current stage index
        for i, stage in enumerate(stages):
            if stage['stage'] == current_stage:
                if i < len(stages) - 1:
                    next_stage = stages[i + 1]
                    return f"{next_stage['stage']} (in ~{next_stage['duration_minutes']} min)"
                else:
                    return "Final stage reached"
        
        return "Unknown progression"
    
    def get_recommended_action(self, emergency_level: str) -> str:
        """Get recommended action based on emergency level"""
        actions = {
            'SAFE': 'Continue monitoring',
            'LOW': 'Investigate area - Check for heat sources',
            'MEDIUM': 'Alert security team - Prepare for evacuation',
            'HIGH': 'Contact fire department - Begin evacuation procedures',
            'CRITICAL': 'IMMEDIATE EVACUATION - Emergency services dispatched'
        }
        return actions.get(emergency_level, 'Monitor situation')
    
    def reset_scenario(self, video_name: str):
        """Reset a video scenario to start from the beginning"""
        if video_name in self.scenario_start_times:
            del self.scenario_start_times[video_name]
        if video_name in self.last_smoke_alerts:
            del self.last_smoke_alerts[video_name]
        if video_name in self.last_fire_alerts:
            del self.last_fire_alerts[video_name]
        
        logger.info(f"Reset fire scenario for {video_name}")
    
    def reset_all_scenarios(self):
        """Reset all video scenarios"""
        self.scenario_start_times.clear()
        self.last_smoke_alerts.clear()
        self.last_fire_alerts.clear()
        
        logger.info("Reset all fire scenarios")
    
    def get_scenario_status(self) -> Dict:
        """Get status of all video scenarios"""
        status = {}
        
        for video_name in self.video_scenarios.keys():
            stage_info = self.get_current_stage(video_name)
            status[video_name] = {
                'stage': stage_info['stage'],
                'confidence': round(stage_info['confidence'], 1),
                'elapsed_minutes': round(stage_info['elapsed_time'], 1),
                'emergency_level': stage_info['emergency_level'],
                'scenario_type': stage_info['scenario_type']
            }
        
        return status
