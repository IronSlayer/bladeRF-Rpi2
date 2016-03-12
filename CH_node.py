#!/usr/bin/python
import signal
import sys
from gnuradio import gr
import simple_transceiver
import bladeRF_transceiver
from time import sleep

def signal_handler(signal, frame):
	global rf
	print('You pressed Ctrl+C!')
	rf.stop()
	sys.exit(0)

if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)
	try:
		rf = bladeRF_transceiver.bladeRF_transceiver()
		rf.set_frequency_tx(long(450e6))
		rf.set_frequency_rx(long(473e6))
		rf.start()

		while True:
			# Send a string
			beacon = gr.message_from_string('AI01')
			rf.msg_source_msgq_in.insert_tail(beacon)

			# if rf.msg_sink_msgq_out.count():
			# 	data = rf.msg_sink_msgq_out.delete_head().to_string()
			#   	if data == 'AI01'*8:
			#   		print '[Data] : %s '% data[:4]
			
			# Receive a string
			if rf.msg_sink_msgq_out.count():
				msg = rf.msg_sink_msgq_out.delete_head().to_string()
				print msg
			
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")



