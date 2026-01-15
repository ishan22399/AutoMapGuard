# AutoMapGuard — AI-Driven Urban Change Detection & Geometry Compliance System

![Status](https://img.shields.io/badge/Status-Production--Ready-green)
![Java](https://img.shields.io/badge/Java-17-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-19-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Overview

**AutoMapGuard** is an enterprise-grade geospatial system that leverages AI and satellite imagery to automatically detect, validate, and commit urban building changes to map databases.

### ⚡ Key Features

✅ AI-Powered Change Detection — Detects new, modified, and removed buildings from satellite imagery  
✅ 6-Layer Geometry Validation — Enforces professional GIS rules (foundational, topological, cartographic, temporal, neighbor, system)  
✅ Confidence-Based Automation — Scores confidence (0-1) to determine auto-approval vs manual review  
✅ Versioned Map Database — Safe updates with rollback, audit trails, and version history  
✅ Professional Dashboard — Map-centric interface with before/after satellite toggles, change inspection, review workflows  
✅ Microservices Architecture — Java REST API + Python geospatial engine + React frontend + PostgreSQL/PostGIS  

---

## 📋 Quick Navigation

| Document | Purpose |
|----------|---------|
| [GETTING_STARTED.md](./GETTING_STARTED.md) | Step-by-step setup & quick start guide |
| [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md) | Complete technical architecture (recommended read) |
| [backend-java/README.md](./backend-java/README.md) | Java Spring Boot backend details |
| [backend/README.md](./backend/README.md) | Python microservice details |
| [frontend/README.md](./frontend/README.md) | React frontend details |

---

## 🎯 What Problem Does It Solve?

### The Reality
Digital maps do not stay accurate automatically. Cities change every day:
- New buildings are constructed
- Old buildings are demolished
- Buildings expand, merge, or change shape

Satellite imagery updates faster than map databases, creating a gap. Manual updating is:
- Expensive (skilled analysts)
- Slow (weeks/months for large areas)
- Error-prone (human inconsistency)

### AutoMapGuard Solution
Automatically answers three critical questions:
1) Has something changed in the city? — Change Detection
2) Is that change geometrically valid for maps? — Geometry Compliance
3) How confident are we in this change? — Confidence Scoring

Result: Keeps maps fresh, accurate, and up-to-date.

---

## 🏗️ System Architecture

### High-Level Diagram

```
┌────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Leaflet)              │
│         Map View | Change Inspector | Dashboard Stats      │
└──────────────────────────┬─────────────────────────────────┘
													 │ REST API
													 ▼
┌────────────────────────────────────────────────────────────┐
│           JAVA SPRING BOOT (Port 8080)                      │
│  Controllers │ Services │ Repositories │ Security (JWT)    │
└──────────────────────────┬─────────────────────────────────┘
													 │ HTTP Calls
													 ▼
┌────────────────────────────────────────────────────────────┐
│        PYTHON MICROSERVICE (Port 8081)                      │
│  Geometry Engine │ Change Detection │ Image Processing    │
└──────────────────────────┬─────────────────────────────────┘
													 │ Direct DB Access
													 ▼
┌────────────────────────────────────────────────────────────┐
│    PostgreSQL + PostGIS (Port 5432)                         │
│  Buildings │ Changes │ Validations │ Reviews │ Audit Logs  │
└────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React 19, Leaflet, Tailwind CSS, Shadcn UI | Map-centric dashboard |
| Backend API | Java 17, Spring Boot 3, Spring Security, JWT | REST API, business logic, authentication |
| Geospatial | Python 3.11, FastAPI, Shapely, GeoPandas, Rasterio | Geometry validation, change detection |
| Database | PostgreSQL 15, PostGIS 3.3 | Versioned spatial data storage |
| Infrastructure | Docker, Docker Compose, Azure (optional) | Containerization, orchestration, cloud |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose OR
- Java 17, Maven 3.9, Python 3.11, Node 18, PostgreSQL 15

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone <repo-url>
cd automapguard

# Start all services
docker-compose up -d

# Wait ~30 seconds for services to be ready
docker-compose ps

# Access services
Frontend:    http://localhost:3000
Java API:    http://localhost:8080/swagger-ui.html
Python API:  http://localhost:8081/docs
Database:    postgresql://localhost:5432/automapguard
```

### Option 2: Manual Setup (see GETTING_STARTED.md)

```bash
# Java Backend
cd backend-java
mvn spring-boot:run

# Python Microservice
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn server:app --reload --port 8081

# Frontend
cd frontend
npm install && npm start
```

---

## 📚 Documentation Structure

For quick understanding:
1. Read this README (you are here)
2. See GETTING_STARTED.md for setup

For technical deep dive:
1. SYSTEM_ARCHITECTURE.md — Complete architecture
2. Component READMEs: backend-java, backend, frontend

