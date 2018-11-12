
import pathlib
import json
import socket

def validate_machine(name, machine_info):
    if "start-cmd" not in machine_info:
        raise Exception("Invalid machine \""+name+"\": missing start-cmd parameter")
    if "delay-after-boot" not in machine_info:
        raise Exception("Invalid machine \""+name+"\": missing delay-after-boot parameter")
    if "stop-cmd" not in machine_info:
        raise Exception("Invalid machine \""+name+"\": missing stop-cmd parameter")
    if "network-connection" not in machine_info:
        raise Exception("Invalid machine \""+name+"\": missing network-connection parameter")
    if len(machine_info) != 4:
        raise Exception("Invalid machine \""+name+"\": unkown extra parameters")
    
    if machine_info["start-cmd"] != None and not isinstance(machine_info["start-cmd"], str):
        raise Exception("Invalid machine \""+name+"\": start-cmd must be a string or null")
    if machine_info["stop-cmd"] != None and not isinstance(machine_info["stop-cmd"], str):
        raise Exception("Invalid machine \""+name+"\": stop-cmd must be a string or null")
    if machine_info["network-connection"] != None:
        if not isinstance(machine_info["network-connection"], dict):
            raise Exception("Invalid machine \""+name+"\": network-connection must either be null or a json object")
        
        if "ip" not in machine_info["network-connection"]:
            raise Exception("Invalid machine \""+name+"\": network-connection must contain a field \"ip\"")
        if "port" not in machine_info["network-connection"]:
            raise Exception("Invalid machine \""+name+"\": network-connection must contain a field \"port\"")
        if "user" not in machine_info["network-connection"]:
            raise Exception("Invalid machine \""+name+"\": network-connection must contain a field \"user\"")
        if "non-unix-cmds" not in machine_info["network-connection"]:
            raise Exception("Invalid machine \""+name+"\": network-connection must contain a field \"non-unix-cmds\"")
        if len(machine_info["network-connection"]) != 4:
            raise Exception("Invalid machine \""+name+"\": unknown extra field in network-connection")
        
        if not isinstance(machine_info["network-connection"]["ip"], str):
            raise Exception("Invalid machine \""+name+"\": ip in network-connection must be a string")
        if machine_info["network-connection"]["port"] != None and not isinstance(machine_info["network-connection"]["port"], int):
            raise Exception("Invalid machine \""+name+"\": port in network-connection must be either an integer or null")
        if not isinstance(machine_info["network-connection"]["user"], str):
            raise Exception("Invalid machine \""+name+"\": user in network-connection must be a string")
        if machine_info["network-connection"]["non-unix-cmds"] != None and not isinstance(machine_info["network-connection"]["non-unix-cmds"], dict):
            raise Exception("Invalid machine \""+name+"\": non-unix-cmds in network-connection must be either a json object or null")
            
        try:
            socket.inet_aton(machine_info["network-connection"]["ip"])
        except socket.error:
            raise Exception("Invalid machine \""+name+"\": ip in network-connection is invalid")
            
        if len(machine_info["network-connection"]["user"]) == 0:
            raise Exception("Invalid machine \""+name+"\": user in network-connection cannot be empty")
        if ' ' in machine_info["network-connection"]["user"]:
            raise Exception("Invalid machine \""+name+"\": user in network-connection cannot contain spaces")
        if '\'' in machine_info["network-connection"]["user"]:
            raise Exception("Invalid machine \""+name+"\": user in network-connection cannot contain apostrophes (')")
        if '\t' in machine_info["network-connection"]["user"]:
            raise Exception("Invalid machine \""+name+"\": user in network-connection cannot contain tabs")
        if '\r' in machine_info["network-connection"]["user"] or '\n' in machine_info["network-connection"]["user"]:
            raise Exception("Invalid machine \""+name+"\": user in network-connection cannot contain new lines")
            
        if machine_info["network-connection"]["non-unix-cmds"] != None:
            Cmds = machine_info["network-connection"]["non-unix-cmds"]
            
            if "test-dir-cmd" not in Cmds:
                raise Exception("Invalid machine \""+name+"\": non-unix-cmds (in network-connection) must contain a field \"test-dir-cmd\"")
            if "rm-dir-cmd" not in Cmds:
                raise Exception("Invalid machine \""+name+"\": non-unix-cmds (in network-connection) must contain a field \"rm-dir-cmd\"")
            if "mk-dir-cmd" not in Cmds:
                raise Exception("Invalid machine \""+name+"\": non-unix-cmds (in network-connection) must contain a field \"mk-dir-cmd\"")
            if len(Cmds) != 3:
                raise Exception("Invalid machine \""+name+"\": unknown extra field in non-unix-cmds")
                
            if not isinstance(Cmds["test-dir-cmd"], str):
                raise Exception("Invalid machine \""+name+"\": test-dir-cmd in non-unix-cmds (in network-connection) must be a string")
            if not isinstance(Cmds["rm-dir-cmd"], str):
                raise Exception("Invalid machine \""+name+"\": rm-dir-cmd in non-unix-cmds (in network-connection) must be a string")
            if not isinstance(Cmds["mk-dir-cmd"], str):
                raise Exception("Invalid machine \""+name+"\": mk-dir-cmd in non-unix-cmds (in network-connection) must be a string")
                
            if '\'' in Cmds["test-dir-cmd"]:
                raise Exception("Invalid machine \""+name+"\": test-dir-cmd in non-unix-cmds (in network-connection) cannot contain apostrophes (')")
            if '\r' in Cmds["test-dir-cmd"] or '\n' in Cmds["test-dir-cmd"]:
                raise Exception("Invalid machine \""+name+"\": test-dir-cmd in non-unix-cmds (in network-connection) cannot contain new lines")
            
            if '\'' in Cmds["rm-dir-cmd"]:
                raise Exception("Invalid machine \""+name+"\": rm-dir-cmd in non-unix-cmds (in network-connection) cannot contain apostrophes (')")
            if '\r' in Cmds["rm-dir-cmd"] or '\n' in Cmds["rm-dir-cmd"]:
                raise Exception("Invalid machine \""+name+"\": rm-dir-cmd in non-unix-cmds (in network-connection) cannot contain new lines")
                
            if '\'' in Cmds["mk-dir-cmd"]:
                raise Exception("Invalid machine \""+name+"\": mk-dir-cmd in non-unix-cmds (in network-connection) cannot contain apostrophes (')")
            if '\r' in Cmds["mk-dir-cmd"] or '\n' in Cmds["mk-dir-cmd"]:
                raise Exception("Invalid machine \""+name+"\": mk-dir-cmd in non-unix-cmds (in network-connection) cannot contain new lines")

