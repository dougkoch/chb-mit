import datetime
import numpy as np
from pyedflib import EdfReader

from .utils import cached_getter

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

    @cached_getter
    def get_n_channels(self):
        """
        Number of channels
        """
        return len(self._file.getSampleFrequencies())

    @cached_getter
    def get_n_data_points(self):
        """
        Number of data points
        """
        if len(self._file.getNSamples()) < 1:
            raise ValueError("Number of channels is less than 1")
        return self._file.getNSamples()[0]

    @cached_getter
    def get_channel_names(self):
        """
        Names of channels
        """
        return self._file.getSignalLabels()

    @cached_getter
    def get_channel_scalings(self):
        """
        Channel scalings as an array
        :return:
        """
        out = np.zeros(self.get_n_channels())
        for i in range(self.get_n_channels()):
            out[i] = self._file.getPhysicalMaximum(i) - self._file.getPhysicalMinimum(i)
        return out

    @cached_getter
    def get_file_duration(self):
        """
        Returns the file duration in seconds
        """
        return self._file.getFileDuration()

    @cached_getter
    def get_sampling_rate(self):
        """
        Get the frequency
        """
        if len(self._file.getSampleFrequencies()) < 1:
            raise ValueError("Number of channels is less than 1")
        return self._file.getSampleFrequency(0)

    @cached_getter
    def get_channel_data(self, channel_id):
        """
        Get raw data for a single channel
        """
        if channel_id >= self.get_n_channels() or channel_id < 0:
            raise ValueError(f"Illegal channel id selected {channel_id}")
        return self._file.readSignal(channel_id)

    @cached_getter
    def get_data(self):
        """
        Get raw data for all channels
        """
        output_data = np.zeros((self.get_n_data_points(), self.get_n_channels()))
        for i in range(self.get_n_channels()):
            output_data[:,i] = self._file.readSignal(i)
        return output_data

    @cached_getter
    def get_start_datetime(self):
        """
        Get the starting date and time
        """
        return self._file.getStartdatetime()

    @cached_getter
    def get_end_datetime(self):
        return self._file.getStartdatetime() + datetime.timedelta(seconds=self._file.getFileDuration())
    
    filename = property(get_filename)
    n_channels = property(get_n_channels)
    n_data_points = property(get_n_data_points)
    channel_names = property(get_channel_names)
    channel_scalings = property(get_channel_scalings)
    file_duration = property(get_file_duration)
    sampling_rate = property(get_sampling_rate)
    data = property(get_data)
    start_datetime = property(get_start_datetime)
    end_datetime = property(get_end_datetime)