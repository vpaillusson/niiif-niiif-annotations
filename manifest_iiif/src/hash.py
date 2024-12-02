# Importing the hashlib module.
import hashlib

#function to create pictures hash
def hash_pictures(filename_path):
    """
    Returns the hash of the file passed into the function
    :param filename_path: the path of the file to hash
    :return: the hash of the file
    """
    
    # The size of each read from the file
    BLOCK_SIZE = 65536 
    try:
        # Create the hash object
        file_hash = hashlib.sha1() 

        # Open the file to read it's bytes
        with open(filename_path, 'rb') as f:
            # Read from the file. Take in the amount declared above
            fb = f.read(BLOCK_SIZE) 
            # While there is still data being read from the file
            while len(fb) > 0: 
                # Update the hash
                file_hash.update(fb) 
                # Read the next block from the file
                fb = f.read(BLOCK_SIZE) 
            
        # Get the hexadecimal digest of the hash
        return file_hash.hexdigest()
    except Exception as err:
        print(err)