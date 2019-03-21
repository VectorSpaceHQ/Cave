EESchema Schematic File Version 4
LIBS:cave-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R_PHOTO R1
U 1 1 5C52D602
P 7400 4300
F 0 "R1" H 7470 4346 50  0000 L CNN
F 1 "R_PHOTO" H 7470 4255 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 7450 4050 50  0001 L CNN
F 3 "~" H 7400 4250 50  0001 C CNN
	1    7400 4300
	1    0    0    -1  
$EndComp
$Comp
L Device:LED_RCBG D2
U 1 1 5C52D7AD
P 5800 5900
F 0 "D2" H 5800 5433 50  0000 C CNN
F 1 "LED_RCBG" H 5800 5524 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm-4_RGB_Staggered_Pins" H 5800 5850 50  0001 C CNN
F 3 "~" H 5800 5850 50  0001 C CNN
	1    5800 5900
	-1   0    0    1   
$EndComp
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 5C52DF81
P 3950 5350
F 0 "J1" H 3950 6828 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 3750 6700 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical" H 3950 5350 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 3950 5350 50  0001 C CNN
	1    3950 5350
	1    0    0    -1  
$EndComp
$Comp
L Regulator_Switching:LM2576S-5 U1
U 1 1 5C52F079
P 1550 4700
F 0 "U1" V 1504 4930 50  0000 L CNN
F 1 "LM2576S-5" V 1595 4930 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-5_Vertical" H 1550 4450 50  0001 L CIN
F 3 "http://www.ti.com/lit/ds/symlink/lm2576.pdf" H 1550 4700 50  0001 C CNN
	1    1550 4700
	0    1    1    0   
$EndComp
Wire Wire Line
	1650 3850 1800 3850
Wire Wire Line
	1800 3850 1800 3650
Wire Wire Line
	1250 4700 1200 4700
$Comp
L power:+24V #PWR01
U 1 1 5C52F30E
P 1500 2750
F 0 "#PWR01" H 1500 2600 50  0001 C CNN
F 1 "+24V" H 1515 2923 50  0000 C CNN
F 2 "" H 1500 2750 50  0001 C CNN
F 3 "" H 1500 2750 50  0001 C CNN
	1    1500 2750
	1    0    0    -1  
$EndComp
$Comp
L power:-24V #PWR02
U 1 1 5C52F37C
P 1500 3600
F 0 "#PWR02" H 1500 3700 50  0001 C CNN
F 1 "-24V" H 1515 3773 50  0000 C CNN
F 2 "" H 1500 3600 50  0001 C CNN
F 3 "" H 1500 3600 50  0001 C CNN
	1    1500 3600
	-1   0    0    1   
$EndComp
Wire Wire Line
	1650 3850 1650 4050
Wire Wire Line
	2550 5350 2550 4050
Wire Wire Line
	2550 4050 3050 4050
$Comp
L Sensor_Temperature:DS18B20 U2
U 1 1 5C52FCA2
P 7400 3250
F 0 "U2" V 7033 3250 50  0000 C CNN
F 1 "DS18B20" V 7124 3250 50  0000 C CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 6400 3000 50  0001 C CNN
F 3 "http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf" H 7250 3500 50  0001 C CNN
	1    7400 3250
	0    1    1    0   
$EndComp
Wire Wire Line
	4750 5050 6750 5050
Wire Wire Line
	6750 5050 6750 3850
Wire Wire Line
	6750 3850 7400 3850
Wire Wire Line
	7400 3850 7400 3550
Wire Wire Line
	4150 4050 4150 4000
Wire Wire Line
	4150 4000 7400 4000
Wire Wire Line
	7700 4000 7700 3250
$Comp
L Device:R_US R2
U 1 1 5C5313A3
P 7400 4600
F 0 "R2" H 7468 4646 50  0000 L CNN
F 1 "10K" H 7468 4555 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 7440 4590 50  0001 C CNN
F 3 "~" H 7400 4600 50  0001 C CNN
	1    7400 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 4150 7400 4000
Connection ~ 7400 4000
Wire Wire Line
	7400 4000 7700 4000
Wire Wire Line
	3150 5350 3000 5350
