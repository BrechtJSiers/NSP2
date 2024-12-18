from Load_eshel_sun_data_orde_3 import orde_3
from Load_eshel_sun_data_orde_7 import orde_7
from Load_eshel_sun_data_orde_13 import orde_13
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
model_H_alpha = orde_3()
# model_Na = orde_7()
model_Mg = orde_13()

avg_opt_A_H, pcov_n_A_H, avg_opt_B_H, pcov_n_B_H = model_H_alpha.returns_H_alpha()
avg_opt_A_C, pcov_n_A_C, avg_opt_B_C, pcov_n_B_C = model_H_alpha.returns_Ca_1()
avg_opt_A_T, pcov_n_A_T, avg_opt_B_T, pcov_n_B_T = model_H_alpha.returns_Ti_1()
# avg_opt_D1_A, pcov_D1_A, avg_opt_D1_B, pcov_D1_B = model_Na.returns_D1()
# avg_opt_D2_A, pcov_D2_A, avg_opt_D2_B, pcov_D2_B = model_Na.returns_D2()
avg_opt_b1_A, pcov_b1_A, avg_opt_b1_B, pcov_b1_B = model_Mg.returns_b1()
avg_opt_b2_A, pcov_b2_A, avg_opt_b2_B, pcov_b2_B = model_Mg.returns_b2()
avg_opt_b3_A, pcov_b3_A, avg_opt_b3_B, pcov_b3_B = model_Mg.returns_b3()


R=696342000
error_R = 65000
c=299792458

def omlooptijd(min_A_g, error_A_g, min_B_g, error_B_g):
    lambda_gem = (min_A_g+min_B_g)/2
    delta_lambda = abs(lambda_gem - min_A_g)
    v = c * (delta_lambda/lambda_gem)
    T = ((2*np.pi*R)/v)/(60*60*24)
    print(f"{T} is de omlooptijd in dagen")

    error_C = ((((2*np.pi*error_R/c)*((min_A_g+min_B_g)/(min_B_g-min_A_g)))**2 +
        ((2*np.pi*R/c)*((2*min_B_g*error_A_g)/((min_A_g-min_B_g)**2)))**2 +
        ((2*np.pi*R/c)*((2*min_A_g*error_B_g)/((min_B_g-min_A_g)**2)))**2)**(1/2))/(60*60*24)
    print(f"{error_C} is de error van de omlooptijd in dagen")
    return T, error_C

T_H_alpha, T_error_H_alpha = omlooptijd(avg_opt_A_H, pcov_n_A_H, avg_opt_B_H, pcov_n_B_H)
T_Ca_1,T_error_Ca_1 = omlooptijd(avg_opt_A_C, pcov_n_A_C,avg_opt_B_C, pcov_n_B_C)
T_Ti_1, T_error_Ti_1 = omlooptijd(avg_opt_A_T, pcov_n_A_T,avg_opt_B_T, pcov_n_B_T)
# T_Na_D1, T_error_Na_D1 = omlooptijd(avg_opt_D1_A, pcov_D1_A, avg_opt_D1_B, pcov_D1_B)
# T_Na_D2, T_error_Na_D2 = omlooptijd(avg_opt_D2_A, pcov_D2_A, avg_opt_D2_B, pcov_D2_B)
T_Mg_b1, T_error_Mg_b1 = omlooptijd(avg_opt_b1_A, pcov_b1_A, avg_opt_b1_B, pcov_b1_B)
T_Mg_b2, T_error_Mg_b2 = omlooptijd(avg_opt_b2_A, pcov_b2_A, avg_opt_b2_B, pcov_b2_B)
T_Mg_b3, T_error_Mg_b3 = omlooptijd(avg_opt_b3_A, pcov_b3_A, avg_opt_b3_B, pcov_b3_B)

all_periods = [T_H_alpha, T_Ca_1, T_Ti_1,  T_Mg_b1, T_Mg_b2, T_Mg_b3] #T_Na_D1, T_Na_D2,
all_periods_name = ['H-alpha (6562.81)', 'Ca_1 (6717.687)', 'Ti_1(6678.576)', 'Mg b1 (5183.62)', 'Mg b2 (5172.70)', 'Mg b3 (5168.91)'] # 'Na D1 (5895.92)', 'Na D2 (5889.95)',
all_errors_periods = [T_error_H_alpha, T_error_Ca_1, T_error_Ti_1, T_error_Mg_b1, T_error_Mg_b2, T_error_Mg_b3] #T_error_Na_D1, T_error_Na_D2,
number_of_lines = [1, 2, 3, 4,5,6] #  5, 6

    
line_list = []
error_line = []
def straight_line(x, p):
    return p 


popt_s, pcov_s = curve_fit(straight_line, number_of_lines, all_periods, p0=[25], sigma=all_errors_periods)
print(popt_s[0], pcov_s)
for i in range(len(number_of_lines)):
    line_list.append(popt_s[0])
    error_line.append(pcov_s[0][0])



plt.ylabel("Omlooptijd (dagen)")
plt.errorbar(all_periods_name, all_periods, yerr=all_errors_periods, fmt='o', ecolor='red', capsize=3, label='Rotationperiods with errorbars')
# plt.scatter(all_periods_name, all_periods, c='blue')
# plt.plot(all_periods_name, omlooptijd_fit)
# plt.errorbar(all_periods_name, line_list, yerr=error_line, fmt='-', label='Gemiddelde omlooptijd')
plt.axhline(popt_s[0], color='black', linestyle='-', linewidth=1, label = 'Average rotation period')
plt.axhline(popt_s[0]+pcov_s[0][0], color='gray', linestyle='--', linewidth=1, label = 'Error average rotation period')
plt.axhline(popt_s[0]-pcov_s[0][0], color='gray', linestyle='--', linewidth=1)
plt.ylabel('Omlooptijd equator (dagen)')
plt.xlabel('Wavelength absorptionlines (Angstrom)')
plt.legend()
plt.show()

print(f"De gemiddelde omlooptijd is {popt_s[0]} dagen met een error van {pcov_s[0][0]}")