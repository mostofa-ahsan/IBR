import pandas as pd
import os
from datetime import datetime as dt
import numpy as np

#### variables
base_dir = '/n01/data/nlp_aeac/itemized_bill_review/charts'
output_name = 'ibr_'
curr_date = dt.now()
manifest_name = 'ibr_'+curr_date.strftime("%m%d%Y%I%M%S")+'.txt'
manifest_path = os.path.join(base_dir, manifest_name)
manifest_run_mode = '1' # meta files separated out by document
manifest_read_type = '0' # read directly from NAS
manifest_priority = '1'

#### functions
def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))  

#### main
all_files = list(absoluteFilePaths(base_dir))
final_files = [i for i in all_files if '.pdf' in i]
final_files = [i for i in final_files if '.png' not in i]
final_files = [i for i in final_files if 'xml' not in i]
df = pd.DataFrame(final_files, columns = ['file_path'])
df['tracking_number'] = np.arange(len(df))
num_records = df.shape[0]

##### structure
hdr_rec = 'HDR'+'|'+manifest_name+'|'+manifest_run_mode+'|'+manifest_read_type+'|'+manifest_priority
section_header = 'tracking_no|priority|file_path_url|file_path'
trl_rec = 'TRL|'+curr_date.strftime("%m%d%Y")+'|'+curr_date.strftime("%I%M%S")+'|'+str(num_records)

# write records to file
with open(manifest_path, 'w') as final_file:
    final_file.write(hdr_rec+'\n') # header
    final_file.write(section_header+'\n') # section header

    for ix,row in df.iterrows():
        tracking_number = row['tracking_number']
        file_path_url = ''
        file_path = row['file_path']

        final_file.write(str(tracking_number)+'|'+manifest_priority+'|'+file_path_url+'|'+file_path+'\n')

    final_file.write(trl_rec+'\n')
