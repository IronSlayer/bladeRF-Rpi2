#!/usr/bin/python
import signal, sys, time, threading, bladeRF_transceiver1, datetime
from gnuradio import gr
from time import sleep

def signal_handler(signal, frame):
	global rf
	print('You pressed Ctrl+C!')
	rf.stop()
	sys.exit(0)

def send_str(payload):
	rf.msg_source_msgq_in.insert_tail(gr.message_from_string(payload))

if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)
	try:
		rf = bladeRF_transceiver1.bladeRF_transceiver()
		ID = 'AI01'
		MSG = 'THIS IS JUST A TEST MESSAGE'
		rf.set_frequency_tx(long(850e6))
		rf.set_frequency_rx(long(900e6))
		rf.start()
		while True:
                        
			if rf.msg_sink_msgq_out.count():
				data = rf.msg_sink_msgq_out.delete_head().to_string()
				if data == ID:
					TS = str(datetime.datetime.now())
					TS = TS[:19]
					frame = gr.message_from_string(MSG+' '+TS)
					rf.msg_source_msgq_in.insert_tail(frame)
					rf.msg_source_msgq_in.insert_tail(frame)
					rf.msg_source_msgq_in.insert_tail(frame)
				else:
					print 'no valid ID'
			
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")



