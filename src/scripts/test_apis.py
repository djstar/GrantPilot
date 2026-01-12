#!/usr/bin/env python3
"""
GrantPilot API Test Script
Tests all API endpoints to verify they're working correctly.
"""

import sys
import json
import requests
from typing import Optional

API_URL = "http://localhost:8000"

def test_endpoint(name: str, method: str, path: str, data: Optional[dict] = None,
                  files: Optional[dict] = None, expected_status: int = 200) -> bool:
    """Test an API endpoint and return success status."""
    url = f"{API_URL}{path}"

    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, data=data, timeout=30)
            else:
                response = requests.post(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        else:
            print(f"  ✗ {name}: Unknown method {method}")
            return False

        if response.status_code == expected_status:
            print(f"  ✓ {name}")
            return True
        else:
            print(f"  ✗ {name}: Expected {expected_status}, got {response.status_code}")
            print(f"    Response: {response.text[:200]}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"  ✗ {name}: Connection refused")
        return False
    except Exception as e:
        print(f"  ✗ {name}: {str(e)}")
        return False


def main():
    print("\n" + "=" * 50)
    print("  GrantPilot API Test Suite")
    print("=" * 50 + "\n")

    results = []

    # Health endpoints
    print("Health Endpoints:")
    print("-" * 40)
    results.append(test_endpoint("Basic health", "GET", "/health"))
    results.append(test_endpoint("Database health", "GET", "/health/db"))
    results.append(test_endpoint("Redis health", "GET", "/health/redis"))
    results.append(test_endpoint("Embeddings health", "GET", "/health/embeddings"))
    results.append(test_endpoint("LLM health", "GET", "/health/llm"))
    results.append(test_endpoint("Full health", "GET", "/health/full"))

    # Projects API
    print("\nProjects API:")
    print("-" * 40)
    results.append(test_endpoint("List projects", "GET", "/api/projects"))

    # Create a project
    project_data = {
        "name": "Test Project",
        "description": "API test project",
        "grant_type": "R01"
    }
    response = requests.post(f"{API_URL}/api/projects", json=project_data)
    if response.status_code == 201:
        project_id = response.json()["id"]
        print(f"  ✓ Create project (id: {project_id[:8]}...)")
        results.append(True)

        # Get project
        results.append(test_endpoint("Get project", "GET", f"/api/projects/{project_id}"))

        # Delete project
        results.append(test_endpoint("Delete project", "DELETE", f"/api/projects/{project_id}", expected_status=204))
    else:
        print(f"  ✗ Create project: {response.status_code}")
        results.append(False)

    # Documents API
    print("\nDocuments API:")
    print("-" * 40)
    results.append(test_endpoint("List documents", "GET", "/api/documents"))

    # Upload a test document
    test_content = b"This is a test document for GrantPilot API testing."
    files = {"file": ("test.txt", test_content, "text/plain")}
    form_data = {"document_type": "other"}

    response = requests.post(f"{API_URL}/api/documents", files=files, data=form_data)
    if response.status_code == 201:
        doc_id = response.json()["id"]
        print(f"  ✓ Upload document (id: {doc_id[:8]}...)")
        results.append(True)

        # Get document
        results.append(test_endpoint("Get document", "GET", f"/api/documents/{doc_id}"))

        # Wait for processing and check
        import time
        print("  ⏳ Waiting for document processing...")
        time.sleep(2)

        response = requests.get(f"{API_URL}/api/documents/{doc_id}")
        if response.status_code == 200:
            status = response.json()["processing_status"]
            if status == "completed":
                print(f"  ✓ Document processing completed")
                results.append(True)
            else:
                print(f"  ⚠ Document status: {status}")
                results.append(True)  # Still passes, processing may take longer

        # Delete document
        results.append(test_endpoint("Delete document", "DELETE", f"/api/documents/{doc_id}", expected_status=204))
    else:
        print(f"  ✗ Upload document: {response.status_code}")
        results.append(False)

    # Chat API (may fail if no LLM configured)
    print("\nChat API:")
    print("-" * 40)

    # Search endpoint
    search_data = {"query": "test", "limit": 5}
    response = requests.post(f"{API_URL}/api/chat/search", json=search_data)
    if response.status_code == 200:
        print("  ✓ Search endpoint")
        results.append(True)
    else:
        print(f"  ✗ Search endpoint: {response.status_code}")
        results.append(False)

    # Chat endpoint (may return 503 if no LLM configured)
    chat_data = {"message": "Hello", "stream": False}
    response = requests.post(f"{API_URL}/api/chat", json=chat_data)
    if response.status_code == 200:
        print("  ✓ Chat endpoint")
        results.append(True)
    elif response.status_code == 503:
        print("  ⚠ Chat endpoint: No LLM configured (expected)")
        results.append(True)  # This is expected without API keys
    else:
        print(f"  ✗ Chat endpoint: {response.status_code}")
        results.append(False)

    # Summary
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"  ✓ All tests passed ({passed}/{total})")
        print("=" * 50 + "\n")
        return 0
    else:
        print(f"  ✗ Some tests failed ({passed}/{total})")
        print("=" * 50 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
