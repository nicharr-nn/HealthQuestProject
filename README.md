# HealthQuestProject
HealthQuest is a fitness platform that combines structured workout programs, gamified progression, and nutrition tracking. Users set goals, earn XP, and unlock new features as they advance through Bronze, Silver, and Gold levels. With coach-member support, personalized guidance, and private recipe sharing, HealthQuest fosters sustainable healthy habits in an engaging and supportive ecosystem. <br/>
This app was created as part of the [Individual Software Process](https://cpske.github.io/ISP/) course at [Kasetsart University](https://www.ku.ac.th/th).

**Running the Backend Development Server**

**Clone the Repository:**
```bash
git clone https://github.com/nicharr-nn/HealthQuestProject.git
cd HealthQuestProject
```
**Navigate to the backend directory and create a virtual environment:**
```bash
cd backend
python -m venv venv
```

**Activate the virtual environment:**
 **macOS/Linux**

  ```bash
  source venv/bin/activate
  ```
   
  **Windows**

  ```bash
  .venv\Scripts\activate
  ```


**Install dependencies and load data:**
```bash
pip install -r requirements.txt
```
**Run the migrations**
```bash
python manage.py migrate
```

**start the development server:**
```bash
python manage.py runserver
```
## Running the Frontend Development Server

**Navigate to the frontend directory:**
```bash
cd ../frontend
```

**Install dependencies and start the development server:**
```bash
npm install
npm run dev
```

## Set up Guideline for .env file
[env](https://docs.google.com/document/d/1h1x5TZ3u6hHrHdlbAVwmRFn0uFI_wlpZDJ_6jKpH0ww/edit?tab=t.uiqgvupjbb5p#heading=h.43vfy3c0u3ty)
