const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const fs = require('fs');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(cors());
app.use(express.json());

const SECRET_KEY = "nitesh_family_tracker_9335212392";
let users = [];

if (fs.existsSync('users.json')) {
  users = JSON.parse(fs.readFileSync('users.json'));
} else {
  fs.writeFileSync('users.json', JSON.stringify([]));
}

app.post('/register', async (req, res) => {
  const { name = "Nitesh Kumar", phone = "9335212392", email, password } = req.body;
  if (users.find(u => u.email === email)) return res.status(400).json({ msg: "User already exists" });

  const hashed = await bcrypt.hash(password, 10);
  const user = { id: Date.now().toString(), name, phone, email, password: hashed };
  users.push(user);
  fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
  res.json({ msg: "Registered successfully", user });
});

app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ msg: "Invalid credentials" });
  }
  const token = jwt.sign({ id: user.id }, SECRET_KEY);
  res.json({ token, user: { id: user.id, name: user.name, phone: user.phone } });
});

app.get('/users', (req, res) => {
  res.json(users.map(u => ({ id: u.id, name: u.name, phone: u.phone })));
});

io.on('connection', (socket) => {
  socket.on('join', (userId) => socket.join('family'));
  socket.on('sendLocation', (data) => {
    io.to('family').emit('newLocation', { ...data, timestamp: Date.now() });
  });
});

server.listen(5000, () => console.log("✅ Server running on http://localhost:5000"));