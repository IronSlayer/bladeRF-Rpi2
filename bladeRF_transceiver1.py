#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: bladeRF_transceiver
# Author: Renzo Chan Rios
# Generated: Sun Mar 13 00:27:54 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import cc1111
import math
import osmosdr
import time


class bladeRF_transceiver(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "bladeRF_transceiver")

        ##################################################
        # Variables
        ##################################################
        self.symbole_rate = symbole_rate = 10e3
        self.samp_rate = samp_rate = 1e6
        self.rat_interop = rat_interop = 8
        self.rat_decim = rat_decim = 5
        self.firdes_transition_width = firdes_transition_width = 15000
        self.firdes_decim = firdes_decim = 4
        self.firdes_cuttoff = firdes_cuttoff = 21e3
        self.tx_rf_gain = tx_rf_gain = 10
        self.tx_bb_gain = tx_bb_gain = -20
        self.samp_per_sym_source = samp_per_sym_source = ((samp_rate/2/firdes_decim)*rat_interop/rat_decim) / symbole_rate
        self.samp_per_sym = samp_per_sym = int(samp_rate / symbole_rate)
        self.rx_rf_gain = rx_rf_gain = 3
        self.rx_bb_gain = rx_bb_gain = 20
        self.preamble = preamble = '0101010101010101'
        self.msg_source_msgq_in = msg_source_msgq_in = gr.msg_queue(2)
        self.msg_sink_msgq_out = msg_sink_msgq_out = gr.msg_queue(2)
        self.frequency_tx = frequency_tx = 450e6
        self.frequency_shift = frequency_shift = 520000
        self.frequency_rx = frequency_rx = 450.0e6
        self.firdes_filter = firdes_filter = firdes.low_pass(1,samp_rate/2, firdes_cuttoff, firdes_transition_width)
        self.bit_per_sym = bit_per_sym = 1
        self.bandwith = bandwith = 6e6
        self.access_code = access_code = '11010011100100011101001110010001'

        ##################################################
        # Blocks
        ##################################################
        self.xlating_fir_filter_1 = filter.freq_xlating_fir_filter_ccc(2, (1, ), frequency_shift, samp_rate)
        self.xlating_fir_filter_0 = filter.freq_xlating_fir_filter_ccc(firdes_decim, (firdes_filter), 0, samp_rate/2)
        self.throttle = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate/2,True)
        self.rational_resampler = filter.rational_resampler_ccc(
                interpolation=rat_interop,
                decimation=rat_decim,
                taps=None,
                fractional_bw=None,
        )
        self.quadrature_demod = analog.quadrature_demod_cf(2)
        self.osmosdr_source = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=1" )
        self.osmosdr_source.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_source.set_sample_rate(samp_rate)
        self.osmosdr_source.set_center_freq(frequency_rx-frequency_shift, 0)
        self.osmosdr_source.set_freq_corr(0, 0)
        self.osmosdr_source.set_dc_offset_mode(0, 0)
        self.osmosdr_source.set_iq_balance_mode(2, 0)
        self.osmosdr_source.set_gain_mode(False, 0)
        self.osmosdr_source.set_gain(rx_rf_gain, 0)
        self.osmosdr_source.set_if_gain(0, 0)
        self.osmosdr_source.set_bb_gain(rx_bb_gain, 0)
        self.osmosdr_source.set_antenna("", 0)
        self.osmosdr_source.set_bandwidth(bandwith, 0)
          
        self.osmosdr_sink = osmosdr.sink( args="numchan=" + str(1) + " " + "bladerf=1" )
        self.osmosdr_sink.set_sample_rate(samp_rate)
        self.osmosdr_sink.set_center_freq(frequency_tx, 0)
        self.osmosdr_sink.set_freq_corr(0, 0)
        self.osmosdr_sink.set_gain(tx_rf_gain, 0)
        self.osmosdr_sink.set_if_gain(0, 0)
        self.osmosdr_sink.set_bb_gain(tx_bb_gain, 0)
        self.osmosdr_sink.set_antenna("", 0)
        self.osmosdr_sink.set_bandwidth(bandwith, 0)
          
        self.gmsk_mod = digital.gmsk_mod(
            samples_per_symbol=int(samp_per_sym),
            bt=0.5,
            verbose=False,
            log=False,
        )
        self.correlate_access_code = digital.correlate_access_code_bb(access_code, 4)
        self.clock_recovery = digital.clock_recovery_mm_ff(samp_per_sym_source*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.cc1111_packet_encoder = cc1111.cc1111_packet_mod_base(cc1111.cc1111_packet_encoder(
                        samples_per_symbol=samp_per_sym,
                        bits_per_symbol=bit_per_sym,
                        preamble=preamble,
                        access_code=access_code,
                        pad_for_usrp=True,
                do_whitening=True,
                add_crc=True
                ),
            source_queue=msg_source_msgq_in
            )
        self.cc1111_packet_decoder = cc1111.cc1111_packet_decoder(msg_sink_msgq_out,True, True, False, True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.binary_slicer = digital.binary_slicer_fb()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.binary_slicer, 0), (self.correlate_access_code, 0))    
        self.connect((self.cc1111_packet_decoder, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.cc1111_packet_encoder, 0), (self.gmsk_mod, 0))    
        self.connect((self.clock_recovery, 0), (self.binary_slicer, 0))    
        self.connect((self.correlate_access_code, 0), (self.cc1111_packet_decoder, 0))    
        self.connect((self.gmsk_mod, 0), (self.osmosdr_sink, 0))    
        self.connect((self.osmosdr_source, 0), (self.xlating_fir_filter_1, 0))    
        self.connect((self.quadrature_demod, 0), (self.clock_recovery, 0))    
        self.connect((self.rational_resampler, 0), (self.quadrature_demod, 0))    
        self.connect((self.throttle, 0), (self.xlating_fir_filter_0, 0))    
        self.connect((self.xlating_fir_filter_0, 0), (self.rational_resampler, 0))    
        self.connect((self.xlating_fir_filter_1, 0), (self.throttle, 0))    


    def get_symbole_rate(self):
        return self.symbole_rate

    def set_symbole_rate(self, symbole_rate):
        self.symbole_rate = symbole_rate
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))
        self.set_samp_per_sym_source(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cuttoff, self.firdes_transition_width))
        self.set_samp_per_sym(int(self.samp_rate / self.symbole_rate))
        self.set_samp_per_sym_source(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)
        self.osmosdr_sink.set_sample_rate(self.samp_rate)
        self.osmosdr_source.set_sample_rate(self.samp_rate)
        self.throttle.set_sample_rate(self.samp_rate/2)

    def get_rat_interop(self):
        return self.rat_interop

    def set_rat_interop(self, rat_interop):
        self.rat_interop = rat_interop
        self.set_samp_per_sym_source(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_rat_decim(self):
        return self.rat_decim

    def set_rat_decim(self, rat_decim):
        self.rat_decim = rat_decim
        self.set_samp_per_sym_source(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_firdes_transition_width(self):
        return self.firdes_transition_width

    def set_firdes_transition_width(self, firdes_transition_width):
        self.firdes_transition_width = firdes_transition_width
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cuttoff, self.firdes_transition_width))

    def get_firdes_decim(self):
        return self.firdes_decim

    def set_firdes_decim(self, firdes_decim):
        self.firdes_decim = firdes_decim
        self.set_samp_per_sym_source(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim) / self.symbole_rate)

    def get_firdes_cuttoff(self):
        return self.firdes_cuttoff

    def set_firdes_cuttoff(self, firdes_cuttoff):
        self.firdes_cuttoff = firdes_cuttoff
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cuttoff, self.firdes_transition_width))

    def get_tx_rf_gain(self):
        return self.tx_rf_gain

    def set_tx_rf_gain(self, tx_rf_gain):
        self.tx_rf_gain = tx_rf_gain
        self.osmosdr_sink.set_gain(self.tx_rf_gain, 0)

    def get_tx_bb_gain(self):
        return self.tx_bb_gain

    def set_tx_bb_gain(self, tx_bb_gain):
        self.tx_bb_gain = tx_bb_gain
        self.osmosdr_sink.set_bb_gain(self.tx_bb_gain, 0)

    def get_samp_per_sym_source(self):
        return self.samp_per_sym_source

    def set_samp_per_sym_source(self, samp_per_sym_source):
        self.samp_per_sym_source = samp_per_sym_source
        self.clock_recovery.set_omega(self.samp_per_sym_source*(1+0.0))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym

    def get_rx_rf_gain(self):
        return self.rx_rf_gain

    def set_rx_rf_gain(self, rx_rf_gain):
        self.rx_rf_gain = rx_rf_gain
        self.osmosdr_source.set_gain(self.rx_rf_gain, 0)

    def get_rx_bb_gain(self):
        return self.rx_bb_gain

    def set_rx_bb_gain(self, rx_bb_gain):
        self.rx_bb_gain = rx_bb_gain
        self.osmosdr_source.set_bb_gain(self.rx_bb_gain, 0)

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

    def get_frequency_shift(self):
        return self.frequency_shift

    def set_frequency_shift(self, frequency_shift):
        self.frequency_shift = frequency_shift
        self.osmosdr_source.set_center_freq(self.frequency_rx-self.frequency_shift, 0)
        self.xlating_fir_filter_1.set_center_freq(self.frequency_shift)

    def get_frequency_rx(self):
        return self.frequency_rx

    def set_frequency_rx(self, frequency_rx):
        self.frequency_rx = frequency_rx
        self.osmosdr_source.set_center_freq(self.frequency_rx-self.frequency_shift, 0)

    def get_firdes_filter(self):
        return self.firdes_filter

    def set_firdes_filter(self, firdes_filter):
        self.firdes_filter = firdes_filter
        self.xlating_fir_filter_0.set_taps((self.firdes_filter))

    def get_bit_per_sym(self):
        return self.bit_per_sym

    def set_bit_per_sym(self, bit_per_sym):
        self.bit_per_sym = bit_per_sym

    def get_bandwith(self):
        return self.bandwith

    def set_bandwith(self, bandwith):
        self.bandwith = bandwith
        self.osmosdr_sink.set_bandwidth(self.bandwith, 0)
        self.osmosdr_source.set_bandwidth(self.bandwith, 0)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = bladeRF_transceiver()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
