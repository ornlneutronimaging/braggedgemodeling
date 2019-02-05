import unittest
import os
import numpy as np
import shutil

from bem.texture.preparation.vdrive_to_mtex import VDriveToMtex


class TestVDriveToMtexHandler(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path,
                                                      '../../data/'))
        self.export_folder = self.data_path + '/temporary_folder/'
        self.export_filename = "my_VULCAN.rpf"
        self.input_filename = os.path.join(self.data_path, 'my_ducu.txt')
        os.mkdir(self.export_folder)

        # max diff allowed to compare two arrays
        self.maxDiff = 0.0001

    def tearDown(self):
        shutil.rmtree(self.export_folder)

    def test_input_file_mandatory(self):
        """assert error raised if input file missing or does not exist"""
        # no input file
        self.assertRaises(ValueError, VDriveToMtex)
        # file does not exist
        input_file = "i_do_not_exist"
        self.assertRaises(ValueError, VDriveToMtex, input_file)

    def test_loading_data(self):
        """assert data are correctly loaded, and just as they are, raw"""
        input_file = self.input_filename
        o_handler = VDriveToMtex(filename=input_file)
        o_handler.load()

        raw_data = o_handler.raw_data
        expected_shape = (217, 12)
        returned_shape = np.shape(raw_data)

        self.assertEqual(expected_shape, returned_shape)

    def test_sorting_data(self):
        """assert the data are sorted using ascending psi and phi"""
        input_file = self.input_filename
        o_handler = VDriveToMtex(filename=input_file)
        o_handler.load()
        o_handler.sort_raw_data()

        data_sorted = o_handler.raw_data_sorted
        psi_column = np.array(data_sorted['#psi'])
        phi_column = np.array(data_sorted['phi'])

        expected_phi_column = np.array([0, 0, 30, 60, 90, 120, 150])
        returned_phi_column = phi_column[0: 7]
        self.assertTrue((expected_phi_column == returned_phi_column).all())

        expected_psi_column = np.array([0, 5, 5, 5, 5, 5, 5])
        returned_psi_column = psi_column[0: 7]
        self.assertTrue((expected_psi_column == returned_psi_column).all())

    def test_a111_arrays(self):
        """assert the a111 is correctly defined"""
        input_file = self.input_filename
        o_handler = VDriveToMtex(filename=input_file)
        o_handler.load()
        o_handler.sort_raw_data()

        a111 = o_handler.a111
        # psi and phi == 0
        a111_expected = np.zeros((19, 12))
        a111_expected[0, :] = 0.81264008
        a111_expected[1, 0] = 0.842873
        a111_expected[1, 1] = 0.7020292
        a111_expected[1, 2] = 0.6603301

        for _returned, _expected in zip(a111[0, :], a111_expected[0, :]):
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)
        for _returned, _expected in zip(a111[1, 0:3], a111_expected[1, 0:3]):
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_interpolation(self):
        """assert interpolation of a111 works"""
        input_file = self.input_filename
        o_handler = VDriveToMtex(filename=input_file)
        o_handler.load()
        o_handler.sort_raw_data()
        o_handler.interpolation()

        a111_interpolated = o_handler.a111_interpolated
        a111_1_1_expected = [0.8429,  0.8194,  0.7959,  0.7725,  0.7490,  0.7255,  0.7020, 0.6951,
                             0.6881,  0.6812,  0.6742,  0.6673,  0.6603,  0.6725,  0.6846,  0.6967,
                             0.7089,  0.7210,  0.7331,  0.7414,  0.7497,  0.7580,  0.7663,  0.7746,
                             0.7828,  0.7918,  0.8008,  0.8097,  0.8187,  0.8276,  0.8366,  0.8401,
                             0.8437,  0.8473,  0.8508,  0.8544,  0.8580,  0.8880,  0.9179,  0.9479,
                             0.9779,  1.0079, 1.0379, 1.0434,  1.0490,  1.0545,  1.0601,  1.0656,
                             1.0712,  1.0594,  1.0476,  1.0358,  1.0241,  1.0123,  1.0005,  1.0030,
                             1.0056,  1.0082,  1.0107,  1.0133,  1.0159,  1.0113,  1.0067,  1.0022,
                             0.9976,  0.9930,  0.9885,  0.9642,  0.9399,  0.9157,  0.8914,  0.8671]
        a111_1_1_returned = a111_interpolated[1, :]

        for _returned, _expected in zip(a111_1_1_returned, a111_1_1_expected):
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_export(self):
        """assert export works"""
        input_file = self.input_filename
        o_handler = VDriveToMtex(filename=input_file)
        o_handler.load()
        o_handler.sort_raw_data()
        o_handler.interpolation()

        self.assertRaises(ValueError, o_handler.export)

        output_file_name = os.path.join(self.export_folder, self.export_filename)
        o_handler.export(filename=output_file_name)

        def _read_ascii(filename=''):
            f = open(filename, 'r')
            text = []
            for line in f:
                text.append(line)
            f.close()
            return text

        text_created = _read_ascii(output_file_name)
        text_expected = ["*Dump of file:XQG",
                         "*Sample: VULCAN",
                         "*Corrected, rescaled data * Phi range    0.00 -  360.00 Step    5.00",
                         "*Pole figure: 111",
                         "*Khi =   0.00",
                         "0.8126  0.8126  0.8126  0.8126  0.8126  0.8126  0.8126  0.8126",
                         "0.8126  0.8126  0.8126  0.8126  0.8126  0.8126  0.8126  0.8126"]

        for _returned, _expected in zip(text_created[0:7], text_expected):
            self.assertTrue(_returned.strip() == _expected)
