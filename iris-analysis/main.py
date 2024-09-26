import os
import sys
import threading
from tqdm import tqdm
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import numpy as np
import cv2
from scipy import stats
from iris_evaluation import FeatureExtraction, Hamming


class AnalysisConfig(object):
    def __init__(self, instruction_path, script_dir):
        self.__instructions = self.__load_instructions(instruction_path)
        self.script_dir = f'{script_dir}/data'

    def __load_instructions(self, instruction_path):
        if os.path.exists(instruction_path):
            with open(instruction_path, 'r') as f:
                return json.load(f) 

    def __get_gabor_extraction(self):
        if self.__instructions["gabor_extraction"] == "True":
            return True
        else:
            return False
    
    def __get_comparison_mode(self):
        if self.__instructions["hamming_distance"] == "True":
            return True
        else:
            return False
        
    def __get_verbose(self):
        if self.__instructions["verbose"] == "True":
            return True
        else:
            return False
        
    def __get_roll(self):
        if self.__instructions["bitShifts"] == "True":
            return True
        else:
            return False
    
    def __get_wavelength(self):
        wavelength = None
        try:
            wavelength = int(self.__instructions["wavelength"])
        except:
            pass
        return wavelength
    
    def __get_threads(self):
        threads = None
        try:
            threads = int(self.__instructions["threads"])
        except:
            pass
        return threads
    
    def __get_batch_size(self):
        batch_size = None
        try:
            batch_size = int(self.__instructions["batchSize"])
        except:
            pass
        return batch_size
    
    gabor_extraction = property(fget=__get_gabor_extraction)
    comparison_mode = property(fget=__get_comparison_mode)
    verbose = property(fget=__get_verbose)
    roll = property(fget=__get_roll)
    wavelength = property(fget=__get_wavelength)
    threads = property(fget=__get_threads)
    batch_size = property(fget=__get_batch_size)

    #TODO combine these two methods w/ flag to differentiate

    def clean_image_sets(self):
        count = 0
        adjustment = 1

        for f in os.listdir(f'{self.script_dir}/image_sets'):
            if ']__' in f:
                continue
            if os.path.isdir(f'{self.script_dir}/image_sets/{f}') and not f.startswith('.'):
                new_name = None
                try:
                    img_dict = {}
                    for img in os.listdir(f'{self.script_dir}/image_sets/{f}'):
                        if img.lower().endswith(('.jpg', '.png')) and not img.startswith('.'):
                            img_np_name = img.lower().replace('.jpg', '').replace('.png', '')
                            img_dict[img_np_name] = cv2.imread(f'{self.script_dir}/image_sets/{f}/{img}')

                    if f.startswith('reference-'):
                        new_name = f'{self.script_dir}/image_sets/[R]__{f}'
                        adjustment = adjustment - 1
                    else:
                        new_name = f'{self.script_dir}/image_sets/[{count+adjustment}]__{f}'
                    os.rename(f'{self.script_dir}/image_sets/{f}', new_name)
                    np.savez(f'{new_name}.npz', **img_dict)
                    count = count + 1
                except Exception as e:
                    print(f"Error: {e}")
                    count = count + 1
                    continue
            
    def get_image_sets(self, active_dir):
        count = 0
        image_sets = []

        for npz in os.listdir(active_dir):
            if npz.endswith(".npz") and not npz.startswith("."):
                if npz.startswith("[R]__"):
                    image_sets.insert(0, f'{active_dir}/{npz}')
                    count = count + 1
                else:
                    image_sets.append(f'{active_dir}/{npz}')
          
        if count > 1 or count == 0:
            return -1

        return tuple(image_sets)

class GUIHandler(BaseHTTPRequestHandler):
    #IO functions only work with serve_forever method
    def do_POST(self):
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            json_path = os.path.join(script_dir, 'iris-analysis.json')
            print(f"Saving to: {json_path}", flush=True)
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError as e:
                # If there's an error decoding JSON, respond with 400 Bad Request
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return

            try:
                with open(json_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"Data saved: {data}", flush=True)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Error writing file")
                print(f"Error writing file: {e}", flush=True)
                return
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"JSON received")


        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error")
            print(f"Unexpected error: {e}", flush=True)
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Allow', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

class SpecialServer():
    def __init__(self, script_dir, gui_dir, json_dir):
        self.server = HTTPServer(('localhost', 8000), GUIHandler)
        self.gui_dir = gui_dir
        self.script_dir = script_dir
        self.json_dir = json_dir
        self.__instructions = None

    def __run_server(self):
        self.server.serve_forever()
    
    def launch(self):
        webbrowser.open(f"file://{os.path.abspath(self.gui_dir)}")
        server_thread = threading.Thread(target=self.__run_server)
        server_thread.start()

        print(self.json_dir)

        while True:
            if not os.path.exists(self.json_dir):
                continue
            else:
                self.server.shutdown()
                server_thread.join()
                break

        with open(self.json_dir, 'r') as json_file:
            self.__instructions = json.load(json_file)
            
        json_file.close()

    def __get_instructions(self):
        return self.__instructions
    
    instructions = property(fget = __get_instructions)

