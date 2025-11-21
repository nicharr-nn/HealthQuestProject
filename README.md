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

5. **Access the Application:**
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- PgAdmin: `http://localhost:8081`
- Django Admin: `http://localhost:8000/admin`

6. **Create Superuser (First Time Only)**
```bash
# Create Django superuser
docker-compose exec backend python manage.py createsuperuser
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

**Activate the virtual environment:**
 **macOS/Linux**

  ```bash
  source venv/bin/activate
  ```
   
  **Windows**

  ```bash
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
python manage.py loaddata fixtures/sample_data.json
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
``bash
# Start all services
docker-compose up

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up --build

```
### Without Docker

#### Run Backend
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
python manage.py runserver
```