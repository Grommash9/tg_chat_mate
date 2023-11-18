import express from 'express';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';
import path from 'path';

const app = express();
const port = 3000;
const httpServer = createServer(app);
const io = new SocketIOServer(httpServer);

app.use(express.static(path.join(__dirname, 'dist')));
app.use(express.json()); // Middleware to parse JSON requests

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Endpoint to send a message to the server and broadcast it to all connected clients via Socket.IO
app.post('/send-message', (req, res) => {
  const { text, chat_id } = req.body;
  console.log(req.body);
  io.emit('new_message', { text: text, chat_id: chat_id });
  res.status(200).send('Message sent to all clients');
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

// Start the server
httpServer.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});