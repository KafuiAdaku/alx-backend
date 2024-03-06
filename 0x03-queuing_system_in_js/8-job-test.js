import createPushNotificationsJobs from './8-job.js';
import { expect } from 'chai';
import kue from 'kue';


describe('createPushNotificationsJobs', () => {
    let queue;

    before(() => {
        queue = kue.createQueue();
        queue.testMode.enter();
    });

    afterEach(() => {
        queue.testMode.clear();
    });

    after(() => {
        queue.testMode.exit();
    });

    it('should create jobs in the queue', () => {
        const jobs = [
            {phoneNumber: '1234567890', message: 'Hello!'},
            {phoneNumber: '0987654321', message: 'Hi!'}
        ];

        createPushNotificationsJobs(jobs, queue);

        expect(queue.testMode.jobs.length).to.equal(2);
        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    })

    it('should throw an error if jobs is not an array', () => {
        expect( () => createPushNotificationsJobs('not an array', queue))
            .to.throw('Jobs is not an array');
    });
});