Wire Wire Line
	3000 5350 3000 3800
Wire Wire Line
	3000 3800 6050 3800
Wire Wire Line
	6050 3800 6050 4450
Wire Wire Line
	6050 4450 7400 4450
Connection ~ 7400 4450
Wire Wire Line
	5400 6100 5600 6100
Wire Wire Line
	4750 5250 5000 5250
Wire Wire Line
	4750 6150 5200 6150
Wire Wire Line
	3150 5150 2850 5150
Wire Wire Line
	3150 5250 2650 5250
Wire Wire Line
	4750 5450 4850 5450
Wire Wire Line
	5500 5450 5500 5700
Wire Wire Line
	5500 5700 5600 5700
Wire Wire Line
	5400 5900 5400 5550
Wire Wire Line
	5400 5550 5150 5550
Wire Wire Line
	5400 5900 5600 5900
Wire Wire Line
	4750 6050 4850 6050
Wire Wire Line
	5400 6050 5400 6100
$Comp
L power:GND #PWR0104
U 1 1 5C5444F4
P 4050 6650
F 0 "#PWR0104" H 4050 6400 50  0001 C CNN
F 1 "GND" H 4055 6477 50  0000 C CNN
F 2 "" H 4050 6650 50  0001 C CNN
F 3 "" H 4050 6650 50  0001 C CNN
	1    4050 6650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 5C544584
P 7100 3250
F 0 "#PWR0105" H 7100 3000 50  0001 C CNN
F 1 "GND" H 7105 3077 50  0000 C CNN
F 2 "" H 7100 3250 50  0001 C CNN
F 3 "" H 7100 3250 50  0001 C CNN
	1    7100 3250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5C5445D2
P 7400 4750
F 0 "#PWR0106" H 7400 4500 50  0001 C CNN
F 1 "GND" H 7405 4577 50  0000 C CNN
F 2 "" H 7400 4750 50  0001 C CNN
F 3 "" H 7400 4750 50  0001 C CNN
	1    7400 4750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5C54465E
P 6000 5900
F 0 "#PWR0107" H 6000 5650 50  0001 C CNN
F 1 "GND" H 6005 5727 50  0000 C CNN
F 2 "" H 6000 5900 50  0001 C CNN
F 3 "" H 6000 5900 50  0001 C CNN
	1    6000 5900
	1    0    0    -1  
$EndComp
$Comp
L Amplifier_Audio:LM386 U3
U 1 1 5C6E9B1D
P 9350 5050
F 0 "U3" H 9650 4950 50  0000 L CNN
F 1 "LM386" H 9550 4850 50  0000 L CNN
F 2 "Package_DIP:DIP-8_W7.62mm" H 9450 5150 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm386.pdf" H 9550 5250 50  0001 C CNN
	1    9350 5050
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C2
U 1 1 5C6E9ED0
P 9450 5500
F 0 "C2" H 9332 5454 50  0000 R CNN
F 1 "10uF" H 9332 5545 50  0000 R CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 9488 5350 50  0001 C CNN
F 3 "~" H 9450 5500 50  0001 C CNN
	1    9450 5500
	-1   0    0    1   
$EndComp
Wire Wire Line
	9450 5650 9350 5650
Wire Wire Line
	9350 5650 9350 5350
Wire Wire Line
	9050 5150 9050 5350
Wire Wire Line
	9050 5350 9250 5350
Wire Wire Line
	9050 4950 8800 4950
$Comp
L Device:R_POT_US RV1
U 1 1 5C6ECA44
P 8650 4950
F 0 "RV1" H 8582 4996 50  0000 R CNN
F 1 "10K" H 8582 4905 50  0000 R CNN
F 2 "Potentiometer_THT:Potentiometer_ACP_CA14-H2,5_Horizontal" H 8650 4950 50  0001 C CNN
F 3 "~" H 8650 4950 50  0001 C CNN
	1    8650 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	9050 5150 8650 5150
Wire Wire Line
	8650 5150 8650 5100
