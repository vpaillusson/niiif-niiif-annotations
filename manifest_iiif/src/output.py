import csv

# Create a csv outputfile with manifest data and Nakala data identifier
class Output:
    @staticmethod
    def output_csv(manifest_data, dataIdentifier, csv_output):
        """
        Write the manifest data and the Nakala data identifier in a csv file
        :param manifest_data: the manifest data
        :param dataIdentifier: the Nakala data identifier
        :param csv_output: the csv output file
        :return: None
        """

        # Open the csv output file with append mode
        with open(csv_output, 'a', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['dataIdentifier', 'manifest_data']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header if the file is empty
            if csv_file.tell() == 0:
                writer.writeheader()

            # Write the manifest data and the Nakala data identifier
            writer.writerow({'dataIdentifier': dataIdentifier,
                             'manifest_data': manifest_data})