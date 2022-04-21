import threading
import time

window_size = 4
pkt_sent = 0
new_pkt = False
ack = []
should_continue = True
    

def sender(num_pkts):
    global pkt_sent
    global ack
    global new_pkt
    sf=0
    sn=0
    i = 0
    resend = -1
    np = 0
    print("\n")
    while np<num_pkts:
        if resend !=-1:
            pkt_sent=resend
            resend = -1
            new_pkt=True
            print(f"Packet {pkt_sent} re-sent.")
        elif sn-sf<=window_size-1 and sn != num_pkts and sf !=num_pkts:
            pkt_sent = sn
            sn+=1
            new_pkt = True
            print(f"Packet {pkt_sent} sent.")

        i+=1
        time.sleep(0.1)
        if sf in ack:
            print(f"Acknowledge recieved for {sf}")
            sf+=1
            np+=1
        else:
            print(f"N-ACK for {sf} recieved")
            resend = sf
    should_continue = False


def reciever(lost_pkt, lost_ack, num_pkts):
    global new_pkt
    global pkt_sent
    global ack
    i = 0
    lost_pkt_flag = True
    lost_ack_flag = True
    while i<num_pkts and should_continue == True:
        if new_pkt==True:
            if pkt_sent == lost_pkt and lost_pkt_flag == True:
                new_pkt = False
                lost_pkt_flag = False
            elif pkt_sent == lost_ack and lost_ack_flag == True:
                new_pkt = False
                lost_ack_flag = False
            else:
                new_pkt = False
                print(f"Recieved Packet {pkt_sent}.")
                ack.append(pkt_sent)
            



num_pkts = int(input("Number of packets: "))
lost_ack = int(input("Acknowledgement lost: "))
lost_pkt = int(input("Packet Lost: "))

t1 = threading.Thread(target=sender , args=(num_pkts,))
t2 = threading.Thread(target=reciever, args=(lost_pkt, lost_ack, num_pkts,))

t1.start()
t2.start()

t1.join()
t2.join()