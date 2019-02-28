import time

from django_rq.decorators import job
from sklearn.externals import joblib

from src.encoding.models import Encoding
from src.labelling.models import Labelling
from pred_models.models import ModelSplit, PredModels
from src.split.models import Split
from src.predictive_model.models import PredictiveModel
from src.clustering.clustering import Clustering
from src.core.constants import CLASSIFICATION, UPDATE
from src.core.core import calculate
from src.core.hyperopt_wrapper import calculate_hyperopt
from src.jobs.models import Job, CREATED, RUNNING, COMPLETED, ERROR
from src.jobs.ws_publisher import publish


@job("default", timeout='1h')
def prediction_task(job_id):
    print("Start prediction task ID {}".format(job_id))
    job = Job.objects.get(id=job_id)
    try:
        if job.status == CREATED:
            job.status = RUNNING
            job.save()
            start_time = time.time()
            if job.config.get('hyperopt', {}).get('use_hyperopt', False):
                result, model_split = hyperopt_task(job)
            else:
                result, model_split = calculate(job.to_dict())
            elapsed_time = time.time() - start_time
            print('\tJob took: {} in HH:MM:ss'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
            if job.config.get('create_models', False):
                save_models(model_split, job)
            job.result = result
            job.status = COMPLETED
    except Exception as e:
        print("error " + str(e.__repr__()))
        job.status = ERROR
        job.error = str(e.__repr__())
        raise e
    finally:
        job.save()
        publish(job)


def save_models(to_model_split, job):
    print("Start saving models of JOB {}".format(job.id))
    job_split = job.split
    if job_split.type == 'single':
        log = job_split.original_log
    else:
        log = job_split.training_log
    if job.type == UPDATE or job.config['incremental_train']['base_model'] is not None:
        job.type = CLASSIFICATION
        filename_model = 'cache/model_cache/job_{}-split_{}-predictive_model-{}-v{}.sav'.format(job.id, job.split.id,
                                                                                          job.type,
                                                                                          str(time.time()))
    else:
        filename_model = 'cache/model_cache/job_{}-split_{}-predictive_model-{}-v0.sav'.format(job.id, job.split.id, job.type)
    joblib.dump(to_model_split['classifier'], filename_model)
    model_split, created = ModelSplit.objects.get_or_create(type=to_model_split['type'], model_path=filename_model,
                                                            predtype=job.type)
    if to_model_split['type'] == Clustering.KMEANS:  # TODO this will change when using more than one type of cluster
        filename_clusterer = 'cache/model_cache/job_{}-split_{}-clusterer-{}-v0.sav'.format(job.id, job.split.id, job.type)
        joblib.dump(to_model_split['clusterer'], filename_clusterer)
        model_split.clusterer_path = filename_clusterer
        model_split.save()
    PredModels.objects.create(pk=job.id, split=model_split, type=job.type, log=log, config=job.config)
    #TODO this will become a Predictive_model object DB
    # PredictiveModel.objects.create(
    #     split= Split.objects.filter(id=job['split'])[0],
    #     encoding= Encoding.objects.filter()[0],
    #     labelling=Labelling.objects.filter()[0],
    #     model_type=
    # )


def hyperopt_task(job):
    job_dict = job.to_dict()
    results, config, model_split = calculate_hyperopt(job_dict)
    method_conf_name = "{}.{}".format(job_dict['type'], job_dict['method'])
    job.config[method_conf_name] = config
    return results, model_split
