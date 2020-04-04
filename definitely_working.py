import time, random, threading
from queue import Queue

CUSTOMERS_SEATS = 15        #Number of seats in BarberShop 
BARBERS = 3                #Number of Barbers working
EVENT = threading.Event()   #Event flag, keeps track of Barber/Customer interactions
global Earnings
global SHOP_OPEN

class Customer(threading.Thread):       #Producer Thread
    def __init__(self, queue):          #Constructor passes Global Queue (all_customers) to Class
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        if not self.queue.full(): #Check queue size
            EVENT.set() #Sets EVENT flag to True i.e. Customer available in the Queue
            EVENT.clear() #Alerts Barber that their is a Customer available in the Queue
        else:
            print("Queue full, customer has left.") #If Queue is full, Customer leaves. 

    def trim(self):
        print("Customer haircut started.")
        a = 3 * random.random() #Retrieves random number.
        time.sleep(a) #Simulates the time it takes for a barber to give a haircut.
        print("Haircut finished. Haircut took {}".format(a))    #Barber finished haircut.


class Barber(threading.Thread):     #Consumer Thread
    def __init__(self, queue):      #Constructor passes Global Queue (all_customers) to Class
        threading.Thread.__init__(self)
        self.queue = queue
        self.sleep = True   #No Customers in Queue therefore Barber sleeps by deafult
    
    def is_empty(self, queue):  #Simple function that checks if there is a customer in the Queue and if so  
        if self.queue.empty():
            self.sleep = True   #If nobody in the Queue Barber sleeps.
        else:
            self.sleep = False  #Else he wakes up.
        print("------------------\nBarber sleep {}\n------------------".format(self.sleep))
    
    def run(self):
        global SHOP_OPEN
        while SHOP_OPEN:
            while self.queue.empty():
                EVENT.wait()    #Waits for the Event flag to be set, Can be seen as the Barber Actually sleeping.
                print("Barber is sleeping...")
            print("Barber is awake.")
            cust = self.queue
            self.is_empty(self.queue)   
            cust = cust.get()  #FIFO Queue So first customer added is gotten.
            if cust is None:
                break
            else:
                cust.trim() #Customers Hair is being cut
                cust = self.queue
                cust.task_done()    #Customers Hair is cut  
                print(self.name)    #Which Barber served the Customer     

def wait():
    time.sleep(1 * random.random())

def opening_hours():
    print("OH LOOK AT ME PLEASE We're done -----------------------------------------")

if __name__ == '__main__':
    SHOP_OPEN = True
    barbers = []
    all_customers = Queue(CUSTOMERS_SEATS) #A queue of size Customer Seats
    timer = threading.Timer(7.0, opening_hours)
    timer.start()

    for b in range(BARBERS):
        b=Barber(all_customers) #Passing the Queue to the Barber class
        b.daemon=True   #Makes the Thread a super low priority thread allowing it to be terminated easier
        b.start()   #Invokes the run method in the Barber Class
        barbers.append(b)   #Adding the Barber Thread to an array for easy referencing later on.
    for c in range(10): #Loop that creates infinite Customers
        print("----")
        print(all_customers.qsize())    #Simple Tracker too see the qsize (NOT RELIABLE!)
        wait()
        c = Customer(all_customers) #Passing Queue object to Customer class
        all_customers.put(c)    #Puts the Customer Thread in the Queue
        c.start()   #Invokes the run method in the Customer Class
    
    timer.join()
    all_customers.join()    #Terminates all Customer Threads
    print(all_customers.empty())
    SHOP_OPEN = False
    
    for i in range(BARBERS):
        print("Go home")
        all_customers.put(None)
        EVENT.set()
        EVENT.clear()
    print(all_customers.empty())
    print(all_customers.get())
    for i in barbers:
        i.join()    #Terminates all Barbers
        #Program hangs due to infinite loop in Barber Class, use ctrl-z to exit.
    self
    print("do we get here at all?????????????????????????")

        def stop(self):
        self.queue.put(None)
        for i in range(self.NUMBER_OF_PROCESS):
            self.workers[i].join()
        self.queue.close()