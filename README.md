# 2D Mapping - Building Detection System

## Overview

Geospatial application for automated building change detection and management using satellite imagery analysis with GIS validation.

### Features

- AI-powered building change detection (new, modified, removed)
- Multi-layer geometry validation with professional GIS rules
- Confidence scoring system for automated approval workflows
- Map-centric dashboard with satellite imagery comparison
- Microservices architecture (Java, Python, React, PostgreSQL/PostGIS)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | React 18.2, Leaflet, Tailwind CSS, Shadcn UI |
| Backend API | Java 17, Spring Boot, Spring Security, JWT |
| Geospatial Service | Python 3.11, FastAPI, Shapely, GeoPandas |
| Database | PostgreSQL 15+ with PostGIS |
| Build Tools | Maven, npm, Create React App with Craco |

## Prerequisites

- Java 17+
- Maven 3.9+
- Python 3.11+
- Node.js 18+ with npm
- PostgreSQL 15+ with PostGIS

## Setup & Installation

### 1. Backend (Java Spring Boot)
```bash
cd backend-java
mvn clean install
mvn spring-boot:run
```
Runs on http://localhost:8080

### 2. Python Microservice
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python -m uvicorn server:app --reload --port 8081
```
Runs on http://localhost:8081

### 3. Frontend
```bash
cd frontend
npm install
npm start
```
Runs on http://localhost:3000

## API Endpoints

- Frontend: http://localhost:3000
- Java API: http://localhost:8080/api
- Swagger UI: http://localhost:8080/swagger-ui.html
- Python API: http://localhost:8081
- Python Docs: http://localhost:8081/docs

## Environment Configuration

### Frontend `.env`
```env
REACT_APP_BACKEND_URL=http://localhost:8080
REACT_APP_PYTHON_SERVICE_URL=http://localhost:8081
WDS_SOCKET_PORT=3000
```

## Core Functionality

### Geometry Validation Layers
- **Layer 0**: Foundational (closed polygon, min 4 vertices, valid coordinates)
- **Layer 1**: Topology (no self-intersections, correct orientation)
- **Layer 2**: Cartographic (min area 20 m², min edge 1 m, regularization)
- **Layers 3-6**: Temporal, neighbor conflicts, auto-fix, system safety

### Confidence Scoring
Automatic confidence calculation (0-1 scale) determines approval workflow:
- 0.8+ → Auto-approve
- 0.5-0.8 → Review required
- <0.5 → Manual review

## API Examples

### Authentication
```bash
# Register
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123","fullName":"User Name"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123"}'
```

### Geometry Validation
```bash
curl -X POST http://localhost:8081/geometry/validate \
  -H "Content-Type: application/json" \
  -d '{
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[-74.0060,40.7128],[-74.0050,40.7128],[-74.0050,40.7138],[-74.0060,40.7138],[-74.0060,40.7128]]]
    }
  }'
```

## Testing

```bash
# Java backend
cd backend-java && mvn test

# Python service
cd backend && pytest

# Frontend
cd frontend && npm test
```

## Project Status

### Current Implementation
- Backend API with JWT authentication
- Python geospatial service operational
- React frontend application
- Multi-layer geometry validation
- Confidence scoring algorithm

### In Development
- Satellite imagery integration
- Enhanced dashboard UI
- Real-time notifications
- Batch processing

## License

MIT License
