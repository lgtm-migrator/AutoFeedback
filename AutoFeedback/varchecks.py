import importlib

def exists(varname,modname=None):
    if not modname:
        mod = importlib.import_module('main')
    else:
        mod=modname

    varstring="mod."+varname # get variable from main code
    try:
        var=eval(varstring)
        return(True)
    except:
        return(False)
        
def get_var(varname,modname=None):
    if not modname:
        mod = importlib.import_module('main')
    else:
        mod=modname
    varstring="mod."+varname # get variable from main code
    return(eval(varstring))

def check_size(a,b):
    if hasattr(b,"shape") and hasattr(a,"shape"): #both ndarrays
        return a.shape==b.shape
    if hasattr(b,"__len__") and  hasattr(a,"__len__"): # both arrays
        return len(a)==len(b) # size of arrays matches
    elif not (hasattr(b,"__len__") or hasattr(a,"__len__")):# both scalars
        return True
    else:# mismatch in type
        return False

def check_value(a,b):
    import numpy as np
    import sympy as sp

    if (isinstance(a,str) and isinstance(b,str)) \
        or (isinstance(a,dict) and isinstance(b,dict)):
        return (a==b)
    elif (isinstance(a,sp.Basic) and isinstance(b,sp.Basic)):
        try: 
            sp.simplify(a) 
            sp.simplify(b)
            return(sp.simplify(a)==sp.simplify(b) or (sp.factor(a) == sp.factor(b))) 
        except:
            return(a==b)
    else:
        try: # treat inputs as ndarrays and compare with builtin
            return np.all(np.isclose(a,b))
        except: # if not ndarrays, treat as list (of strings) and compare elements
            try: 
                for x,y in zip(a,b):
                    if not(x==y): return False
                return True
            except:
                return False

def check_vars(varname,expected,modname=None,output=True):
    from AutoFeedback.variable_error_messages import print_error_message
    try:
        assert(exists(varname,modname)), "existence"
        var=get_var(varname,modname)
        assert(check_size(var,expected)), "size"
        assert(check_value(var,expected)), "value"
        if output: print_error_message("success",varname,expected,var)
    except AssertionError as error:
        if output: print_error_message(error,varname,expected,var)
        return(False)
    return(True)

def check_output(expected):
    from AutoFeedback.variable_error_messages import output_check
    return output_check(expected)
