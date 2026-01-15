# 2D Mapping — Urban Building Detection & Change Management System

![Status](https://img.shields.io/badge/Status-Development-yellow)
![Java](https://img.shields.io/badge/Java-17-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Overview

**2D Mapping** is a geospatial system for detecting and managing urban building changes using AI and satellite imagery with professional GIS validation.

### ⚡ Key Features

✅ **AI-Powered Change Detection** — Detects new, modified, and removed buildings from satellite imagery  
✅ **6-Layer Geometry Validation** — Enforces professional GIS rules (foundational, topological, cartographic, temporal, neighbor, system)  
✅ **Confidence-Based Automation** — Scores confidence (0-1) to determine auto-approval vs manual review  
✅ **Versioned Map Database** — Safe updates with rollback, audit trails, and version history  
✅ **Professional Dashboard** — Map-centric interface with before/after satellite toggles, change inspection, review workflows  
✅ **Microservices Architecture** — Java REST API + Python geospatial engine + React frontend + PostgreSQL/PostGIS  

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
| **Frontend** | React 18.2, Leaflet 1.9.4, Tailwind CSS 3.4, Shadcn UI, React Router 7.5 | Map-centric dashboard |
| **Backend API** | Java 17, Spring Boot 3.x, Spring Security, JWT | REST API, business logic, authentication |
| **Geospatial** | Python 3.11, FastAPI, Shapely, GeoPandas, Rasterio | Geometry validation, change detection |
| **Database** | PostgreSQL 15+, PostGIS 3.3+ | Versioned spatial data storage |
| **Build Tools** | Maven 3.9+, Create React App 5.0 with Craco 7.1, npm/yarn | Project build and dependency management |
| **Infrastructure** | Docker, Docker Compose | Containerization, local development |

---

## 🚀 Quick Start

### Prerequisites
- **Java 17+** (JDK)
- **Maven 3.9+**
- **Python 3.11+**
- **Node.js 18+** with npm
- **PostgreSQL 15+** with PostGIS extension

### Local Development Setup

#### 1. Backend (Java Spring Boot)
```bash
cd backend-java
mvn clean install
mvn spring-boot:run
# Runs on http://localhost:8080
```

#### 2. Python Microservice
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn server:app --reload --port 8081
# Runs on http://localhost:8081
```

#### 3. Frontend (React)
```bash
cd frontend
npm install
npm start
# Runs on http://localhost:3000
```

### Access Points
- **Frontend Dashboard**: http://localhost:3000
- **Java API**: http://localhost:8080/api
- **Java Swagger**: http://localhost:8080/swagger-ui.html
- **Python API**: http://localhost:8081
- **Python Docs**: http://localhost:8081/docs
- **Database**: postgresql://localhost:5432/2dmapping

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

### Backend Testing
```bash
# Java backend tests
cd backend-java
mvn test

# Python microservice tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### API Documentation
- **Java Swagger UI**: http://localhost:8080/swagger-ui.html
- **Java OpenAPI**: http://localhost:8080/v3/api-docs
- **Python FastAPI Docs**: http://localhost:8081/docs
- **Python OpenAPI**: http://localhost:8081/openapi.json

---

## 🚢 Deployment

### Local Development
Each service runs independently on its own port:
- Frontend: Port 3000
- Java Backend: Port 8080  
- Python Service: Port 8081
- PostgreSQL: Port 5432

### Environment Configuration

#### Frontend `.env`
```env
REACT_APP_BACKEND_URL=http://localhost:8080
REACT_APP_PYTHON_SERVICE_URL=http://localhost:8081
WDS_SOCKET_PORT=3000
ENABLE_HEALTH_CHECK=false
NODE_ENV=development
```

#### Backend Configuration
See `backend-java/src/main/resources/application.yml` and `backend/.env` for database and service configurations.

### Production Considerations
- Set secure JWT secrets (32+ characters)
- Configure CORS for production domains
- Enable HTTPS/TLS
- Set up database backups
- Configure logging and monitoring
- Use environment-specific configuration files

---

## 🏆 Development Checklist

**Backend Setup**
- ✅ Java 17+ installed and configured
- ✅ Maven dependencies resolved
- ✅ PostgreSQL database running
- ✅ Spring Boot application starts successfully
- ✅ JWT authentication configured

**Python Service**
- ✅ Python 3.11+ virtual environment created
- ✅ All pip dependencies installed
- ✅ FastAPI server starts successfully
- ✅ Geometry validation endpoints working

**Frontend Setup**
- ✅ Node.js 18+ and npm installed
- ✅ All npm packages installed (React 18.2, dependencies)
- ✅ Environment variables configured (.env file)
- ✅ Development server runs on port 3000
- ✅ No ESLint errors or warnings

**Integration**
- ✅ Frontend connects to backend API
- ✅ Backend communicates with Python service
- ✅ Database migrations applied
- ✅ CORS configured for localhost
- ✅ All services accessible from browser

---

## 📊 System Requirements

### Development Environment
- **Minimum**: 4 GB RAM, 2 CPU cores, 20 GB disk space
- **Recommended**: 8 GB RAM, 4 CPU cores, 50 GB disk space (SSD preferred)

### Software Requirements
- **Java**: JDK 17 or higher
- **Maven**: 3.9 or higher
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **PostgreSQL**: 15 or higher with PostGIS extension
- **Git**: Latest version

### Operating Systems
- ✅ Windows 10/11
- ✅ macOS 12+
- ✅ Linux (Ubuntu 20.04+, Debian 11+)

---

## 🤝 Contributing

1) Fork the repository  
2) Create feature branch: git checkout -b feature/my-feature  
3) Write tests  
4) Commit: git commit -am "Add my feature"  
5) Push: git push origin feature/my-feature  
6) Open Pull Request

