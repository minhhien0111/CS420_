from utils import create_input_files
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create input files for image captioning")
    parser.add_argument('--dataset', type=str, default='coco', help="Name of the dataset (e.g., coco, flickr8k)")
    parser.add_argument('--karpathy_json_path', type=str, required=True, help="Path to Karpathy JSON file")
    parser.add_argument('--image_folder', type=str, required=True, help="Folder with images")
    parser.add_argument('--captions_per_image', type=int, default=5, help="Number of captions per image")
    parser.add_argument('--min_word_freq', type=int, default=5, help="Minimum word frequency")
    parser.add_argument('--output_folder', type=str, required=True, help="Folder to save output files")
    parser.add_argument('--max_len', type=int, default=50, help="Maximum caption length")
    
    args = parser.parse_args()

    # Call the function with parsed arguments
    create_input_files(dataset=args.dataset,
                       karpathy_json_path=args.karpathy_json_path,
                       image_folder=args.image_folder,
                       captions_per_image=args.captions_per_image,
                       min_word_freq=args.min_word_freq,
                       output_folder=args.output_folder,
                       max_len=args.max_len)
