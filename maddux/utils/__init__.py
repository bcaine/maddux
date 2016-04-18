from animate_path import animate_path

utils = {
    "animate_path": animate_path,
}

def run_util(**kwargs):
    util = kwargs.get('util')
    environment = kwargs.get('environment')
    input_file = kwargs.get('input')
    output_file = kwargs.get('output')
    
    if not util:
        print "Please provide a util"
        return False

    if util in utils:
        if util == "animate_path":
            if input_file is None:
                print "Please Provide an input file"
                return False
            if environment is None:
                print "Please provide an environment"
                return False
            animate_path(environment, input_file, output_file)
        else:
            utils[util]()
        return True
    return False
