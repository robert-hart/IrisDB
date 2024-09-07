import os
import sys
import threading
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

class GUIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get the current directory where the script is running
            script_dir = os.path.dirname(os.path.realpath(__file__))
            json_path = os.path.join(script_dir, 'instructions.json')
            print(f"Saving to: {json_path}", flush=True)
            
            # Read the content length and the POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Try to decode the JSON data
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError as e:
                # If there's an error decoding JSON, respond with 400 Bad Request
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return

            # Write the decoded JSON to a file
            try:
                with open(json_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"Data saved: {data}", flush=True)
            except Exception as e:
                # Handle file write errors
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Error writing file")
                print(f"Error writing file: {e}", flush=True)
                return
            
            # If successful, send 200 OK response
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"JSON received")


        except Exception as e:
            # Catch-all for any other server errors
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error")
            print(f"Unexpected error: {e}", flush=True)
        
    def do_OPTIONS(self):
        # Handling OPTIONS request for CORS preflight
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


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_dir = os.path.join(script_dir, 'instructions.json')
    gui_dir = os.path.join(script_dir, "docs/gui.html")
    instructions = None

    if os.path.exists(json_dir):
       with open('instructions.json', 'r') as json_file:
            instructions = json.load(json_file)
    else:
        print("NO INSTRUCTIONS.JSON DETECTED!\n\n")
        print("###############################\n\n")
        print("\tENTER 1 TO MAKE INSTRUCTIONS USING GUI TOOL")
        print("\tENTER ANYTHING BUT 1 TO CLOSE\n\n")
        print("###############################")
        user_input = input(">>>:")
        try:
            user_int = int(user_input)
            if int(user_input) == 1:
                GUIserver = SpecialServer(script_dir, gui_dir, json_dir)
                GUIserver.launch()
                instructions = GUIserver.instructions
            else:
                sys.exit()
        except ValueError:
            sys.exit()

    print(instructions)

if __name__ == "__main__":
    main()