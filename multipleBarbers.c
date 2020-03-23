// Assumptions about the meaning of 'haircut':
// each thread has a unique PID
// each thread can get its own PID via system.info.PID
// a barber uses a customer's PID to cut that custmer's hair
// a customer uses a barber's PID to get his hair cut by that barber
// Assumptions about the operating environment:
// a semaphore releases threads in the order that they were queued

Semaphore Customers = 0;
Semaphore Barbers = 0;
Mutex AccessSeats = 1;
int NumberOfFreeSeats = N;
int SeatPocket[N];  // (or 'PID SeatPocket[N];' if PID is a data type)
int SitHereNext = 0;
int ServeMeNext = 0;

// main program must start a copy of this thread for each barber in the shop
Barber {
    int mynext, C;
    while(1) {
        sem_wait(Barbers);  // join queue of sleeping barbers
        sem_wait(AccessSeats);  // mutex to protect seat changes
        ServeMeNext = (ServeMeNext++) mod N;  // select next customer
        mynext = ServeMeNext;
        C = SeatPocket[mynext];  // get selected customer's PID
        SeatPocket[mynext] = system.info.PID;  // leave own PID for customer
        sem_post(AccessSeats);  // release the seat change mutex
        sem_post(Customers);  // wake up selected customer
        //
        // barber is cutting hair of customer 'C'
        //
    }
}

// main program must start a copy of this thread at random intervals
// to represent the arrival of a continual stream of customers
Customer {
    int myseat, B;
    sem_wait(AccessSeats);  // mutex to protect seat changes
    if(NumberOfFreeSeats > 0) {
        NumberOfFreeSeats--;  // sit down in one of the seats
        SitHereNext = (SitHereNext++) mod N;
        myseat = SitHereNext;
        SeatPocket[myseat] = system.info.PID;
        sem_post(AccessSeats);  // release the seat change mutex
        sem_post(Barbers);  // wake up one barber
        sem_wait(Customers);  // join queue of sleeping customers
        sem_wait(AccessSeats);  // mutex to protect seat changes
        B = SeatPocket[myseat];  // barber replaced my PID with his own
        NumberOfFreeSeats++;  // stand up
        sem_post(AccessSeats);  // release the seat change mutex
        //
        // customer is having hair cut by barber 'B'
        //
    } else {
        sem_post(AccessSeats);  // release the seat change mutex
        // customer leaves without haircut
    }
    system.thread.exit;  // (or signal main program to kill this thread)
}