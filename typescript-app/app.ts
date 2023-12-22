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
    rejectUnauthorized: false
  })
});

console.log('__dirname is: ', __dirname);

app.use(express.static(__dirname));
app.use(express.json());
app.use(cors());

app.get('/', (req, res) => {
  const token = req.cookies['AUTHToken'];
  const payload = { token: token };

  const domain = process.env.DOMAIN;

  axiosInstance
    .post(`https://${domain}/tg-bot/check_token`, payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then((response) => {
      console.log('Status:', response.status);
      if (response.status !== 200) {
        res.sendFile(path.join(__dirname, 'login.html'));
        throw new Error(`Network response was not ok: ${response.status}`);
      }
      res.sendFile(path.join(__dirname, 'index.html'));
      console.log('Success:', response.data);
    })
    .catch((error) => {
      console.error('Error:', error);
      res.sendFile(path.join(__dirname, 'login.html'));
    });
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

app.post('/send-message', (req, res) => {
  const xRealIP = req.headers['x-real-ip']!;
  const ip = Array.isArray(xRealIP) ? xRealIP[0] : xRealIP;
  if (ip.startsWith('192.168.1.')) {
    const { message } = req.body;
    io.emit('new_message', {
      message_text: message['message_text'],
      date: message['date'],
      chat_id: message['chat_id'],
      from_user: message['from_user'],
      unread: message['unread'],
      attachment: message['attachment'],
      location: message['location'],
      manager_name: message['manager_name'],
      reply_to_message: message['reply_to_message']
    });
    res.status(200).send('Message sent to all clients');
  } else {
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
