import requests
import sys
import json
from datetime import datetime

class AutoMapGuardAPITester:
    def __init__(self, base_url="https://urbandetector.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.user_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_base}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and len(response_data) <= 3:
                        print(f"   Response: {response_data}")
                    elif isinstance(response_data, list):
                        print(f"   Response: List with {len(response_data)} items")
                    else:
                        print(f"   Response: {type(response_data).__name__}")
                except:
                    print(f"   Response: Non-JSON response")
                return True, response.json() if response.content else {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        return success

    def test_register(self):
        """Test user registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_user = {
            "email": f"test_user_{timestamp}@example.com",
            "password": "TestPass123!",
            "full_name": f"Test User {timestamp}"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=test_user
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_id = response.get('user', {}).get('id')
            print(f"   Token obtained: {self.token[:20]}...")
            return True
        return False

    def test_login(self):
        """Test user login with existing credentials"""
        # Try to login with the registered user
        if not self.token:
            return False
            
        # For now, we'll use the token from registration
        # In a real test, we'd test login separately
        return True

    def test_get_me(self):
        """Test get current user info"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        return success

    def test_detect_changes(self):
        """Test change detection simulation"""
        success, response = self.run_test(
            "Detect Changes (Simulation)",
            "POST",
            "changes/detect",
            200,
            data={"simulate": True}
        )
        
        if success and isinstance(response, list):
            print(f"   Detected {len(response)} changes")
            return len(response) > 0
        return False

    def test_list_changes(self):
        """Test listing changes"""
        success, response = self.run_test(
            "List Changes",
            "GET",
            "changes/list",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} changes")
            return True
        return False

    def test_geometry_validation(self):
        """Test geometry validation"""
        test_geometry = {
            "type": "Polygon",
            "coordinates": [[
                [-74.0060, 40.7128],
                [-74.0050, 40.7128],
                [-74.0050, 40.7138],
                [-74.0060, 40.7138],
                [-74.0060, 40.7128]
            ]]
        }
        
        success, response = self.run_test(
            "Geometry Validation",
            "POST",
            "geometry/validate",
            200,
            data={"geometry": test_geometry}
        )
        return success

    def test_review_queue(self):
        """Test review queue"""
        success, response = self.run_test(
            "Get Review Queue",
            "GET",
            "review-queue",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} review items")
            return True
        return False

    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        success, response = self.run_test(
            "Dashboard Statistics",
            "GET",
            "dashboard/stats",
            200
        )
        
        if success and isinstance(response, dict):
            required_fields = ['total_buildings', 'pending_changes', 'pending_reviews', 'total_detections', 'accuracy_rate']
            has_all_fields = all(field in response for field in required_fields)
            if has_all_fields:
                print(f"   Stats: {response}")
                return True
            else:
                print(f"   Missing required fields in response")
        return False

    def test_footprints_list(self):
        """Test listing building footprints"""
        success, response = self.run_test(
            "List Building Footprints",
            "GET",
            "footprints/list",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} footprints")
            return True
        return False

def main():
    print("🚀 Starting AutoMapGuard API Tests")
    print("=" * 50)
    
    tester = AutoMapGuardAPITester()
    
    # Test sequence
    tests = [
        ("Root Endpoint", tester.test_root_endpoint),
        ("User Registration", tester.test_register),
        ("Get Current User", tester.test_get_me),
        ("Change Detection", tester.test_detect_changes),
        ("List Changes", tester.test_list_changes),
        ("Geometry Validation", tester.test_geometry_validation),
        ("Review Queue", tester.test_review_queue),
        ("Dashboard Stats", tester.test_dashboard_stats),
        ("List Footprints", tester.test_footprints_list),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - Exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   - {test}")
    else:
        print("\n✅ All tests passed!")
    
    return 0 if len(failed_tests) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())