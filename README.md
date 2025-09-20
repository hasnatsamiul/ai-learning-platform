# ai-learning-platform

## How to Run 
This project is built with React, Node.js, Express, PostgreSQL, TensorFlow, and is completely containerized with Docker.
It is very easy to run on your local computer.



The project includes:

Frontend (React + Material-UI + Nginx) → User interface

Backend (Node.js + Express + PostgreSQL) → API, course DB & chatbot orchestration

ML Service (FastAPI) → Dummy ML model returning predictions (extendable with TensorFlow/PyTorch)

Database (Postgres) → Stores courses & search logs

##Features

AI Chatbot → Ask about topics like Python, Web Development, Data Science

Course Recommender → Suggests courses from the Postgres DB

Admin Dashboard → Shows top searched categories & courses

Persistent Database → Courses + search logs stored in PostgreSQL

One-click deployment with Docker Compose
