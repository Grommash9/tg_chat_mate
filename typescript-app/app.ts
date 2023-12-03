import express from 'express';
import axios from 'axios';
import cookieParser from 'cookie-parser';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';
import path from 'path';
const https = require('https');

const app = express();
app.use(cookieParser());
const port = 3000;
const httpServer = createServer(app);
const io = new SocketIOServer(httpServer);
const cors = require('cors');
const axiosInstance = axios.create({
  httpsAgent: new https.Agent({  
    rejectUnauthorized: false // Disable SSL certificate validation
  })
});

app.use(express.static(path.join(__dirname, 'dist')));
app.use(express.json()); // Middleware to parse JSON requests
app.use(cors());

// have no idea why it's not working as static file 
app.get('/main.css', (req, res) => {
  res.sendFile(path.join(__dirname, 'main.css'));
});


app.get('/mixkit-correct-answer-tone-2870.wav', (req, res) => {
  res.sendFile(path.join(__dirname, 'mixkit-correct-answer-tone-2870.wav'));
});

app.get('/user_empty_photo.png', (req, res) => {
  res.sendFile(path.join(__dirname, 'user_empty_photo.png'));
});

app.get('/manager_empty_photo.png', (req, res) => {
  res.sendFile(path.join(__dirname, 'manager_empty_photo.png'));
});

app.get('/mixkit-message-pop-alert-2354.mp3', (req, res) => {
  res.sendFile(path.join(__dirname, 'mixkit-message-pop-alert-2354.mp3'));
});

app.get('/normal.css', (req, res) => {
  res.sendFile(path.join(__dirname, 'normal.css'));
});

app.get('/login.css', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.css'));
});

app.get('/', (req, res) => {
  const token = req.cookies['AUTHToken'];
  const payload = { "token": token };

  const domain = process.env.DOMAIN;
  
axiosInstance.post(`https://${domain}/tg-bot/check_token`, payload, {
    headers: {
      'Content-Type': 'application/json',
    }
  })
  .then(response => {
    console.log("Status:", response.status)
    // Check if the status code is 200
    if (response.status !== 200) {
      // If not, send the login page
      res.sendFile(path.join(__dirname, 'login.html'));
      throw new Error(`Network response was not ok: ${response.status}`);
    }
    // If the status code is 200, send the index page
    res.sendFile(path.join(__dirname, 'index.html'));
    console.log('Success:', response.data);
  })
  .catch(error => {
    // Log the error and send the login page
    console.error('Error:', error);
    res.sendFile(path.join(__dirname, 'login.html'));
  });
});


app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

// Endpoint to send a message to the server and broadcast it to all connected clients via Socket.IO
app.post('/send-message', (req, res) => {
  const xRealIP = req.headers['x-real-ip']!;
  const ip = Array.isArray(xRealIP) ? xRealIP[0] : xRealIP;
  if (ip.startsWith('192.168.1.')) {
  const { message } = req.body;
  io.emit('new_message', { message_text: message["message_text"], date: message["date"], chat_id: message["chat_id"], from_user: message["from_user"], unread: message["unread"], attachment: message["attachment"], location: message["location"], manager_name: message["manager_name"] });
  res.status(200).send('Message sent to all clients');}
  else {
    return res.status(403).send('Forbidden');
  }
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});


httpServer.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});