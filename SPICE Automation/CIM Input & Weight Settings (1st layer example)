import numpy as np
import os
import sys


test_binaryinput = np.loadtxt('/home/laveriteforme2000/data/test_binaryinput.csv', delimiter=',', dtype=np.int)

# just for the first & only one input scenario
binaryinput_0 = test_binaryinput[0]

firstlayer_inputs_0 = binaryinput_0[0:256]
firstlayer_inputs_1 = binaryinput_0[256:512]
firstlayer_inputs_2 = binaryinput_0[512:768]
firstlayer_inputs_3 = np.hstack([binaryinput_0[768:784], np.zeros((240,))])

row = 256
for a in range(0, 4):
    globals()['fOUT_{}'.format(a)] = open("./SPICE_Codes/MLP_1stlayer_inputs/firstlayer_inputs_"+str(a)+".sp", "w")
    for r in range(0, len(globals()['firstlayer_inputs_{}'.format(a)])):
        if globals()['firstlayer_inputs_{}'.format(a)][r] == 1:
            globals()['fOUT_{}'.format(a)].write('''
vmwl_%d	mwl_%d	0	pwl	(0			xvdr
+				0.4n			xvdr
+				'0.4n+tr'		xvrst
+				'0.4n+tr+tEn'		xvrst
+				'0.4n+tr+tEn+tf'	xvdr)

vmwlb_%d	mwlb_%d	0	pwl	(0			xvss
+				0.4n			xvss
+				'0.4n+tr'		xvrst
+				'0.4n+tr+tEn'		xvrst
+				'0.4n+tr+tEn+tf'	xvss)''' %(r, r, r, r))
        
        elif globals()['firstlayer_inputs_{}'.format(a)][r] == 0:
            globals()['fOUT_{}'.format(a)].write('''
vmwl_%d	mwl_%d	0	pwl	(0			xvrst
+				0.4n			xvrst
+				'0.4n+tr'		xvrst
+				'0.4n+tr+tEn'		xvrst
+				'0.4n+tr+tEn+tf'	xvrst)

vmwlb_%d	mwlb_%d	0	pwl	(0			xvrst
+				0.4n			xvrs
+				'0.4n+tr'		xvrst
+				'0.4n+tr+tEn'		xvrst
+				'0.4n+tr+tEn+tf'	xvrst)''' %(r, r, r, r))

        else:
            globals()['fOUT_{}'.format(a)].write('''
vmwl_%d	mwl_%d	0	pwl	(0			xvss
+				0.4n			xvss
+				'0.4n+tr'		xvrst
+				'0.4n+tr+tEn'		xvrst
+				'0.4n+tr+tEn+tf'	xvss)

vmwlb_%d	mwlb_%d	0	pwl	(0			xvdr
+				0.4n			xvdr
+				'0.4n+tr'		xvrst
+				'0.4n+tr+tEn'		xvrst
+				'0.4n+tr+tEn+tf'	xvdr)''' %(r, r, r, r))

    

# now setting the weights
for b in range(0, 32):
    globals()['firstlayer_weights_{}'.format(b)] = np.loadtxt('/home/laveriteforme2000/data/extracted_binary_weights/weight_submatrices/firstlayer_weights_'+str(b)+'.csv', delimiter=',', dtype=np.int)    
    globals()['fOUT_w_{}'.format(b)] = open("./SPICE_Codes/MLP_1stlayer_weights/firstlayer_weights_"+str(b)+".sp", "w")
    rows = len(globals()['firstlayer_weights_{}'.format(b)])
    for r_w in range(0, rows):
        cols = len(globals()['firstlayer_weights_{}'.format(b)][r_w])
        for c_w in range(0, cols):
            if 1 == globals()['firstlayer_weights_{}'.format(b)][r_w][c_w]:
                globals()['fOUT_w_{}'.format(b)].write('''
.ic v(xi%d.xi%d.q)=xvdd \t v(xi%d.xi%d.qb)=xvss \n''' %(r_w, c_w, r_w, c_w))
            else:
                globals()['fOUT_w_{}'.format(b)].write('''
.ic v(xi%d.xi%d.q)=xvss \t v(xi%d.xi%d.qb)=xvdd \n''' %(r_w, c_w, r_w, c_w))
