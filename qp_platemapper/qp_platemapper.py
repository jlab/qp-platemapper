from os.path import join, dirname
from os import makedirs
import shutil
from functools import partial

import pandas as pd

from qiita_client import ArtifactInfo
from qiita_client.util import system_call
import qp_platemapper

def platemapper(qclient, job_id, parameters, out_dir):
    out_dir = join(out_dir, 'platemapper_out')
    qclient.update_job_step(job_id, "Step 1 of 3: Platemapper started!")

    artifact_id = parameters['Sequencing library']
    artifact_info = qclient.get("/qiita_db/artifacts/%s/" % artifact_id)

    prep_info = qclient.get(
        '/qiita_db/prep_template/%s/' % artifact_info['prep_information'][0])
    df = pd.read_csv(prep_info['prep-file'], sep='\t')

    qclient.update_job_step(job_id, "Step 2 of 3: Validating prep information.")

    # Generating artifact
    pb = partial(join, out_dir)
    final_visualization = pb('platemapping.qzv')
    makedirs(dirname(final_visualization), exist_ok=True)

    # TODO: this must be replaced with platemapper file generation!
    qclient.update_job_step(job_id, "Step 3 of 3: Generating Emperor visualization")
    shutil.copyfile(
        "/qp-platemapper/qp_platemapper/tests/pax5_emperor.qzv",
        final_visualization)

    # with open(final_visualization, 'w') as f:
    #     f.write("Hallo Welt")

    ainfo = [ArtifactInfo('interactive plate layout(s)', 'q2_visualization',
                          [(final_visualization, 'qzv')])]
    return True, ainfo, ""
