CREATE TABLE courses (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT,
  description TEXT
);

CREATE TABLE search_logs (
  id SERIAL PRIMARY KEY,
  query TEXT NOT NULL,
  response TEXT,
  category TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO courses (title, category, description) VALUES
('Python for Beginners', 'Python', 'Start coding with Python basics'),
('Advanced Python', 'Python', 'Deep dive into Python advanced topics'),
('Intro to Web Development', 'Web Development', 'Learn HTML, CSS, JS basics'),
('Data Science 101', 'Data Science', 'Introductory data science course'),
('Machine Learning with TensorFlow', 'Data Science', 'Hands-on ML using TensorFlow');
