# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cirq_google/api/v1/program.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import operations_pb2 as cirq__google_dot_api_dot_v1_dot_operations__pb2
from . import params_pb2 as cirq__google_dot_api_dot_v1_dot_params__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n cirq_google/api/v1/program.proto\x12\x12\x63irq.google.api.v1\x1a#cirq_google/api/v1/operations.proto\x1a\x1f\x63irq_google/api/v1/params.proto\"~\n\x07Program\x12\x31\n\noperations\x18\x01 \x03(\x0b\x32\x1d.cirq.google.api.v1.Operation\x12@\n\x10parameter_sweeps\x18\x02 \x03(\x0b\x32\".cirq.google.api.v1.ParameterSweepB\x02\x18\x01\"J\n\nRunContext\x12<\n\x10parameter_sweeps\x18\x01 \x03(\x0b\x32\".cirq.google.api.v1.ParameterSweep\"e\n\x13ParameterizedResult\x12\x31\n\x06params\x18\x01 \x01(\x0b\x32!.cirq.google.api.v1.ParameterDict\x12\x1b\n\x13measurement_results\x18\x02 \x01(\x0c\"H\n\x0eMeasurementKey\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x06qubits\x18\x02 \x03(\x0b\x32\x19.cirq.google.api.v1.Qubit\"\xa8\x01\n\x0bSweepResult\x12\x13\n\x0brepetitions\x18\x01 \x01(\x05\x12<\n\x10measurement_keys\x18\x02 \x03(\x0b\x32\".cirq.google.api.v1.MeasurementKey\x12\x46\n\x15parameterized_results\x18\x03 \x03(\x0b\x32\'.cirq.google.api.v1.ParameterizedResult\"@\n\x06Result\x12\x36\n\rsweep_results\x18\x01 \x03(\x0b\x32\x1f.cirq.google.api.v1.SweepResultB/\n\x1d\x63om.google.cirq.google.api.v1B\x0cProgramProtoP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cirq_google.api.v1.program_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\035com.google.cirq.google.api.v1B\014ProgramProtoP\001'
  _globals['_PROGRAM'].fields_by_name['parameter_sweeps']._options = None
  _globals['_PROGRAM'].fields_by_name['parameter_sweeps']._serialized_options = b'\030\001'
  _globals['_PROGRAM']._serialized_start=126
  _globals['_PROGRAM']._serialized_end=252
  _globals['_RUNCONTEXT']._serialized_start=254
  _globals['_RUNCONTEXT']._serialized_end=328
  _globals['_PARAMETERIZEDRESULT']._serialized_start=330
  _globals['_PARAMETERIZEDRESULT']._serialized_end=431
  _globals['_MEASUREMENTKEY']._serialized_start=433
  _globals['_MEASUREMENTKEY']._serialized_end=505
  _globals['_SWEEPRESULT']._serialized_start=508
  _globals['_SWEEPRESULT']._serialized_end=676
  _globals['_RESULT']._serialized_start=678
  _globals['_RESULT']._serialized_end=742
# @@protoc_insertion_point(module_scope)
