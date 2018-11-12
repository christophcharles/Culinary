
def analyse_cmdline(argv):
    if len(argv) < 3:
        return ()
    
    project = argv[1]
    branch = argv[2]
    configs = argv[3:]
    
    if ' ' in project:
        raise Exception("Invalid project name: spaces are forbidden in project name")
    if '\'' in project:
        raise Exception("Invalid project name: apostrophes are forbidden in project name")
    if '\t' in project:
        raise Exception("Invalid project name: tabs are forbidden in project name")
        
    if ' ' in branch:
        raise Exception("Invalid project name: spaces are forbidden in branch name")
    if '\'' in branch:
        raise Exception("Invalid project name: apostrophes are forbidden in branch name")
    if '\t' in branch:
        raise Exception("Invalid project name: tabs are forbidden in branch name")
        
    for config in configs:
        if ' ' in config:
            raise Exception("Invalid project name: spaces are forbidden in config name")
        if '\'' in config:
            raise Exception("Invalid project name: apostrophes are forbidden in config name")
        if '\t' in config:
            raise Exception("Invalid project name: tabs are forbidden in config name")
        
    return (project, branch, configs)
