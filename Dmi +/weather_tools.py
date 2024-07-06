
import csv
from FileManager import *

def format_parameters(parameters):
        formatted_parameters = []
        # Reading the CSV file
        with open('Dmi +\Dmi_api_parameterindex.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                formatted_parameters.append(row)
        
        #Create a dictionary with the parameter names as keys and the technical parameter names as values (mapping)
        param_to_tech = {row['parameter-name']: row['Technical parameter-name'] for row in formatted_parameters}
        #param_to_unit = {row['parameter-name']: row['Unit'] for row in formatted_parameters}
        #write_json_file("Dmi +\\parameter_unit_map.json", param_to_unit)
        
# if __name__ == "__main__":
#     format_parameters("Dmi")