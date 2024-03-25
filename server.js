//react-scripts start - was old start command

const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware to parse JSON
app.use(express.json());

app.get('/api/data', (req, res) => {
    const dataPath = path.join(__dirname, 'db.json'); // Adjust if your db.json is in another directory
    const fileContent = fs.readFileSync(dataPath, 'utf8');
    res.json(JSON.parse(fileContent));
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
