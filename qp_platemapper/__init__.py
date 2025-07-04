# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from qiita_client import QiitaPlugin, QiitaCommand
from .qp_platemapper import platemapper

# Initialize the plugin
plugin = QiitaPlugin(
    'Platemapper', '0.2.0',
    'Visualize plate layout for sequencing library construction')


req_params = {'Sequencing library': ('artifact', ['FASTA', 'FASTA_Sanger', 'SFF', 'FASTQ', 'per_sample_FASTQ', 'Demultiplexed'])}
opt_params = {
    'Column name for well positions': ['choice:["well_id"]', 'well_id'],
    'Column name for plate ID': ['choice:["plate_id"]', 'plate_id'],
    'plate layout': ['choice:["96-well plate(s)"]', '96-well plate(s)']}
outputs = {'interactive plate layout(s)': 'q2_visualization'}
dflt_param_set = {
    'Defaults': {
        'Column name for well positions': 'well_id',
        'Column name for plate ID': 'plate_id',
        'plate layout': '96-well plate(s)'}}
command = QiitaCommand(
    "generate plate mapping",
    "Takes well position information (if given) of the prep data to create an interactive visualization",
    platemapper,
    req_params, opt_params,
    outputs,
    dflt_param_set)

plugin.register_command(command)
