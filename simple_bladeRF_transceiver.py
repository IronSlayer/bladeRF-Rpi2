#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Simple Bladerf Transceiver
# Author: Renzo Chan Rios
# Generated: Tue Mar  8 09:38:05 2016
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import osmosdr
from time import sleep


class simple_bladeRF_transceiver(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Simple Bladerf Transceiver")

        ##################################################
        # Variables
        ##################################################
        self.symbole_rate = symbole_rate = 10e4
        self.samp_rate = samp_rate = 0.5e6
        self.samp_per_sym = samp_per_sym = int(samp_rate / symbole_rate)
        self.preamble = preamble = '0101010101010101'
        self.msg_source_msgq_in = msg_source_msgq_in = gr.msg_queue(2)
        self.msg_sink_msgq_out = msg_sink_msgq_out = gr.msg_queue(2)
        self.frequency_tx = frequency_tx = 473e6
        self.frequency_rx = frequency_rx = 473e6
        self.bit_per_sym = bit_per_sym = 1
        self.access_code = access_code = '11010011100100011101001110010001'

        ##################################################
        # Blocks
        ##################################################
        self.packet_encoder = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=samp_per_sym,
        		bits_per_symbol=bit_per_sym,
        		preamble=preamble,
        		access_code=access_code,
        		pad_for_usrp=False,
        	),
        	payload_length='',
        )
        self.packet_decoder = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code=access_code,
        		threshold=-1,
        		callback=lambda ok, payload: self.packet_decoder.recv_pkt(ok, payload),
        	),
        )
        self.osmosdr_source = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_source.set_sample_rate(samp_rate)
        self.osmosdr_source.set_center_freq(frequency_rx, 0)
        self.osmosdr_source.set_freq_corr(0, 0)
        self.osmosdr_source.set_dc_offset_mode(0, 0)
        self.osmosdr_source.set_iq_balance_mode(0, 0)
        self.osmosdr_source.set_gain_mode(False, 0)
        self.osmosdr_source.set_gain(3, 0)
        self.osmosdr_source.set_if_gain(0, 0)
        self.osmosdr_source.set_bb_gain(10, 0)
        self.osmosdr_source.set_antenna("", 0)
        self.osmosdr_source.set_bandwidth(6e6, 0)
          
        self.osmosdr_sink = osmosdr.sink( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_sink.set_sample_rate(samp_rate)
        self.osmosdr_sink.set_center_freq(frequency_tx, 0)
        self.osmosdr_sink.set_freq_corr(0, 0)
        self.osmosdr_sink.set_gain(15, 0)
        self.osmosdr_sink.set_if_gain(0, 0)
        self.osmosdr_sink.set_bb_gain(-4, 0)
        self.osmosdr_sink.set_antenna("", 0)
        self.osmosdr_sink.set_bandwidth(6e6, 0)
          
        self.gmsk_mod = digital.gmsk_mod(
        	samples_per_symbol=samp_per_sym,
        	bt=1,
        	verbose=False,
        	log=False,
        )
        self.gmsk_demod = digital.gmsk_demod(
        	samples_per_symbol=samp_per_sym,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )

        # initialize the blocks
        self.file_source = blocks.message_source(gr.sizeof_char*1, self.msg_source_msgq_in)
        self.file_sink = blocks.message_sink(gr.sizeof_char*1, self.msg_sink_msgq_out, True)


        #self.file_source = blocks.file_source(gr.sizeof_char*1, "/home/ipen/Escritorio/message.txt", True)
        #self.file_sink = blocks.file_sink(gr.sizeof_char*1, "/home/ipen/Escritorio/data_rx.txt", False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.file_source, 0), (self.packet_encoder, 0))    
        self.connect((self.gmsk_demod, 0), (self.packet_decoder, 0))    
        self.connect((self.gmsk_mod, 0), (self.osmosdr_sink, 0))    
        self.connect((self.osmosdr_source, 0), (self.gmsk_demod, 0))    
        self.connect((self.packet_decoder, 0), (self.file_sink, 0))    
        self.connect((self.packet_encoder, 0), (self.gmsk_mod, 0))    

    def send_pkt(self, payload):
        self.source_queue.insert_tail(gr.message_from_string(payload))

    def recv_pkt(self):
        pkt = ""

        if self.sink_queue.count():
            pkt = self.sink_queue.delete_head().to_string()

        return pkt  

    def get_symbole_rate(self):
        return self.symbole_rate

    def set_symbole_rate(self, symbole_rate):
        self.symbole_rate = symbole_rate
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))
        self.osmosdr_sink.set_sample_rate(self.samp_rate)
        self.osmosdr_source.set_sample_rate(self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_msg_source_msgq_in(self):
        return self.msg_source_msgq_in

    def set_msg_source_msgq_in(self, msg_source_msgq_in):
        self.msg_source_msgq_in = msg_source_msgq_in

    def get_msg_sink_msgq_out(self):
        return self.msg_sink_msgq_out

    def set_msg_sink_msgq_out(self, msg_sink_msgq_out):
        self.msg_sink_msgq_out = msg_sink_msgq_out

    def get_frequency_tx(self):
        return self.frequency_tx

    def set_frequency_tx(self, frequency_tx):
        self.frequency_tx = frequency_tx
        self.osmosdr_sink.set_center_freq(self.frequency_tx, 0)

    def get_frequency_rx(self):
        return self.frequency_rx

    def set_frequency_rx(self, frequency_rx):
        self.frequency_rx = frequency_rx
        self.osmosdr_source.set_center_freq(self.frequency_rx, 0)

    def get_bit_per_sym(self):
        return self.bit_per_sym

    def set_bit_per_sym(self, bit_per_sym):
        self.bit_per_sym = bit_per_sym

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = simple_bladeRF_transceiver()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
