import re

def std_str_assert_str(lh,comp,rh):
    str_ret = ""
    str_ret += "if(!(assert_str_eq("+lh+","+rh+") "+comp+" 0 )){\n"
    str_ret += "    return test_failed(\""+lh.replace("\"","\\\"")+comp.replace("\"","\\\"")+rh.replace("\"","\\\"")+"\");\n"
    str_ret += "} else {\n"
    str_ret += "    test_passed(\""+lh.replace("\"","\\\"")+comp.replace("\"","\\\"")+rh.replace("\"","\\\"")+"\");\n"
    str_ret += "}\n"
    return str_ret

def get_format_from_type(f_type):
    # N.B. only sane type orders allowed. I.e "unsigned long long int *" is OK
    # but "long int unsigned long *" etc. will default to verbatim ... 
    if not f_type:
        return "verbatim"

    if f_type == "verbatim": #dont check if we know there are no type
        return "verbatim"
    if re.fullmatch(r'\s*(signed\s)?\s*long(\s+int)?\s*\*?\s*',f_type):
        return "%li"
    if re.fullmatch(r'\s*((signed\s)?\s*long\s+long\s*(int)?\s*\*?\s*',f_type):
        return "%lli"
    if re.fullmatch(r'\s*(signed\s)?\s*int\s*\*?\s*',f_type):
        return "%i"
    if re.fullmatch(r'\s*(signed\s)?\s*short(\s+int)?\s*\*?\s*',f_type):
        return "%hi"
    if re.fullmatch(r'\s*(unsigned\s)?\s*long(\s+int)?\s*\*?\s*',f_type):
        return "%lu"
    if re.fullmatch(r'\s*((unsigned\s)?\s*long\s+long\s*(int)?\s*\*?\s*',f_type):
        return "%llu"
    if re.fullmatch(r'\s*unsigned\s*(int)?\s*\*?\s*',f_type):
        return "%u"
    if re.fullmatch(r'\s*(unsigned\s)?\s*short(\s+int)?\s*\*?\s*',f_type):
        return "%hu"
    if re.fullmatch(r'\s*float\s*\*?\s*',f_type):
        return "%f"
    if re.fullmatch(r'\s*double\s*\*?\s*',f_type):
        return "%f"
    if re.fullmatch(r'\s*long\s*double\s*\*?\s*',f_type):
        return "%Lf"
    if re.fullmatch(r'\s*((un)?signed\s)?\s*char\s*\*?\s*',f_type):
        return "%c"
    return "verbatim" #fallback type

def std_assert_str(lh,comp,rh,f_type):
    str_ret = ""

    format = get_format_from_type(f_type) #check if type suits printf()

    if f_type == "verbatim" or format == "verbatim":
        str_ret += "if(assert_true("+lh+comp+rh+")){\n"
        str_ret += "    return test_failed(\""+lh+comp+rh+"\");\n"
        str_ret += "} else {\n"
        str_ret += "    test_passed(\""+lh+comp+rh+"\");\n"
        str_ret += "}\n"
        return str_ret
    else: #the function type is specified
        
        #check if f_type is a pointer
        if f_type.count("*")!=0:
            ptr = "*"
        else:
            ptr = ""

        str_ret += "{\n"
        str_ret += "    "+f_type +"tmp = "+lh+";\n"
        str_ret += "    "+"if(assert_true("+ptr+"tmp "+comp+rh+")){\n"
        str_ret += "    "+"    "+"int errn = test_failed(\""+lh+comp+rh+"\n\");\n"
        str_ret += "    "+"    "+"printf(\"        Actual:"+format+" "+comp+" "+format+"\n\","+ptr+"tmp,"+rh+");\n"
        str_ret += "    "+"    "+"return errn;\n"
        str_ret += "    "+"} else {\n"
        str_ret += "    "+"    "+"test_passed(\""+lh+comp+rh+"\");\n"
        str_ret += "    "+"    "+"printf(\"        Actual:"+format+" "+comp+" "+format+"\n\","+ptr+"tmp,"+rh+");\n"
        str_ret += "    "+"}\n"
        str_ret += "}\n"
        return str_ret 

def assert_eq(lh,rh,f_type):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"==",rh)
    
    return std_assert_str(lh,"==",rh,f_type)

def assert_less(lh,rh,f_type):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"<",rh)

    return std_assert_str(lh,"<",rh,f_type)
    
def assert_greater(lh,rh,f_type):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,">",rh)

    return std_assert_str(lh,">",rh,f_type)

def assert_greater_eq(lh,rh,f_type):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,">=",rh)

    return std_assert_str(lh,">=",rh,f_type)

def assert_less_eq(lh,rh,f_type):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"<=",rh)

    return std_assert_str(lh,"<=",rh,f_type)

def assert_not_eq(lh,rh,f_type):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"!=",rh)

    return std_assert_str(lh,"!=",rh,f_type)