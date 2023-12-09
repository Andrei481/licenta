def concatenate_files(file1_path, file2_path, output_file_path, chunk_size=8192):
    try:
        with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
            with open(output_file_path, 'wb') as output_file:
                # Copy content from file1 to output_file in chunks
                while chunk := file1.read(chunk_size):
                    output_file.write(chunk)

                # Copy content from file2 to output_file in chunks
                while chunk := file2.read(chunk_size):
                    output_file.write(chunk)

        print(f"Files '{file1_path}' and '{file2_path}' have been successfully concatenated to '{output_file_path}'.")
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file1_path = 'dataset.txt'
file2_path = 'ro.txt'
output_file_path = 'dataset_ro_full.txt'

concatenate_files(file1_path, file2_path, output_file_path)

