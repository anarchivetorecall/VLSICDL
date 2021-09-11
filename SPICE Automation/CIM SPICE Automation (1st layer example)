import numpy as np
import os
import sys


# setting codes for measuring the output MBL voltage
for i in range(0, 32):
    globals()['layer1_cycle{}'.format(i)] = open("/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/measSPICEcodes/meas_layer1_cycle"+str(i)+".sp", "w")
    for j in range(0, 64):
        globals()['layer1_cycle{}'.format(i)].write(".meas TRAN  layer1_cycle"+str(i)+"_col%d	 FIND	 v(MBL_%d)	 AT=25n \n" %(j, j))
    globals()['layer1_cycle{}'.format(i)].close()


# setting SPICE codes for each cycle
for a in range(0, 32, 4):
    globals()['cycle{}'.format(a)] = open("/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_0_x_firstlayer_weights_"+str(a)+".sp", "w")
    globals()['cycle{}'.format(a)].write('''
.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/hspiceD/schematic/netlist/input.ckt"
.include "/home/laveriteforme2000/virtuoso/test/7nm_TT.model"

.param tEn = 20n 
.param tr = 0.5n
.param tf = 0.5n

.param xvdd = 1.0
.param xvss = 0
.param xvdr = 0.8
.param xvrst = 0.4

vdd vdd gnd xvdd
vss vss gnd xvss
$ fundamentals: supply voltage & ground


vrst_mbl	rst_mbl	0	pwl	(0			xvss
+				0.5n			xvss
+				'0.5n+tr'		xvdd
+				'0.5n+tr+tEn'		xvdd
+				'0.5n+tr+tEn+tf'	xvss)
$ RST signal for precharging MBL

vrst rst gnd xvrst

vpch_bl	pch_bl	gnd	xvdd
$ PCH_BL for precharging BL (Useless for implementing simulation)


.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/wl_voltage_set.sp"
$ WL voltage setting (Useless for implementing simulation)


.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_weights/firstlayer_weights_'''+str(a)+'''.sp"
$ setting weight set

.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_inputs/firstlayer_inputs_0.sp"
$ setting input set

.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/measSPICEcodes/meas_layer1_cycle'''+str(a)+'''.sp"
$ including .MEAS codes

.tran .5n 30n
.option post

.end''')
    globals()['cycle{}'.format(a)].close()

for b in range(1, 32, 4):
    globals()['cycle{}'.format(b)] = open("/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_1_x_firstlayer_weights_"+str(b)+".sp", "w")
    globals()['cycle{}'.format(b)].write('''
.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/hspiceD/schematic/netlist/input.ckt"
.include "/home/laveriteforme2000/virtuoso/test/7nm_TT.model"

.param tEn = 20n 
.param tr = 0.5n
.param tf = 0.5n

.param xvdd = 1.0
.param xvss = 0
.param xvdr = 0.8
.param xvrst = 0.4

vdd vdd gnd xvdd
vss vss gnd xvss
$ fundamentals: supply voltage & ground


vrst_mbl	rst_mbl	0	pwl	(0			xvss
+				0.5n			xvss
+				'0.5n+tr'		xvdd
+				'0.5n+tr+tEn'		xvdd
+				'0.5n+tr+tEn+tf'	xvss)
$ RST signal for precharging MBL

vrst rst gnd xvrst

vpch_bl	pch_bl	gnd	xvdd
$ PCH_BL for precharging BL (Useless for implementing simulation)


.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/wl_voltage_set.sp"
$ WL voltage setting (Useless for implementing simulation)


.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_weights/firstlayer_weights_'''+str(b)+'''.sp"
$ setting weight set

.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_inputs/firstlayer_inputs_1.sp"
$ setting input set

.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/measSPICEcodes/meas_layer1_cycle'''+str(b)+'''.sp"
$ including .MEAS codes

.tran .5n 30n
.option post

.end''')
    globals()['cycle{}'.format(b)].close()

