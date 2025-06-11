#!/usr/bin/env python3
"""
Network Test Script for Myriad-Mind Phase 2 Step 2.3
Tests network communication between Lightbulb_Definition_AI and Lightbulb_Function_AI agents
"""

import requests
import json
import time
import threading
import sys
import os
from multiprocessing import Process
import subprocess

# Add agents to Python path
sys.path.append('agents/lightbulb_definition_ai')
sys.path.append('agents/lightbulb_function_ai')

from agents.lightbulb_definition_ai.app import app as definition_app
from agents.lightbulb_function_ai.app import app as function_app

class NetworkTester:
    def __init__(self):
        self.definition_port = 5001
        self.function_port = 5002
        self.definition_url = f"http://localhost:{self.definition_port}"
        self.function_url = f"http://localhost:{self.function_port}"
        self.test_results = []
        
    def start_agents(self):
        """Start both agents in separate processes"""
        print("🚀 Starting agents...")
        
        # Start Definition AI
        def run_definition_agent():
            definition_app.run(host='0.0.0.0', port=self.definition_port, debug=False)
            
        # Start Function AI  
        def run_function_agent():
            function_app.run(host='0.0.0.0', port=self.function_port, debug=False)
            
        # Start processes
        self.definition_process = Process(target=run_definition_agent)
        self.function_process = Process(target=run_function_agent)
        
        self.definition_process.start()
        self.function_process.start()
        
        # Wait for agents to start
        print("⏳ Waiting for agents to initialize...")
        time.sleep(3)
        
    def stop_agents(self):
        """Stop both agents"""
        print("🛑 Stopping agents...")
        if hasattr(self, 'definition_process'):
            self.definition_process.terminate()
            self.definition_process.join()
        if hasattr(self, 'function_process'):
            self.function_process.terminate()
            self.function_process.join()
            
    def test_health_endpoints(self):
        """Test health endpoints for both agents"""
        print("\n🔍 Testing Health Endpoints...")
        
        # Test Definition AI health
        try:
            response = requests.get(f"{self.definition_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.test_results.append({
                    'test': 'Definition AI Health Check',
                    'status': 'PASS',
                    'response_code': response.status_code,
                    'response_data': data
                })
                print(f"✅ Definition AI Health: {data}")
            else:
                self.test_results.append({
                    'test': 'Definition AI Health Check',
                    'status': 'FAIL',
                    'response_code': response.status_code,
                    'error': 'Non-200 status code'
                })
                print(f"❌ Definition AI Health: HTTP {response.status_code}")
        except Exception as e:
            self.test_results.append({
                'test': 'Definition AI Health Check',
                'status': 'FAIL',
                'error': str(e)
            })
            print(f"❌ Definition AI Health: {str(e)}")
            
        # Test Function AI health
        try:
            response = requests.get(f"{self.function_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.test_results.append({
                    'test': 'Function AI Health Check',
                    'status': 'PASS',
                    'response_code': response.status_code,
                    'response_data': data
                })
                print(f"✅ Function AI Health: {data}")
            else:
                self.test_results.append({
                    'test': 'Function AI Health Check',
                    'status': 'FAIL',
                    'response_code': response.status_code,
                    'error': 'Non-200 status code'
                })
                print(f"❌ Function AI Health: HTTP {response.status_code}")
        except Exception as e:
            self.test_results.append({
                'test': 'Function AI Health Check',
                'status': 'FAIL',
                'error': str(e)
            })
            print(f"❌ Function AI Health: {str(e)}")
            
    def test_definition_queries(self):
        """Test definition queries to Lightbulb_Definition_AI"""
        print("\n🔍 Testing Definition Queries...")
        
        test_cases = [
            {'intent': 'define', 'expected_success': True},
            {'intent': 'invalid_intent', 'expected_success': False},
            {'invalid_key': 'value', 'expected_success': False}
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                response = requests.post(
                    f"{self.definition_url}/query",
                    json=test_case,
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                
                data = response.json()
                
                if test_case['expected_success']:
                    if response.status_code == 200 and 'success' in data and data['success']:
                        self.test_results.append({
                            'test': f'Definition Query {i+1} (Valid)',
                            'status': 'PASS',
                            'response_code': response.status_code,
                            'response_data': data
                        })
                        print(f"✅ Definition Query {i+1}: {data}")
                    else:
                        self.test_results.append({
                            'test': f'Definition Query {i+1} (Valid)',
                            'status': 'FAIL',
                            'response_code': response.status_code,
                            'error': 'Expected success but got failure'
                        })
                        print(f"❌ Definition Query {i+1}: Expected success but got {data}")
                else:
                    if response.status_code == 400 or (response.status_code == 200 and not data.get('success', True)):
                        self.test_results.append({
                            'test': f'Definition Query {i+1} (Invalid)',
                            'status': 'PASS',
                            'response_code': response.status_code,
                            'response_data': data
                        })
                        print(f"✅ Definition Query {i+1}: Correctly rejected invalid request")
                    else:
                        self.test_results.append({
                            'test': f'Definition Query {i+1} (Invalid)',
                            'status': 'FAIL',
                            'response_code': response.status_code,
                            'error': 'Expected failure but got success'
                        })
                        print(f"❌ Definition Query {i+1}: Expected failure but got {data}")
                        
            except Exception as e:
                self.test_results.append({
                    'test': f'Definition Query {i+1}',
                    'status': 'FAIL',
                    'error': str(e)
                })
                print(f"❌ Definition Query {i+1}: {str(e)}")
                
    def test_function_queries(self):
        """Test function queries to Lightbulb_Function_AI"""
        print("\n🔍 Testing Function Queries...")
        
        test_cases = [
            {'intent': 'explain_limitation', 'expected_success': True, 'description': 'Critical roadmap requirement'},
            {'intent': 'turn_on', 'expected_success': True, 'description': 'Function operation'},
            {'intent': 'turn_off', 'expected_success': True, 'description': 'Function operation'},
            {'intent': 'dim', 'level': 50, 'expected_success': True, 'description': 'Function with parameter'},
            {'intent': 'status', 'expected_success': True, 'description': 'Status query'},
            {'intent': 'invalid_intent', 'expected_success': False, 'description': 'Invalid intent'},
            {'invalid_key': 'value', 'expected_success': False, 'description': 'Invalid request format'}
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                # Extract description and expected_success for logging
                description = test_case.pop('description', '')
                expected_success = test_case.pop('expected_success')
                
                response = requests.post(
                    f"{self.function_url}/query",
                    json=test_case,
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                
                data = response.json()
                
                if expected_success:
                    if response.status_code == 200 and 'success' in data and data['success']:
                        self.test_results.append({
                            'test': f'Function Query {i+1} ({description})',
                            'status': 'PASS',
                            'response_code': response.status_code,
                            'response_data': data
                        })
                        print(f"✅ Function Query {i+1} ({description}): {data}")
                    else:
                        self.test_results.append({
                            'test': f'Function Query {i+1} ({description})',
                            'status': 'FAIL',
                            'response_code': response.status_code,
                            'error': 'Expected success but got failure'
                        })
                        print(f"❌ Function Query {i+1} ({description}): Expected success but got {data}")
                else:
                    if response.status_code == 400 or (response.status_code == 200 and not data.get('success', True)):
                        self.test_results.append({
                            'test': f'Function Query {i+1} ({description})',
                            'status': 'PASS',
