import os
import time
import csv
import json
from lettuce import step, world
from subprocess import check_call, CalledProcessError
from bigml.api import check_resource, HTTP_NOT_FOUND
from bigmler.checkpoint import file_number_of_lines
from common_steps import (check_debug, store_init_resources,
                          store_final_resources, check_init_equals_final)
from basic_test_prediction_steps import shell_execute


@step(r'I create a BigML source from file "(.*)" storing results in "(.*)"')
def i_create_source_from_file(step, data=None, output_dir=None):
    if data is None or output_dir is None:
        assert False
    command = ("bigmler --train " + data + " --store --output-dir " +
               output_dir +
               " --no-dataset --no-model --store")
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


def i_check_source_exists_by_id(step, source_id):
    source = check_resource(source_id,
                            world.api.get_source)
    if (source['code'] != HTTP_NOT_FOUND):
        assert True
        world.source = source
    else:
        assert False

@step(r'I check that the source exists$')
def i_check_source_exists(step):
    source_file = "%s%ssource" % (world.directory, os.sep)
    try:
        source_file = open(source_file, "r")
        source_id = source_file.readline().strip()
        i_check_source_exists_by_id(step, source_id)
        source_file.close()
        assert True
    except Exception, exc:
        assert False, str(exc)


@step(r'I check that the source doesn\'t exist$')
def i_check_source_does_not_exist(step, source_id=None):
    if source_id is None:
        source_id = world.source['resource']
    source = world.api.get_source(source_id)
    if (source['code'] == HTTP_NOT_FOUND):
        assert True
    else:
        assert False


