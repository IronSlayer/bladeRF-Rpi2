#!/usr/bin/python
import signal
import sys
from gnuradio import gr
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
		FID = '1'
		SN = '1'
		D_CID = 'A'
		S_CID = 'C'
		M = '1'
		rf.set_frequency_tx(long(450e6))
		rf.set_frequency_rx(long(476e6))
		arduinoPort = serial.Serial('/dev/ttyUSB0',9600,timeout=0.5)
		sleep(2)		
		rf.start()

		while True:
			# Send a string
			#beacon = gr.message_from_string('AI01')
			#rf.msg_source_msgq_in.insert_tail(beacon)
                        # Receive a string
                        
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
				else:
					print 'no valid ID'
			
	except KeyboardInterrupt:
		print("W: interrupt received, proceeding")



