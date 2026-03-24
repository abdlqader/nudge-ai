"""
Nudge API Tools - Allows AI agent to interact with the Nudge API
Based on the Postman collection for authentication and task management
"""

import os
import requests
from typing import Optional, Dict, Any
from contextvars import ContextVar
from tools import ToolRegistry


# Context variable for thread-safe, request-scoped auth token
_auth_token: ContextVar[Optional[str]] = ContextVar('auth_token', default=None)


def _get_base_url() -> str:
    """Get the base URL from environment or use default"""
    return os.getenv("NUDGE_API_BASE_URL", "http://localhost:8080")


def _get_headers(include_auth: bool = False) -> Dict[str, str]:
    """Get request headers, optionally including auth token"""
    headers = {"Content-Type": "application/json"}
    if include_auth:
        token = _auth_token.get()
        if token:
            headers["Authorization"] = f"Bearer {token}"
    return headers


# Create registry for Nudge API tools
nudge_registry = ToolRegistry()

@nudge_registry.tool(
    description="Create a new task. Requires authentication. Returns created task details."
)
def create_task(
    name: str,
    task_category: str,
    status: str = "CREATED",
    expected_duration: Optional[int] = None,
    category: Optional[str] = None,
    notes: Optional[str] = None,
    start_at: Optional[int] = None
) -> dict:
    """
    Create a new task for the authenticated user
    
    Args:
        name: Task name/description
        task_category: Task category (ACTION, ANCHOR, or TRANSIT)
        status: Task status (default: CREATED)
        expected_duration: Expected duration in minutes
        category: User-defined category (e.g., Work, Health)
        notes: Additional notes
        start_at: Start time in minutes from midnight (e.g., 540 for 9:00 AM)
    
    Returns:
        dict: Created task details or error message
    """
    url = f"{_get_base_url()}/tasks"
    payload = {
        "name": name,
        "task_category": task_category,
        "status": status
    }
    
    if expected_duration is not None:
        payload["expected_duration"] = expected_duration
    if category:
        payload["category"] = category
    if notes:
        payload["notes"] = notes
    if start_at is not None:
        payload["start_at"] = start_at
    
    try:
        response = requests.post(url, json=payload, headers=_get_headers(include_auth=True))
        return {
            "success": response.status_code == 201,
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@nudge_registry.tool(
    description="Get all tasks for the authenticated user. Supports filtering by status, category, and search."
)
def get_all_tasks(
    status: Optional[str] = None,
    task_category: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None
) -> dict:
    """
    Retrieve all tasks for the authenticated user
    
    Args:
        status: Filter by status (CREATED, COMPLETED, FAILED, DEFERRED)
        task_category: Filter by task category (ACTION, ANCHOR, TRANSIT)
        category: Filter by user-defined category
        search: Search in task name (partial match)
    
    Returns:
        dict: List of tasks or error message
    """
    url = f"{_get_base_url()}/tasks"
    params = {}
    
    if status:
        params["status"] = status
    if task_category:
        params["task_category"] = task_category
    if category:
        params["category"] = category
    if search:
        params["search"] = search
    
    try:
        response = requests.get(url, params=params, headers=_get_headers(include_auth=True))
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@nudge_registry.tool(
    description="Get a specific task by ID. Requires authentication."
)
def get_task_by_id(task_id: str) -> dict:
    """
    Retrieve a specific task by its ID
    
    Args:
        task_id: UUID of the task
    
    Returns:
        dict: Task details or error message
    """
    url = f"{_get_base_url()}/tasks/{task_id}"
    
    try:
        response = requests.get(url, headers=_get_headers(include_auth=True))
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@nudge_registry.tool(
    description="Update an existing task. All fields are optional. Requires authentication."
)
def update_task(
    task_id: str,
    name: Optional[str] = None,
    status: Optional[str] = None,
    task_category: Optional[str] = None,
    expected_duration: Optional[int] = None,
    actual_duration: Optional[int] = None,
    category: Optional[str] = None,
    notes: Optional[str] = None,
    start_at: Optional[int] = None
) -> dict:
    """
    Update an existing task
    
    Args:
        task_id: UUID of the task to update
        name: Updated task name
        status: Updated status (CREATED, COMPLETED, FAILED, DEFERRED)
        task_category: Updated task category (ACTION, ANCHOR, TRANSIT)
        expected_duration: Updated expected duration in minutes
        actual_duration: Actual duration in minutes
        category: Updated user-defined category
        notes: Updated notes
        start_at: Updated start time in minutes from midnight
    
    Returns:
        dict: Updated task details or error message
    """
    url = f"{_get_base_url()}/tasks/{task_id}"
    payload = {}
    
    if name:
        payload["name"] = name
    if status:
        payload["status"] = status
    if task_category:
        payload["task_category"] = task_category
    if expected_duration is not None:
        payload["expected_duration"] = expected_duration
    if actual_duration is not None:
        payload["actual_duration"] = actual_duration
    if category:
        payload["category"] = category
    if notes:
        payload["notes"] = notes
    if start_at is not None:
        payload["start_at"] = start_at
    
    try:
        response = requests.put(url, json=payload, headers=_get_headers(include_auth=True))
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@nudge_registry.tool(
    description="Delete a task by ID. Requires authentication."
)
def delete_task(task_id: str) -> dict:
    """
    Delete a task
    
    Args:
        task_id: UUID of the task to delete
    
    Returns:
        dict: Deletion confirmation or error message
    """
    url = f"{_get_base_url()}/tasks/{task_id}"
    
    try:
        response = requests.delete(url, headers=_get_headers(include_auth=True))
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@nudge_registry.tool(
    description="Check if the Nudge API is running and healthy."
)
def health_check() -> dict:
    """
    Verify the Nudge API is operational
    
    Returns:
        dict: Health status or error message
    """
    url = f"{_get_base_url()}/health"
    
    try:
        response = requests.get(url)
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_auth_status() -> dict:
    """
    Check if user is currently authenticated
    
    Returns:
        dict: Authentication status information
    """
    token = _auth_token.get()
    return {
        "authenticated": token is not None,
        "token_present": bool(token)
    }


def set_auth_token(token: str) -> None:
    """
    Set the authentication token for API calls (request-scoped, thread-safe)
    
    Args:
        token: JWT token string
    """
    _auth_token.set(token)


def clear_auth_token() -> None:
    """Clear the stored authentication token (request-scoped, thread-safe)"""
    _auth_token.set(None)
