import numpy as np
import os
import pandas as pd
from scipy.interpolate import interp1d


class VDriveToMtex(object):

    vdrive_handler_file = ''  # name of input file (produced by vdrive_handler.py
    raw_data = []
    raw_data_sorted = []

    a111 = np.zeros((19, 12))
    a200 = np.zeros((19, 12))
    a220 = np.zeros((19, 12))
    a311 = np.zeros((19, 12))
    a222 = np.zeros((19, 12))

    a111_interpolated = []

    psi = np.arange(0, 91, 5)
    phi = np.arange(0, 331, 30)

    def __init__(self, filename=''):
        if filename == '':
            raise ValueError("Please provide an input file (output of vdrive_handler.py")

        if not os.path.exists(filename):
            raise ValueError("File does not exist ({})".format(filename))

        self.vdrive_handler_file = filename

    def run(self):
        self.load()
        self.sort_raw_data()
        self.interpolation()

    def load(self):
        vdrive_handler_file = self.vdrive_handler_file
        self.raw_data = pd.read_csv(vdrive_handler_file, sep=',')

    def sort_raw_data(self):
        """format the ducu.txt data

        only the first 7 columns of data will be used
        The data are sorted according to psi and then phi
        """
        raw_data_sorted = self.raw_data.sort_values(['#psi', 'phi'])
        self.raw_data_sorted = raw_data_sorted

        # get ride of first 2 columns (psi and phi
        clean_data_sorted = np.array(raw_data_sorted.drop(['#psi', 'phi'], axis=1))
        self.i_over_v_data_only = clean_data_sorted

        a111 = self.a111
        a200 = self.a200
        a220 = self.a220
        a311 = self.a311
        a222 = self.a222

        a111_flatten = a111.flatten()
        a200_flatten = a200.flatten()
        a220_flatten = a220.flatten()
        a311_flatten = a311.flatten()
        a222_flatten = a222.flatten()

        # special case for psi and phi = 0
        a111_flatten[0:12] = clean_data_sorted[0, 0]
        a200_flatten[0:12] = clean_data_sorted[0, 1]
        a220_flatten[0:12] = clean_data_sorted[0, 2]
        a311_flatten[0:12] = clean_data_sorted[0, 3]
        a222_flatten[0:12] = clean_data_sorted[0, 4]

        # all over psi and phi
        i_over_v_flatten_for_a111 = clean_data_sorted[:, 0].flatten()
        a111_flatten[12: ] = i_over_v_flatten_for_a111[1: ]

        i_over_v_flatten_for_a200 = clean_data_sorted[:, 1].flatten()
        a200_flatten[12: ] = i_over_v_flatten_for_a200[1: ]

        i_over_v_flatten_for_a220 = clean_data_sorted[:, 2].flatten()
        a220_flatten[12: ] = i_over_v_flatten_for_a220[1: ]

        i_over_v_flatten_for_a311 = clean_data_sorted[:, 3].flatten()
        a311_flatten[12: ] = i_over_v_flatten_for_a311[1: ]

        i_over_v_flatten_for_a222 = clean_data_sorted[:, 4].flatten()
        a222_flatten[12: ] = i_over_v_flatten_for_a222[1: ]

        # reshaping the arrays
        a111 = np.reshape(a111_flatten, (19, 12))
        a200 = np.reshape(a200_flatten, (19, 12))
        a220 = np.reshape(a220_flatten, (19, 12))
        a311 = np.reshape(a311_flatten, (19, 12))
        a222 = np.reshape(a222_flatten, (19, 12))

        self.a111 = a111
        self.a200 = a200
        self.a220 = a220
        self.a311 = a311
        self.a222 = a222

    def interpolation(self):
        """this will create an interpolated version of the arrays

        before phi axis: [0, 30, 60, 90 .... 330]
        after phi axis: [0, 5, 10, 15, 20, 25, 30, 35, 40]
        """
        psi = self.psi
        old_xaxis = self.phi
        old_xaxis = np.append(old_xaxis, 360) # duplicate of value at 0 degrees for interpolation
        new_xaxis = np.arange(0, 359, 5)

        def __interpolation(a):
            # copy angle=0 value to end (360 degrees)
            a_interpolated = []
            for _row in a:
                _row = np.append(_row, _row[0])
                f = interp1d(old_xaxis, _row)
                a_interpolated.append(f(new_xaxis))
            return np.array(a_interpolated)

        self.a111_interpolated = __interpolation(self.a111)
        self.a200_interpolated = __interpolation(self.a200)
        self.a220_interpolated = __interpolation(self.a220)
        self.a222_interpolated = __interpolation(self.a222)
        self.a311_interpolated = __interpolation(self.a311)

    def export(self, filename=''):
        if filename == '':
            raise ValueError("Please provide a file name")

        psi = self.psi
        data = []

        def _create_data_array(pole_figure, a_interpolated):
            """create the string array for the given a interpolated"""
            data.append("*Dump of file:XQG")
            data.append("*Sample: VULCAN")
            data.append("*Corrected, rescaled data * Phi range    0.00 -  360.00 Step    5.00")
            data.append("*Pole figure: {}".format(pole_figure))

            for _index, _psi in enumerate(psi):
                data.append("*Khi =   {:.2f}".format(_psi))
                _local_data_reshape = np.reshape(a_interpolated[_index, :], (9, 8))
                for _row in _local_data_reshape:
                    _str_row = ["{:1.4f}".format(value) for value in _row]
                    new_entry = "  " + "  ".join(_str_row)
                    data.append(new_entry)

            data.append("")

        _create_data_array("111", self.a111_interpolated)
        _create_data_array("200", self.a200_interpolated)
        _create_data_array("220", self.a220_interpolated)
        _create_data_array("311", self.a311_interpolated)
        self.data = data

        self.__create_ascii(data=data, filename=filename)

    def __create_ascii(self, data=[], filename=''):
        with open(filename, 'w') as f:
            for _data in data:
                _line = _data + "\n"
                f.write(_line)

