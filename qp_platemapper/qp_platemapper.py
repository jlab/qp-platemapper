from qiita_client import ArtifactInfo
from qiita_client.util import system_call
import qp_platemapper

def platemapper(qclient, job_id, parameters, out_dir):
    out_dir = join(out_dir, 'platemapper_out')
    qclient.update_job_step(job_id, "Step 1 of X: Platemapper started!")

    artifact_id = parameters['Sequencing library']
    artifact_info = qclient.get("/qiita_db/artifacts/%s/" % artifact_id)

    prep_info = qclient.get(
        '/qiita_db/prep_template/%s/' % artifact_info['prep_information'][0])
    df = pd.read_csv(prep_info['prep-file'], sep='\t')

    # Generating artifact
    pb = partial(join, out_dir)
    final_visualization = pb('platemapping.qzv')
    with open(final_visualization, 'w') as f:
        f.write("Hallo Welt")

    ainfo = [ArtifactInfo('interactive plate layout(s)', 'q2_visualization',
                          [(final_visualization, 'qzv')])]
    return True, ainfo, ""
