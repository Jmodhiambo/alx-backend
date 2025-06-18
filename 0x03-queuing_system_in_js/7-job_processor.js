import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

/**
 * Sends a notification while managing job progress and handling blacklisted numbers.
 * @param {string} phoneNumber
 * @param {string} message
 * @param {object} job - The Kue job object
 * @param {function} done - The callback function to mark the job as done or failed
 */
function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);

  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  return done();
}

// Process jobs from the queue 'push_notification_code_2', max 2 at a time
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
