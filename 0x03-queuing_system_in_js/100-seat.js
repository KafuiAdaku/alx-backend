import express from 'express';
import kue from 'kue';
import { createClient } from 'redis';
import {promisify} from 'util';

const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
const PORT = 1245;
const HOSTNAME = '127.0.0.1'

let reservationEnabled = true;

async function reserveSeat(number) {
    await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
    return await getAsync('available_seats');
}

const queue = kue.createQueue();
const app = express();

app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', async (req, res) => {
    if (reservationEnabled === false) {
        res.json({ 'status': 'Reservation are blocked' });
        return;
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            res.json({status: 'Reservation failed'});
        } else {
            res.json({status: 'Reservation in process'});
        }
    });

    job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
    job.on('failed', (err) => console.log(`Seat reservation job ${job.id} failed: ${err}`));
});

app.get('/process', async (req, res) => {
    queue.process('reserve_seat', async (job, done) => {
        let seats = await getCurrentAvailableSeats();
        seats--;
        if (seats >= 0) {
            await reserveSeat(seats);
            done();
        } else {
            done(new Error('Not enough seats available'));
        }

        if (seats === 0) {
            reservationEnabled = false;
        }
    });
    res.json({ status: 'Queue processing' });
});

app.listen(PORT, HOSTNAME, async () => {
    console.log(`Server running at http://${HOSTNAME}:${PORT}/`);
    await reserveSeat(50);
});
