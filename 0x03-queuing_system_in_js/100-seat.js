// 100-seat.js
const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Initialize variables
const initialSeats = 50;
let reservationEnabled = true;

// Reserve seats in Redis
const reserveSeat = async (number) => await setAsync('available_seats', number);
const getCurrentAvailableSeats = async () => Number(await getAsync('available_seats')) || 0;

// Set initial seats
reserveSeat(initialSeats);

// Kue queue
const queue = kue.createQueue();

// Route to get available seats
app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

// Route to reserve seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) return res.json({ status: 'Reservation failed' });
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
  job.on('failed', (error) => console.log(`Seat reservation job ${job.id} failed: ${error.message}`));
});

// Route to process queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const seats = await getCurrentAvailableSeats();
    
    if (seats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    await reserveSeat(seats - 1);
    if (seats - 1 === 0) reservationEnabled = false;
    done();
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
