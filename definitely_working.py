import time, random, threading
from queue import Queue

# dict mapping for names of barbers --> utilize IDs as well.
# Only including 3 names as this was what was asked as the
# max case in the specification.
# This aspect can be removed to allow for more than 3 barbers.
barber_names = ["John", "Jill", "Jacob"]

# set to whatever length of time (seconds) we want the 'barbershop' to be open for.
opening_time_length = 20

# count of customers who have been taken from the waiting room by a barber / worker
customers_gone_for_cut = 0
# count of customers who have then successfully had 
# their haircuts completed. (The trim() method run successfully.)
haircuts_completed = 0

num_seats = 15        #Number of seats in BarberShop 
num_barbers = 3              #Number of Barbers working
EVENT = threading.Event()   #Event flag, keeps track of Barber/Customer interactions
shop_open = threading.Event()

class Customer(threading.Thread):       #Producer Thread
    def __init__(self, queue):          #Constructor passes Global Queue (waiting_room) to Class
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        if not self.queue.full(): #Check queue size
            self.queue.put(self)
            print("Customer has joined the queue", threading.currentThread())
            EVENT.set() #Sets EVENT flag to True i.e. Customer available in the Queue
            EVENT.clear() #Alerts Barber that their is a Customer available in the Queue
        else:
            print("Queue full, customer has left.") #If Queue is full, Customer leaves.

    def trim(self):
        print("Customer haircut started.")
        a = 10 * random.random() #Retrieves random number.
        time.sleep(a) #Simulates the time it takes for a barber to give a haircut.
        global haircuts_completed
        haircuts_completed += 1
        print("Haircut finished. Haircut took {}".format(a))    #Barber finished haircut.


class Barber(threading.Thread):     #Consumer Thread
    def __init__(self, queue):      #Constructor passes Global Queue (waiting_room) to Class
        threading.Thread.__init__(self)
        self.queue = queue
        self.sleep = True   #No Customers in Queue therefore Barber sleeps by deafult
    
    def run(self):
        while not shop_open.is_set():
            while self.queue.empty():
                EVENT.wait()    #Waits for the Event flag to be set, Can be seen as the Barber Actually sleeping.
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

def customer_frequency():
    time.sleep(1 * random.random())

# naming our barbers
def map_barber(barber):
    if num_barbers <= 3:
        barber.name = "{} | {} | ({})".format(barber_names[int(b.name[-1]) - 1], b.name, str(b.ident))
    else:
        b.name = "{} | ({})".format(b.name, str(b.ident))
    

if __name__ == '__main__':
    barbers = []
    waiting_room = Queue(num_seats) #A queue of size Customer Seats

    for b in range(num_barbers):
        b=Barber(waiting_room) #Passing the Queue to the Barber class
        b.daemon=True   #Makes the Thread a super low priority thread allowing it to be terminated easier
        b.start()   #Invokes the run method in the Barber Class

        map_barber(b)

        print("Barber ID: ", b.name)
        barbers.append(b)   #Adding the Barber Thread to an array for easy referencing later on.






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
    #for i in range(num_barbers):
    #    print("Go home")
        #EVENT.set()
        #EVENT.clear()
    print(waiting_room.empty())

    #for i in barbers:
    #   print("please", threading.activeCount())
    #   EVENT.set()
    #   i.join()   #Terminates all Barbers
        #Program hangs due to infinite loop in Barber Class, use ctrl-z to exit.
    for i in barbers:
        if i.sleep is False:
            print("I've come into this now")
            print("still Stuck here")
        print("Not working: ", i.sleep)

    shop_open.set()

    print("Active Threads", threading.activeCount())

    print("how many went -->", customers_gone_for_cut)
    print("Total haircuts completed during opening time: ", haircuts_completed)


    # get average process time



    # a customer object is added to the queue and then gets started. We set the EVENT flag to true and then quickly back to false
    # essentially giving notice that there is now someone new in the queue