def validate_config(name, config_info, machines):
    if "machine" not in config_info:
        raise Exception("Invalid configuration \""+name+"\": missing machine parameter")
    if "project-dir" not in config_info:
        raise Exception("Invalid configuration \""+name+"\": missing project-dir parameter")
    if "build-dir" not in config_info:
        raise Exception("Invalid configuration \""+name+"\": missing build-dir parameter")
    if "git-source" not in config_info:
        raise Exception("Invalid configuration \""+name+"\": missing git-source parameter")
    if "rmdir-before-build" not in config_info:
        raise Exception("Invalid configuration \""+name+"\": missing rmdir-before-build parameter")
    if "build-cmds" not in config_info:
        raise Exception("Invalid configuration \""+name+"\": missing build-cmds parameter")
    if len(config_info) != 6:
        raise Exception("Invalid configuration \""+name+"\": unkown extra parameters")
        
    if not isinstance(config_info["machine"], str):
        raise Exception("Invalid configuration \""+name+"\": machine parameter must be a string")
    if not isinstance(config_info["project-dir"], str):
        raise Exception("Invalid configuration \""+name+"\": project-dir parameter must be a string")
    if not isinstance(config_info["build-dir"], str):
        raise Exception("Invalid configuration \""+name+"\": build-dir parameter must be a string")
    if not isinstance(config_info["git-source"], str):
        raise Exception("Invalid configuration \""+name+"\": git-source parameter must be a string")
    if not isinstance(config_info["rmdir-before-build"], bool):
        raise Exception("Invalid configuration \""+name+"\": rmdir-before-build parameter must be a boolean")
    if not isinstance(config_info["build-cmds"], list):
        raise Exception("Invalid configuration \""+name+"\": build-cmds parameter must be a json array")
        
    if config_info["machine"] not in machines:
        raise Exception("Invalid configuration \""+name+"\": unknown machine referenced")
    if '\'' in config_info["project-dir"]:
        raise Exception("Invalid configuration \""+name+"\": apostrophe (') in directory names not handled by Compile.py (see project-dir)")
    if '\'' in config_info["build-dir"]:
        raise Exception("Invalid configuration \""+name+"\": apostrophe (') in directory names not handled by Compile.py (see build-dir)")
    if '\'' in config_info["git-source"]:
        raise Exception("Invalid configuration \""+name+"\": apostrophe (') in url names not handled by Compile.py (see git-source)")
    
    for cmd in config_info["build-cmds"]:
        if not isinstance(cmd, str):
            raise Exception("Invalid configuration \""+name+"\": build-cmds parameter must only contain strings")
        if '\'' in cmd:
            raise Exception("Invalid configuration \""+name+"\": apostrophe (') in commands not handled by Compile.py (see build-cmds)")

def load_project_info(parameters):
    project_json_file = parameters[0] + ".json"
    
    project_json_path = pathlib.Path(project_json_file)
    if not project_json_path.is_file():
        raise Exception("The project file \""+project_json_file+"\" could not be found.")
        
    project_json = json.load(project_json_path.open())
    if "project_name" not in project_json:
        raise Exception("The project file \""+project_json_file+"\" has invalid structure (no project_name key)")
    if "config" not in project_json:
        raise Exception("The project file \""+project_json_file+"\" has invalid structure (no config key)")
    if "machines" not in project_json:
        raise Exception("The project file \""+project_json_file+"\" has invalid structure (no machines key)")
        
    if project_json["project_name"] != parameters[0]:
        raise Exception("The project file \""+project_json_file+"\" has invalid structure (project_name does not match)")
        
    for machine, desc in project_json["machines"].items():
        validate_machine(machine, desc)
        
    for config, desc in project_json["config"].items():
        validate_config(config, desc, project_json["machines"])
        
    return project_json
        
