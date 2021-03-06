import numpy as np
import argparse
import os
import sys

parser = argparse.ArgumentParser(description= 'Acquiring HW inference accuracy')
parser.add_argument('--i', type = int, help= 'the number of test set iteration')
args = parser.parse_args()

num_iter = 1
exp_iter = args.i


# First simulation is needed.
os.system("python3.8 Layer1_inputs_weights_settings.py")
os.system("python3.8 Layer1_SPICE_Automation.py")
os.system("python3.8 /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1_Analysis.py")
os.system("python3.8 Layer2_inputs_weights_settings.py")
os.system("python3.8 Layer2_SPICE_Automation.py")
os.system("python3.8 /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer2_Analysis.py")
os.system("python3.8 Layer3_inputs_weights_settings.py")
os.system("python3.8 Layer3_SPICE_Automation.py")
os.system("python3.8 /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer3_Analysis.py")
os.system("python3.8 LayerOut_inputs_weights_settings.py")
os.system("python3.8 LayerOut_SPICE_Automation.py")
os.system("python3.8 -n 0 /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/LayerOut_Analysis.py")
print("-------------------------------------------------------------------------------------------------------------------------------------------")
print("Simulation for test_input [0] is finished")
print("-------------------------------------------------------------------------------------------------------------------------------------------")

ideal_label = np.loadtxt("/home/laveriteforme2000/data/mnist_test.csv", dtype = np.int).reshape(-1, 1)

# Iteration for obtaining HW inference accuracy starts from now
while True:
        
    with open("/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/Layer1_inputs_weights_settings.py", "r") as Layer1_xw:
        old1 = Layer1_xw.read()
    replace1 = old1.replace("test_binaryinput["+str(num_iter-1)+"]", "test_binaryinput["+str(num_iter)+"]")
    with open("/home/laveriteforme2000/deepneuralnetwork/C3SRAM_SPICE_Automation/Layer1_inputs_weights_settings.py", "w") as newLayer1_xw:
        newLayer1_xw.write(replace1)
    print("\n Layer1 Inputs & Weights Setting Update for iteration number"+str(num_iter)+" is Finished \n")
    os.system("python3.8 Layer1_SPICE_Automation.py")
    os.system("python3.8 /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer1_Analysis.py")
    os.system("python3.8 Layer2_inputs_weights_settings.py")
    os.system("python3.8 Layer2_SPICE_Automation.py")
    os.system("python3.8 /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer2_Analysis.py")
    os.system("python3.8 Layer3_inputs_weights_settings.py")
    os.system("python3.8 Layer3_SPICE_Automation.py")
    os.system("python3.8 /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/Layer3_Analysis.py")
    os.system("python3.8 LayerOut_inputs_weights_settings.py")
    os.system("python3.8 LayerOut_SPICE_Automation.py")
    os.system("python3.8 -n "+str(num_iter)+" /home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/LayerOut_Analysis.py")
    print("\n -------------------------------------------------------------------------------------------------------------------------------------------")
    print("Simulation for test_input ["+str(num_iter)+"] is finished")
    print("------------------------------------------------------------------------------------------------------------------------------------------- \n")
           
    num_iter += 1
    if num_iter == exp_iter:
        break
    
TF_table = np.loadtxt("/home/laveriteforme2000/simulation/7nm_C3SRAM_256x64/MLP_SPICE_Simulation/accuracy_tf.csv", dtype = np.int, delimiter= ',')
correct_sets = np.count_nonzero(TF_table)

Accuracy = (correct_sets/exp_iter) * 100

print("HW Inference Accuracy = %.2f%%" %(Accuracy))
