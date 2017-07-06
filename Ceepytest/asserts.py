import re

def std_str_assert_str(lh,comp,rh):
    str_ret = ""
    str_ret += "if(!(assert_str_eq("+lh+","+rh+") "+comp+" 0 )){\n"
    str_ret += "    return test_failed(\""+lh.replace("\"","\\\"")+comp.replace("\"","\\\"")+rh.replace("\"","\\\"")+"\");\n"
    str_ret += "} else {\n"
    str_ret += "    test_passed(\""+lh.replace("\"","\\\"")+comp.replace("\"","\\\"")+rh.replace("\"","\\\"")+"\");\n"
    str_ret += "}\n"
    return str_ret

def std_assert_str(lh,comp,rh):
    str_ret = ""
    str_ret += "if(assert_true("+lh+comp+rh+")){\n"
    str_ret += "    return test_failed(\""+lh+comp+rh+"\");\n"
    str_ret += "} else {\n"
    str_ret += "    test_passed(\""+lh+comp+rh+"\");\n"
    str_ret += "}\n"
    return str_ret

def assert_eq(lh,rh):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"==",rh)
    
    return std_assert_str(lh,"==",rh)

def assert_less(lh,rh):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"<",rh)

    return std_assert_str(lh,"<",rh)
    
def assert_greater(lh,rh):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,">",rh)

    return std_assert_str(lh,">",rh)

def assert_greater_eq(lh,rh):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,">=",rh)

    return std_assert_str(lh,">=",rh)

def assert_less_eq(lh,rh):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"<=",rh)

    return std_assert_str(lh,"<=",rh)

def assert_not_eq(lh,rh):
    #check if either side are "string literals"
    if(re.match(r'".*"',lh) or re.match(r'".*"',rh)):
        return std_str_assert_str(lh,"!=",rh)

    return std_assert_str(lh,"!=",rh)