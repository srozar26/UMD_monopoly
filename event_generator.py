import random

def event_generator():
    """randomly selects an event to occur
    """
    good_events = {1:" you get a car",3:"you get a new dorm",
                   5:"you get a scooter"}
    
    bad_events = {2:"you get a parking ticket",4:"you have your dorm flooded",
                  6:"you get a flat on your scooter wheel"}
    random_good_event = random.choice(list(good_events.values()))
    random_bad_event = random.choice(list(bad_events.values()))

    random_event = random.randint(1,2)


    if random_event == 1:

        print("Your good event is",random_good_event)
    else:
        print("Your bad event is",random_bad_event)
if __name__ == "__main__":
    event_generator()
