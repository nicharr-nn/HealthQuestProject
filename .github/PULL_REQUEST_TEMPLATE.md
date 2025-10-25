## Description
This pull request includes the following changes:
- Improves UI/UX styles across the user dashboard
- Adds CRUD APIs and tests for Recipe models.
- Cleans up unused code and improves readability.
- Adds Docker Hub integration for frontend and backend images.
- Adds pgAdmin container for PostgreSQL management.

## Type of Change
- [X] feat (new functionality)
- [X] fix (non-breaking change that fixes an issue)
- [X] refactor (code restructuring without changing functionality)
- [X] style (code style improvements, formatting)
- [X] test (adding or updating tests))

## Changes Introduced

### workflow
- Add ESLint test

### Build / Frontend
- **Fixed Rollup binary issue**
  - Ensured correct Rollup behavior on ARM64 systems.
  - Updated Dockerfile to use **Node 20.19 LTS**, compatible with Vite 7.
  - Cleaned up Docker volumes to preserve `node_modules`.

### Backend / Infrastructure
-  **Added pgAdmin container** in `docker-compose.yml` for easier PostgreSQL visualization and management.
  - Uses `dpage/pgadmin4` image.
  - Configured ports and environment variables via `.env`.
  - Added persistent `pgadmin_data` volume for configuration storage.
  - Added Hub repository with images
  - Add Recipe, workoutassignment models
  - Add api CRUD for recipe
  - Add test for recipe access and create
- Added pgAdmin service to docker-compose.yml for database visualization.
       Image: dpage/pgadmin4
      Port: 8081
      Persistent volume: pgadmin_data
- Added Docker Hub image build and push workflows (primfordatabase/healthquestproject-*).
- Added new Recipe and WorkoutAssignment models.
- Implemented CRUD APIs for Recipe.
- Added unit tests for Recipe access and creation logic.

## Testing Checklist
- Verified frontend builds successfully under Node 20.19.
- Confirmed Rollup no longer throws module resolution errors.
- Confirmed pgAdmin accessible at http://localhost:8081/.
- Verified PostgreSQL and pgAdmin containers network correctly (depends_on: db).
- Tested backend CRUD endpoints for Recipe.

## Checklist
- [x] Docker build completes successfully
- [x] Frontend serves correctly with Vite
- [x] Rollup binary issue resolved on ARM & x64
- [x] pgAdmin container operational and connected to Postgres
- [x] Updated `.env.example` with new pgAdmin vars
- [x] Lint tests pass (ESLint & Prettier) 

## Technical Checklist
- [ ] Code follows project style guidelines
- [ ] No console errors in browser developer tools
- [ ] API endpoints return expected status codes
- [ ] Database migrations work correctly

## Database Changes
- [X] New migrations added
- [ ] Existing migrations modified

## Steps to check
1. rm -nodemodules
2. npm install in frontend
3. docker-compose up --build
4. if you can't use frontend remove nodemodules, package-lock.json and docker-compose up --build frontend
5. docker-compose exec backend python manage.py migrate
6. docker-compose exec backend python manage.py createsuperuser
7. docker pull primfordatabase/healthquestproject-frontend:latest
8. docker pull primfordatabase/healthquestproject-backend:latest