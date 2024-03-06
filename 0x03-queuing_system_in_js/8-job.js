import kue from 'kue';
const queue = kue.createQueue();

export default function createPushNotificationsJobs(jobs, queue) {
    if (!(Array.isArray(jobs))) {
        throw new Error('Jobs is not an array');
    }
    if (jobs.length === 0) {
        return;
    }
    jobs.forEach((job) => {
        const jobData = {
            phoneNumber: job.phoneNumber,
            message: job.message
        }
        const newJob = queue.create('push_notification_code_3', jobData).save((err) => {
            if (!err) {
                console.log(`Notification job created: ${newJob.id}`);
            }
        newJob.on('complete', () => {
            console.log(`Notification job #${newJob.id} completed`);
        });
        newJob.on('failed', (err) => {
            console.log(`Notification job #${newJob.id} failed: ${err}`);
        });
        newJob.on('progress', (progress) => {
            console.log(`Notification job #${newJob.id} ${progress}% complete`);
        })
        });
    });
}
