#!/bin/bash

# ==============================================================================
# API Endpoint Test Script
#
# This script tests the full CRUD (Create, Read, Delete) functionality of the
# timeline post API.
#
#   1. POST:    Creates a new post with random content.
#   2. GET:     Verifies that the new post was successfully added.
#   3. DELETE:  Deletes the post that was just created.
#   4. GET:     Verifies that the post has been successfully removed.
#
# ==============================================================================

# --- Configuration ---
API_URL="http://localhost:5000/api/timeline_post"

# --- Helper Function for Headers ---
print_header() {
  echo ""
  echo "================================================="
  echo "$1"
  echo "================================================="
}

# --- Generate Random Content ---
RANDOM_CONTENT="Test post content $(date +%s)"
echo "Generated unique content for this test run: '$RANDOM_CONTENT'"

# ==============================================================================
# STEP 1: CREATE a new timeline post (POST)
# ==============================================================================
print_header "STEP 1: Creating a new post via POST ${API_URL}"

# Use curl to send a POST request with form data. The -s flag makes it silent.
CREATE_RESPONSE=$(curl -s -X POST \
  -d "name=Shlok" \
  -d "email=Shlok@example.com" \
  -d "content=$RANDOM_CONTENT" \
  "$API_URL")

# A successful response should contain the random content.
if ! echo "$CREATE_RESPONSE" | grep -q "$RANDOM_CONTENT"; then
  echo "ERROR: Failed to create the post. Server response:"
  echo "$CREATE_RESPONSE"
  exit 1
fi

# Extract the ID of the newly created post from the JSON response.
POST_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id": *[0-9]*' | awk '{print $2}')

if [ -z "$POST_ID" ]; then
    echo "ERROR: Could not extract post ID from server response."
    echo "$CREATE_RESPONSE"
    exit 1
fi

echo "SUCCESS: Post created successfully. New post ID is $POST_ID."

# ==============================================================================
# STEP 2: VERIFY post creation (GET)
# ==============================================================================
print_header "STEP 2: Verifying post creation via GET ${API_URL}"

GET_RESPONSE=$(curl -s -X GET "$API_URL")

if ! echo "$GET_RESPONSE" | grep -q "$RANDOM_CONTENT"; then
  echo "TEST FAILED: The new post was NOT found in the timeline."
  echo "Server response:"
  echo "$GET_RESPONSE"
  exit 1
fi

echo "SUCCESS: The new post was found in the timeline. $GET_RESPONSE"

# ==============================================================================
# STEP 3: DELETE the created post (DELETE)
# ==============================================================================
print_header "STEP 3: Deleting the post via DELETE ${API_URL}/${POST_ID}"

DELETE_RESPONSE=$(curl -s -X DELETE "${API_URL}/${POST_ID}")

if ! echo "$DELETE_RESPONSE" | grep -q "success"; then
    echo "ERROR: The DELETE request failed."
    echo "Server response:"
    echo "$DELETE_RESPONSE"
    exit 1
fi

echo "SUCCESS: The DELETE request was successful."
echo "Server response: $DELETE_RESPONSE"

# ==============================================================================
# STEP 4: VERIFY post deletion (GET)
# ==============================================================================
print_header "STEP 4: Verifying post has been deleted via GET ${API_URL}"

FINAL_GET_RESPONSE=$(curl -s -X GET "$API_URL")

if echo "$FINAL_GET_RESPONSE" | grep -q "$RANDOM_CONTENT"; then
  echo "TEST FAILED: The deleted post was found in the timeline."
  echo "Server response:"
  echo "$FINAL_GET_RESPONSE"
  exit 1
fi

echo "SUCCESS: The post has been successfully removed from the timeline."
echo ""
echo "ALL TESTS PASSED!"

