import shutil
import os
src_directory = './common_component'
dst_directory = './layers/common_component/python/common_component'
# Check if the destination directory already exists
if os.path.exists(dst_directory):
    # Remove the destination directory and its contents
    shutil.rmtree(dst_directory)

# Copy the source directory to the destination
shutil.copytree(src_directory, dst_directory)