for c in range(2, 32, 4):
    globals()['cycle{}'.format(c)] = open("/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_2_x_firstlayer_weights_"+str(c)+".sp", "w")
    globals()['cycle{}'.format(c)].write('''
.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/hspiceD/schematic/netlist/input.ckt"
.include "/home/laveriteforme2000/virtuoso/test/7nm_TT.model"

.param tEn = 20n 
.param tr = 0.5n
.param tf = 0.5n

.param xvdd = 1.0
.param xvss = 0
.param xvdr = 0.8
.param xvrst = 0.4

vdd vdd gnd xvdd
vss vss gnd xvss
$ fundamentals: supply voltage & ground


vrst_mbl	rst_mbl	0	pwl	(0			xvss
+				0.5n			xvss
+				'0.5n+tr'		xvdd
+				'0.5n+tr+tEn'		xvdd
+				'0.5n+tr+tEn+tf'	xvss)
$ RST signal for precharging MBL

vrst rst gnd xvrst

vpch_bl	pch_bl	gnd	xvdd
$ PCH_BL for precharging BL (Useless for implementing simulation)


.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/wl_voltage_set.sp"
$ WL voltage setting (Useless for implementing simulation)


.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_weights/firstlayer_weights_'''+str(c)+'''.sp"
$ setting weight set

.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_inputs/firstlayer_inputs_2.sp"
$ setting input set

.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/measSPICEcodes/meas_layer1_cycle'''+str(c)+'''.sp"
$ including .MEAS codes

.tran .5n 30n
.option post

.end''')
    globals()['cycle{}'.format(c)].close()

for d in range(3, 32, 4):
    globals()['cycle{}'.format(d)] = open("/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_3_x_firstlayer_weights_"+str(d)+".sp", "w")
    globals()['cycle{}'.format(d)].write('''
.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/hspiceD/schematic/netlist/input.ckt"
.include "/home/laveriteforme2000/virtuoso/test/7nm_TT.model"

.param tEn = 20n 
.param tr = 0.5n
.param tf = 0.5n

.param xvdd = 1.0
.param xvss = 0
.param xvdr = 0.8
.param xvrst = 0.4

vdd vdd gnd xvdd
vss vss gnd xvss
$ fundamentals: supply voltage & ground


vrst_mbl	rst_mbl	0	pwl	(0			xvss
+				0.5n			xvss
+				'0.5n+tr'		xvdd
+				'0.5n+tr+tEn'		xvdd
+				'0.5n+tr+tEn+tf'	xvss)
$ RST signal for precharging MBL

vrst rst gnd xvrst

vpch_bl	pch_bl	gnd	xvdd
$ PCH_BL for precharging BL (Useless for implementing simulation)


.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/wl_voltage_set.sp"
$ WL voltage setting (Useless for implementing simulation)


.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_weights/firstlayer_weights_'''+str(d)+'''.sp"
$ setting weight set

.include "/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/SPICE_Codes/MLP_1stlayer_inputs/firstlayer_inputs_3.sp"
$ setting input set

.include "/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/measSPICEcodes/meas_layer1_cycle'''+str(d)+'''.sp"
$ including .MEAS codes

.tran .5n 30n
.option post

.end''')
    globals()['cycle{}'.format(d)].close()
    
    
# automatically starts the simulation from now
for inputs0 in range(0, 32, 4):
    os.system("runHspice /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_0_x_firstlayer_weights_"+str(inputs0)+".sp")
    
for inputs1 in range(1, 32, 4):
    os.system("runHspice /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_1_x_firstlayer_weights_"+str(inputs1)+".sp")
    
for inputs2 in range(2, 32, 4):
    os.system("runHspice /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_2_x_firstlayer_weights_"+str(inputs2)+".sp")
    
for inputs3 in range(3, 32, 4):
    os.system("runHspice /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1/firstlayer_inputs_3_x_firstlayer_weights_"+str(inputs3)+".sp")
