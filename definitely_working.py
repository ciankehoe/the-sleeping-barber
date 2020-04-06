import threading
import time
import random
import queue

# dict mapping for names of barbers --> utilize IDs as well.
# Only including 3 names as this was what was asked as the
# max case in the specification.
# This aspect can be removed to allow for more than 3 barbers.
barber_names = ["John", "Jill", "Jacob"]

# set to whatever length of time (seconds)
# we want the 'barbershop' to be open for.
opening_time_length = 10

# count of customers who have been taken
# from the waiting room by a barber / worker.
customers_gone_for_cut = 0
# count of customers who have then successfully had
# their haircuts completed. (The trim() method run successfully.)
haircuts_completed = 0

# Count of total time spent cutting hair.
total_haircut_time = 0

num_seats = 15                  # Number of seats available in Barbershop waiting room.
num_barbers = 3                 # Number of Barbers working.

# Acts as a flag to notify barber when a new Customer has entered the Queue. Also used to wake barber.
customer_available = threading.Event()

# Flag to control state of barbershop (open/closed); used to allow barber threads to terminate.
shop_open = threading.Event()


def customer_frequency():
    time.sleep(1 * random.random())


# naming our barbers
def map_barber(barber):
    """Simple function to map our barbers to individual names and
       thread ID.
       To give names to more than 3 barbers, you will need to add
       to the barber_names list.
    """

    if num_barbers <= len(barber_names):
        barber.name = "{} | {} | ({})".format(barber_names[int(barber.name[-1]) - 1], barber.name, str(barber.ident))
    else:
        barber.name = "{} | ({})".format(barber.name, str(barber.ident))


class Barber(threading.Thread):
    """Consumer Thread"""

    def __init__(self, queue):      #Constructor passes Global Queue (waiting_room) to Class
        threading.Thread.__init__(self, daemon=True) #Makes the Thread a super low priority thread allowing it to be terminated easier
        self.queue = queue
        self.sleep = True   #No Customers in Queue therefore Barber sleeps by deafult

    def run(self):
        while not shop_open.is_set():
            while self.queue.empty():
                customer_available.wait()    #Waits for the Event flag to be set, Can be seen as the Barber Actually sleeping.
                print(self.name, "Barber is sleeping...")
            #mutex.acquire()
            print(self.name, "Barber is awake.")
            cust = self.queue
            self.is_empty(self.queue)
            cust = cust.get()  #FIFO Queue So first customer added is gotten.
            global customers_gone_for_cut
            customers_gone_for_cut += 1
            cust.trim() #Customers Hair is being cut
            cust = self.queue
            cust.task_done()    #Customers Hair is cut
            print(self.name)    #Which Barber served the Customer }

    def is_empty(self, queue):  #Simple function that checks if there is a customer in the Queue and if so
        if self.queue.empty():
            self.sleep = True   #If nobody in the Queue Barber sleeps.
        else:
            self.sleep = False  #Else he wakes up.
        print("------------------\n{} Barber sleep {}\n------------------".format(self.name, self.sleep))

class Customer(threading.Thread):
    """Producer Thread"""

    def __init__(self, queue):          #Constructor passes Global Queue (waiting_room) to Class
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        if not self.queue.full(): #Check queue size
            self.queue.put(self)
            print("Customer has joined the queue", threading.currentThread())
            customer_available.set() #Sets customer_available flag to True i.e. Customer available in the Queue
            customer_available.clear() #Alerts Barber that their is a Customer available in the Queue
        else:
            print("Queue full, customer has left.") #If Queue is full, Customer leaves.

    def trim(self):
        print("Customer haircut started.")
        a = 10 * random.random() #Retrieves random number.
        time.sleep(a) #Simulates the time it takes for a barber to give a haircut.
        global total_haircut_time
        total_haircut_time += a

        global haircuts_completed
        haircuts_completed += 1
        print("Haircut finished. Haircut took {}".format(a))    #Barber finished haircut.


if __name__ == '__main__':
    barbers = []

    # The Queue constructor creates a lock to protect the queue (our shared resource) when an element is added or removed. 
    # Some conditions objects are created to notify events like the queue is not empty (get() call stops blocking), 
    # queue is not full (put() call stops blocking) and all items have been processed (join() call stops blocking).

    # Our waiting room is a queue of size num_seats
    waiting_room = queue.Queue(num_seats)

    for worker in range(num_barbers):
        worker=Barber(waiting_room) # Giving the Queue access to the Barber.
        worker.start()              # Starts the thread which calls the run method.

        map_barber(worker)

        print("Barber ID: ", worker.name)
        barbers.append(worker)   #Adding the Barber Thread to an array for easy referencing later on.






    timeout = time.time() + opening_time_length #Loop that creates infinite Customers

    while True: # infinitely create customers while the shop is open / still accepting customers
        if time.time() > timeout:
            print("NO MORE CUSTOMERS")
            break
        print("----")
        print("Length of Queue", waiting_room.qsize())    #Simple Tracker too see the qsize (NOT RELIABLE!)
        customer_frequency()
        c = Customer(waiting_room) #Passing Queue object to Customer class
        print("unique customer thread ID", c.ident)
        #waiting_room.put(c)    #Puts the Customer Thread in the Queue --> going into the waiting room
        c.start()   #Invokes the run method in the Customer Class
        time.sleep(1) # prevents hogging of resources


    waiting_room.join()  # terminates all Customer Threads

    print("The shop is closed, is the queue empty?", waiting_room.empty())
    print(waiting_room.empty())

    shop_open.set()

    print("Active Threads", threading.activeCount())
    print("#")
    print("#")
    print("#")
    print("#")
    print("#")
    print("#")
    print("Number of customers accepted for haircut (during opening time): {:>}".format(customers_gone_for_cut))
    print("----------------------------------")


    print("Total number of haircuts completed (during opening time): {:>7}".format(haircuts_completed))
    print("----------------------------------")


    # get average process time
    print("Average haircut time: ", total_haircut_time / haircuts_completed)


    # The Queue module takes care of locking for us which is a great advantage.

 

    # a customer object is added to the queue and then gets started. We set the customer_available flag to true and then quickly back to false
    # essentially giving notice that there is now someone new in the queue