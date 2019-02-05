import unittest
import os
import numpy as np
import re
import shutil
import pandas as pd

from bem.texture.preparation.vdrive_handler import VDriveHandler


class TestVDriveHandler(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path,
                                                      '../../data/'))
        self.export_folder = self.data_path + '/temporary_folder/'
        self.filename = os.path.join(self.data_path, 'vdrive_filename.txt')
        os.mkdir(self.export_folder)

        # max diff allowed to compare two arrays
        self.maxDiff = 0.000001

    def tearDown(self):
        shutil.rmtree(self.export_folder)

    def test_vdrive_input_filename_should_not_be_empty(self):
        """assert VDrive filename should not be empty"""
        self.assertRaises(ValueError, VDriveHandler)

    def test_vdrive_input_filename_should_exists(self):
        """assert error is raised when VDrive filename does not exists"""
        vdrive_file = 'do_not_exist.txt'
        self.assertRaises(ValueError, VDriveHandler, vdrive_file)

    def test_vdrive_correctly_loaded(self):
        """assert raw VDrive file is correctly loaded"""
        filename = self.filename
        o_vdrive = VDriveHandler(filename=filename)
        filename_saved = o_vdrive.data.filename
        self.assertEqual(filename_saved, filename)

        _data = o_vdrive.data.raw
        first_runs = list(_data.index[0:9])
        first_runs_expected = list(np.arange(78901.0, 78910.0))
        self.assertEqual(first_runs_expected, first_runs)

    def test_keep_columns_of_interest(self):
        """assert vdrive data keeps only the columns of interest (I/V and eI/V)"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.keep_columns_of_interest()

        pd_vdrive_data_iv = o_vdrive.data.raw_iv
        pd_vdrive_data_eiv = o_vdrive.data.raw_eiv

        list_name_of_iv_columns = pd_vdrive_data_iv.columns.values
        list_name_of_eiv_columns = pd_vdrive_data_eiv.columns.values

        # make sure all the columns are iv or eiv
        number_of_iv_columns = 0
        number_of_eiv_columns = 0

        iv_re_string = r'^I/V_\w*$'
        for _index, _label in enumerate(list_name_of_iv_columns):
            m_iv = re.match(iv_re_string, _label)
            if m_iv:
                number_of_iv_columns += 1
        self.assertEqual(number_of_iv_columns, len(list_name_of_iv_columns))

        eiv_re_string = r'^eI/V_\w*$'
        for _index, _label in enumerate(list_name_of_eiv_columns):
            m_eiv = re.match(eiv_re_string, _label)
            if m_eiv:
                number_of_eiv_columns += 1
        self.assertEqual(number_of_eiv_columns, len(list_name_of_eiv_columns))

    def test_isolating_banks(self):
        """assert bank1 and bank2 data are correctly isolated"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()

        # bank1
        bank1_iv_columns_values = o_vdrive.bank1.iv.columns.values
        bank1_iv_columns_expected = ['I/V_Ni111_1',
                                     'I/V_Ni200_1',
                                     'I/V_Ni220_1',
                                     'I/V_Ni311_1',
                                     'I/V_Ni222_1',
                                     'I/V_Ni400_1']
        self.assertTrue((bank1_iv_columns_values[0:6] == bank1_iv_columns_expected).all())

        bank1_eiv_columns_values = o_vdrive.bank1.eiv.columns.values
        bank1_eiv_columns_expected = ['eI/V_Ni111_1',
                                      'eI/V_Ni200_1',
                                      'eI/V_Ni220_1',
                                      'eI/V_Ni311_1',
                                      'eI/V_Ni222_1',
                                      'eI/V_Ni400_1']
        self.assertTrue((bank1_eiv_columns_values[0:6] == bank1_eiv_columns_expected).all())

        # bank2
        bank2_iv_columns_values = o_vdrive.bank2.iv.columns.values
        bank2_iv_columns_expected = ['I/V_Ni111_2',
                                     'I/V_Ni200_2',
                                     'I/V_Ni220_2',
                                     'I/V_Ni311_2',
                                     'I/V_Ni222_2',
                                     'I/V_Ni400_2']
        self.assertTrue((bank2_iv_columns_values[0:6] == bank2_iv_columns_expected).all())

        bank2_eiv_columns_values = o_vdrive.bank2.eiv.columns.values
        bank2_eiv_columns_expected = ['eI/V_Ni111_2',
                                      'eI/V_Ni200_2',
                                      'eI/V_Ni220_2',
                                      'eI/V_Ni311_2',
                                      'eI/V_Ni222_2',
                                      'eI/V_Ni400_2']
        self.assertTrue((bank2_eiv_columns_values[0:6] == bank2_eiv_columns_expected).all())

    def test_bank1_axis_initialization(self):
        """assert bank1 hrot, omega, psi and phi are correctly created"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank1_xaxis()
        index_tested = [0, 5, 12, 19, 24, 36, 49, 67, 79, 89, 101, 111]

        omega_created = o_vdrive.bank1.omega
        omega_expected = [45, 45, 50, 50, 55, 60, 65, 70, 75, 80, 85, 90]
        omega_returned = [omega_created[_index] for _index in index_tested]
        self.assertEqual(omega_expected, omega_returned)

        hrot_created = o_vdrive.bank1.hrot
        hrot_expected = [0, 150, 330, 120, 0, 330, 30, 120, 210, 180, 150, 240]
        hrot_returned = [hrot_created[_index] for _index in index_tested]
        self.assertEqual(hrot_expected, hrot_returned)

        psi_created = o_vdrive.bank1.psi
        psi_expected = [0, 0, 5, 5, 10, 15, 20, 25, 30, 35, 40, 45]
        psi_returned = [psi_created[_index] for _index in index_tested]
        self.assertEqual(psi_expected, psi_returned)

        phi_created = o_vdrive.bank1.phi
        phi_expected = [0, 210, 30, 240, 0, 30, 330, 240, 150, 180, 210, 120]
        phi_returned = [phi_created[_index] for _index in index_tested]
        self.assertEqual(phi_expected, phi_returned)

    def test_bank2_axis_initialization(self):
        """assert bank2 omega, hrot, psi and phi are correctly created"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank2_xaxis()
        index_tested = [0, 5, 12, 19, 24, 36, 49, 67, 79, 89, 101, 111]

        omega_created = o_vdrive.bank2.omega
        omega_expected = [45, 45, 50, 50, 55, 60, 65, 70, 75, 80, 85, 90]
        omega_returned = [omega_created[_index] for _index in index_tested]
        self.assertEqual(omega_expected, omega_returned)

        hrot_created = o_vdrive.bank2.hrot
        hrot_expected = [0, 150, 330, 120, 0, 330, 30, 120, 210, 180, 150, 240]
        hrot_returned = [hrot_created[_index] for _index in index_tested]
        self.assertEqual(hrot_expected, hrot_returned)

        psi_created = o_vdrive.bank2.psi
        psi_expected = [90, 90, 85, 85, 80, 75, 70, 65, 60, 55, 50, 45]
        psi_returned = [psi_created[_index] for _index in index_tested]
        self.assertEqual(psi_expected, psi_returned)

        phi_created = o_vdrive.bank2.phi
        phi_expected = [180, 30, 210, 60, 180, 210, 150, 60, 330, 0, 30, 300]
        phi_returned = [phi_created[_index] for _index in index_tested]
        self.assertEqual(phi_expected, phi_returned)

    def test_bank_axis_initialization(self):
        """assert bank1 and bank2 axis are correctly created"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank_xaxis()

        # bank1
        index_tested = [0, 5, 12, 19, 24, 36, 49, 67, 79, 89, 101, 111]
        omega_created = o_vdrive.bank1.omega
        omega_expected = [45, 45, 50, 50, 55, 60, 65, 70, 75, 80, 85, 90]
        omega_returned = [omega_created[_index] for _index in index_tested]
        self.assertEqual(omega_expected, omega_returned)

        hrot_created = o_vdrive.bank1.hrot
        hrot_expected = [0, 150, 330, 120, 0, 330, 30, 120, 210, 180, 150, 240]
        hrot_returned = [hrot_created[_index] for _index in index_tested]
        self.assertEqual(hrot_expected, hrot_returned)

        psi_created = o_vdrive.bank1.psi
        psi_expected = [0, 0, 5, 5, 10, 15, 20, 25, 30, 35, 40, 45]
        psi_returned = [psi_created[_index] for _index in index_tested]
        self.assertEqual(psi_expected, psi_returned)

        phi_created = o_vdrive.bank1.phi
        phi_expected = [0, 210, 30, 240, 0, 30, 330, 240, 150, 180, 210, 120]
        phi_returned = [phi_created[_index] for _index in index_tested]
        self.assertEqual(phi_expected, phi_returned)

        # bank2
        omega_created = o_vdrive.bank2.omega
        omega_expected = [45, 45, 50, 50, 55, 60, 65, 70, 75, 80, 85, 90]
        omega_returned = [omega_created[_index] for _index in index_tested]
        self.assertEqual(omega_expected, omega_returned)

        hrot_created = o_vdrive.bank2.hrot
        hrot_expected = [0, 150, 330, 120, 0, 330, 30, 120, 210, 180, 150, 240]
        hrot_returned = [hrot_created[_index] for _index in index_tested]
        self.assertEqual(hrot_expected, hrot_returned)

        psi_created = o_vdrive.bank2.psi
        psi_expected = [90, 90, 85, 85, 80, 75, 70, 65, 60, 55, 50, 45]
        psi_returned = [psi_created[_index] for _index in index_tested]
        self.assertEqual(psi_expected, psi_returned)

        phi_created = o_vdrive.bank2.phi
        phi_expected = [180, 30, 210, 60, 180, 210, 150, 60, 330, 0, 30, 300]
        phi_returned = [phi_created[_index] for _index in index_tested]
        self.assertEqual(phi_expected, phi_returned)

    def test_sin_omega(self):
        """assert sin omega is working"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank_xaxis()
        o_vdrive.calculate_sin_omega()

        # bank1
        sin_omega_bank1_returned = o_vdrive.bank1.sin_omega
        omega_bank1 = o_vdrive.bank1.omega
        sin_omega_bank1_expected = [np.sin(np.pi*_omega/180.) for _omega in omega_bank1]
        self.assertTrue((sin_omega_bank1_expected == sin_omega_bank1_returned).all())

        # bank2
        sin_omega_bank2_returned = o_vdrive.bank2.sin_omega
        omega_bank2 = o_vdrive.bank2.omega
        sin_omega_bank2_expected = [np.sin(np.pi*_omega/180.) for _omega in omega_bank2]
        self.assertTrue((sin_omega_bank2_expected == sin_omega_bank2_returned).all())

    def test_mean_omega_45(self):
        """assert mean omega 45 works correctly for iv and eiv (bank1)"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.calculate_mean_omega_45()
        self.assertEqual(o_vdrive.bank1.iv_mean_omega_45, [])
        self.assertEqual(o_vdrive.bank1.eiv_mean_omega_45, [])

        vdrive_file = self.filename
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()
        o_vdrive.calculate_mean_omega_45()

        # iv
        mean_iv_omega_45_returned = o_vdrive.bank1.iv_mean_omega_45
        mean_iv_omega_45_expected = [2.451589167, 2.399450833,
                                     0.841268417, 1.271379167,
                                     0.320264833, 0.288333667]

        _returned_expected = zip(mean_iv_omega_45_expected[0:6], mean_iv_omega_45_returned)
        for _returned, _expected in _returned_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # eiv
        mean_eiv_omega_45_returned = o_vdrive.bank1.eiv_mean_omega_45
        mean_eiv_omega_45_expected = [0.054312417, 0.053232583,
                                      0.01754925, 0.01939325,
                                      0.007362275, 0.00547845]

        _returned_expected = zip(mean_eiv_omega_45_expected[0:6], mean_eiv_omega_45_returned)
        for _returned, _expected in _returned_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_stdev_omega_45(self):
        """assert std dev omega 45 works correctly"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.calculate_stdev_omega_45()
        self.assertEqual(o_vdrive.bank1.iv_stdev_omega_45, [])
        self.assertEqual(o_vdrive.bank1.eiv_stdev_omega_45, [])

        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()
        o_vdrive.calculate_stdev_omega_45()

        # iv
        std_iv_omega_45_returned = o_vdrive.bank1.iv_stdev_omega_45
        std_iv_omega_45_expected = [0.260401269, 0.332260911,
                                    0.057889314, 0.122683245,
                                    0.031568719, 0.040697648]

        _returned_expected = zip(std_iv_omega_45_returned[0:6], std_iv_omega_45_expected)
        for _returned, _expected in _returned_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_table2_bank1(self):
        """assert table2 works for banks 1"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank_xaxis()
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()
        o_vdrive.calculate_mean_omega_45()
        o_vdrive.calculate_sin_omega()
        o_vdrive.calculate_bank2_iv_ratio_omega_90()
        o_vdrive.calculate_table2()

        # bank1
        bank1_table2_calculated = o_vdrive.bank1.table2
        # col 0 - first 17 elements
        bank1_table2_expected_col_0 = [1.733535324, np.NaN, np.NaN, np.NaN, np.NaN,
                                       np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                       np.NaN, 1.497578584, 1.408625503, 1.563963996,
                                       1.669969226, 1.784584795]
        _returned_expected = zip(bank1_table2_calculated[:17, 0], bank1_table2_expected_col_0)
        for _returned, _expected in _returned_expected:
            if np.isnan(_returned) and np.isnan(_expected):
                self.assertTrue(True)
            else:
                self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # col 0 - last 17 elements
        bank1_table2_expected_col_0 = [2.430585, 2.776015, 2.66494, 2.263505, 2.796755,
                                       2.478, 2.0942, 2.009715, 2.978445, 2.883115,
                                       1.982715, 2.527035]
        _returned_expected = zip(bank1_table2_calculated[-12:, 0], bank1_table2_expected_col_0)
        for _returned, _expected in _returned_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # col 2
        bank1_table2_expected_col_2 = [0.594866602, np.NaN, np.NaN, np.NaN, np.NaN,
                                       np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                       np.NaN, 0.505373308, 0.538642618, 0.649678462,
                                       0.588877515, 0.568471623]
        _returned_expected = zip(bank1_table2_calculated[:17, 2], bank1_table2_expected_col_2)
        for _returned, _expected in _returned_expected:
            if np.isnan(_returned) and np.isnan(_expected):
                self.assertTrue(True)
            else:
                self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # col 3 - last 17 elements
        bank1_table2_expected_col_3 = [0.897326, 0.9429855, 0.8060015, 1.102025,
                                       0.802711, 0.9386, 0.8509655, 1.007736,
                                       0.853531, 0.8713325, 0.79393, 0.8506025]
        _returned_expected = zip(bank1_table2_calculated[-12:, 3], bank1_table2_expected_col_3)
        for _returned, _expected in _returned_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_bank2_iv_ratio_omega_90(self):
        """assert bank2 iv ratio omega 90"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank_xaxis()
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()
        o_vdrive.calculate_mean_omega_45()
        o_vdrive.calculate_sin_omega()
        o_vdrive.calculate_bank2_iv_ratio_omega_90()

        # col 0
        iv_ratio_omega_90_calculated = o_vdrive.bank2.iv_ratio_omega_90[:,0]
        iv_ratio_omega_90_expected = [1.033983906, 0.879617289, 0.892355783, 0.715981561,
                                      0.691115888, 0.652407466, 0.530479435, 0.749767571,
                                      0.700354435, 1.079204328, 1.05466988, 1.327044616]
        _returned_vs_expected = zip(iv_ratio_omega_90_calculated, iv_ratio_omega_90_expected)
        for _returned, _expected in _returned_vs_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # col 2
        iv_ratio_omega_90_calculated = o_vdrive.bank2.iv_ratio_omega_90[:,2]
        iv_ratio_omega_90_expected = [1.124049719, 0.994620789, 0.762225514, 0.963104237,
                                      0.555244755, 0.579175129, 0.742196268, 0.836293488,
                                      0.792550412, 1.015357199, 1.17216025, 1.084610855]
        _returned_vs_expected = zip(iv_ratio_omega_90_calculated, iv_ratio_omega_90_expected)
        for _returned, _expected in _returned_vs_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # mean values
        _mean_iv_ratio_omega_90_calculated = o_vdrive.bank2.mean_iv_ratio_omega_90[0:7]
        _mean_iv_ratio_omega_90_expected = [0.85891518, 0.857602759, 0.885132385, 0.891429027,
                                            0.928733701, 0.908020406, 0.919771881]
        _returned_vs_expected = zip(_mean_iv_ratio_omega_90_calculated, _mean_iv_ratio_omega_90_expected)
        for _returned, _expected in _returned_vs_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_table2_bank2(self):
        """assert sin(omega)*iv works for banks 2"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank_xaxis()
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()
        o_vdrive.calculate_mean_omega_45()
        o_vdrive.calculate_sin_omega()
        o_vdrive.calculate_bank2_iv_ratio_omega_90()
        o_vdrive.calculate_table2()

        bank2_table_calculated = o_vdrive.bank2.table2

        # top part of col 0
        top_part_col_0_calculated = bank2_table_calculated[0:10, 0]
        top_part_col_0_expected = [1.655954058, 1.589657279, 1.379463645, 1.03711278,
                                   1.64395099, 0.898081364, 1.146506992, 0.907738153,
                                   0.879945042, 0.885502018]
        _returned_vs_expected = zip(top_part_col_0_calculated, top_part_col_0_expected)
        for _returned, _expected in _returned_vs_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # top part of col 2
        top_part_col_2_calculated = bank2_table_calculated[0:10, 2]
        top_part_col_2_expected = [1.075608189, 0.810566687, 0.741113623, 0.652813589,
                                   0.553629733, 1.147922011, 0.766310021, 0.537520495,
                                   0.48164904, 0.627781758]
        _returned_vs_expected = zip(top_part_col_2_calculated, top_part_col_2_expected)
        for _returned, _expected in _returned_vs_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # bottom part of col 0
        bottom_part_col_0_calculated = bank2_table_calculated[-12:, 0]
        bottom_part_col_0_expected = [2.478929294, 2.189971774, 3.270427705, 2.801114774,
                                      1.88676372, 2.323232895, 1.96169545, 2.769796199,
                                      2.55591012, 2.735695043, 3.342786421, 3.290499535]
        _returned_vs_expected = zip(bottom_part_col_0_calculated, bottom_part_col_0_expected)
        for _returned, _expected in _returned_vs_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_mean_table(self):
        """assert mean table2 is correct"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank_xaxis()
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()
        o_vdrive.calculate_mean_omega_45()
        o_vdrive.calculate_sin_omega()
        o_vdrive.calculate_bank2_iv_ratio_omega_90()
        o_vdrive.calculate_table2()
        o_vdrive.calculate_mean_table2()

        mean_calculated = o_vdrive.mean_table
        mean_expected = [2.133214161, 1.168463923, 0.836050093, 0.969270446,
                         0.279793507, 0.143081008, 0.413152847, 0.370048531]
        _calculated_vs_expected = zip(mean_calculated, mean_expected)
        for _returned, _expected in _calculated_vs_expected:
            self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_output_table(self):
        """assert output table is correctly calculated"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)
        o_vdrive.initialize_bank_xaxis()
        o_vdrive.keep_columns_of_interest()
        o_vdrive.isolating_banks()
        o_vdrive.calculate_mean_omega_45()
        o_vdrive.calculate_sin_omega()
        o_vdrive.calculate_bank2_iv_ratio_omega_90()
        o_vdrive.calculate_table2()
        o_vdrive.calculate_mean_table2()
        o_vdrive.calculate_output_table()

        output_table_calculated = o_vdrive.output_table

        # col 0 top
        output_table_col0_top_expected = [0.812640079, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                      np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                      0.702029178, 0.660330092, 0.733149078, 0.782841806,
                                      0.836570855, 0.857984191, 1.03785908, 1.071183875,
                                      1.000483599]
        _returned_expected = zip(output_table_calculated[0:21, 0],
                                 output_table_col0_top_expected)
        for _returned, _expected in _returned_expected:
            if np.isnan(_returned) and np.isnan(_expected):
                self.assertTrue(True)
            else:
                self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

        # col 0 bottom
        output_table_col0_bottom_expected = [1.01526225, 2.307186346, 0.879244772,
                                             1.163050838, 0.779546467, 1.154482123,
                                             1.578486721, 1.142830628, 1.402556211,
                                             np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
                                            np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN]
        _returned_expected = zip(output_table_calculated[-21:, 0],
                                 output_table_col0_bottom_expected)
        for _returned, _expected in _returned_expected:
            if np.isnan(_returned) and np.isnan(_expected):
                self.assertTrue(True)
            else:
                self.assertAlmostEqual(_returned, _expected, delta=self.maxDiff)

    def test_export_table(self):
        """assert table correctly exported"""
        vdrive_file = self.filename
        o_vdrive = VDriveHandler(filename=vdrive_file)

        # raise error if one previous step is missing
        self.assertRaises(ValueError, o_vdrive.export, filename='test_me.txt')

        o_vdrive.run()

        # raise error if filename is missing
        self.assertRaises(ValueError, o_vdrive.export)

        # good to go now
        output_file = os.path.join(self.export_folder, 'test_output.txt')
        o_vdrive.export(filename=output_file)

        # test loading the file and checking content
        data_saved = pd.read_csv(output_file)
        row0_created = data_saved.iloc[1].values[:9]
        row0_expected = [5, 30, 0.702029178, 1.727360629, 0.604477306, 0.795381176,
                         0.681151972, 1.70530957, 0.636809108]
        _created_expected = zip(row0_created, row0_expected)
        for _created, _expected in _created_expected:
            self.assertAlmostEqual(_created, _expected, delta=self.maxDiff)