Connection ~ 9050 5150
$Comp
L Device:C C1
U 1 1 5C6ED881
P 8650 4650
F 0 "C1" H 8765 4696 50  0000 L CNN
F 1 "0.1uF" H 8765 4605 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" H 8688 4500 50  0001 C CNN
F 3 "~" H 8650 4650 50  0001 C CNN
	1    8650 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	8650 4500 8450 4500
$Comp
L Device:Microphone MK1
U 1 1 5C6EEBCD
P 8250 4700
F 0 "MK1" H 8380 4746 50  0000 L CNN
F 1 "Microphone" H 8380 4655 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" V 8250 4800 50  0001 C CNN
F 3 "~" V 8250 4800 50  0001 C CNN
	1    8250 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	8650 5150 8250 5150
Wire Wire Line
	8250 5150 8250 4900
Connection ~ 8650 5150
$Comp
L Device:R_US R3
U 1 1 5C6EFCC7
P 8450 4350
F 0 "R3" H 8518 4396 50  0000 L CNN
F 1 "1K" H 8518 4305 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 8490 4340 50  0001 C CNN
F 3 "~" H 8450 4350 50  0001 C CNN
	1    8450 4350
	1    0    0    -1  
$EndComp
Connection ~ 8450 4500
Wire Wire Line
	8450 4500 8250 4500
$Comp
L power:+5V #PWR03
U 1 1 5C6EFE35
P 8450 4200
F 0 "#PWR03" H 8450 4050 50  0001 C CNN
F 1 "+5V" H 8465 4373 50  0000 C CNN
F 2 "" H 8450 4200 50  0001 C CNN
F 3 "" H 8450 4200 50  0001 C CNN
	1    8450 4200
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5C6F019C
P 8900 800
F 0 "#FLG01" H 8900 875 50  0001 C CNN
F 1 "PWR_FLAG" H 8900 974 50  0000 C CNN
F 2 "" H 8900 800 50  0001 C CNN
F 3 "~" H 8900 800 50  0001 C CNN
	1    8900 800 
	1    0    0    -1  
$EndComp
Wire Wire Line
	8450 4200 9250 4200
Wire Wire Line
	9250 4200 9250 4750
Connection ~ 8450 4200
$Comp
L Device:CP C3
U 1 1 5C6F1C38
P 9500 4750
F 0 "C3" V 9755 4750 50  0000 C CNN
F 1 "10uF" V 9664 4750 50  0000 C CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 9538 4600 50  0001 C CNN
F 3 "~" H 9500 4750 50  0001 C CNN
	1    9500 4750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	9650 4750 9800 4750
Wire Wire Line
	9800 4750 9800 5650
Wire Wire Line
	9800 5650 9450 5650
Connection ~ 9450 5650
$Comp
L Device:CP C5
U 1 1 5C6F40B1
P 10250 5050
F 0 "C5" V 10505 5050 50  0000 C CNN
F 1 "100uF" V 10414 5050 50  0000 C CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 10288 4900 50  0001 C CNN
F 3 "~" H 10250 5050 50  0001 C CNN
	1    10250 5050
	0    -1   -1   0   
$EndComp
$Comp
L Device:C C4
U 1 1 5C6F4CC8
P 9950 5200
F 0 "C4" H 10065 5246 50  0000 L CNN
F 1 "0.047uF" H 10065 5155 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D3.0mm_W1.6mm_P2.50mm" H 9988 5050 50  0001 C CNN
F 3 "~" H 9950 5200 50  0001 C CNN
	1    9950 5200
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R4
U 1 1 5C6F4D42
P 9950 5500
F 0 "R4" H 10018 5546 50  0000 L CNN
F 1 "10" H 10018 5455 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 9990 5490 50  0001 C CNN
F 3 "~" H 9950 5500 50  0001 C CNN
	1    9950 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	9950 5650 9800 5650
Connection ~ 9800 5650
Wire Wire Line
	9650 5050 9950 5050
Wire Wire Line
	10100 5050 9950 5050
