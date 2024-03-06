import express from 'express';

import { promisify } from 'util';

import { createClient, print } from 'redis';
const client = createClient();
client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));
client.on('connect', () => console.log(`Redis client connected to the server`));

const port = 1245;
const hostname = '127.0.0.1';


const listProducts = [
    {'itemId': 1, 'itemName': 'Suitcase 250', 'price': 50, 'initialAvailableQuantity': 4},
    {'itemId': 2, 'itemName': 'Suitcase 450', 'price': 100, 'initialAvailableQuantity': 10},
    {'itemId': 3, 'itemName': 'Suitcase 650', 'price': 350, 'initialAvailableQuantity': 2},
    {'itemId': 4, 'itemName': 'Suitcase 1050', 'price': 550, 'initialAvailableQuantity': 5}
]

function getItemById(id) {
    return listProducts.find(product => product.itemId === id);
}


const setAsync = promisify(client.set).bind(client);
async function reserveStockById(itemId, stock) {
    const item = getItemById(itemId);
    if (item) {
        await setAsync(`item.${itemId}`, stock, print);
    }
}

const getAsync = promisify(client.get).bind(client);
async function getCurrentReservedStockById(itemId) {
    const stock = await getAsync(`item.${itemId}`);
    return parseInt(stock);
}

const app = express();

app.get('/list_products', (req, res) => {
    res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const item = getItemById(itemId);
    if (!item) {
        res.status(404).json({ 'status': 'Product not found' });
        return;
    }
    const stock = await getCurrentReservedStockById(itemId);
    item.currentQuantity = item.initialAvailableQuantity - stock;
    res.json({...item, 'currentQuantity': item.currentQuantity});
})

app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const item = getItemById(itemId);
    if (!item) {
        res.status(404).json({'status': 'Product not found'});
        return;
    }
    const stock = await getCurrentReservedStockById(itemId);
    if (stock <= 0) {
        res.status(403).json({'status': 'Not enough stock available', 'itemId': itemId});
        return;
    }
    await reserveStockById(itemId, stock - 1);
    return res.json({'status': 'Reservation confirmed', 'itemId': itemId});
})

app.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
})
