import argparse
import ast
import os
import glob

def txt_to_dict(filename):
    '''
    Read txt file and try to evaluate it as a dict.

    Parameters
    ----------
    filename : str
        Path to input file.
    '''

    with open(filename, 'r') as f:
        s = f.read()
        d = ast.literal_eval(s)
    return d

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Create todinfo.txt for given cuts release.')
    parser.add_argument("release_file", help='Path to release file')
    parser.add_argument("ofile", help='Path to output file')
    args = parser.parse_args()

    rls_dict = txt_to_dict(args.release_file)
    odir, ofilename = os.path.split(args.ofile)
    if not os.path.exists(odir):
        os.mkdirs(odir)
    
    depot = rls_dict['depot']
    stods_basedir = os.path.join(depot, 'SelectedTODs')

    with open(args.ofile, 'a') as text_file:                
        for tag in rls_dict['tags']:
            
            # Assume tag is "paX_fXXX_sXX_.."
            pa, freq, season = tag.split('_')[:3]            
            print("# {} {} {}".format(pa, freq, season), file=text_file)

            stods_dir = os.path.join(stods_basedir, rls_dict['tags'][tag]['tag_out'])
            print('p = {}'.format(stods_dir), file=text_file)

            tod_files = glob.glob(os.path.join(stods_dir, '*.txt'))            
            for tod_file in tod_files:
                
                _, tod_filename = os.path.split(tod_file)
                # Assume tod_file = selectedTODs_<obs>.txt 
                obs = tod_filename[tod_filename.index('_')+1:-4]
            
                print("{{p}}/{:<50s} {} {} :{} {}".format(tod_filename, season, pa, freq, obs),
                      file=text_file)

            print('', file=text_file)
            
