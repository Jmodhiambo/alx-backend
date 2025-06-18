import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

// Product Data
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

// Express App
const app = express();
const port = 1245;

// Redis client setup
const client = createClient();
client.on('error', (err) => console.error('Redis client error', err));
client.connect();

const reserveStockById = async (itemId, stock) => {
  await client.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const stock = await client.get(`item.${itemId}`);
  return stock !== null ? parseInt(stock) : null;
};

const getItemById = (id) => listProducts.find(item => item.itemId === id);

// Routes
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reserved = await getCurrentReservedStockById(itemId);
  const currentQuantity = reserved !== null ? item.initialAvailableQuantity - reserved : item.initialAvailableQuantity;

  res.json({
    ...item,
    currentQuantity
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reserved = await getCurrentReservedStockById(itemId) || 0;
  const available = item.initialAvailableQuantity - reserved;

  if (available < 1) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }

  await reserveStockById(itemId, reserved + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

// Start server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
