import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

/**
 * Sends a notification to a phone number
 * @param {string} phoneNumber
 * @param {string} message
 */
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Process jobs in the 'push_notification_code' queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done();
});
