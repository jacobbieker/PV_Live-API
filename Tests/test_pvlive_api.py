"""
Unit tests for the pvlive library.
Author: Ethan Jones
Written: 07/11/2020
"""

import unittest
from datetime import datetime, date
import pytz

import pandas.api.types as ptypes
from pvlive_api import PVLive

class PVLiveTestCase(unittest.TestCase):
    """Tests for `pvlive.py`."""

    def setUp(self):
        """
        Setup the instance of class.
        """
        self.api = PVLive()
        self.expected_dtypes = {
            'pes_id': ptypes.is_integer_dtype,
            'datetime_gmt': ptypes.is_datetime64_any_dtype,
            'generation_mw': ptypes.is_float_dtype,
            'bias_error': ptypes.is_float_dtype,
            'capacity_mwp': ptypes.is_float_dtype,
            'installedcapacity_mwp': ptypes.is_float_dtype,
            'lcl_mw': ptypes.is_float_dtype,
            'stats_error': ptypes.is_float_dtype,
            'ucl_mw': ptypes.is_float_dtype,
            'uncertainty_MW': ptypes.is_float_dtype,
            'site_count': ptypes.is_integer_dtype
        }

    def check_df_dtypes(self, api_df):
        """
        Check the dtypes of a Pandas DataFrame
        against the expected dtypes from the API.
        """
        for column in api_df.columns:
            with self.subTest(column=column):
                assert self.expected_dtypes[column](api_df[column])

    def check_tuple_dtypes(self, data):
        """
        Check the dtypes of a tuple
        against the expected dtypes from the API.
        """
        with self.subTest(column='pes_id'):
            assert isinstance(data[0], int)
        with self.subTest(column='datetime_gmt'):
            assert isinstance(data[1], str)
        with self.subTest(column='generation_mw'):
            assert isinstance(data[2], float)

    def check_tuple(self, data):
        """
        Check the length of the returned tuple
        against the expected length.
        """
        with self.subTest():
            assert isinstance(data, tuple) and len(data) == 3

    def check_df_columns(self, data):
        """
        Check the columns of the returned DataFrame
        against the expected columns.
        """
        with self.subTest():
            assert 'pes_id' in data and 'datetime_gmt' in data and 'generation_mw' in data

    def test_latest(self):
        """Tests the latest function."""
        data = self.api.latest()
        self.check_tuple(data)
        self.check_tuple_dtypes(data)
        data = self.api.latest(dataframe=True)
        self.check_df_columns(data)
        self.check_df_dtypes(data)
        data = self.api.latest(extra_fields="ucl_mw,lcl_mw,installedcapacity_mwp,stats_error",
                                dataframe=True)
        self.check_df_dtypes(data)

    def test_day_peak(self):
        """Tests the day_peak function."""
        data = self.api.day_peak(d=date(2018, 6, 3))
        self.check_tuple(data)
        self.check_tuple_dtypes(data)
        data = self.api.day_peak(d=date(2018, 6, 3), dataframe=True)
        self.check_df_columns(data)
        self.check_df_dtypes(data)
        data = self.api.day_peak(d=date(2018, 6, 3),
                                  extra_fields="ucl_mw,lcl_mw,installedcapacity_mwp,stats_error",
                                  dataframe=True)
        self.check_df_dtypes(data)

    def test_day_energy(self):
        """Tests the day_energy function."""
        data = self.api.day_energy(d=date(2018, 6, 3))
        assert isinstance(data, float)

    def test_between(self):
        """Test the between function."""
        data = self.api.between(start=datetime(2018, 7, 3, 12, 20, tzinfo=pytz.utc),
                         end=datetime(2018, 7, 3, 14, 00, tzinfo=pytz.utc))
        with self.subTest():
            assert isinstance(data, list)
        data = self.api.between(start=datetime(2018, 7, 4, 12, 20, tzinfo=pytz.utc),
                         end=datetime(2018, 7, 5, 14, 00, tzinfo=pytz.utc), dataframe=True)
        self.check_df_columns(data)
        self.check_df_dtypes(data)
        data = self.api.day_peak(d=date(2018, 6, 3),
                                  extra_fields="ucl_mw,lcl_mw,installedcapacity_mwp,stats_error",
                                  dataframe=True)
        self.check_df_dtypes(data)

    def test_at_time(self):
        """Test the at_time function."""
        data = self.api.at_time(datetime(2018, 6, 3, 12, 35, tzinfo=pytz.utc))
        self.check_tuple(data)
        self.check_tuple_dtypes(data)
        data = self.api.at_time(datetime(2018, 6, 3, 12, 35, tzinfo=pytz.utc), dataframe=True)
        self.check_df_columns(data)
        self.check_df_dtypes(data)
        data = self.api.at_time(datetime(2018, 6, 3, 12, 35, tzinfo=pytz.utc),
                                extra_fields="ucl_mw,lcl_mw,installedcapacity_mwp,stats_error",
                                dataframe=True)
        self.check_df_dtypes(data)

if __name__ == "__main__":
    unittest.main(verbosity=2)
