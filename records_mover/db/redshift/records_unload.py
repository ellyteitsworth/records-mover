from ...utils import quiet_remove
from ...records.hints import cant_handle_hint
from typing import Dict, Any, Set
from sqlalchemy_redshift.commands import Format
from ...records.records_format import (
    DelimitedRecordsFormat, ParquetRecordsFormat, BaseRecordsFormat
)

RedshiftUnloadOptions = Dict[str, Any]


# https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html
#
def redshift_unload_options(unhandled_hints: Set[str],
                            records_format: BaseRecordsFormat,
                            fail_if_cant_handle_hint: bool) -> RedshiftUnloadOptions:
    redshift_options: RedshiftUnloadOptions = {}
    if isinstance(records_format, ParquetRecordsFormat):
        redshift_options['format'] = Format.parquet
        return redshift_options

    if not isinstance(records_format, DelimitedRecordsFormat):
        raise NotImplementedError("Redshift export only supported via Parquet and "
                                  "delimited currently")
    hints = records_format.hints
    if hints['escape'] == '\\':
        redshift_options['escape'] = True
    elif hints['escape'] is not None:
        cant_handle_hint(fail_if_cant_handle_hint, 'escape', hints)

    quiet_remove(unhandled_hints, 'escape')

    if hints['record-terminator'] == "\n":
        # This is Redshift's one and only export format
        pass
    else:
        cant_handle_hint(fail_if_cant_handle_hint, 'record-terminator', hints)
    quiet_remove(unhandled_hints, 'record-terminator')

    # https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html
    #
    # When CSV, unloads to a text file in CSV format using a comma ( ,
    # ) character as the delimiter. If a field contains commas, double
    # quotation marks, newline characters, or carriage returns, then
    # the field in the unloaded file is enclosed in double quotation
    # marks. A double quotation mark within a data field is escaped by
    # an additional double quotation mark.
    #
    # The FORMAT and AS keywords are optional. You can't use CSV with
    # DELIMITER or FIXEDWIDTH.
    if (hints['field-delimiter'] == ',' and
       hints['doublequote'] and
       hints['quotechar'] == '"' and
       hints['quoting'] == 'minimal'):
        redshift_options['format'] = Format.csv
        quiet_remove(unhandled_hints, 'quoting')
        quiet_remove(unhandled_hints, 'doublequote')
        quiet_remove(unhandled_hints, 'quotechar')
    else:
        redshift_options['delimiter'] = hints['field-delimiter']
        quiet_remove(unhandled_hints, 'field-delimiter')
        if hints['quoting'] == 'all':
            if hints['doublequote'] is not False:
                cant_handle_hint(fail_if_cant_handle_hint, 'doublequote', hints)
            if hints['quotechar'] != '"':
                cant_handle_hint(fail_if_cant_handle_hint, 'quotechar', hints)
            redshift_options['add_quotes'] = True
        elif hints['quoting'] is None:
            redshift_options['add_quotes'] = False
        else:
            cant_handle_hint(fail_if_cant_handle_hint, 'quoting', hints)
        quiet_remove(unhandled_hints, 'quoting')
        quiet_remove(unhandled_hints, 'doublequote')
        quiet_remove(unhandled_hints, 'quotechar')
    if hints['compression'] == 'GZIP':
        redshift_options['gzip'] = True
    elif hints['compression'] is None:
        # good to go
        pass
    else:
        cant_handle_hint(fail_if_cant_handle_hint, 'compression', hints)
    quiet_remove(unhandled_hints, 'compression')
    if hints['encoding'] != 'UTF8':
        cant_handle_hint(fail_if_cant_handle_hint, 'encoding', hints)
    quiet_remove(unhandled_hints, 'encoding')
    if hints['datetimeformattz'] != 'YYYY-MM-DD HH:MI:SSOF':
        cant_handle_hint(fail_if_cant_handle_hint, 'datetimeformattz', hints)
    quiet_remove(unhandled_hints, 'datetimeformattz')
    if hints['datetimeformat'] != 'YYYY-MM-DD HH24:MI:SS':
        cant_handle_hint(fail_if_cant_handle_hint, 'datetimeformat', hints)
    quiet_remove(unhandled_hints, 'datetimeformat')
    if hints['dateformat'] != 'YYYY-MM-DD':
        cant_handle_hint(fail_if_cant_handle_hint, 'dateformat', hints)
    quiet_remove(unhandled_hints, 'dateformat')
    # Redshift doesn't have a time without date type, so there's
    # nothing that could be exported there.
    quiet_remove(unhandled_hints, 'timeonlyformat')

    if hints['header-row']:
        # Redshift unload doesn't know how to add headers on an
        # unload.  Bleh.
        # https://stackoverflow.com/questions/24681214/unloading-from-redshift-to-s3-ith-headers
        cant_handle_hint(fail_if_cant_handle_hint, 'header-row', hints)
    else:
        quiet_remove(unhandled_hints, 'header-row')

    return redshift_options
