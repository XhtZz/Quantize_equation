#coding=utf-8 

import random
import math

in_frac = 4
w_frac = 8
b_frac = 5
out_frac = 4

in_add_w_minus_b = in_frac+w_frac-b_frac
in_add_w_minus_out = in_frac+w_frac-out_frac
b_minus_out = b_frac-out_frac

for i in range(10000):
    input = random.randint(1,2000)
    weight = random.randint(1,2000)
    bias = random.randint(1,2000)

    '''
    <<:左移floor   >>:右移floor
    <<<：左移round >>>:右移round
    '''

    #1：in、w、b分别fake_quant    
    result0 = round((input*pow(2.0,-in_frac) * weight*pow(2.0,-w_frac) + bias*pow(2.0,-b_frac)) * pow(2.0,out_frac))

    #2：提取pow(2.0,-in_frac)*pow(2.0,-w_frac)
    #(input*weight+(bias<<in_add_w_minus_b))>>>in_add_w_minus_out
    result1 = round((input*weight + bias*pow(2.0,in_add_w_minus_b))*pow(2.0,-in_add_w_minus_out))

    #3：需满足条件b_minus_out>0 && in_add_w_minus_b>=0 && in_add_w_minus_out>=0
    #((input*weight+(bias<<in_add_w_minus_b))>>in_add_w_minus_b)>>>b_minus_out
    result2_1   = round(math.floor((input*weight + bias*pow(2.0,in_add_w_minus_b))*pow(2.0,-in_add_w_minus_b))*pow(2.0,-b_minus_out))
    #(input*weight>>in_add_w_minus_b+bias)>>>b_minus_out
    result2     = round((math.floor(input*weight*pow(2.0,-in_add_w_minus_b)) + bias)*pow(2.0,-b_minus_out))

    if result0!=result1 or result1!=result2 or result0!=result2:
        print("%d %d %d, result0:%f result1:%f result2:%f" % (input,weight,bias,result0,result1,result2))

