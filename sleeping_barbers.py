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
opening_time_length = 20

# count of customers who have been taken
# from the waiting room by a barber / worker.
customers_gone_for_cut = 0
# count of customers who have then successfully had
# their haircuts completed. (The cut() method run successfully.)
haircuts_completed = 0

# Count of total time spent cutting hair.
total_haircut_time = 0

num_seats = 15   # Number of seats available in Barbershop waiting room.
num_barbers = 3   # Number of Barbers working.

# Acts as a flag to notify barber when a new Customer
# has entered the Queue. Also used to wake barber.
customer_available = threading.Event()

# Flag to control state of barbershop (open/closed); used to
# allow barber threads to terminate.
shop_open = threading.Event()


def customer_frequency():
    """Manages the random length of time between Customers arriving."""
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
    """Consumer (Thread) Class"""

    def __init__(self, queue):
        """The shared queue (waiting room) is passed to the constructor."""

        # daemon threads can be terminated more easily
        # as the entire program exits when only these are left
        threading.Thread.__init__(self, daemon=True)
        self.queue = queue
        # When the Barbers starts work (thread is created),
        # there are no customers.
        # Therefore each barber is initially asleep.
        self.sleep = True

    def run(self):
        while not shop_open.is_set():
            while self.queue.empty():
                # Barber sleeps, waiting for customer to
                # set flag arrival flag.
                customer_available.wait()
                print("Barber ", self.name, " - [ASLEEP]")
            print("Barber ", self.name, " - [AWAKE]")
            current_customer = self.queue
            self.is_empty(self.queue)

            # We retrieve the Customer at the front of the queue.
            # get() call acts as a lock mechanism for the shared resource.
            current_customer = current_customer.get()

            global customers_gone_for_cut
            customers_gone_for_cut += 1

            current_customer.cut()  # Customers Hair is being cut

            # I'm not assigning specific names to the customers, so
            # each customers 'name' is simply their Thread ID Number.
            customerID = current_customer.name

            current_customer = self.queue

            # Indicate that the formerly enqueued task is complete.
            # Customers haircut is complete.
            current_customer.task_done()

            # Showing that one specific barber is paired off with,
            # and only cutting the hair of one customer.
            print("The barber ", self.name, " cut the hair of Customer ", customerID)

    def is_empty(self, queue):
        """This is an additional function to check again
           whether the queue is empty now that customer_available flag
           was set. We want to make sure that if the queue is empty, the
           unrequired barbers go back to sleep.
        """

        if self.queue.empty():
            self.sleep = True
        else:
            self.sleep = False
        print(" * {} - [ASLEEP --> {}]".format(self.name, self.sleep))


class Customer(threading.Thread):
    """Producer (Thread) Class"""

    def __init__(self, queue):
        """The shared queue (waiting room) is passed to the constructor."""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        # Customer checks if queue is at capacity and puts itself
        # in if not. Otherwise leaves
        if self.queue.full():
            print("No seats remaining in waiting room (QUEUE FULL). Customer {} has left.".format(self.name))
        else:
            self.queue.put(self)
            print("Customer {} has successfully entered the waiting room.".format(self.name))
            # Sets customer_available flag to True.
            # Notifies barber of customer in waiting room.
            customer_available.set()
            # Sets customer_available flag back to False.
            # Customer only wants to give a quick notification
            # so that new customers can use flag next.
            customer_available.clear()

    def cut(self):
        print("Customer {} is now getting their hair cut.".format(self.name))

        cutTime = 10 * random.random()
        # Simulate time take for cut / processing of producer
        time.sleep(cutTime)

        global total_haircut_time
        total_haircut_time += cutTime

        global haircuts_completed
        haircuts_completed += 1

        print("Haircut complete. Time for haircut -> {}".format(cutTime))


if __name__ == '__main__':

    barbers = []

    # The Queue constructor creates a lock to protect the queue (our shared resource) when an element is added or removed.
    # Some conditions objects are created to notify events like the queue is not empty (get() call stops blocking),
    # queue is not full (put() call stops blocking) and all items have been processed (join() call stops blocking).

    # Our waiting room is a queue of size num_seats
    waiting_room = queue.Queue(num_seats)

    for worker in range(num_barbers):
        # Giving the Barber access to the Queue (waiting room).
        worker = Barber(waiting_room)
        # Starts the thread which calls the run method.
        worker.start()

        # Name our barber thread for easy identification.
        map_barber(worker)

        print("Barber ID: ", worker.name)
        barbers.append(worker)

    # Timeout used to control the production of new customers
    # for only the opening_time_length period.
    # Simulating an opening period for the barber shop.
    timeout = time.time() + opening_time_length

    # infinitely create customers while the shop
    # is open / still accepting customers.
    while True:
        if time.time() > timeout:
            print("STORE CLOSED. NO MORE CUSTOMERS ARE ALLOWED ENTER.")
            # No more customers are allowed to enter, but the ones
            # already inside can still get their hair cut.
            break
        print(" - Number of customer in waiting room", waiting_room.qsize())

        customer_frequency()

        new_customer = Customer(waiting_room)
        print("unique customer thread ID", new_customer.ident)

        # Start the new customer thread.
        new_customer.start()
        # This sleep prevents hogging of resources in infinite loop
        # due to use of timeout system.
        time.sleep(1)

    # Once the store is no longer open, terminate
    # all customer threads by waiting for all customers
    # threads in the waiting room to complete.
    waiting_room.join()

    print("The shop is closed, is the queue empty?", waiting_room.empty())

    shop_open.set()
    print("###############################")
    print("Barbershop closed. Stats below.")
    print("############################\n" * 2)
    print("Number of customers accepted for haircut (during opening time): {:>}".format(customers_gone_for_cut))
    print("----------------------------------")
    print("Total number of haircuts completed (during opening time): {:>7}".format(haircuts_completed))
    print("----------------------------------")
    print("Average haircut time: ", total_haircut_time / haircuts_completed)
