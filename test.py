import sched
import time
  
# instance is created
scheduler = sched.scheduler(time.time,
                            time.sleep)
  
# function to print time 
# and name of the event
def print_event(name):
    print('EVENT:', time.time(), name)
  
# printing starting time
print ('START:', time.time())
  
# first event with delay of
# 1 second
e1 = scheduler.enter(1, 1, 
                     print_event, ('1 st', ))
  
# second event with delay of
# 2 seconds
e1 = scheduler.enter(2, 1, 
                     print_event, (' 2nd', ))
  
# executing the events
scheduler.run()