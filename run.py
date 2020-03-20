import os

import glob
import os
import sys

# import re
import json
# import datetime

from ast import literal_eval

from src import initialize_log, update_log

LOG_CONFIG = 'config.json'
TASK_DICT_CONFIG = 'task_dict.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)

    return param

def logging(**cfg):

	### loading needed params
	out_path = cfg['out_path']
	ext = cfg['ext']
	parent_dir = cfg['parent_dir']
	STUDY_FOLDERS = literal_eval(cfg['STUDY_FOLDERS'])
	LOG_COLUMNS = literal_eval(cfg['LOG_COLUMNS'])
	TASKS_DICT = cfg['TASKS_DICT']

	ALL = '*'

	for study in glob.glob(os.path.join(parent_dir, ALL)):
	    if study.split('/')[-1] in STUDY_FOLDERS:
	        for task in glob.glob(os.path.join(study, ALL)):
	            file_name = task.split('/')[-1]
	            log_name = file_name + '_log.csv'
	            target_dir = task
	            
	            initialize_log(LOG_COLUMNS,
	                           out_path, log_name)
	            update_log(ext, target_dir, out_path, log_name, TASKS_DICT)

def main(targets):
	if 'logging' in targets:
		cfg = load_params(LOG_CONFIG)
		logging(**cfg)


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)