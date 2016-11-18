from amqpstorm.tests.utility import TestFunctionalFramework
from amqpstorm.tests.utility import setup


class BasicFunctionalTests(TestFunctionalFramework):
    @setup()
    def test_functional_basic_qos(self):
        result = self.channel.basic.qos(prefetch_count=100)
        self.assertEqual(result, {})

    @setup(queue=True)
    def test_functional_basic_get(self):
        self.channel.queue.declare(self.queue_name)
        self.channel.basic.publish(self.message, self.queue_name)

        message = self.channel.basic.get(self.queue_name)
        self.assertEqual(message.body, self.message)
        message.ack()

    @setup(queue=True)
    def test_functional_basic_cancel(self):
        self.channel.queue.declare(self.queue_name)
        consumer_tag = self.channel.basic.consume(None, self.queue_name)

        result = self.channel.basic.cancel(consumer_tag)
        self.assertEqual(result['consumer_tag'], consumer_tag)

    @setup(queue=True)
    def test_functional_basic_recover(self):
        self.channel.queue.declare(self.queue_name)
        self.channel.basic.publish(self.message, self.queue_name)

        self.assertEqual(self.channel.basic.recover(requeue=True), {})

    @setup(queue=True)
    def test_functional_basic_ack(self):
        self.channel.queue.declare(self.queue_name)
        self.channel.basic.publish(self.message, self.queue_name)

        message = self.channel.basic.get(self.queue_name, to_dict=True)

        result = self.channel.basic.ack(
            delivery_tag=message['method']['delivery_tag'])

        self.assertEqual(result, None)

        # Make sure the message wasn't requeued.
        self.assertFalse(self.channel.basic.get(self.queue_name, to_dict=True))

    @setup(queue=True)
    def test_functional_basic_nack(self):
        self.channel.queue.declare(self.queue_name)
        self.channel.basic.publish(self.message, self.queue_name)

        message = self.channel.basic.get(self.queue_name, to_dict=True)

        result = self.channel.basic.nack(
            requeue=False,
            delivery_tag=message['method']['delivery_tag'])

        self.assertEqual(result, None)

        # Make sure the message wasn't requeued.
        self.assertFalse(self.channel.basic.get(self.queue_name, to_dict=True))

    @setup(queue=True)
    def test_functional_basic_nack_requeue(self):
        self.channel.queue.declare(self.queue_name)
        self.channel.basic.publish(self.message, self.queue_name)

        message = self.channel.basic.get(self.queue_name, to_dict=True)

        result = self.channel.basic.nack(
            requeue=True,
            delivery_tag=message['method']['delivery_tag'])

        self.assertEqual(result, None)

        # Make sure the message was requeued.
        self.assertIsInstance(self.channel.basic.get(self.queue_name,
                                                     to_dict=True), dict)

    @setup(queue=True)
    def test_functional_basic_reject(self):
        self.channel.queue.declare(self.queue_name)
        self.channel.basic.publish(self.message, self.queue_name)

        message = self.channel.basic.get(self.queue_name, to_dict=True)

        result = self.channel.basic.reject(
            requeue=False,
            delivery_tag=message['method']['delivery_tag'])

        self.assertEqual(result, None)

        # Make sure the message wasn't requeued.
        self.assertFalse(self.channel.basic.get(self.queue_name, to_dict=True))

    @setup(queue=True)
    def test_functional_basic_reject_requeue(self):
        self.channel.queue.declare(self.queue_name)
        self.channel.basic.publish(self.message, self.queue_name)

        message = self.channel.basic.get(self.queue_name, to_dict=True)

        result = self.channel.basic.reject(
            requeue=True,
            delivery_tag=message['method']['delivery_tag'])

        self.assertEqual(result, None)

        # Make sure the message was requeued.
        self.assertIsInstance(self.channel.basic.get(self.queue_name,
                                                     to_dict=True), dict)
