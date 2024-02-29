import shutil
import os
dst_directory = 'common_component_layer_zip'
# Check if the destination directory already exists
if os.path.exists(dst_directory):
    # Remove the destination directory and its contents
    shutil.rmtree(dst_directory)

shutil.make_archive('./zip_files/common_component_zip_layer', 'zip', './layers/common_component')
 