import threading
import time

pkt_sent = 0
ack = 0
last_ack = 1
i=0
should_continue = True
new_pkt = False

def timer(timeInMilliseconds):
    global ack
    global last_ack
    while timeInMilliseconds > 0:
        timeInMilliseconds -= 1
        if last_ack != ack:
            break
        else:
            time.sleep(0.1)

def sender(num_pkts):
    global pkt_sent
    global ack
    global last_ack
    global new_pkt
    print("\n")
    while pkt_sent < num_pkts:
        if ack != last_ack:
            last_ack = ack
            pkt_sent += 1
            print(f"Packet {pkt_sent} sent.")
        else:
            print("Acknowledge timed out.")
            print(f"Packet {pkt_sent} re-sent.")
        new_pkt = True
        #time out of upto 0.5 seconds
        timer(5)
    should_continue = False

def reciever(lost_pkt, lost_ack):
    global ack
    global pkt_sent
    global new_pkt
    global should_continue

    pkt_loss = True
    ack_loss = True

    while should_continue:
        if new_pkt == True:
            if pkt_sent == lost_pkt and pkt_loss == True:
                pkt_loss = False
            elif pkt_sent == lost_ack and ack_loss == True:
                ack_loss = False
            else:
                ack = (ack+1)%2
                print(f"Acknowledgement {ack} recieved.")
                print("\n")
            new_pkt = False

num_pkts = int(input("Number of packets: "))
lost_ack = int(input("Acknowledgement lost: "))
lost_pkt = int(input("Packet Lost: "))

t1 = threading.Thread(target=sender , args=(num_pkts,))
t2 = threading.Thread(target=reciever, args=(lost_pkt, lost_ack,))

t1.start()
t2.start()

t1.join()
t2.join()