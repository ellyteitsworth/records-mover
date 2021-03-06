from records_mover.db.vertica.unloader import VerticaUnloader
from records_mover.records.records_format import DelimitedRecordsFormat
import unittest
from mock import patch, Mock, ANY


class TestVerticaUnloader(unittest.TestCase):
    maxDiff = None

    @patch('records_mover.db.vertica.unloader.vertica_export_options')
    def test_can_unload_this_format_with_s3_true(self, mock_vertica_export_options):
        mock_db = Mock(name='db')
        mock_source_records_format = Mock(name='source_records_format', spec=DelimitedRecordsFormat)
        mock_s3_temp_base_loc = Mock(name='s3_temp_base_loc')
        vertica_unloader = VerticaUnloader(db=mock_db, s3_temp_base_loc=mock_s3_temp_base_loc)
        mock_resultset = Mock(name='resultset')
        mock_db.execute.return_value = mock_resultset
        mock_resultset.fetchall.return_value = ['awslib']
        mock_source_records_format.hints = {}
        out = vertica_unloader.can_unload_this_format(mock_source_records_format)
        mock_db.execute.\
            assert_called_with("SELECT lib_name from user_libraries where lib_name = 'awslib'")
        mock_vertica_export_options.assert_called_with(set(), ANY)
        self.assertEqual(True, out)

    @patch('records_mover.db.vertica.unloader.vertica_export_options')
    def test_can_unload_this_format_with_s3_false(self, mock_vertica_export_options):
        mock_db = Mock(name='db')
        mock_source_records_format = Mock(name='source_records_format', spec=DelimitedRecordsFormat)
        mock_s3_temp_base_loc = Mock(name='s3_temp_base_loc')
        vertica_unloader = VerticaUnloader(db=mock_db, s3_temp_base_loc=mock_s3_temp_base_loc)
        mock_resultset = Mock(name='resultset')
        mock_db.execute.return_value = mock_resultset
        mock_resultset.fetchall.return_value = ['awslib']
        mock_source_records_format.hints = {}
        mock_vertica_export_options.side_effect = NotImplementedError
        out = vertica_unloader.can_unload_this_format(mock_source_records_format)
        mock_db.execute.\
            assert_called_with("SELECT lib_name from user_libraries where lib_name = 'awslib'")
        mock_vertica_export_options.assert_called_with(set(), ANY)
        self.assertEqual(False, out)

    def test_known_supported_records_formats_for_unload(self):
        mock_db = Mock(name='db')
        mock_source_records_format = Mock(name='source_records_format', spec=DelimitedRecordsFormat)
        mock_s3_temp_base_loc = Mock(name='s3_temp_base_loc')
        vertica_unloader = VerticaUnloader(db=mock_db, s3_temp_base_loc=mock_s3_temp_base_loc)
        mock_resultset = Mock(name='resultset')
        mock_db.execute.return_value = mock_resultset
        mock_resultset.fetchall.return_value = ['awslib']
        mock_source_records_format.hints = {}
        out = vertica_unloader.known_supported_records_formats_for_unload()
        mock_db.execute.\
            assert_called_with("SELECT lib_name from user_libraries where lib_name = 'awslib'")
        self.assertEqual(out, [DelimitedRecordsFormat(variant='vertica')])
