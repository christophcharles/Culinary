#!/usr/bin/env python3

import sys
import time
import math
import CmdLine
import JsonInfo
import Machine

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

def select_configurations(project_info, configs):
    results = {}
    
    filtered = {}
    if len(configs) > 0:
        for c in configs:
            if c in project_info["config"]:
                filtered[c] = project_info["config"][c]
            else:
                raise Exception("Unknown configuration: \"" + c + "\"")
    else:
        filtered = project_info["config"]
        
    for machine in project_info["machines"]:
        results[machine] = {}
        for config, desc in filtered.items():
            if desc["machine"]==machine:
                results[machine][config] = desc
        if not results[machine]:
            del results[machine]
    
    return results

def format_plural(count, amount):
    if count==0 or count==1:
        return str(count)+" "+amount
    else:
        return str(count)+" "+amount+"s"

def format_time(seconds):
    minutes = math.floor(seconds/60)
    seconds = round(seconds - 60*minutes)
    hours = math.floor(minutes/60)
    minutes = minutes - 60*hours
    if hours != 0:
        return format_plural(hours, "hour")+" "+format_plural(minutes,"minute")+" "+format_plural(seconds,"second")
    else:
        if minutes !=0:
            return format_plural(minutes,"minute")+" "+format_plural(seconds,"second")
        else:
            return format_plural(seconds,"second")

def main():
    sys.stdout = Unbuffered(sys.stdout)
    try:
        parameters = CmdLine.analyse_cmdline(sys.argv)
        if len(parameters) == 0:
            print("Usage: "+ sys.argv[0] + " PROJECT BRANCH [CONFIGS...]\n")
            print("PROJECT: the name of a project to be compiled.")
            print("BRANCH: branch to select for compilation.")
            print("CONFIGS: list of configuration to compile - if ignored all configurations will be used")
            return
        
        begin = time.perf_counter()
        total = 0
        successful = 0
        successful_details = {}
        
        project_info = JsonInfo.load_project_info(parameters)
        
        print("Compiling project \""+parameters[0]+"\" on branch \""+parameters[1]+"\".")
        
        selected_configs=select_configurations(project_info, parameters[2])
        print("The following configurations have being selected:")
        for machine, dic in selected_configs.items():
            configlist = ""
            for config in dic:
                configlist = configlist + " " + config
            print("- for machine \""+machine+"\":"+configlist)
        print()
        
        print("Starting compilation process...")
        for machine, dic in selected_configs.items():
            print("- Compiling on machine \""+machine+"\"...")
            print("  -> Starting machine")
            if not Machine.start_machine(project_info["machines"], machine):
                print("     FAILED to launch machine")
                for config, desc in dic.items():
                    total = total+1
                    successful_details[config] = (False, 0)
                continue
            
            for config, desc in dic.items():
                print("  -> Compiling configuration \""+config+"\"...")
                begin_local = time.perf_counter()
                successful_local = Machine.compile_config(project_info["machines"], desc, parameters[1])
                end_local = time.perf_counter()
                total = total + 1
                successful_details[config] = (successful_local, end_local-begin_local)
                if successful_local:
                    successful = successful + 1
            
            print("  -> Stopping machine")
            if not Machine.stop_machine(project_info["machines"], machine):
                print("     FAILED to stop machine")
                print("     To prevent possible multiple vm execution, stopping compilation sequence")
                break
        
        end = time.perf_counter()
        ellapsed = end-begin
        
        print()
        print("Results:")
        for config, info in successful_details.items():
            if info[0]:
                text = "OK"
            else:
                text = "FAILED"
            print("- " + config + ": " + text + " ("+format_time(info[1])+")")
        print()
        
        print(str(successful)+"/"+str(total)+" successful builds for a total time of "+format_time(ellapsed) + " (" +str(ellapsed)+" seconds)")
        
    except Exception as exc:
        print(exc)
        return
    
if __name__ == '__main__':
   main()