---

## 🐛 Known Issues & Status

### Current Status
- ✅ Backend API fully functional
- ✅ Python geospatial service operational
- ✅ Frontend React application running
- ✅ Authentication and JWT working
- ⚠️ Change detection using simulated data (ready for real imagery integration)
- ⚠️ Frontend components scaffolded (UI implementation in progress)

### Known Limitations
- Change detection currently simulates satellite imagery analysis
- Review workflow UI needs enhancement
- No real-time WebSocket notifications yet
- Single-user focus (multi-user editing not implemented)
- Performance optimizations needed for large datasets

### Planned Improvements
- Integrate real satellite imagery processing
- Complete dashboard UI components
- Add real-time change notifications
- Implement batch processing for large areas
- Add comprehensive test coverage

---

## 📄 License

MIT License — see LICENSE

---

## 🎓 Project Highlights

### Technical Demonstrations
- **Full-Stack Development**: Java backend, Python microservice, React frontend
- **Microservices Architecture**: Service separation with clear responsibilities
- **Geospatial Engineering**: PostGIS, Shapely, geometry validation
- **Modern Frontend**: React 18.2, Tailwind CSS, Shadcn UI components
- **API Design**: RESTful principles, Swagger/OpenAPI documentation
- **Security**: JWT authentication, Spring Security, role-based access
- **Database Design**: Spatial data modeling, versioning, audit trails
- **Build Tools**: Maven, npm, Create React App with Craco

### Software Engineering Practices
- Clean code architecture
- Separation of concerns
- Comprehensive error handling
- API documentation
- Environment-based configuration
- Version control best practices

---

## 📈 Roadmap

### ✅ Completed (Current Version)
- Full microservices architecture
- Java Spring Boot backend with JWT authentication
- Python FastAPI geospatial service
- React 18.2 frontend with Tailwind CSS
- PostgreSQL with PostGIS spatial database
- 6-layer geometry validation system
- Confidence scoring algorithm
- REST API endpoints
- Basic dashboard structure

### 🚧 In Progress
- Complete dashboard UI components
- Review workflow interface
- Real satellite imagery integration
- Map visualization enhancements
- Test coverage expansion

### 📅 Planned (Next Release)
- WebSocket real-time notifications
- Advanced change detection algorithms
- Batch processing capabilities
- Admin dashboard
- Performance optimizations
- CI/CD pipeline setup

### 🔮 Future Enhancements
- Multi-region support
- Advanced ML models
- GraphQL API option
- Mobile application
- Offline mode support

---

## 📞 Support & Documentation

- **Getting Started**: See [GETTING_STARTED.md](./GETTING_STARTED.md) for detailed setup instructions
- **Architecture**: Review [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md) for technical details
- **Backend API**: Check [backend-java/README.md](./backend-java/README.md)
- **Python Service**: See [backend/README.md](./backend/README.md)  
- **Frontend**: Visit [frontend/README.md](./frontend/README.md)
- **Issues**: Report bugs or request features via GitHub Issues

---

## 🙏 Acknowledgments

Built with:
- Spring Boot for robust backend services
- FastAPI for high-performance Python APIs
- React for dynamic user interfaces
- PostgreSQL/PostGIS for spatial data management
- Leaflet for interactive mapping

---

**Ready to start?** → Follow the Quick Start guide above  
**Need help?** → Check the documentation files or open an issue  
**Want to contribute?** → See the Contributing section above
