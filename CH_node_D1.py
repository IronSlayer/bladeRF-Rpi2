#!/usr/bin/python
import signal, sys, time, threading, bladeRF_transceiver, datetime
from gnuradio import gr
from time import sleep

def signal_handler(signal, frame):
	global rf
	print('You pressed Ctrl+C!')
	rf.stop()
	sys.exit(0)

def creartxt():
	nf = str(datetime.datetime.now())
	nf = nf[:10]
	archi=open(nf,'w')
	archi.close()

def grabartxt():
	try:
		nf = str(datetime.datetime.now())
		nf = nf[:10]
		archi=open(nf,'a')
		archi.write(msg+'\n')
		archi.close()
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")

	threading.Timer(5, grabartxt).start()

def send_str(payload):
	rf.msg_source_msgq_in.insert_tail(gr.message_from_string(payload))

def recv_str():
    pkt = rf.msg_sink_msgq_out.delete_head().to_string()
    return pkt            

def print_console():
	try:
		print msg
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")

	threading.Timer(5, print_console).start()

def send():
	try:
		# Send a Beacon:
		send_str('AI01')
		send_str('AI01')
		send_str('AI01')
		send_str('AI01')
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")
	threading.Timer(5, send).start()

if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)
	try:
		msg = '=============== EXPERIMENT D1 - Cluster Head Node and Sensor Node Interaction ==============='
		rf = bladeRF_transceiver.bladeRF_transceiver()
		rf.set_frequency_tx(long(900e6))
		rf.set_frequency_rx(long(850e6))
		rf.start()
		grabartxt()
		send()
		print_console()

		while True:
			if rf.msg_sink_msgq_out.count():
				msg = rf.msg_sink_msgq_out.delete_head().to_string()
				
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")