Connection ~ 9950 5050
Text Label 3150 5550 2    50   ~ 0
MicInput
Text Label 10400 5050 0    50   ~ 0
MicInput
$Comp
L power:PWR_FLAG #FLG03
U 1 1 5C7007EA
P 8350 800
F 0 "#FLG03" H 8350 875 50  0001 C CNN
F 1 "PWR_FLAG" H 8350 974 50  0000 C CNN
F 2 "" H 8350 800 50  0001 C CNN
F 3 "~" H 8350 800 50  0001 C CNN
	1    8350 800 
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR08
U 1 1 5C700834
P 8350 800
F 0 "#PWR08" H 8350 550 50  0001 C CNN
F 1 "GND" H 8355 627 50  0000 C CNN
F 2 "" H 8350 800 50  0001 C CNN
F 3 "" H 8350 800 50  0001 C CNN
	1    8350 800 
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x03_Male J2
U 1 1 5C70565E
P 2350 6050
F 0 "J2" H 2322 5980 50  0000 R CNN
F 1 "PIRsensor" H 2322 6071 50  0000 R CNN
F 2 "Connector_JST:JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical" H 2350 6050 50  0001 C CNN
F 3 "~" H 2350 6050 50  0001 C CNN
	1    2350 6050
	-1   0    0    1   
$EndComp
$Comp
L power:+5V #PWR05
U 1 1 5C70655E
P 2150 5950
F 0 "#PWR05" H 2150 5800 50  0001 C CNN
F 1 "+5V" V 2165 6078 50  0000 L CNN
F 2 "" H 2150 5950 50  0001 C CNN
F 3 "" H 2150 5950 50  0001 C CNN
	1    2150 5950
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR06
U 1 1 5C70662E
P 2150 6150
F 0 "#PWR06" H 2150 5900 50  0001 C CNN
F 1 "GND" V 2155 6022 50  0000 R CNN
F 2 "" H 2150 6150 50  0001 C CNN
F 3 "" H 2150 6150 50  0001 C CNN
	1    2150 6150
	0    1    1    0   
$EndComp
Text Label 2150 6050 2    50   ~ 0
PIR
Text Label 3150 5650 2    50   ~ 0
PIR
$Comp
L power:+24V #PWR09
U 1 1 5C70C9FD
P 9800 800
F 0 "#PWR09" H 9800 650 50  0001 C CNN
F 1 "+24V" H 9815 973 50  0000 C CNN
F 2 "" H 9800 800 50  0001 C CNN
F 3 "" H 9800 800 50  0001 C CNN
	1    9800 800 
	-1   0    0    1   
$EndComp
$Comp
L power:PWR_FLAG #FLG04
U 1 1 5C70D4A5
P 9800 800
F 0 "#FLG04" H 9800 875 50  0001 C CNN
F 1 "PWR_FLAG" H 9800 974 50  0000 C CNN
F 2 "" H 9800 800 50  0001 C CNN
F 3 "~" H 9800 800 50  0001 C CNN
	1    9800 800 
	1    0    0    -1  
$EndComp
$Comp
L power:-24V #PWR07
U 1 1 5C70D5A2
P 7900 800
F 0 "#PWR07" H 7900 900 50  0001 C CNN
F 1 "-24V" H 7915 973 50  0000 C CNN
F 2 "" H 7900 800 50  0001 C CNN
F 3 "" H 7900 800 50  0001 C CNN
	1    7900 800 
	-1   0    0    1   
$EndComp
$Comp
L power:PWR_FLAG #FLG02
U 1 1 5C70D69F
P 7900 800
F 0 "#FLG02" H 7900 875 50  0001 C CNN
F 1 "PWR_FLAG" H 7900 974 50  0000 C CNN
F 2 "" H 7900 800 50  0001 C CNN
F 3 "~" H 7900 800 50  0001 C CNN
	1    7900 800 
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0109
U 1 1 5C7105F9
P 9050 5350
F 0 "#PWR0109" H 9050 5100 50  0001 C CNN
F 1 "GND" H 9055 5177 50  0000 C CNN
F 2 "" H 9050 5350 50  0001 C CNN
F 3 "" H 9050 5350 50  0001 C CNN
	1    9050 5350
	1    0    0    -1  
