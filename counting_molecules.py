if __name__ == "__main__":
    # get inputs
    c, h, o = input().split()
    c = int(c)
    h = int(h)
    o = int(o)
    
    # calculate output
    x = (12*o + 6*h - 24*c) // 24
    y = (12*o - 6*h) // 24
    z = (h + 4*c - 2*o) // 24
    
    # Check for errors
    x_remainder = (12*o+6*h-24*c)%24
    y_remainder = (12*o-6*h)%24
    z_remainder = (h+4*c-2*o)%24
    
    if (x_remainder != 0 or y_remainder != 0 or z_remainder != 0):
        print("Error")
    elif (x < 0 or y < 0 or z < 0):
        print("Error")
    else:
        # If there is no errors, print output
        print('{} {} {}'.format(x,y,z))
