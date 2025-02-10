// Backend: server.js
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(express.json());
app.use(cors());

// Create database connection
const db = new sqlite3.Database(path.join(__dirname, 'ecommerce.db'), (err) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('Connected to SQLite database');
  }
});

// Database setup queries
const setupQueries = [
  `CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
  )`,
  
  `CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image_url TEXT
  )`,
  
  `CREATE TABLE IF NOT EXISTS cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
  )`
];

// Run setup queries
setupQueries.forEach(query => {
  db.run(query, (err) => {
    if (err) console.error('Database setup error:', err);
  });
});

// Create default admin user
const createAdminUser = async () => {
  try {
    const hashedPassword = await bcrypt.hash('admin123', 10);
    db.run(
      'INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)',
      ['admin', hashedPassword, 1]
    );
  } catch (err) {
    console.error('Error creating admin user:', err);
  }
};
createAdminUser();

// Generate random products
const generateProducts = () => {
  const categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports'];
  
  db.get('SELECT COUNT(*) as count FROM products', [], (err, row) => {
    if (err) {
      console.error('Error checking products:', err);
      return;
    }

    if (row.count === 0) {
      for (let i = 1; i <= 50; i++) {
        const category = categories[Math.floor(Math.random() * categories.length)];
        db.run(
          'INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)',
          [
            `${category} Item ${i}`,
            `This is a ${category} product description`,
            (Math.random() * 100 + 10).toFixed(2),
            `https://picsum.photos/200/200?random=${i}`
          ]
        );
      }
    }
  });
};

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const token = req.headers['authorization']?.split(' ')[1];
  if (!token) return res.sendStatus(401);

  jwt.verify(token, 'your_jwt_secret', (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// Routes
app.post('/register', async (req, res) => {
  try {
    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    db.run(
      'INSERT INTO users (username, password) VALUES (?, ?)',
      [req.body.username, hashedPassword],
      function(err) {
        if (err) return res.status(400).json({ error: 'Username already exists' });
        res.status(201).json({ message: 'User created successfully' });
      }
    );
  } catch (error) {
    res.status(500).json({ error: 'Error creating user' });
  }
});

app.post('/login', (req, res) => {
  db.get(
    'SELECT * FROM users WHERE username = ?',
    [req.body.username],
    async (err, user) => {
      if (err || !user) return res.status(400).json({ error: 'User not found' });
      
      const validPassword = await bcrypt.compare(req.body.password, user.password);
      if (!validPassword) return res.status(400).json({ error: 'Invalid password' });
      
      const token = jwt.sign({ id: user.id, username: user.username }, 'your_jwt_secret');
      res.json({ token });
    }
  );
});

app.get('/products', (req, res) => {
  const searchTerm = req.query.search || '';
  db.all(
    'SELECT * FROM products WHERE name LIKE ? OR description LIKE ?',
    [`%${searchTerm}%`, `%${searchTerm}%`],
    (err, rows) => {
      if (err) return res.status(500).json({ error: 'Error fetching products' });
      res.json(rows);
    }
  );
});

app.post('/cart', authenticateToken, (req, res) => {
  const { productId, quantity } = req.body;
  db.run(
    'INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)',
    [req.user.id, productId, quantity],
    (err) => {
      if (err) return res.status(500).json({ error: 'Error adding to cart' });
      res.json({ message: 'Added to cart successfully' });
    }
  );
});

app.get('/cart', authenticateToken, (req, res) => {
  db.all(
    `SELECT ci.*, p.name, p.price, p.image_url 
     FROM cart_items ci 
     JOIN products p ON ci.product_id = p.id 
     WHERE ci.user_id = ?`,
    [req.user.id],
    (err, rows) => {
      if (err) return res.status(500).json({ error: 'Error fetching cart' });
      res.json(rows);
    }
  );
});

app.delete('/cart/:itemId', authenticateToken, (req, res) => {
  db.run(
    'DELETE FROM cart_items WHERE id = ? AND user_id = ?',
    [req.params.itemId, req.user.id],
    (err) => {
      if (err) return res.status(500).json({ error: 'Error removing from cart' });
      res.json({ message: 'Removed from cart successfully' });
    }
  );
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  generateProducts();
});