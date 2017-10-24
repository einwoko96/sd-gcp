def num_frames_to_fraction(num_frames):
    from fractions import Fraction
    t = range(0,num_frames)
    frac_str = []
    for ind, num in enumerate(t):
        frac = Fraction(num, num_frames)
        frac_str.append( str(frac.numerator) + '-' + str(frac.denominator) )
    return frac_str
def fraction_to_ind(frac_str,num_frames):
    import re
    inds = []
    for ind, val in enumerate(frac_str):
        num_den = re.split('-',val)
        num = int(num_den[0])
        den = int(num_den[1])
        inds.append(num*num_frames/den)   
    return(inds)