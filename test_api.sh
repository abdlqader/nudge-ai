#!/bin/bash

# Test script for AI Agent API with external authentication

echo "🧪 Testing AI Agent API with External Authentication"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000"
NUDGE_API_URL="http://localhost:8080"

# 1. Health check
echo "1️⃣  Health Check"
echo "   Request: GET $BASE_URL/health"
curl -s $BASE_URL/health | jq '.'
echo ""

# 2. Login to Nudge API
echo "2️⃣  Login to Nudge API (external)"
echo "   Request: POST $NUDGE_API_URL/auth/login"
LOGIN_RESPONSE=$(curl -s -X POST $NUDGE_API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mk.com", "password": "Testing123"}')

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')

if [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ]; then
    echo "   ✅ Login successful!"
    echo "   Token: ${TOKEN:0:30}..."
    echo ""
else
    echo "   ❌ Login failed!"
    echo "   Response: $LOGIN_RESPONSE"
    exit 1
fi

# 3. Check agent status
echo "3️⃣  Agent Status"
echo "   Request: GET $BASE_URL/agent/status"
curl -s $BASE_URL/agent/status | jq '.'
echo ""

# 4. Send message without token (should work but tasks may fail)
echo "4️⃣  Message without authentication"
echo "   Request: POST $BASE_URL/agent/message (no token)"
curl -s -X POST $BASE_URL/agent/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Can you help me manage tasks?"}' | jq '.'
echo ""

# 5. Send message with token - health check
echo "5️⃣  Message with authentication - Health Check"
echo "   Request: POST $BASE_URL/agent/message (with token)"
curl -s -X POST $BASE_URL/agent/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Check if the Nudge API is healthy"}' | jq '.'
echo ""

# 6. Create a task
echo "6️⃣  Create a task"
echo "   Request: POST $BASE_URL/agent/message (with token)"
curl -s -X POST $BASE_URL/agent/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Create a task called Test Task in ACTION category for Work"}' | jq '.'
echo ""

# 7. Get all tasks
echo "7️⃣  Get all tasks"
echo "   Request: POST $BASE_URL/agent/message (with token)"
curl -s -X POST $BASE_URL/agent/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Show me all my tasks"}' | jq '.'
echo ""

echo "✅ Test complete!"
echo ""
echo "Note: Token is provided per-request via Authorization header"
echo "      No server-side session storage"
