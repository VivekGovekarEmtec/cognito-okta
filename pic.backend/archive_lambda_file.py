import shutil
import os

# Define the names of the files
# files_to_zip = [
#     "requirements.txt",
#     "requirements-local.txt",
#     "runtime.txt",
#     ".gitignore",
# ]
# Use below names for lambda folder zip
##########REFERENCE#########################
# reference

##########STATION MASTER#########################
# station_master
# station_master_command

##########COMPETITOR#############################
# competitor
# competitor_command

##########SURVEY#############################
# survey
# survey_command

##########SURVEY MANAGEMENT#############################
# survey_management
# survey_management_command

##########UNREVIEWED SURVEY#############################
# unreviewed_survey

##########UNREVIEWED SURVEY BANNER#############################
# unreviewed_survey_banner

##########OUTLET PRICE#############################
# outlet_price

##########PRICING#############################
# pricing
# pricing_command

##########TACTICAL#############################
# tactical
# tactical_command

##########TACTICAL#############################
# email_lambda
# regulated_pricing

# -----------------------------------------------------------------------------------------------------------

##########pricing#############################
# get_cancel_price
# get_price_change_auth_data
# get_station_information
# get_station_info
# get_regulated_price_details
# get_header

##########pricing_command#################################33
# create_pricing_note
# update_price_on_hold
# delete_price_on_hold
# insert_price_on_hold_json
# save_reset_price
# delete_price_change
# save_price_change_auth  -> save
# is_regulated_price_file_exists
# upload_file
# create_regulated_price_header
# update_regulated_price_ns
# nb_apply_pricing
# update_regulated_price_nb
# update_mark_survey_as_pending_review
# create_price_hold
# update_survey_as_review
# create_price_change

################# tactical #####################################
# get_all_tactical_competitors
# get_reset_time_by_site_id
# get_tactic_competitor_observe
# get_tactical_movement_behaviours
# is_site_tactic_time_overlap
# is_tactic_competitor_association
# is_tactic_competitor_observe_associated


################# tactical_command #####################################
# add_tactical_competitors_to_outlets
# create_site_tactic
# delete_site_tactics
# update_site_tactic
# update_tactic_competitors
# update_tactic_follow_action_status


########## reference #################################
# brands
# cities
# facility_types
# get_base_products
# get_contact_types
# get_notification_types
# get_outlet_selector
# get_outlet_time_zones
# get_product_types
# get_tactic_follow_action_status_list
# get_tactic_follow_movement_list
# languages
# marketers
# outlet_status
# provinces
# tactic_pricing_zone
# site_ratings
# is_available_kent_id
# competitor_device_types


########## outlet_price #################################
# get_outlet_price
# get_outlet_price_bulloch
# get_price_change_validation
# get_scheduled_price_changes


root_folder = input("Enter root folder :- ")
folder = input("Enter sub folder name :- ")


def copy_files_to_temp(source_folder, temp_folder):
    # Ensure the temporary folder exists
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Iterate over files in the source folder and copy them to the temporary folder
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(temp_folder, file)
            shutil.copy2(source_path, destination_path)


def create_zip_archive(source_folder, zip_filename):
    # Create a temporary folder
    temp_directory = 'temp_folder'

    # Copy files to the temporary folder
    copy_files_to_temp(source_folder, temp_directory)

    # Create the zip archive from the temporary folder
    shutil.make_archive('./zip_files/' + root_folder + "/" + zip_filename, 'zip', temp_directory)

    # Remove the temporary folder and its contents
    shutil.rmtree(temp_directory)


# Example usage:
folder_to_zip = root_folder+"/"+folder
zip_filename = folder + '_lambda_zip_file'

create_zip_archive(folder_to_zip, zip_filename)