@step(r'I delete the source by id using --ids storing results in "(.*)"$')
def i_delete_source_by_ids(step, output_dir=None):
    if output_dir is None:
        assert False
    command = ("bigmler delete --ids " + world.source['resource'] +
               " --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I delete the source by id using --ids and --dry-run storing results in "(.*)"$')
def i_delete_source_by_ids(step, output_dir=None):
    if output_dir is None:
        assert False
    command = ("bigmler delete --ids " + world.source['resource'] +
               " --dry-run --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I delete the source by id using --ids and --resource-types "(.*)" storing results in "(.*)"$')
def i_delete_source_by_ids_filtered(step, resource_types=None, output_dir=None):
    if output_dir is None or resource_types is None:
        assert False
    command = ("bigmler delete --ids " + world.source['resource'] +
               " --dry-run --output-dir " + output_dir +
               " --resource-types " + resource_types)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I delete the source by id using --from-file and the source file storing results in "(.*)"$')
def i_delete_source_by_file(step, output_dir=None):
    if output_dir is None:
        assert False
    command = ("bigmler delete --from-file %s%ssource " % (output_dir, os.sep) +
               " --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I delete the source by id using --from-file, the source file and --resource-types "(.*)" storing results in "(.*)"$')
def i_delete_source_by_file_filtered(step, resource_types=None, output_dir=None):
    if output_dir is None or resource_types is None:
        assert False
    command = ("bigmler delete --from-file %s%ssource " % (output_dir, os.sep) +
               " --output-dir " + output_dir +
               " --resource-types " + resource_types)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I store the source id as (lower|upper|reference)$')
def i_store_source_id_as_bound(step, which=None):
    if which == 'lower':
        world.source_lower = world.source['resource']
    elif which == 'upper':
        world.source_upper = world.source['resource']
    elif which == 'reference':
        world.source_reference = world.source['resource']


@step(r'I delete the source using --older-than and --newer-than storing results in "(.*)"$')
def i_delete_source_older_newer(step, output_dir=None):
    if output_dir is None:
        assert False
    command = ("bigmler delete --older-than " + world.source_upper +
               " --newer-than " + world.source_lower +
               " --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I check that the reference source doesn\'t exist$')
def i_check_reference_source_does_not_exist(step):
    i_check_source_does_not_exist(step, source_id=world.source_reference)


@step(r'I delete the source using --older-than and --newer-than with resource_types "(.*)" storing results in "(.*)"$')
def i_delete_source_older_newer_with_resource_types(step, resource_types=None, output_dir=None):
    if output_dir is None or resource_types is None:
        assert False
    command = ("bigmler delete --older-than " + world.source_upper +
               " --newer-than " + world.source_lower +
               " --resource-types " + resource_types +
               " --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I check that the reference source exists$')
def i_check_reference_source_exists(step):
    i_check_source_exists_by_id(step, source_id=world.source_reference)


@step(r'I create a BigML source from file "(.*)" with tag "(.*)" storing results in "(.*)"')
def i_create_source_from_file_with_tag(step, data=None, tag=None, output_dir=None):
    if data is None or output_dir is None or tag is None:
        assert False
    command = ("bigmler --train " + data + " --store --output-dir " +
               output_dir + " --tag " + tag +
               " --no-dataset --no-model --store")
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I delete the source using --newer-than and --source-tag "(.*)" storing results in "(.*)"$')
def i_delete_source_newer_and_tag(step, tag=None, output_dir=None):
    if output_dir is None or tag is None:
        assert False
    command = ("bigmler delete --newer-than " + world.source_lower +
               " --source-tag " + tag +
               " --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I check that the upper source exists$')
def i_check_upper_source_exists(step):
    i_check_source_exists_by_id(step, source_id=world.source_upper)


@step(r'I create a BigML dataset from the source with tag "(.*)" storing results in "(.*)"')
def i_create_dataset_from_source_with_tag(step, tag=None, output_dir=None):
    if tag is None or output_dir is None:
        assert False
    command = ("bigmler --source " + world.source['resource'] +
               " --tag " + tag +
               " --store --output-dir " + output_dir +
               " --no-model --store")
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


def i_check_dataset_exists_by_id(step, dataset_id):
    dataset = check_resource(dataset_id,
                             world.api.get_dataset)
    if (dataset['code'] != HTTP_NOT_FOUND):
        assert True
        world.dataset = dataset
    else:
        assert False


@step(r'I check that the dataset exists$')
def i_check_dataset_exists(step):
    dataset_file = "%s%sdataset" % (world.directory, os.sep)
    try:
        dataset_file = open(dataset_file, "r")
        dataset_id = dataset_file.readline().strip()
        i_check_dataset_exists_by_id(step, dataset_id)
        dataset_file.close()
        assert True
    except Exception, exc:
        assert False, str(exc)


@step(r'I check that the dataset doesn\'t exist$')
def i_check_dataset_does_not_exist(step, dataset_id=None):
    if dataset_id is None:
        dataset_id = world.dataset['resource']
    dataset = world.api.get_dataset(dataset_id)
    if (dataset['code'] == HTTP_NOT_FOUND):
        assert True
    else:
        assert False


@step(r'I delete the resources using --newer-than and --all-tag "(.*)" storing results in "(.*)"$')
def i_delete_resources_newer_and_tag(step, tag=None, output_dir=None):
    if output_dir is None or tag is None:
        assert False
    command = ("bigmler delete --newer-than " + world.source_lower +
               " --all-tag " + tag +
               " --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I create BigML resources uploading train "(.*)" storing results in "(.*)"$')
def i_create_all_resources_in_output_dir(step, data=None, output_dir=None):
    if output_dir is None or data is None:
        assert False
    command = ("bigmler --train " + data +
               " --output-dir " + output_dir)
    shell_execute(command, os.path.join(output_dir, "p.csv"), test=None)


@step(r'I check that the number of resources has changed$')
def i_check_changed_number_of_resources(step):
    store_final_resources()
    assert (world.final_sources_count != world.init_sources_count or
            world.final_dataset_count != world.init_dataset_count or
            world.final_model_count != world.init_model_count)


@step(r'I delete the resources from the output directory$')
def i_delete_resources_from_dir(step):
    command = ("bigmler delete --from-dir " + world.directory +
               " --output-dir " + world.directory)
    shell_execute(command, os.path.join(world.directory, "p.csv"), test=None)


@step(r'the number of resources has not changed$')
def i_check_equal_number_of_resources(step):
    store_final_resources()
    check_init_equals_final()
