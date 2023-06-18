from datetime import datetime, timedelta

def parse(x):
    #returns the string in singular form and lowered
    x = x.lower()
    if x[-1] == 's':
        return x[:-1]
    else:
        return x
    
def human_time_to_seconds(human_time):
    time_map = {"day":86400,"hour":3600,"minute":60,"second":1}
    time =[parse(i) for i in human_time.split(" ")]
    
    tot_seconds = 0
    for i in range(1,len(time),2):
        tot_seconds += (int(time[i-1]) * time_map[time[i]])
    return tot_seconds


if __name__ == "__main__":
    print (human_time_to_seconds("1 hour 30 minutes"))

    
