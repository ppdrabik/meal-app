# Deal&Meal

Prosty prototyp fullstack na podstawie ekranów z PDF/Figmy.

## Stack

- Frontend: React + Vite
- Backend: FastAPI
- Baza danych: SQLite + SQLAlchemy

## Uruchomienie

### Backend

Nic nie musisz instalować ani konfigurować dla bazy. `SQLite` utworzy plik bazy automatycznie przy pierwszym starcie backendu.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
npm install
npm run dev
```

Frontend oczekuje API pod `http://127.0.0.1:8000`.
