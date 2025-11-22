# HealthQuestProject
HealthQuest is a fitness platform that combines structured workout programs, gamified progression, and nutrition tracking. Users set goals, earn XP, and unlock new features as they advance through Bronze, Silver, and Gold levels. With coach-member support, personalized guidance, and private recipe sharing, HealthQuest fosters sustainable healthy habits in an engaging and supportive ecosystem. <br/>
This app was created as part of the [Individual Software Process](https://cpske.github.io/ISP/) course at [Kasetsart University](https://www.ku.ac.th/th).

**Running the Backend Development Server**

**Clone the Repository:**
```bash
git clone https://github.com/nicharr-nn/HealthQuestProject.git
cd HealthQuestProject
```

## Installation

### Option 1: Docker (Recommended)
1. **create a .env file in the root directory:**
```bash
cp .env.example .env
# Edit .env with your settings
```
2. **create a virtual environment**
```bash
python -m venv venv
# Activate the virtual environment
# macOS/Linux
source venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. **Create a .env file in the backend directory:**
```bash
cd backend
cp .env.example .env
# Edit .env with your settings
cd ..
```

4. **Build and run the Docker containers:**
```bash
docker-compose up --build
# Or run in detached mode (background)
docker-compose up -d --build
```

5. **Run migrateions and load sample data:**
```bash
# Apply database migrations
docker-compose exec backend python manage.py migrate
# Load sample data (optional)
docker-compose exec backend python manage.py flush --no-input
docker-compose exec backend python manage.py loaddata mock_data/data.json
```

5. **Access the Application:**
- Backend API: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`
- PgAdmin: `http://127.0.0.1:8081`
- Django Admin: `http://127.0.0.1:8000/admin`

6. **Create Superuser (First Time Only)**
```bash
# Create Django superuser
docker-compose exec backend python manage.py createsuperuser
```
7. **If using mock data:**
```bash
# To login as a user from the mock data, use the dev-login endpoint
# Replace <username> with the desired username from the mock data
curl http://127.0.0.1:8000/dev-login/?username=<username>
# Then access the dashboard
curl http://127.0.0.1:5173/dashboard
# If coach, access coach dashboard
curl http://127.0.0.1:5173/coach-dashboard
```

### Option 2: Manual Setup & Running the Application

#### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```
2. **Create virtual environment:**
```bash
python -m venv venv
# Activate the virtual environment
# macOS/Linux
source venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional):**
```bash
python manage.py loaddata mock_data/data.json
curl http://127.0.0.1:8000/dev-login/?username=<username>
curl http://127.0.0.1:5173/dashboard
```

8. **Start the development server:**
```bash
python manage.py runserver
```
#### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies and start the development server:**
```bash
npm install
npm run dev
```

## Running the Application
### With Docker

#### Start all services
```bash
docker-compose up
```

#### Stop all services
```bash
docker-compose down
```

#### Rebuild after code changes
```bash
docker-compose up --build
```

### Without Docker

#### Run Backend
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
python manage.py runserver
```

#### Run Frontend
```bash
cd frontend
npm run dev
```

## Set up Guideline for .env file
[env](https://docs.google.com/document/d/1h1x5TZ3u6hHrHdlbAVwmRFn0uFI_wlpZDJ_6jKpH0ww/edit?tab=t.uiqgvupjbb5p#heading=h.43vfy3c0u3ty)