def exit_app(script_dir):
    #TODO instructions for creating instructions in browser
    
    print(f"TO MAKE iris-analysis.json, FOLLOW PROMPTS FOR GUI TOOL OR CREATE ONE AT https://robert-hart.github.io/iris-evaluation/\n")
    print(f"\tMAKE SURE THAT 'iris-analysis.json' IS PLACED IN THE FOLLOWING DIRECTORY: {script_dir}!\n")
    print(f"\tMAKE SURE THAT DATA IS CORRECTLY PLACED IN THE SUB-DIRECTORIES: {script_dir}/data!\n")
    print('##### EXITING #####')

    sys.exit()

def main():
    #check if readme exists, else delete
    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_dir = os.path.join(script_dir, 'iris-analysis.json')
    gui_dir = os.path.join(script_dir, "docs/gui.html")
    args = None
    instructions = None

    #make sure requisite directories exist
    os.makedirs(os.path.join(script_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(script_dir, "data/image_sets"), exist_ok=True)
    os.makedirs(os.path.join(script_dir, "data/results"), exist_ok=True)



    if os.path.exists(json_dir):
        args = AnalysisConfig(f'{script_dir}/iris-analysis.json', script_dir)
        print("\niris-analysis.json DETECTED!")
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n")
        print(f'\tthreads: {args.threads}')
        print(f'\tcomparison_mode: {args.comparison_mode}')
        print(f'\tverbose: {args.verbose}')
        print(f'\troll: {args.roll}')
        print(f'\twavelength: {args.wavelength}')
        print(f'\tbatch_size: {args.batch_size}')
        print(f'\tgabor_extraction: {args.gabor_extraction}')
        print(f'\tthreads: {args.threads}\n')

        print("###############################\n")
        print("\tINPUT 1 TO CONINTUE WITH THE INSTRUCTIONS ABOVE!")
        print("\tINPUT 2 TO CREATE NEW ANALYSIS PARAMETERS USING GUI TOOL!")
        print("\tINPUT ANYTHING ELSE TO EXIT!")
        print("\n###############################")
        user_input = input(">>>")
        try:
            user_int = int(user_input)
            if user_int == 1:
                GUIserver = SpecialServer(script_dir, gui_dir, json_dir)
                instructions = GUIserver.instructions
            elif user_int == 2:
                os.remove(json_dir)
                GUIserver = SpecialServer(script_dir, gui_dir, json_dir)
                GUIserver.launch()
                instructions = GUIserver.instructions
            else:
                exit_app(script_dir)
        except Exception as e:
            print(f"Error: {e}")
            exit_app(script_dir)
    else:
        print("iris-analysis.json NOT DETECTED!")
        print("###############################\n")
        print("\tINPUT 1 TO CONTINUE WITH NEW INSTRUCTIONS USING GUI TOOL")
        print("\tINPUT ANYTHING ELSE TO EXIT!")
        print("\n###############################")
        user_input = input(">>>")
        try:
            user_int = int(user_input)
            if int(user_input) == 1:
                GUIserver = SpecialServer(script_dir, gui_dir, json_dir)
                GUIserver.launch()
                instructions = GUIserver.instructions
            else:
                #safe
                exit_app(script_dir)

        except ValueError:
            exit_app(script_dir)
            #safe

    args.clean_image_sets()

    if bool(args.gabor_extraction): #run gabor extraction
        target_paths = []

        image_paths = args.get_image_sets(f'{script_dir}/data/image_sets')

        if image_paths == -1:
            print("TOO MANY OR TOO FEW REFERENCE DATASETS! MAKE SURE THAT THERE IS ONLY ONE SET OF IMAGES IN THE FOLLOWING DIRECTORY:\n\t{script_dir}/reference")
            exit_app(script_dir)

        feature_extraction_path = f'{script_dir}/data/results/feature_extraction'
        os.makedirs(feature_extraction_path, exist_ok=True)
        
        for i, source in enumerate(image_paths):
                source_images = np.load(f'{source}', allow_pickle=True) #load the source images
                target_name = source.rpartition('/')[2].replace('.npz', '')
                target_path = f'{feature_extraction_path}/{target_name}' #make the target path
                target_paths.append(target_path)
                os.makedirs(target_path, exist_ok=True)

                logistical_parameters = {
                    'source': source_images, #maybe just source?
                    'target_path': target_path,
                    'threads': int(args.threads)
                }

                shared_parameters = {
                    "segment": 1,
                    "multiplicative_factor": 2,
                    "image_size": 256,
                    "output_y": 45,
                    "output_x": 360,
                    "verbose": bool(args.verbose),
                    "wavelength": int(args.wavelength),
                    "octaves": 1,
                }

                FE = FeatureExtraction(logistical_parameters, shared_parameters)
                print(f'EXTRACTING FEATURES OF DATASET {i+1} OF {len(image_paths)}')
                FE.calculate()
                FE.clean()

    if args.comparison_mode:
        data_paths = args.get_image_sets(f'{script_dir}/data/results/feature_extraction')
        results_path = f'{script_dir}/data/results/comparisons'
        os.makedirs(results_path, exist_ok=True)

        hamming_params = {
            "roll" : args.roll,
            "verbose" : True,
            "pairwise" : True,
            "data_paths" : data_paths,
            "results_path" : results_path,
            "reference_batch_size" : int(args.batch_size),
        }

        HammingSetup = Hamming(hamming_params)
        HammingSetup.calculator()

if __name__ == "__main__":
    main()