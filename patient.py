import glob
import numpy as np

from chb_edf_file import ChbEdfFile
from chb_label_wrapper import ChbLabelWrapper

class Patient:
    def __init__(self, id):
        self._id = id
        self._edf_files = map(
            lambda filename: ChbEdfFile(filename, self._id),
            glob.glob("physionet.org/pn6/chbmit/chb%02d/*.edf" % self._id)
        )
        self._cumulative_duration = [0]
        
        for file in self._edf_files[:-1]:
            self._cumulative_duration.append(self._cumulative_duration[-1] + file.get_file_duration())
        
        self._duration = sum(self._cumulative_duration)
        
        self._seizure_list = ChbLabelWrapper("physionet.org/pn6/chbmit/chb%02d/chb%02d-summary.txt" % (self._id, self._id)).get_seizure_list()
        self._seizure_intervals = []

        for i, file in enumerate(self._seizure_list):
            for seizure in file:
                begin = seizure[0] * self._edf_files[i].get_sampling_rate() + self._cumulative_duration[i]
                end = seizure[1] * self._edf_files[i].get_sampling_rate() + self._cumulative_duration[i]
                self._seizure_intervals.append((begin, end))

    def get_channel_names(self):
        return self._edf_files[0].get_channel_names()

    def get_eeg_data(self):
        for i, file in enumerate(self._edf_files):
            print "Reading EEG data from file %s" % file._filename
            if not i:
                data = file.get_data()
            else:
                data = np.vstack((data, file.get_data()))

        return data

    def get_seizures(self):
        return self._seizure_list

    def get_seizure_intervals(self):
        return self._seizure_intervals

    def get_seizure_labels(self):
        labels = np.zeros(self._duration)

        for i, interval in enumerate(self._seizure_intervals):
                labels[interval[0]:interval[1]] = 1

        return labels

    def get_seizure_clips(self):
        clips = []
        data = self.get_eeg_data()
        labels = self.get_seizure_labels()

        for i in range(len(self._seizure_intervals)):
            if not i:
                left = 0
            else:
                left = (self._seizure_intervals[i-1][1] + self._seizure_intervals[i][0]) / 2
            if i == len(self._seizure_intervals) - 1:
                right = -1
            else:
                right = (self._seizure_intervals[i][1] + self._seizure_intervals[i+1][0]) / 2
            clips.append((data[left:right], labels[left:right]))
        
        return clips