$EndComp
Connection ~ 9050 5350
NoConn ~ 3150 5750
NoConn ~ 3150 5850
NoConn ~ 3150 5950
NoConn ~ 3150 6050
NoConn ~ 3650 6650
NoConn ~ 3750 6650
NoConn ~ 3850 6650
NoConn ~ 3950 6650
NoConn ~ 4150 6650
NoConn ~ 4250 6650
NoConn ~ 4750 5850
NoConn ~ 4750 5750
NoConn ~ 4750 5650
NoConn ~ 4750 5150
NoConn ~ 4750 4850
NoConn ~ 4750 4750
NoConn ~ 4750 4550
NoConn ~ 4750 4450
NoConn ~ 4050 4050
NoConn ~ 3850 4050
NoConn ~ 3150 4450
NoConn ~ 3150 4550
NoConn ~ 3150 4750
NoConn ~ 3150 4850
NoConn ~ 3150 4950
$Comp
L power:GND #PWR0110
U 1 1 5C73DE4D
P 1200 5650
F 0 "#PWR0110" H 1200 5400 50  0001 C CNN
F 1 "GND" H 1205 5477 50  0000 C CNN
F 2 "" H 1200 5650 50  0001 C CNN
F 3 "" H 1200 5650 50  0001 C CNN
	1    1200 5650
	1    0    0    -1  
$EndComp
Connection ~ 1200 4700
NoConn ~ 3550 6650
$Comp
L power:+3V3 #PWR0111
U 1 1 5C7434A9
P 4150 3700
F 0 "#PWR0111" H 4150 3550 50  0001 C CNN
F 1 "+3V3" H 4300 3800 50  0000 C CNN
F 2 "" H 4150 3700 50  0001 C CNN
F 3 "" H 4150 3700 50  0001 C CNN
	1    4150 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 4000 4150 3700
Connection ~ 4150 4000
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5C747E06
P 9350 800
F 0 "#FLG0101" H 9350 875 50  0001 C CNN
F 1 "PWR_FLAG" H 9350 974 50  0000 C CNN
F 2 "" H 9350 800 50  0001 C CNN
F 3 "~" H 9350 800 50  0001 C CNN
	1    9350 800 
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0112
U 1 1 5C74A1AE
P 9350 800
F 0 "#PWR0112" H 9350 650 50  0001 C CNN
F 1 "+5V" H 9365 973 50  0000 C CNN
F 2 "" H 9350 800 50  0001 C CNN
F 3 "" H 9350 800 50  0001 C CNN
	1    9350 800 
	-1   0    0    1   
$EndComp
$Comp
L power:+3.3V #PWR0113
U 1 1 5C74A27E
P 8900 800
F 0 "#PWR0113" H 8900 650 50  0001 C CNN
F 1 "+3.3V" H 8915 973 50  0000 C CNN
F 2 "" H 8900 800 50  0001 C CNN
F 3 "" H 8900 800 50  0001 C CNN
	1    8900 800 
	-1   0    0    1   
$EndComp
$Comp
L power:+24V #PWR0114
U 1 1 5C74BA40
P 1800 3650
F 0 "#PWR0114" H 1800 3500 50  0001 C CNN
F 1 "+24V" H 1815 3823 50  0000 C CNN
F 2 "" H 1800 3650 50  0001 C CNN
F 3 "" H 1800 3650 50  0001 C CNN
	1    1800 3650
	0    1    1    0   
$EndComp
Connection ~ 1800 3650
$Comp
L Connector_Generic:Conn_01x02 J3
U 1 1 5C8A9888
P 950 2850
F 0 "J3" H 870 2525 50  0000 C CNN
F 1 "PWR" H 870 2616 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 950 2850 50  0001 C CNN
F 3 "~" H 950 2850 50  0001 C CNN
	1    950  2850
	-1   0    0    1   
$EndComp
Wire Wire Line
	1500 2750 1150 2750
Wire Wire Line
	1150 2850 1150 3350
Wire Wire Line
	3450 3100 3450 3550
Wire Wire Line
	3450 3550 5200 3550
Wire Wire Line
	5200 3550 5200 6150
Wire Wire Line
	3250 3100 3250 3700
Wire Wire Line
	3250 3700 2850 3700
Wire Wire Line
	2850 3700 2850 5150
Wire Wire Line
	3150 3100 3150 3600
Wire Wire Line
	3150 3600 2650 3600
