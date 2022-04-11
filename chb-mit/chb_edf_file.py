from abc import abstractmethod, ABCMeta
from collections import OrderedDict
import datetime
import numpy as np
import re

from pyedflib import EdfReader

class ChbEdfFile(object):
    """
    Edf reader using pyedflib
    """
    def __init__(self, filename, patient_id=None):
        self._filename = filename
        self._patient_id = patient_id
        self._file = EdfReader(filename)

    def get_filename(self):
        return self._filename

    def get_n_channels(self):
        """
        Number of channels
        """
        return len(self._file.getSampleFrequencies())

    def get_n_data_points(self):
        """
        Number of data points
        """
        if len(self._file.getNSamples()) < 1:
            raise ValueError("Number of channels is less than 1")
        return self._file.getNSamples()[0]

    def get_channel_names(self):
        """
        Names of channels
        """
        return self._file.getSignalLabels()

    def get_channel_scalings(self):
        """
        Channel scalings as an array
        :return:
        """
        out = np.zeros(self.get_n_channels())
        for i in range(self.get_n_channels()):
            out[i] = self._file.getPhysicalMaximum(i) - self._file.getPhysicalMinimum(i)
        return out

    def get_file_duration(self):
        """
        Returns the file duration in seconds
        """
        return self._file.getFileDuration()

    def get_sampling_rate(self):
        """
        Get the frequency
        """
        if len(self._file.getSampleFrequencies()) < 1:
            raise ValueError("Number of channels is less than 1")
        return self._file.getSampleFrequency(0)

    def get_channel_data(self, channel_id):
        """
        Get raw data for a single channel
        """
        if channel_id >= self.get_n_channels() or channel_id < 0:
            raise ValueError("Illegal channel id selected %d" % channel_id)
        return self._file.readSignal(channel_id)

    def get_data(self):
        """
        Get raw data for all channels
        """
        output_data = np.zeros((self.get_n_data_points(), self.get_n_channels()))
        for i in range(self.get_n_channels()):
            output_data[:,i] = self._file.readSignal(i)
        return output_data

    def get_start_datetime(self):
        """
        Get the starting date and time
        """
        return self._file.getStartdatetime()

    def get_end_datetime(self):
        return self._file.getStartdatetime() + datetime.timedelta(seconds=self._file.getFileDuration())