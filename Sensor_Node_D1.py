#!/usr/bin/python
import signal
import sys
from gnuradio import gr
#import simple_transceiver
import bladeRF_transceiver
import serial
import datetime
from time import sleep

def signal_handler(signal, frame):
	global rf
	print('You pressed Ctrl+C!')
	arduinoPort.close()	
	rf.stop()
	sys.exit(0)

def send_str(payload):
	rf.msg_source_msgq_in.insert_tail(gr.message_from_string(payload))

if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)
	try:
		rf = bladeRF_transceiver.bladeRF_transceiver()
		ID = 'AI01'
		MSG = 'THIS IS JUST A TEST MESSAGE'
		rf.set_frequency_tx(long(450e6))
		rf.set_frequency_rx(long(473e6))

		while True:
                        
			if rf.msg_sink_msgq_out.count():
				data = rf.msg_sink_msgq_out.delete_head().to_string()
				if data == ID:
					print data
					arduinoPort.write('a')
					SD = arduinoPort.readline()
					TS = str(datetime.datetime.now())
					TS = TS[:19]
					frame = gr.message_from_string(FID+','+SN+','+TS+','+D_CID+','+S_CID+','+M+','+SD[4:19])
					rf.msg_source_msgq_in.insert_tail(frame)
					rf.msg_source_msgq_in.insert_tail(frame)
					rf.msg_source_msgq_in.insert_tail(frame)
					print FID+','+SN+','+TS+','+D_CID+','+S_CID+','+M+','+SD[4:19]
				else:
					print 'no valid ID'
			
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")