Wire Wire Line
	2650 3600 2650 5250
$Comp
L power:GND #PWR0101
U 1 1 5C8BEC79
P 3550 3100
F 0 "#PWR0101" H 3550 2850 50  0001 C CNN
F 1 "GND" H 3700 3000 50  0000 C CNN
F 2 "" H 3550 3100 50  0001 C CNN
F 3 "" H 3550 3100 50  0001 C CNN
	1    3550 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 3750 3350 3750
Wire Wire Line
	3350 3100 3350 3750
Wire Wire Line
	5000 3750 5000 5250
$Comp
L Connector:Conn_01x06_Male J4
U 1 1 5C8CB942
P 3350 2900
F 0 "J4" V 3410 3140 50  0000 L CNN
F 1 "RelayOutput" V 3501 3140 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 3350 2900 50  0001 C CNN
F 3 "~" H 3350 2900 50  0001 C CNN
	1    3350 2900
	0    1    1    0   
$EndComp
Wire Wire Line
	3050 4050 3050 3250
Connection ~ 3050 4050
Wire Wire Line
	3050 4050 3750 4050
$Comp
L Device:R_US R5
U 1 1 5C8D432C
P 5000 5450
F 0 "R5" H 5068 5496 50  0000 L CNN
F 1 "220" H 5068 5405 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5040 5440 50  0001 C CNN
F 3 "~" H 5000 5450 50  0001 C CNN
	1    5000 5450
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_US R6
U 1 1 5C8D5F7F
P 5000 5550
F 0 "R6" H 5068 5596 50  0000 L CNN
F 1 "220" H 5068 5505 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5040 5540 50  0001 C CNN
F 3 "~" H 5000 5550 50  0001 C CNN
	1    5000 5550
	0    1    1    0   
$EndComp
$Comp
L Device:R_US R7
U 1 1 5C8D5FC9
P 5000 6050
F 0 "R7" H 5068 6096 50  0000 L CNN
F 1 "220" H 5068 6005 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5040 6040 50  0001 C CNN
F 3 "~" H 5000 6050 50  0001 C CNN
	1    5000 6050
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5150 5450 5500 5450
Wire Wire Line
	4850 5550 4750 5550
Wire Wire Line
	5150 6050 5400 6050
$Comp
L Device:CP C6
U 1 1 5C8D8799
P 1400 4050
F 0 "C6" V 1145 4050 50  0000 C CNN
F 1 "100uF" V 1236 4050 50  0000 C CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 1438 3900 50  0001 C CNN
F 3 "~" H 1400 4050 50  0001 C CNN
	1    1400 4050
	0    1    1    0   
$EndComp
Wire Wire Line
	1550 4050 1650 4050
Connection ~ 1650 4050
Wire Wire Line
	1650 4050 1650 4200
Wire Wire Line
	1250 4050 1200 4050
Connection ~ 1200 4050
Wire Wire Line
	1200 4050 1200 4200
Wire Wire Line
	1450 4200 1200 4200
Connection ~ 1200 4200
Wire Wire Line
	1200 4200 1200 4700
$Comp
L Device:L L1
U 1 1 5C8DFE03
P 1950 5350
F 0 "L1" V 1772 5350 50  0000 C CNN
F 1 "100uH" V 1863 5350 50  0000 C CNN
F 2 "Inductor_THT:L_Axial_L5.3mm_D2.2mm_P7.62mm_Horizontal_Vishay_IM-1" H 1950 5350 50  0001 C CNN
F 3 "~" H 1950 5350 50  0001 C CNN
	1    1950 5350
	0    1    1    0   
$EndComp
Wire Wire Line
	2100 5350 2200 5350
Wire Wire Line
	1500 5350 1800 5350
Wire Wire Line
	1450 5200 1500 5200
Wire Wire Line
	1500 5200 1500 5350
$Comp
L Device:D_Schottky D3
U 1 1 5C8E5583
P 1500 5500
F 0 "D3" H 1350 5300 50  0000 C CNN
F 1 "D_Schottky" H 1400 5400 50  0000 C CNN
F 2 "Diode_THT:D_A-405_P7.62mm_Horizontal" H 1500 5500 50  0001 C CNN
F 3 "~" H 1500 5500 50  0001 C CNN
	1    1500 5500
	0    1    1    0   
