import pyaudio
import numpy
import math
import time

import struct

nFFT = 4096
RATE = 44100


class FFTAnalyze:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    def __init__(self, detect_func, *, n_fft=nFFT, rate=RATE, s_freq=0, e_freq=150, keep=10, percent=.45, wait=.5):
        self.detect_func = detect_func
        self.s_freq = s_freq
        self.e_freq = e_freq
        self.keep_amount = keep
        self.percent = percent
        self.wait_time = wait
        self.pyAudio = pyaudio.PyAudio()
        self.run = True
        self.stream = self.pyAudio.open(format=FFTAnalyze.FORMAT,
                                        channels=FFTAnalyze.CHANNELS,
                                        rate=rate,
                                        input=True,
                                        frames_per_buffer=n_fft)
        self.bin_size = rate/n_fft

    def start(self):
        """
        Starts analyzing audio and looking for beats
        """
        lastbeat = time.time()
        averages = []
        for x in range(self.keep_amount):
            averages.append(1)
        while self.run:
            cur_amount = len(averages)
            if self.keep_amount != cur_amount:
                if self.keep_amount < cur_amount:
                    while self.keep_amount != len(averages):
                        averages.pop(0)
                elif self.keep_amount < cur_amount:
                    avg = sum(averages)/cur_amount
                    while self.keep_amount != len(averages):
                        averages.append(avg)
            self.do_fft()
            mag = self.get_average(self.s_freq, self.e_freq)
            avg = sum(averages)/self.keep_amount
            averages.pop(0)
            if (mag/avg)-1 > self.percent:
                now = time.time()
                if ((now-lastbeat) > self.wait_time) and self.relative_range() > .009:
                    lastbeat = now
                    self.detect_func()
                    averages.append(avg)
                else:
                    averages.append(mag)
            else:
                averages.append(mag)

    def do_fft(self):
        """
        Calculates one pass of the fft and stores info about it
        """
        start = time.time()
        self.record_chunk()
        self.window()
        self.calculate_mags()
        end = time.time()

    def window(self):
        """
        Uses the hanning window to prep data
        """
        hanning = numpy.hanning(nFFT)
        for i in range(nFFT):
            self.cur_input[i] *= hanning[i]

    def relative_range(self):
        """
        Prints the total relative magnitude between start and end range
        """
        self.calculate_relative_mags()
        string = '{:.0f}-{:.0f}Hz: {:.5f}'
        s_ind = self.get_bin(self.s_freq)
        e_ind = self.get_bin(self.e_freq)
        lst = self.rel_mags[s_ind:e_ind+1]
        return sum(lst)/len(lst)

    def print_relatives(self):
        """
        Prints the percentages of frequencies relative to each other
        """
        self.calculate_relative_mags()
        string = '{:.0f}-{:.0f}Hz: {:.5f}'
        freq = 0
        next_freq = freq+self.bin_size
        for mag in self.rel_mags[:10]:
            print(string.format(freq, next_freq, mag))
            freq = next_freq
            next_freq += self.bin_size

    def print_octaves(self):
        """
        Prints the percentages of octaves relative to each other
        """
        string = '{:.0f}-{:.0f}Hz: {:.5f}'
        num = 5
        freq = 0
        next_freq = num * self.bin_size
        for octave in self.octaves:
            print(string.format(freq, next_freq, octave))
            freq = next_freq
            num *= 2
            next_freq += num * self.bin_size

    def get_bin(self, freq):
        """
        Gets the bin that contains a certain frequency
        """
        bin_ind = int(freq//self.bin_size)
        if (freq % self.bin_size == 0) and bin_ind != 0:
            bin_ind -= 1
        return bin_ind

    def get_average(self, s_freq, e_freq):
        """
        Gets the average magnitude between two frequencies
        """
        s_ind = self.get_bin(s_freq)
        e_ind = self.get_bin(e_freq)
        lst = self.mags[s_ind:e_ind+1]
        try:
            avg = sum(lst)/len(lst)
        except:
            print(s_ind, e_ind)
            print('werid stuff')
            avg = 0
        return avg

    def divide_octaves(self):
        """
        Divides the relative frequencies into different octaves
        """
        octaves = []
        n_bins = 5
        cur_bin = 0
        cur_octave = 0
        while True:
            octaves.append(0)
            for i in range(n_bins):
                if cur_bin >= len(self.rel_mags):
                    self.octaves = octaves
                    return
                octaves[cur_octave] += self.rel_mags[cur_bin]
                cur_bin += 1
            n_bins *= 2
            cur_octave += 1

    def record_chunk(self):
        """
        Records a nFFT chunk of data and stores in self
        """
        data = self.stream.read(nFFT)
        data_array = bytearray(data)
        self.cur_input = []
        for i in range(nFFT):
            amp = struct.unpack('H', data_array[:2])
            for _ in range(2):
                data_array.pop(0)
            self.cur_input.append(amp)

    def calculate_mags(self):
        """
        Calculates magnitudes of frequencies from input
        """
        res = numpy.fft.rfft(self.cur_input)
        self.mags = []
        for num in res[1:]:
            real = float(numpy.real(num))
            imag = float(numpy.imag(num))
            mag = math.sqrt((real**2)+(imag**2))
            self.mags.append(mag)

    def calculate_relative_mags(self):
        """
        Calculates the relative magnitudes of frequencies based on the total
        """
        total = sum(self.mags)
        self.rel_mags = []
        for mag in self.mags:
            try:
                rel = mag/total
            except ZeroDivisionError:
                rel = 0
            self.rel_mags.append(rel)

    def stop(self):
        """
        Stops recording
        """
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()

if __name__ == '__main__':
    analyze = FFTAnalyze(nFFT)
    analyze.start()
