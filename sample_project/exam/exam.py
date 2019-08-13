"""
These methods can be called inside WebCAT to determine which tests are loaded
for a given section/exam pair.  This allows a common WebCAT submission site to
support different project tests 
"""
def section():
    # Instructor section (instructor to change before distribution)
    #return 8527
    #return 8528
    return 8529


def exam():
    # A or B exam (instructor to change to match specific project distribution

    return "A"
    #return "B"
