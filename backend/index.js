import express from "express";
import axios from "axios";
import pkg from "pg";
const { Pool } = pkg;

const app = express();
const PORT = 5050;

const pool = new Pool({
  user: "postgres",
  host: "db",
  database: "learning",
  password: "postgres",
  port: 5432,
});

app.get("/", (req, res) => {
  res.send("Backend is running ");
});

// Chatbot API
app.get("/api/chatbot", async (req, res) => {
  try {
    const query = req.query.q || "";
    if (!query) return res.status(400).json({ error: "Missing query" });

    const response = await axios.get("http://mlservice:8000/chatbot", {
      params: { query },
    });

    const coursesResult = await pool.query(
      "SELECT * FROM courses WHERE LOWER(category) = LOWER($1) LIMIT 5",
      [response.data.category || ""]
    );

    await pool.query(
      "INSERT INTO search_logs(query, response, category) VALUES($1,$2,$3)",
      [query, response.data.response, response.data.category]
    );

    res.json({
      ...response.data,
      courses: coursesResult.rows || [],
    });
  } catch (err) {
    console.error("Chatbot error:", err.message);
    res.status(500).json({ error: "ML service unavailable" });
  }
});

// Admin stats
app.get("/api/admin/stats", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT category, COUNT(*) as searches
      FROM search_logs
      WHERE category IS NOT NULL
      GROUP BY category
      ORDER BY searches DESC
    `);

    const topCourses = await pool.query(`
      SELECT c.title, COUNT(*) as count
      FROM search_logs s
      JOIN courses c ON LOWER(s.category) = LOWER(c.category)
      GROUP BY c.title
      ORDER BY count DESC
      LIMIT 5
    `);

    res.json({
      categories: result.rows,
      topCourses: topCourses.rows,
    });
  } catch (err) {
    console.error("Stats error:", err.message);
    res.status(500).json({ error: "Failed to fetch stats" });
  }
});

app.listen(PORT, () =>
  console.log(`Backend running on http://localhost:${PORT}`)
);
