# the-sleeping-barber

I ran into some difficulties with regards the termination of the program, in terms of terminating the
barber threads. Obviously had to make sure they'd completed their work.

Notice that, as soon as the main program exits, the thread t1 is killed. This method proves to be extremely useful in cases where program termination can be used to trigger the killing of threads. Note that in Python, the main program terminates as soon as all the non-daemon threads are dead, irrespective of the number of daemon threads alive. Hence, the resources held by these daemon threads, such as open files, database transactions, etc. may not be released properly. The initial thread of control in a python program is not a daemon thread. Killing a thread forcibly is not recommended unless it is known for sure, that doing so will not cause any leaks or deadlocks. --> tested this by making sure the barbers
were all always sleeping by the end as there can't possibly be any more customers to deal with (due to the nature of the trim occuring in the customer class, just joining that does the job. DOUBLE CHECK THIS)

shop open event flag is for dealing with termination of barbers

timer used to only create (accept customers) for a certain amount of time --> simulating an opening period for the barber shop.


we can see affects on the number of haircuts completed through tweaking the length of time it takes for
a haircut (increasing might mean less in the same window of time and vice versa), and increasing the opening hours (timeout), we'll most likely see an increase in the number completed, particularly if we lower the time for a haircut also. 


was originally going to use the Timer() object from threading in order to manage the opening window of the barbershop but instead decided to go down an event driven route
timer = threading.Timer(15, opening_hours)
timer.start()
timer.join()


GET AVERAGES


With one barber, you only need a message queue (the waiting room). Semaphores are embedded in it.

With multiple barbers, coordination aims at:

    preventing several barbers from cutting hair of the same customer.

    preventing from having only one busy barber while the others sleep all day long
#################


The problem referenced in the Wikipedia remark is this: just because you have M barbers in the "barber is cutting hair" state and M customers in the "customer is having hair cut" state, there's no guarantee that some barber isn't trying to clip more than one customer, or that some customer doesn't have several barbers in his hair.

In other words, once the proper number of customers have been allowed into the cutting room, how do the barbers and customers pair off? You can no longer say "barber is cutting hair" and "customer is having hair cut"; you have to say "barber is cutting hair of customer C" and "customer is having hair cut by barber B". 





Sleeping barber problem is about race conditions. Imagine you have the same Producer generating tasks(people coming to barbershop) and Consumer(barber). In case not to do busy waiting your Consumer sleeps when there are no more tasks in the queue, so when a new task arrives it first notifies Consumer that it shouldn't sleep. So now imagine a case, when you Consumer currently is executing task A, and task B arrives, it sees that Consumer is working and will just go to the queue, but its not an atomic operation, so between this check(that Consumer is busy) and adding itself to the queue, Consumer can already finish task A and check the queue, see nothing(as B is still not added), and go to sleep, however B doesn't know about that and will wait till eventually another task C will come and awake Consumer. 
----------------> Talk about how I believe I've avoided this by making use of the event


# Proof of Correctness

Proof of correctness:

No two threads can be reading or writing the shared data numWaiting at a time. numWaiting is accessed only by customer threads, and the waitingRoom lock must be held in order to read or modify its value. YES

The waiting room cannot hold more than NUM_WAITING_CHAIRS customers. The waitingRoom lock must be held in order to examine the number of waiting customers, and the number waiting is incremented if the waiting room is not full before the lock is released. The number of waiting customers is decremented exactly once for every time it is incremented, so it is an accurate count of the number of waiting customers. YES

At most one customer can be in the barber chair at once. A mutex lock prevents more than one customer from possessing the chair at a time. TRICKY TO DEAL WITH DUE TO MULTIPLE CHAIRS

The following events are properly sequenced: customer waits in waiting room, customer sits in barber chair, barber cuts customer's hair, barber finishes haircut, customer leaves. The customer begins by waiting in the waiting room for the barber chair to become availabe. Only one customer at a time can acquire the barber chair lock, and the barber chair lock must be acquired before the customer can sit down. The customer now cannot proceed past waiting for the haircut to finish until the barber has finished the haircut. Meanwhile, the barber cannot proceed past the "waiting for customers" stage until signalled by the customer, which occurs after the customer has sat in the barber chair. The barber then cuts the hair and finishes the haircut, signalling the customer that the haircut is complete. The customer is then able to leave. The barber cannot proceed past the "waiting for customers" stage again until the next customer is seated in the barber's chair. Since only one customer at a time can make it past the "acquire barber chair lock" step, the right customer is signalled when the barber finishes the haircut. (This can also be demonstrated by lining up the customer and barber code side-by-side, pairing the signals and waits on the semaphores - the parts of the customer and barber which overlap between the signals and waits can safely be executed in any order, and using semaphores means that it is OK if one signals before the other waits.)

The barber doesn't oversleep and miss a customer sitting in the barber chair. Each customer signals the barber when they've sat down, and using semaphores means that the order in which the customer signals and the barber waits doesn't matter. (With a condition variable, if the customer signalled before the barber went back to sleep after the previous customer, the barber would miss the wakeup call.) YES

There is no deadlock. The only time that hold-and-wait occurs is when the customer is holding the barberchair lock and is attempting to acquire the waitingRoom lock. However, whenever the waitingRoom lock is held, there is nothing (other than the scheduling of the thread to run) to prevent the lock from being released.