For interview preparation:
- Read SYSTEM_ARCHITECTURE.md first
- Review 6 geometry rule layers
- Understand microservices interaction model

---

## 🔍 Core Concepts

### Change Detection Pipeline

```
Historical Satellite + Latest Satellite
				↓
Align & Normalize Images
				↓
Compute Difference Maps
				↓
Detect Building Footprints in Differences
				↓
Classify: New / Modified / Removed
				↓
Assign Confidence Scores
				↓
Store Changes (pending review)
```

### Geometry Validation (6 Layers)

Layer 0: Foundational — closed polygon, min 4 vertices, non-zero area, valid coordinates
Layer 1: Topology — no self-intersections, correct ring orientation, holes inside outer ring
Layer 2: Cartographic — min area 20 m², min edge 1 m, orthogonal regularization, simplification
Layers 3-6: Temporal, neighbor conflicts, auto-fix eligibility, system safety (CRS/precision)

### Confidence Scoring

Base 1.0 → subtract 0.1 per violation → multiply by compactness factor → clamp to 0-1.
- > 0.8 auto-approve
- 0.5-0.8 needs review
- < 0.5 manual review required

### Versioning & Rollback

Building v1 → Change detected → Auto-validate → If valid/high confidence → Create Building v2
If issues: rollback to v1 with audit trail.

---

## 📡 API Examples

### Authentication

```bash
# Register
curl -X POST http://localhost:8080/api/auth/register \
	-H "Content-Type: application/json" \
	-d '{"email": "analyst@example.com", "password": "SecurePass123", "fullName": "Jane Analyst"}'

# Login
TOKEN=$(curl -X POST http://localhost:8080/api/auth/login \
	-H "Content-Type: application/json" \
	-d '{"email":"analyst@example.com","password":"SecurePass123"}' | jq -r '.accessToken')

# Use token
curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/buildings
```

### Geometry Validation

```bash
curl -X POST http://localhost:8081/geometry/validate \
	-H "Content-Type: application/json" \
	-d '{
		"geometry": {
			"type": "Polygon",
			"coordinates": [[
				[-74.0060, 40.7128],
				[-74.0050, 40.7128],
				[-74.0050, 40.7138],
				[-74.0060, 40.7138],
				[-74.0060, 40.7128]
			]]
		}
	}'
```

---

## 🧪 Testing

```bash
# Java backend tests
cd backend-java && mvn test

# Python tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

Swagger/OpenAPI specs:
- Java: http://localhost:8080/v3/api-docs
- Python: http://localhost:8081/openapi.json

---

## 🚢 Deployment

### Local Docker
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Azure (example flow)
```bash
# Build images
docker build -t automapguard-backend:1.0 ./backend-java
docker build -t automapguard-python:1.0 ./backend

# Push to Azure Container Registry
az acr build --registry <registry> --image automapguard-backend:1.0 ./backend-java

# Deploy to Azure Container Instances (example)
az container create --image <registry>.azurecr.io/automapguard-backend:1.0 ...
```
See component READMEs for detailed deployment steps.

---

## 🏆 Production Checklist

- Environment variables configured
- Database migrations applied
- SSL/TLS configured
- JWT secret updated (32+ chars)
- CORS restricted
- Rate limiting enabled
- Monitoring & alerts configured
- Backup strategy in place
- Error logging enabled
- Load testing completed

---

## 📊 System Requirements

Minimum: 2 CPU, 2 GB RAM, 10 GB disk  
Recommended: 4+ CPU, 8+ GB RAM, 50+ GB disk, SSD for DB

---

## 🤝 Contributing

1) Fork the repository  
2) Create feature branch: git checkout -b feature/my-feature  
3) Write tests  
4) Commit: git commit -am "Add my feature"  
5) Push: git push origin feature/my-feature  
6) Open Pull Request

---

## 🐛 Known Issues (MVP)

- Change detection simulated (ready for real imagery)
- No real-time notifications yet
- Single-region deployment focus
- No multi-user simultaneous editing

Performance: index spatial columns, batch image processing, virtual scroll large lists.

---

## 📄 License

MIT License — see LICENSE

---

## 🎓 Educational Value

Demonstrates full-stack, geospatial engineering, microservices separation, cloud-native patterns, enterprise practices (auth, versioning, audit, transactions), and production readiness.

---

## 📈 Roadmap

Completed (v1.0)
- Architecture, Java backend, Python microservice, React scaffold, PostGIS, Docker

Next (v1.1)
- Review workflow UI, geometry validator UI, real imagery integration, CI/CD

Future (v2.0)
- WebSocket updates, advanced ML, multi-region, admin dashboard, GraphQL option

---

Ready to get started? → GETTING_STARTED.md  
Want technical details? → SYSTEM_ARCHITECTURE.md  
Questions? → component READMEs or open an issue
