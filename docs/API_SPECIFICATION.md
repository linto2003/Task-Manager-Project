# TeamLink — REST API Specification & OpenAPI Documentation

## 1. API Architecture Principles

TeamLink provides a clean, predictable REST API built with **Django REST Framework (DRF)**.

### 1.1 Key API Conventions
- **Base URI:** `/api/v1/` or `/api/`
- **Transport:** HTTPS in production; JSON payloads with `Content-Type: application/json`.
- **Authentication Header:** `Authorization: Bearer <FIREBASE_ID_TOKEN>` on all protected endpoints.
- **Idempotency:** `GET`, `PUT`, `DELETE` operations are strictly idempotent. `PATCH` applies partial updates.

### 1.2 Interactive OpenAPI Documentation
Interactive Swagger UI and ReDoc endpoints are generated automatically via **`drf-spectacular`**:
- **OpenAPI 3.0 Schema (YAML/JSON):** `GET /api/schema/`
- **Swagger UI:** `GET /api/docs/`
- **ReDoc UI:** `GET /api/redoc/`

---

## 2. Standard Response & Error Format

### 2.1 Success Response Envelope
```json
{
  "success": true,
  "data": {
    "id": 101,
    "title": "Configure PostgreSQL Migration Pipeline",
    "status": "IN_PROGRESS",
    "priority": "HIGH"
  },
  "meta": {
    "timestamp": "2026-10-18T06:00:00Z"
  }
}
```

### 2.2 Error Response Envelope
```json
{
  "success": false,
  "error": {
    "code": "TASK_ADMIN_REQUIRED",
    "message": "Cannot assign users to a task without a designated Task Admin.",
    "details": {
      "field": "task_admin"
    }
  }
}
```

---

## 3. Core Resource Endpoints

### 3.1 Accounts Endpoints (`/api/accounts/`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/accounts/me/` | Retrieve profile of the authenticated user. | Yes |
| `PATCH` | `/api/accounts/me/` | Update user details (name, notification settings). | Yes |
| `POST` | `/api/accounts/sync/` | Sync profile details from Firebase payload. | Yes |

### 3.2 Organizations Endpoints (`/api/organizations/`)
| Method | Endpoint | Description | Permitted Action |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/organizations/` | List organizations the user belongs to. | Authenticated |
| `POST` | `/api/organizations/` | Create a new organization tenant. | Authenticated |
| `GET` | `/api/organizations/{slug}/` | Retrieve organization tenant details. | `organization.view` |
| `PATCH` | `/api/organizations/{slug}/` | Update organization name and settings. | `organization.update` |
| `GET` | `/api/organizations/{slug}/members/` | List members of the organization. | `organization.view` |
| `POST` | `/api/organizations/{slug}/members/` | Invite or add a user to the organization. | `organization.manage_members` |
| `DELETE` | `/api/organizations/{slug}/members/{user_id}/` | Remove a member from the organization. | `organization.manage_members` |

### 3.3 Teams & Projects Endpoints
| Method | Endpoint | Description | Permitted Action |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/organizations/{slug}/teams/` | List teams within an organization. | `organization.view` |
| `POST` | `/api/organizations/{slug}/teams/` | Create a team. | `team.create` |
| `POST` | `/api/teams/{id}/members/` | Add user to team. | `team.manage_members` |
| `GET` | `/api/organizations/{slug}/projects/` | List projects in organization. | `organization.view` |
| `POST` | `/api/organizations/{slug}/projects/` | Create a project workspace. | `project.create` |
| `GET` | `/api/projects/{id}/` | Retrieve project details and workflow. | `project.view` |
| `PATCH` | `/api/projects/{id}/` | Update project configuration. | `project.update` |

### 3.4 Tasks Endpoints (`/api/tasks/`)
| Method | Endpoint | Description | Permitted Action |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/tasks/` | List tasks (filters: `is_personal`, `project`, `status`, `assigned_me`). | `task.view` |
| `POST` | `/api/tasks/` | Create a new task (personal or project-scoped). | `task.create` |
| `GET` | `/api/tasks/{id}/` | Retrieve full task details. | `task.view` |
| `PATCH` | `/api/tasks/{id}/` | Update title, description, priority, or status. | `task.update` |
| `DELETE` | `/api/tasks/{id}/` | Delete task. | `task.delete` |
| `POST` | `/api/tasks/{id}/admin/` | Designate or transfer Task Admin. | `task.manage_admin` |
| `GET` | `/api/tasks/{id}/assignments/` | List users assigned to task. | `task.view` |
| `POST` | `/api/tasks/{id}/assignments/` | Assign user (requires valid Task Admin!). | `task.assign` |
| `DELETE` | `/api/tasks/{id}/assignments/{assignment_id}/` | Remove an assignee. | `task.assign` |
| `GET` | `/api/tasks/{id}/subtasks/` | List subtasks. | `task.view` |
| `POST` | `/api/tasks/{id}/subtasks/` | Create subtask under parent. | `task.create` |
| `GET` | `/api/tasks/{id}/comments/` | List discussion comments. | `task.view` |
| `POST` | `/api/tasks/{id}/comments/` | Add a comment to task. | `task.comment` |

### 3.5 Permissions & Workflows Endpoints
| Method | Endpoint | Description | Permitted Action |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/permissions/actions/` | List all available atomic actions in catalog. | Authenticated |
| `GET` | `/api/permissions/roles/` | List custom roles for active organization. | `permissions.manage` |
| `POST` | `/api/permissions/roles/` | Create custom role with action list. | `permissions.manage` |
| `POST` | `/api/permissions/grants/` | Grant role/action to user with scope. | `permissions.manage` |
| `POST` | `/api/permissions/denials/` | Apply explicit negative permission denial. | `permissions.manage` |
| `GET` | `/api/workflows/` | List workflows in organization. | `organization.view` |
| `POST` | `/api/workflows/` | Create workflow with states & transitions. | `workflow.configure` |
