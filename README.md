### The project includes:

Frontend (React + Material-UI + Nginx) → User interface

Backend (Node.js + Express + PostgreSQL) → API, course DB & chatbot orchestration

ML Service (FastAPI) → Simple Tensorflow model returning predictions (can be extended with a complex TensorFlow framework)

Database (Postgres) → Stores courses & search logs

### Features

AI Chatbot --- Ask about topics like Python, Web Development, Data Science

Course Recommender --- Suggests courses from the Postgres DB

Admin Dashboard --- Shows top searched categories & courses

Persistent Database --- Courses + search logs stored in PostgreSQL

One-click deployment with Docker Compose


### How to Run 
This project is built with React, Node.js, Express, PostgreSQL, TensorFlow, and is completely containerized with Docker.
It is very easy to run on your local computer.
1. Install Docker
2. Open the bash
3. git clone "your clone link"
4. cd ai-learning-platform
5. docker-compose build --no-cache
6. docker-compose up

### After Docker Compose -- For Live Demo, just open the link

http://0.0.0.0:8501/

###Other Access
1. Frontend (React UI): http://localhost:3000

2. Backend (Node API): http://localhost:5050

3. ML Service (FastAPI + TensorFlow): http://localhost:8000

4. Database (Postgres): localhost:5432 (user: postgres, password: postgres, db: learning)


### Contact
smhasnats@gmail.com
