#!/usr/bin/python
import signal
import sys
from gnuradio import gr
import bladeRF_transceiver
#import bladeRF_transceiver
from time import sleep
import datetime

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
	nf = str(datetime.datetime.now())
	nf = nf[:10]
	archi=open(nf,'a')
	archi.write(msg+'\n')
	archi.close()

def send_str(payload):
	rf.msg_source_msgq_in.insert_tail(gr.message_from_string(payload))

def recv_str():
    pkt = rf.msg_sink_msgq_out.delete_head().to_string()
    return pkt            

if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)
	try:
		rf = bladeRF_transceiver.bladeRF_transceiver()
		rf.set_frequency_tx(long(473e6))
		rf.set_frequency_rx(long(450e6))
		#creartxt()
		rf.start()

		while True:
			# Send a Beacon:
			send_str('AI01')
			sleep(0.5)
			# Receive a string
			if rf.msg_sink_msgq_out.count():
				msg = rf.msg_sink_msgq_out.delete_head().to_string()
				grabartxt()
				print msg
				
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")


	# signal.signal(signal.SIGINT, signal_handler)
	# try:
	# 	rf = bladeRF_transceiver.bladeRF_transceiver()
	# 	rf.set_frequency_tx(long(450e6))
	# 	rf.set_frequency_rx(long(473000000))
	# 	creartxt()
	# 	rf.start()

	# 	while True:
			
	# 		# Send a string
	# 		beacon = gr.message_from_string('AI01')
	# 		rf.msg_source_msgq_in.insert_tail(beacon)
	# 		#beacon = gr.message_from_string('BI01')
	# 		#rf.msg_source_msgq_in.insert_tail(beacon)
	# 		#sleep(1)
	# 		# if rf.msg_sink_msgq_out.count():
	# 		# 	data = rf.msg_sink_msgq_out.delete_head().to_string()
	# 		#   	if data == 'AI01'*8:
	# 		#   		print '[Data] : %s '% data[:4]
			
	# 		# Receive a string
	# 		if rf.msg_sink_msgq_out.count():
	# 			msg = rf.msg_sink_msgq_out.delete_head().to_string()
	# 			grabartxt()
	# 			print msg
				

