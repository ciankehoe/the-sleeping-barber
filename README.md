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