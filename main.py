import basis
import os
import utils
from Preprocess import read_data
from Preprocess import fill_blank
from Preprocess import velocity_unfold
from Preprocess import cover_boundary

if __name__ == '__main__':
    # Set radar images folder
    img_folder = "C:/Users/12103/Desktop/examples/Z9755/"
    station_num = "Z9755"
    results_folder = 'analysis_result/Z9755/'

    # Generate image config
    basis.check_input_folder(img_folder)
    # Check config file
    basis.validate_config()

    # Get image names from input folder
    all_files = os.listdir(img_folder)
    image_files = [file for file in all_files if os.path.splitext(file)[1].lower() in utils.valid_image_extensions]

    # Check station
    if station_num in utils.need_cover_station:
        need_cover = True
        print("[Info] This radar images need to cover boundaries.")
    else:
        need_cover = False

    # Analise each radar image
    for image_name in image_files:
        # Generate image entire path and result folder path
        image_path = img_folder + image_name
        result_folder_path = results_folder + image_name.split(".")[0] + '/'
        print("----------------------------------")
        print(f"image_path = {image_path}")
        print(f"result_folder_path = {result_folder_path}")

        # Check whether to cover the boundary or not
        if need_cover:
            image_path = cover_boundary.cover_white_boundary(image_path, station_num, result_folder_path)

        gray_img_path = read_data.read_radar_image(result_folder_path, image_path)

        filled_img_path = fill_blank.fill_radar_image(result_folder_path, gray_img_path)

        first_unfold_path = velocity_unfold.unfold_doppler_velocity(result_folder_path, filled_img_path, 1)

        second_unfold_path = velocity_unfold.unfold_doppler_velocity(result_folder_path, first_unfold_path, 2)
