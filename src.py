import re
import os
import datetime
import glob
import os


ID_PAT = r'[_|\-|\#]?(\d{4,})[_|\-|\.|\s]'
TP_PAT = r'[T][|0-9]+'
STUDYS_DICT = {'8': 'CH', '6': 'CL', '4': 'FD', 
             '9' : 'FT', '3' :'NEXT', '3' :'PAC', '7' : 'RF'}
EXT_PAT = r'.\w+$'
TYPE_PAT = r'(raw|summary|[V|v]alidation|[P|p]ractice|gaze)'


def id_finder(file_name, id_pattern = ID_PAT):
    return re.findall(id_pattern, file_name)

def time_point_finder(file_name, tp_pattern = TP_PAT):
    time_point = re.findall(tp_pattern, file_name)
    
    # if there are more than 1 candidate marke as ''; else choose first
    if (len(time_point) != 1):#(time_point[0] != tp_check)
        time_point = ''
    else:
        time_point = time_point[0]
    
    return time_point
    
def ext_finder(file_name, ext_pattern = EXT_PAT):
    try:
        ext = re.findall(ext_pattern, file_name)[0]
    except:
        ext = ''
    return ext
    
def type_finder(file_name, type_pattern = TYPE_PAT):
    try:
        file_type = re.findall(type_pattern, file_name)[0].lower()
    except:
        file_type = ''
    
    return file_type

def study_finder(id_):
    try:
        study = STUDYS_DICT[id_[0][0]]
    except:
        study = 'not found'
    return study

def task_finder(study, file_name):
    try:
        belongings = extract_feature(study, file_name)[0]
    except:
        belongings = 'not assigned'
    
    return belongings
    
    
def clean_task_name_lst(file_name):
    
    task_lst = re.split(r'-|\s|_', file_name)
    file_name_vec = [i.lower().replace(' ', '').replace('_', '').replace('-', '')\
                     for i in task_lst if (not i.isnumeric()) \
                    and (i != '')][:-1] # -1 here is to drop the extension
#     print(file_name_vec)
    return file_name_vec

def extract_feature(study, file_name):
    vec = set()
    for i in clean_task_name_lst(file_name):
        i = i.lower()
        try:
            if (study == 'FT') and (i == ('gonogo')):
                vec.add('Emotional GoNoGo')
            elif (study == 'FT') and (i == ('stroop')):
                vec.add('Emotional Stroop ')
            elif 'AB Eyetracking' in vec:
                vec = set()
                vec.add('AB Eyetracking')
            else:
                vec.add(TASKS_DICT[i])
        except:
            continue
        
#     print(vec)
    return list(vec)

def initialize_log(columns, out_path, log_name):
    '''
    ex: initialize_log('log2.csv', ['col1', 'col2'], '.')
    '''
    assert os.path.exists(out_path), 'not valid output path'
    
    return_path = os.path.join(out_path, log_name)
    with open(return_path, 'w') as file:
        file.write(','.join(columns) + '\n')

def update_log(file_ext, target_dir, out_path, log_name):
    return_path = os.path.join(out_path, log_name)
    
    assert file_ext[0] == '.', 'the extension in not in valid format; use \'.csv\' like [.*]'
    assert os.path.exists(return_path), 'log path & name is not correct; please double check'
    assert os.path.exists(target_dir), 'target_dir is not correct; please double check'
    
    with open(return_path, 'a') as log:
        FID_DEFUALT_LEN = 4
        for name in glob.glob(target_dir  + '/*%s' % file_ext):
            
            mtime = os.stat(name).st_mtime#st_birthtime
            
            date = datetime.datetime.fromtimestamp(mtime).strftime('%m/%d/%Y %I:%M %p')
            
            size = str(os.path.getsize(name))
            
            file_name = name.split('/')[-1]
            
            id_candi = id_finder(file_name)
            
            # time point
            time_point = time_point_finder(file_name)
            
            # extension
            ext = ext_finder(file_name, ext_pattern = EXT_PAT)
            
#             id_set_finder
            dyad, fid = 'not found', 'not found'
            if len(id_candi) != 0:   
                id_ = id_candi[0]
                id_len = len(id_ )
                
                if id_len == 5:
                    dyad = id_[-1]
                    fid = id_[:FID_DEFUALT_LEN]
                    id_ = id_[:5]
                    
                elif id_len == 6:
                    dyad = id_[-2]
                    fid = id_[:FID_DEFUALT_LEN]
                    time_point = id_[-1]
                    
                    id_ = id_[:5]
                    
                elif id_len == 4:
                    dyad = 'not found'
                    id_ = id_[:FID_DEFUALT_LEN]
                    fid = 'not found'
                    
            else:
                id_ = 'not found'
                
            
            # study
            study = study_finder(id_)
            
            # task
            task = task_finder(study, file_name)
    
            # file type
            file_type = type_finder(file_name)
            
            to_write = ','.join([date, size, file_name, study, task,
                                 id_, fid, dyad, time_point, ext, file_type]) + '\n'
            
            log.write(to_write)