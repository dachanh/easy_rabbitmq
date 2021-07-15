from kombu import Exchange, Queue


taskExchange = Exchange('task_add',type='direct')

taskQueue = [Queue('hihi_add',taskExchange,routing_key='hihi'),
            Queue('h0h0_add',taskExchange,routing_key='h0h0'),
            Queue('haha_add',taskExchange,routing_key='haha')]