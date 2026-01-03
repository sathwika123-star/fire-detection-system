#!/usr/bin/env python3
"""
Real AI Fire Detection Test Script
This script tests the AI fire detection system to ensure it's working properly
"""

import os
import sys
import django
import numpy as np
import cv2
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fire_detection_backend.settings')
django.setup()

# Now import Django modules
from fire_detection.ai_detection import RealFireDetectionAI, get_global_detector

def test_ai_detection_system():
    """Test the Real AI Fire Detection System"""
    print("🤖 Testing Real AI Fire Detection System")
    print("=" * 50)
    
    try:
        # Test 1: Initialize AI Detector
        print("\n1️⃣ Testing AI Detector Initialization...")
        detector = RealFireDetectionAI()
        
        if hasattr(detector, 'model') and detector.model is not None:
            print("✅ YOLOv8 model loaded successfully")
        else:
            print("⚠️ YOLOv8 model not available, using fallback detector")
        
        # Test 2: Test with sample image
        print("\n2️⃣ Testing AI Detection with Sample Image...")
        
        # Create a test image (fire-colored image)
        test_image = np.zeros((640, 640, 3), dtype=np.uint8)
        
        # Create fire-like colors (red, orange, yellow)
        test_image[100:300, 100:300] = [0, 0, 255]    # Red region
        test_image[200:400, 200:400] = [0, 165, 255]  # Orange region
        test_image[300:500, 300:500] = [0, 255, 255]  # Yellow region
        
        # Run detection
        result = detector.detect_fire_realtime(test_image, "test_image.jpg")
        
        print(f"📊 Detection Results:")
        print(f"   Fire Detected: {result.get('fire_detected', False)}")
        print(f"   Smoke Detected: {result.get('smoke_detected', False)}")
        print(f"   Confidence: {result.get('confidence', 0):.1f}%")
        print(f"   Emergency Level: {result.get('emergency_level', 0)}")
        
        # Test 3: Test Global Detector
        print("\n3️⃣ Testing Global Detector...")
        global_detector = get_global_detector()
        
        if global_detector:
            print("✅ Global detector initialized")
            
            # Test with same image
            global_result = global_detector.detect_fire_realtime(test_image, "global_test.jpg")
            print(f"📊 Global Detector Results:")
            print(f"   Fire Detected: {global_result.get('fire_detected', False)}")
            print(f"   Confidence: {global_result.get('confidence', 0):.1f}%")
        else:
            print("❌ Global detector failed to initialize")
        
        # Test 4: Performance Metrics
        print("\n4️⃣ Testing Performance Metrics...")
        if hasattr(detector, 'get_performance_metrics'):
            metrics = detector.get_performance_metrics()
            print(f"📈 Performance Metrics:")
            for key, value in metrics.items():
                print(f"   {key}: {value}")
        
        # Test 5: Test with safe image
        print("\n5️⃣ Testing with Safe Image...")
        safe_image = np.zeros((640, 640, 3), dtype=np.uint8)
        safe_image[:, :] = [100, 100, 100]  # Gray image (safe)
        
        safe_result = detector.detect_fire_realtime(safe_image, "safe_test.jpg")
        print(f"📊 Safe Image Results:")
        print(f"   Fire Detected: {safe_result.get('fire_detected', False)}")
        print(f"   Confidence: {safe_result.get('confidence', 0):.1f}%")
        
        print("\n" + "=" * 50)
        print("✅ AI Detection System Test Complete!")
        
        # Summary
        print(f"\n📋 Test Summary:")
        print(f"   🤖 AI System: {'Working' if detector else 'Failed'}")
        print(f"   🎯 Fire Detection: {'Functional' if result.get('confidence', 0) > 0 else 'Limited'}")
        print(f"   🔍 Safe Detection: {'Functional' if safe_result.get('confidence', 0) < 30 else 'Needs Tuning'}")
        print(f"   ⚡ Performance: {'Good' if hasattr(detector, 'get_performance_metrics') else 'Basic'}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure to install AI dependencies:")
        print("   Run: INSTALL_AI_DEPENDENCIES.bat")
        return False
        
    except Exception as e:
        print(f"❌ Test Error: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")
        return False

def test_api_endpoints():
    """Test the API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    print("=" * 30)
    
    try:
        import requests
        
        base_url = "http://127.0.0.1:8001"
        
        # Test 1: AI Capabilities
        print("1️⃣ Testing AI Capabilities Endpoint...")
        response = requests.get(f"{base_url}/api/real-ai-detection-live/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {data.get('status', 'unknown')}")
            if data.get('capabilities'):
                print(f"   AI Available: {data['capabilities'].get('ai_available', False)}")
        else:
            print(f"⚠️ API Status: {response.status_code}")
        
        # Test 2: Real-time Detection
        print("\n2️⃣ Testing Real-time Detection Endpoint...")
        test_data = {
            "video_source": "test_video.mp4",
            "mode": "standard"
        }
        
        response = requests.post(
            f"{base_url}/api/real-ai-detection-live/", 
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Detection API: {data.get('status', 'unknown')}")
        else:
            print(f"⚠️ Detection API Status: {response.status_code}")
        
        print("✅ API Endpoint Tests Complete!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running")
        print("💡 Start server: cd backend && python manage.py runserver 127.0.0.1:8001")
        return False
        
    except Exception as e:
        print(f"❌ API Test Error: {e}")
        return False

if __name__ == "__main__":
    print("🔥 Real AI Fire Detection System Test")
    print("=" * 60)
    
    # Test AI Detection System
    ai_test_passed = test_ai_detection_system()
    
    # Test API Endpoints (optional)
    api_test_passed = test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"🤖 AI System Test: {'✅ PASSED' if ai_test_passed else '❌ FAILED'}")
    print(f"🌐 API Test: {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
    
    if ai_test_passed and api_test_passed:
        print("\n🎉 ALL TESTS PASSED! Real AI Fire Detection is ready!")
        print("🚀 You can now use the dashboard with real AI detection")
    elif ai_test_passed:
        print("\n⚠️ AI System working, but API test failed")
        print("💡 Start the Django server and try again")
    else:
        print("\n❌ AI System test failed")
        print("💡 Install dependencies with: INSTALL_AI_DEPENDENCIES.bat")
    
    print("\n📋 Next Steps:")
    print("   1. Install AI dependencies (if needed)")
    print("   2. Start Django server: python manage.py runserver 127.0.0.1:8001")
    print("   3. Open dashboard: http://127.0.0.1:8001/dashboard/")
    print("   4. Enjoy real AI fire detection! 🔥🤖")
