// 4-redis_advanced_op.js
import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Delete ALX key before re-using it as a hash
client.del('ALX', (err, reply) => {
  if (err) {
    console.error(`Error deleting ALX key: ${err.message}`);
  }

  // Now set the hash values
  client.hset('ALX', 'Portland', 50, redis.print);
  client.hset('ALX', 'Seattle', 80, redis.print);
  client.hset('ALX', 'New York', 20, redis.print);
  client.hset('ALX', 'Bogota', 20, redis.print);
  client.hset('ALX', 'Cali', 40, redis.print);
  client.hset('ALX', 'Paris', 2, redis.print);

  // Display the hash
  client.hgetall('ALX', (err, value) => {
    if (err) {
      console.error(`Error retrieving ALX hash: ${err.message}`);
      return;
    }
    console.log(value);
  });
});
