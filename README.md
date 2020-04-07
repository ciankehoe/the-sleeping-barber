# the-sleeping-barber

## Brief comments on method and implementation. 
I initially started with a much more linear (non Object Oriented) approach which followed a much more traditional implementation. For example, I was making strong use of a mutex to control the state of the single barber, as well as a mutex to control access to the waiting room seats (shared resource). Through this I ensured mutual exclusion as only the single barber or any given new customer could change the state of the queue at once. I made sure to use a queue so as to guarantee a FIFO to avoid the possibility of starvation. 
A variety of other semaphores / mutexes to control the state of the system (like entering the shop, getting their haircut, taking a free waiting room chair) resulted in what I saw as a logically sound solution. 
One simple method of testing at that early stage which I personally found quite effective was lining up the customer and barber code bseide eachother and pairing the signals and waits on the semaphores.
It was a great way of fully understanding the usefulness and importance of correct process synchronization techniques.

However, this solution proved inadequate in design when moving forward and considering the case of multiple barbers, as obviously there is a lot more going on. This is the point at which I moved into the more OO design / implementation , which lead to the final version of my program. 

I have commented my code quite liberally and hope that it provides adequate description of my source code and design. However, I would just like to add, one thing I found particularly challenging was how to logically control the waking of the barbers, in conjunction to accessing a single shared resource. But, the Queue module, in my opinion, deals with locking quite well and seemed to be significantly useful for this.

I did

## Bugs
* 1.
I ran into some difficulties with regards the termination of the
barber threads while obviously making sure they'd completed their work. I initially tried a to join() them as with my Customer threads, but couldn't quite get it to work as I'd of liked. 

I initially considered placing None objects in the queue which would signals to the barber that they were done when they would get them from the queue, but that means the barber would be checking the queue to find out the store is closed. Which would be like, to me, the barber going to check the waiting room and seeing the door has been locked and the owner gone home! I didn't want the barber to have to check the queue to find out s(he) was finished.

As you can see, I finished by making all the barbers into daemon threads which are killed when the main program exits. 

This method proves to be extremely useful in cases where program termination can be used to trigger the killing of threads. the only danger with these daemon threads is that the resources held by them may not be released properly. Killing a thread forcibly is not recommended unless it is known for sure, that doing so will not cause any leaks or deadlocks. 
I used join() on all the customer threads [Ln. 212] to make sure they had finished getting their haircut, whilst also no longer accepting new customers once the shop had closed (timeout had been reached). The inherent design of the cut() method being in the Customer Class means there can't possibly be any more customers to deal with once we've used join() on the waiting_room [Ln. 212]. 

I (roughly) tested that resources were being released properly by tracking the number of customers who were taken for a haircut, followed by the number who completed haircuts. This number was always the same. I also checked that the queue was always empty [Ln. 214] before setting the shop_open flag to False [Ln. 216].

I understand however that this may not be an overall optimal / desired way of completing the program execution, so bugs may present themselves in ways that I've not considered.

* 2
At most one customer can be in a barber chair at once i.e A single Customer need to be paired off with a single Barber to have their hair cut by that barber alone. A mutex lock prevents more than one customer from possessing the chair at a time but I found this much trickier to deal with when it came to multiple barbers as opposed to my earlier solutions with a single barber. Basically preventing several barbers from cutting hair of the same customer.

I did consider applying some sort of pigeonhole-principle style structure to the shared resource / waiting room, in the form of splitting the queue into sub-queues which each barber would work on respectively. But, quickly saw how this would not be ideal; immediately would have lost the FIFO characteristic of the overall queue, amongst other things.

But, I believe I dealt with this somewhat well. I did mapping of Customer Thread IDs to Barber Thread IDs / names in order to test and make sure that only barber was cutting a single customers hair.  Again, I understand this may not be an optimal / bugfree approach. I could well be missing something here and understand possible limitations of my program.

* 3
As I mentioned before, a key problem I believe may still afflict my solution is the waking of all barbers every time a customer enters and having to implement a second check to send the unused barbers back to sleep. I don't believe it's ideal.

## Further Testing
Overall, during the development of my program, I made heavy use of in-program testing (often in the form of various print statements) and the mapping of various thread parameters. 

Looking back, I would have looked further into experimenting with and adding more logging statements and running tests externally somehow. Although I found it difficult to imagine how one might do so particularly efficiently, especially in a specialized manner for a multithreaded program such as this.

We can see affects on the number of haircuts completed through tweaking the length of time it takes for a haircut in the code (increasing might mean less in the same window of time and vice versa). Increasing the opening hours (timeout), we'll most likely see an increase in the number completed, particularly if we lower the time for a haircut also. 

I also did a variety of testing on the averages and affects of tweaking these numbers in some simple ways.

cutTime = 10 * random.random()
customer_frequency() --> time.sleep(1 * random.random())

With the below parameters:
opening_time_length = 20
num_barbers = 3
num_seats = 15

I got the below 6 times which are a random sample of average haircut times

5.143296406185352
5.4519967731533985
5.556107048706706
4.968878027697593
4.841057706803752
4.703623626298269

As we can see they are all approximately similar, however this changes depending on the speed of haircuts and number of barbers.

By reducing:
num_barbers = 1

But keeping the same num_seats (15) we can really see the affects of my implementation, and the importance and efficiency of the multithreading.

Predictably it approximates to being 3 times as slow for the average haircut time.

Sample Average after 200 runs = 14.996796929689852

(Again, it is heavily dependent on the length of time I allow the shop to be open for, as well as the integer constant by which I set the 'random' cuttime and customer frequency to).

I did more of this testing which didn't give back any surprising results. A mixture of writing stats of the program to other files and running scripts over them really helped in this analysis.

(Apologies for the verbose nature of this and it's length! Thanks very much for your time!)