$EndComp
Connection ~ 1500 5350
$Comp
L Device:CP C7
U 1 1 5C8E5F9D
P 2200 5500
F 0 "C7" H 2318 5546 50  0000 L CNN
F 1 "1000uF" H 2318 5455 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D7.5mm_P2.50mm" H 2238 5350 50  0001 C CNN
F 3 "~" H 2200 5500 50  0001 C CNN
	1    2200 5500
	1    0    0    -1  
$EndComp
Connection ~ 2200 5350
Wire Wire Line
	2200 5350 2550 5350
Wire Wire Line
	2200 5650 1500 5650
Connection ~ 1200 5650
Connection ~ 1500 5650
Wire Wire Line
	1500 5650 1200 5650
Wire Wire Line
	1200 4700 1200 5650
Wire Wire Line
	1650 5200 2200 5200
Wire Wire Line
	2200 5200 2200 5350
$Comp
L power:+5V #PWR0102
U 1 1 5C8F27C8
P 3050 3250
F 0 "#PWR0102" H 3050 3100 50  0001 C CNN
F 1 "+5V" H 3065 3423 50  0000 C CNN
F 2 "" H 3050 3250 50  0001 C CNN
F 3 "" H 3050 3250 50  0001 C CNN
	1    3050 3250
	0    -1   -1   0   
$EndComp
Connection ~ 3050 3250
Wire Wire Line
	3050 3250 3050 3100
$Comp
L Device:D_Small D1
U 1 1 5C9239F7
P 1400 3100
F 0 "D1" H 1400 2895 50  0000 C CNN
F 1 "D_Small" H 1400 2986 50  0000 C CNN
F 2 "Diode_THT:D_A-405_P7.62mm_Horizontal" V 1400 3100 50  0001 C CNN
F 3 "~" V 1400 3100 50  0001 C CNN
	1    1400 3100
	-1   0    0    1   
$EndComp
$Comp
L Device:D_Small D4
U 1 1 5C923AEF
P 1400 3600
F 0 "D4" H 1400 3395 50  0000 C CNN
F 1 "D_Small" H 1400 3486 50  0000 C CNN
F 2 "Diode_THT:D_A-405_P7.62mm_Horizontal" V 1400 3600 50  0001 C CNN
F 3 "~" V 1400 3600 50  0001 C CNN
	1    1400 3600
	-1   0    0    1   
$EndComp
$Comp
L Device:D_Small D6
U 1 1 5C923B3F
P 1600 3600
F 0 "D6" H 1600 3395 50  0000 C CNN
F 1 "D_Small" H 1600 3486 50  0000 C CNN
F 2 "Diode_THT:D_A-405_P7.62mm_Horizontal" V 1600 3600 50  0001 C CNN
F 3 "~" V 1600 3600 50  0001 C CNN
	1    1600 3600
	-1   0    0    1   
$EndComp
$Comp
L Device:D_Small D5
U 1 1 5C923B8D
P 1600 3100
F 0 "D5" H 1600 2895 50  0000 C CNN
F 1 "D_Small" H 1600 2986 50  0000 C CNN
F 2 "Diode_THT:D_A-405_P7.62mm_Horizontal" V 1600 3100 50  0001 C CNN
F 3 "~" V 1600 3100 50  0001 C CNN
	1    1600 3100
	-1   0    0    1   
$EndComp
Connection ~ 1500 3600
Connection ~ 1500 3100
Connection ~ 1500 2750
Wire Wire Line
	1500 2750 1500 3100
Wire Wire Line
	1150 3350 1500 3350
Wire Wire Line
	1500 3350 1500 3600
Wire Wire Line
	1300 3600 1300 3100
Wire Wire Line
	1300 3600 1200 3600
Connection ~ 1300 3600
Wire Wire Line
	1200 3600 1200 4050
Wire Wire Line
	1700 3600 1800 3600
Connection ~ 1700 3600
Wire Wire Line
	1800 3600 1800 3650
Wire Wire Line
	1700 3100 1700 3600
$EndSCHEMATC
