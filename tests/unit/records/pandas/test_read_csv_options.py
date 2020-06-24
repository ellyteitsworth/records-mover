from typing_inspect import get_args
import unittest
from records_mover.records.pandas.read_csv_options import pandas_read_csv_options
from records_mover.records.schema import RecordsSchema
from records_mover.records.delimited.types import HintDateFormat
from records_mover.records import DelimitedRecordsFormat, ProcessingInstructions


class TestReadCsvOptions(unittest.TestCase):
    def test_pandas_read_csv_options_bzip(self):
        records_format = DelimitedRecordsFormat(hints={
            'compression': 'BZIP'
        })
        records_schema = RecordsSchema.from_data({
            'schema': 'bltypes/v1'
        })
        unhandled_hints = set(records_format.hints)
        processing_instructions = ProcessingInstructions()
        expectations = {
            'compression': 'bz2'
        }
        out = pandas_read_csv_options(records_format,
                                      records_schema,
                                      unhandled_hints,
                                      processing_instructions)
        self.assertTrue(all(item in out.items() for item in expectations.items()))

    def test_pandas_read_csv_options_understands_all_dateformat_hints(self):
        all_dateformat_hints = list(get_args(HintDateFormat))  # type: ignore
        dateformat_expectation = {
            'YYYY-MM-DD': 123
        }
        for dateformat_hint in all_dateformat_hints:
            records_format = DelimitedRecordsFormat(hints={
                'dateformat': dateformat_hint
            })
            records_schema = RecordsSchema.from_data({
                'schema': 'bltypes/v1'
            })
            unhandled_hints = set(records_format.hints)
            processing_instructions = ProcessingInstructions()
            expectations = {
                # If this raises a KeyError, it's because we haven't
                # adjusted the test for a new dateformat hint value
                'compression': dateformat_expectation[dateformat_hint]
            }
            out = pandas_read_csv_options(records_format,
                                          records_schema,
                                          unhandled_hints,
                                          processing_instructions)
            self.assertTrue(all(item in out.items() for item in expectations.items()),
                            out)
