from kombu import Exchange, Queue


taskExchange = Exchange('task_div',type='direct')

taskQueue = [Queue('hihi_div',taskExchange,routing_key='hihi'),
            Queue('h0h0_div',taskExchange,routing_key='h0h0'),
            Queue('haha_div',taskExchange,routing_key='haha')]