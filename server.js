const express = require('express');
const path = require('path');
const app = express();

// Serve all files in the current directory as static
app.use(express.static(__dirname));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// No need for a separate route for products.html; static middleware handles it

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
