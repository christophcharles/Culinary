
import os
import pathlib
import shutil
import time

def execute_command_on_machine(machines_info, machine, cmd):
    if machines_info[machine]["network-connection"] != None:
        connection_info = machines_info[machine]["network-connection"]
        ip = connection_info["ip"]
        port = connection_info["port"]
        if port == None:
            port = 22
        user = connection_info["user"]
        
        cmdline = "ssh -p " + str(port) + " " + user + "@" + ip + " \'" + cmd + "\'"
        return os.system(cmdline)
    else:
        return os.system(cmd)

def test_connection_once(machines_info, machine):
    testconnectioncmd = "pwd"
    if machines_info[machine]["network-connection"] != None:
        if machines_info[machine]["network-connection"]["non-unix-cmds"] != None:
            testconnectioncmd = machines_info[machine]["network-connection"]["non-unix-cmds"]["connection-attempt"]
    return (execute_command_on_machine(machines_info, machine, testconnectioncmd) == 0)

def test_connection_to_machine(machines_info, machine):
    if machines_info[machine]["connection-attempt-count"] != 0:
        remaining_attempts = machines_info[machine]["connection-attempt-count"]
        success = False
        while (not success) and (remaining_attempts > 0):
            if machines_info[machine]["delay-after-boot"] != 0:
                time.sleep(machines_info[machine]["delay-after-boot"])
            success = test_connection_once(machines_info, machine)
            remaining_attempts = remaining_attempts -1
        return success
    else:
        if machines_info[machine]["delay-after-boot"] != 0:
            time.sleep(machines_info[machine]["delay-after-boot"])
        return True

def start_machine(machines_info, machine):
    if machines_info[machine]["start-cmd"]:
        if os.system(machines_info[machine]["start-cmd"]) != 0:
            return False
    return True

def stop_machine(machines_info, machine):
    if machines_info[machine]["stop-cmd"]:
        return os.system(machines_info[machine]["stop-cmd"]) == 0
    return True

def test_directory_exists(machines_info, config_info, directory):
    machine = config_info["machine"]
    if machines_info[machine]["network-connection"] != None:
        testdircmd = "test -d"
        
        if machines_info[machine]["network-connection"]["non-unix-cmds"] != None:
            testdircmd = machines_info[machine]["network-connection"]["non-unix-cmds"]["test-dir-cmd"]
        
        cmdline = testdircmd + " \'" + directory + "\'"
        return (execute_command_on_machine(machines_info, machine, cmdline) == 0)
    else:
        p = pathlib.Path(directory)
        return p.is_dir()

def erase_directory(machines_info, config_info, directory):
    machine = config_info["machine"]
    if machines_info[machine]["network-connection"] != None:
        rmdircmd = "rm -r"
        
        if machines_info[machine]["network-connection"]["non-unix-cmds"] != None:
            rmdircmd = machines_info[machine]["network-connection"]["non-unix-cmds"]["rm-dir-cmd"]
        
        cmdline = rmdircmd + " \'" + directory + "\'"
        return (execute_command_on_machine(machines_info, machine, cmdline) == 0)
    else:
        try:
            shutil.rmtree(directory)
        except:
            return False
        return True
    
def create_directory(machines_info, config_info, directory):
    machine = config_info["machine"]
    if machines_info[machine]["network-connection"] != None:
        mkdircmd = "mkdir -p"
        
        if machines_info[machine]["network-connection"]["non-unix-cmds"] != None:
            mkdircmd = machines_info[machine]["network-connection"]["non-unix-cmds"]["mk-dir-cmd"]
        
        cmdline = mkdircmd + " \'" + directory + "\'"
        return (execute_command_on_machine(machines_info, machine, cmdline) == 0)
    else:
        try:
            os.makedirs(directory)
        except:
            return False
        return True

def update_source(machines_info, config_info):
    cmd = "cd \'" + config_info["project-dir"] + "\' ; git pull origin"
    return execute_command_on_machine(machines_info, config_info["machine"], cmd) == 0

def download_source(machines_info, config_info):
    p = pathlib.Path(config_info["project-dir"])
    parent_dir = str(p.parent)
    if not test_directory_exists(machines_info, config_info, parent_dir):
        print("Parent directory does not exists!")
        return False
    cmd = "cd \'" + str(p.parent) + "\'; git clone \'" + config_info["git-source"] + "\'"
    return execute_command_on_machine(machines_info, config_info["machine"], cmd) == 0

def select_branch(machines_info, config_info, branch):
    check_cmd = "cd \'" + config_info["project-dir"] + "\'; git rev-parse --verify \'origin/" + branch + "\'"
    if (execute_command_on_machine(machines_info, config_info["machine"], check_cmd) != 0):
        return False
    cmd = "cd \'" + config_info["project-dir"] + "\'; git checkout \'" + branch + "\'"
    return execute_command_on_machine(machines_info, config_info["machine"], cmd) == 0

def prepare_build_directory(machines_info, config_info):
    if config_info["rmdir-before-build"]:
        if test_directory_exists(machines_info, config_info, config_info["build-dir"]):
            if not erase_directory(machines_info, config_info, config_info["build-dir"]):
                return False

    if not test_directory_exists(machines_info, config_info, config_info["build-dir"]):
        if not create_directory(machines_info, config_info, config_info["build-dir"]):
                return False
    
    return True

def execute_build_commands(machines_info, config_info):
    for cmd in config_info["build-cmds"]:
        cmdline = "cd " + config_info["build-dir"] + "; " + cmd
        if execute_command_on_machine(machines_info, config_info["machine"], cmdline) != 0:
            print("Error while building")
            return False
    return True

def compile_config(machines_info, config_info, branch):
    if test_directory_exists(machines_info, config_info, config_info["project-dir"]):
        if not update_source(machines_info, config_info):
            print("Error while updating")
            return False
    else:
        if not download_source(machines_info, config_info):
            print("Error while downloading")
            return False
    
    if not select_branch(machines_info, config_info, branch):
        print("Error while selecting branch \""+branch+"\".")
        return False
    
    if not prepare_build_directory(machines_info, config_info):
        print("Error while preparing build directory")
        return False
    
    return execute_build_commands(machines_info, config_info)
