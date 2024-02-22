import re
import pandas as pd

def split_words_after_last_3_digits(error_code):
    pattern = r'^([A-Z0-9_-]+)\s+(.*)$'
    match = re.match(pattern, error_code)
    if match:
        errcode = match.group(1).strip()
        desc = match.group(2).strip() 
        return errcode, desc
    else:
        return None, None

error_code = """
BT_FT_ERR-001                  Unable to get dll version                         
BT_FT_ERR-002                  Unable to connect to blue core                    
BT_FT_ERR-003                  Unable to Disconnect blue core                    
BT_FT_ERR-004                  Unable to enable the device under test mode       
FT_ERR-004                     Parameter %s is deprecated and no longer in use. Do not use in this action!
BT_FT_ERR-011                  Unable to start TX                                
BT_FT_ERR-013                  Failed reading BD Address                         
BT_FT_ERR-015                  Failed during TX Test                             
BT_FT_ERR-018                  Failed during RX Test                             
BT_FT_ERR-039                  RX BER failed.                                    
BT_FT_ERR-040                  Average TX Power not within limits                
BT_FT_ERR-042                  Freq estimation not within limits. %s , Actual: %.03f Hz; High: %.03f
BT_FT_ERR-043                  Freq drift not within limits. %s , Actual: %.03f Hz; High: %.03f
BT_FT_ERR-044                  20dB BW not within limits                         
BT_FT_ERR-045                  freq drift rate not within limits                 
BT_FT_ERR-046                  delta F1 average not within limits                
BT_FT_ERR-048                  delta F2 max not within limits                    
BT_FT_ERR-049                  EDR EVM average not within limits                 
BT_FT_ERR-050                  EDR EVM peak not within limits                    
BT_FT_ERR-051                  EDR power difference not within limits. %s , Actual: %.03f dB; High: %.03f
BT_FT_ERR-052                  EDR probability EVM 99%% pass not within limits   
BT_FT_ERR-053                  EDR omegaI not within limits                      
BT_FT_ERR-054                  EDR extreme omegaO not within limits              
BT_FT_ERR-055                  EDR extreme omegaIO not within limits             
BT_FT_ERR-057                  Unable to find waveform file                      
BT_FT_ERR-072                  TX BLE Average Power not within limits. %s , Actual: %.03f dBm; High: %.03f; Low: %.03f
BT_FT_ERR-074                  BLE freq estimation not within limits. %s , Actual: %.03f Hz; High: %.03f
BT_FT_ERR-075                  BLE freq drift not within limits. %s , Actual: %.03f Hz; High: %.03f
BT_FT_ERR-076                  BLE freq drift rate not within limits             
BT_FT_ERR-077                  BLE delta F2 max not within limits                
BT_FT_ERR-078                  BLE below 185KHz F2 max not within limits         
BT_FT_ERR-079                  BLE delta F1 average not within limits            
BT_FT_ERR-081                  RX PER failed                                     
BT_FT_ERR-083                  Failed during commit BT NVM                       
BT_FT_ERR-091                  Failed to load NVM files                          
BT_FT_ERR-095                  BT NVM read PID/VID failed                        
BT_FT_ERR-249                  BT OTP read XTAL failed                           
BT_FT_ERR-096                  BT PID/VID do not match expected value            
BT_FT_ERR-097                  Failed to stop Bluetooth TX                       
BT_FT_ERR-099                  BT BD Address does not match expected value       
BT_FT_ERR-105                  BT temperature measurement failure                
BT_FT_ERR-111                  BT Copy XTal Calibration Values From WiFi failed  
BT_FT_ERR-113                  Failed to read BT USC version                     
BT_FT_ERR-114                  Failed to push OTP line into MEM file             
BT_FT_ERR-116                  Error in starting BT TX modulated                 
BT_FT_ERR-117                  Failed to read BD DATA                            
BT_FT_ERR-118                  BT calibration failed, Power difference is too high
BT_FT_ERR-119                  Setting IBISDAC FAILED                            
BT_FT_ERR-125                  Failed to set BD Address                          
BT_FT_ERR-126                  BT Copy Station ID and FTAPI Version from WiFi failed
BT_FT_ERR-248                  BT Set Station ID and FTAPI Version failed        
BT_FT_ERR-129                  Failed to start TX CW mode                        
BT_FT_ERR-130                  Failed during commit common partition in nvm      
BT_FT_ERR-132                  Failed to check if BT NVM is burned               
BT_FT_ERR-133                  Failed loading Si production values from NVM      
BT_FT_ERR-134                  BT Power Configuration Failed                     
BT_FT_ERR-135                  Memfile NVM versions don't match device NVM versions
BT_FT_ERR-137                  Unable to remotely connect to blue core,check USC, Rservice and c:\\ibtusc.cfg
BT_FT_ERR-138                  Power difference is outside of limits             
BT_FT_ERR-140                  Failed to read and log ACP results                
BT_FT_ERR-141                  1.4V output power compensation value is too high (>7)
BT_FT_ERR-142                  Invalid TX test mode requested                    
BT_FT_ERR-146                  Failed to change voltage switching via DDC (parameter ID: 323)
BT_FT_ERR-147                  Failed to change voltage via DDC (parameter ID:324)
BT_FT_ERR-150                  Failed to copy RTRIM from common partition        
BT_FT_ERR-151                  Error setting max power using DDC command         
BT_FT_ERR-152                   %s , Power on +-1MHz Offset of %.3lf dB is above the limit of %0.3lf dB 
BT_FT_ERR-153                   %s , Power on +-2MHz Offset of %.3lf dB is above the limit of %0.3lf dB
BT_FT_ERR-154                   %s , Power on +-3MHz Offset of %.3lf dB is above the limit of %0.3lf dB
BT_FT_ERR-262                   %s , Power on +-4MHz Offset of %.3lf dB is above the limit of %0.3lf dB
BT_FT_ERR-263                   %s , Power on +-5MHz Offset of %.3lf dB is above the limit of %0.3lf dB
BT_FT_ERR-264                  Actual OTP is not equal to the operational cache, just after the operational cache was commited
BT_FT_ERR-211                  Mismatch between input and device                 
BT_FT_ERR-215                  Invalid Bluetooth base address entered            
BT_FT_ERR-236                  NVM is not locked                                 
BT_FT_ERR-237                  Setting max power to DDC failed                   
BT_FT_ERR-238                  Setting TTC path switch failed                    
BT_FT_ERR-239                  Reading DTS temperature failed                    
BT_FT_ERR-240                  Reading TTC registers failed                      
BT_FT_ERR-241                  Setting IDAC_CTRL failed                          
BT_FT_ERR-242                  Setting KFREQ values to DDC failed                
BT_FT_ERR-243                  Setting KFREQ values to NVM failed                
BT_FT_ERR-244                  Setting LPC configuration to DDC failed           
BT_FT_ERR-245                  Setting RF CONF to DDC failed                     
BT_FT_ERR-246                  Setting Diversity Control through DDC failed      
BT_FT_ERR-247                  Setting 1.4V calibration value through DDC failed 
BT_FT_ERR-250                  Failed to get from NVM OTP lock status            
BT_FT_ERR-251                  Mismatch between actual and expected USC version  
BT_FT_ERR-252                  Connection type is NOT supported! Use TCP\\IP connection
BT_FT_ERR-253                  Failed to write data to operation NVM buffer      
BT_FT_ERR-254                  Failed to write XTAL to BT register               
BT_FT_ERR-255                  Failed to set BT TX power configuration           
BT_FT_ERR-256                  Failed to start Intel test mode V2                
BT_FT_ERR-257                  Failed to stop Intel test mode V2                 
BT_FT_ERR-258                  Failed to set deafult antenna                     
BT_FT_ERR-259                  Failed to start ELE TX                            
BT_FT_ERR-260                  Failed to stop ELE TX                             
BT_FT_ERR-261                  Invalid BT Address in SCAN ID and No BD address in EEPROM
BT_FT_ERR-265                  Failed to initialize BT API                       
BT_FT_ERR-266                  UART port number %d is not valid                  
BT_FT_ERR-267                  Failed to write into the usc config file          
BT_FT_ERR-268                  Failed to write into the usc config file          
BT_FT_ERR-269                  Failed to read the usc config file                
BT_FT_ERR-270                  Actual usc config %s is not equal to the required one %s
BT_FT_ERR-271                  BT RX SENSITIVITY failed                          
BT_FT_ERR-272                  Freq estimation not within limits                 
BT_FT_ERR-273                  Freq drift not within limits                      
BT_FT_ERR-274                  EDR power difference not within limits            
BT_FT_ERR-275                  BLE freq estimation not within limits             
BT_FT_ERR-276                  BLE freq drift not within limits                  
BT_FT_ERR-277                  Acp mode is illegal on Low energy                 
BT_FT_ERR-278                  Current not within limits. Actual: %f, High Limit: %f,Low Limit: %f, freq: %d, packet type: %s , pattern type: %s
BT_FT_ERR-279                  Failed to set BT TX power target configuration    
BT_FT_ERR-280                  Failed to toggle (reset/start/stop) BT statistics 
BT_FT_ERR-281                  Failed to get BT Tx expected Power                
BT_FT_ERR-282                  MAC Address must contain only digits or HEXA letters
BT_FT_ERR-E283                 Non linear value must be between 0 and 15         
BT_FT_ERR-284                  Power on +1MHz Offset is above the limit          
BT_FT_ERR-285                  Power on -1MHz Offset is above the limit          
BT_FT_ERR-286                  Power on +2MHz Offset is above the limit          
BT_FT_ERR-287                  Power on -2MHz Offset is above the limit          
BT_FT_ERR-288                  Power on +3MHz Offset is above the limit          
BT_FT_ERR-289                  Power on -3MHz Offset is above the limit          
BT_FT_ERR-290                  Power on +4MHz Offset is above the limit          
BT_FT_ERR-291                  Power on -4MHz Offset is above the limit          
BT_FT_ERR-292                  Power on +5MHz Offset is above the limit          
BT_FT_ERR-347                  Power on -5MHz Offset is above the limit          
BT_FT_ERR-293                  Failed to set rx gain control                     
BT_FT_ERR-294                  Failed to update FW USC cache from NVM Manager operational cache
BT_FT_ERR-296                  Failed to run phy statistics                      
BT_FT_ERR-297                  Failed to enter to static rf mode                 
BT_FT_ERR-298                  Failed to run Bb filter measurement by DUT        
BT_FT_ERR-299                  Failed to retrieve chip id                        
BT_FT_ERR-300                  Failed to apply papd table index                  
BT_FT_ERR-301                  Failed to apply power table EPC or LPC            
BT_FT_ERR-302                  Failed to write the power accuracy data to the NVM cache
BT_FT_ERR-303                  Failed to write the papd tables data to the NVM cache
BT_FT_ERR-304                  Failed to converge to the required threshold in power accuracy calibration
BT_FT_ERR-305                  Failed to write the bb filter cap data to the NVM cache
BT_FT_ERR-306                  Failed to retrieve regulatory status response     
BT_FT_ERR-307                  Failed to set location awareness configuration    
BT_FT_ERR-308                  Samples config cannot set Cyclic Start Address above 0x7FD when Debug memory type!
BT_FT_ERR-309                  when RX_DFE_INPUT injection point, total number of rows should divided by 3, including first address which is 0 --> cyclic start address mod 3 should be equal to 2
BT_FT_ERR-310                  Failure on ADC sample                             
BT_FT_ERR-311                  Failed to set LE scan enable                      
BT_FT_ERR-312                  Failed to get RTRIM value from FW DDC             
BT_FT_ERR-313                  Failed to perform the hadm phase per gain operation
BT_FT_ERR-314                  Failed to use BT Config Rx API                    
BT_FT_ERR-315                  Failed to get BT non linked RSSI                  
BT_FT_ERR-316                  Failed to get power table EPC or LPC              
BT_FT_ERR-317                  Failed to set rssi calibration data               
BT_FT_ERR-318                  Failed to get rssi calibration data               
BT_FT_ERR-319                  Failed to perform dpa captune calibration         
BT_FT_ERR-320                  Failed to set dpa captune to nvm                  
BT_FT_ERR-321                  Failed to read 2DID info from OTP                 
BT_FT_ERR-322                  Failed to read class ULT info from OTP            
BT_FT_ERR-323                  Bt Tx expected power and actual power diff exceed limits
BT_FT_ERR-324                  Bt Rx signal level and rssi diff exceed limits    
BT_FT_ERR-325                  Power on greater then 6MHz Offset is above the limit
BT_FT_ERR-326                  Power on greater then 6MHz Offset is above the limit
BT_FT_ERR-327                  HADM calibration Failed. At least one configuration violated threshold on all iterations 
BT_FT_ERR-328                  Failed to set hadm calibration data               
BT_FT_ERR-329                  Number of acp violation exceeded allowed number of violations 
BT_FT_ERR-330                  HADM calibrated phase diff not within limits      
BT_FT_ERR-331                  Failed to get hadm calibration data               
BT_FT_ERR-332                  Failed to read SMON info from OTP                 
BT_FT_ERR-333                  Failed to read ULT number from OTP                
BT_FT_ERR-334                  Failed to measure valid RSSI on BB filter. This means FW returned same default rssi for all measurments
BT_FT_ERR-335                  Failed to enable DTM mode                         
BT_FT_ERR-336                  Failed to get boost fw version                    
BT_FT_ERR-337                  Optimal cap power is not within limits            
BT_FT_ERR-338                  Rssi is not within limits                         
BT_FT_ERR-339                  Optimal cap is not within limits                  
BT_FT_ERR-340                  Expected power and actual power exceeded max abs diff
BT_FT_ERR-341                  Peak TX Power not within limits                   
BT_FT_ERR-342                  Failing to read DDC                               
BT_FT_ERR-343                  Expected M SAR is not as actual M SAR status      
BT_FT_ERR-344                  BT EDR2 SAR power limits is lower then LCA limit  
BT_FT_ERR-345                  BT failed to set pmic mode                        
BT_FT_ERR-346                  BLE delta F1 F0 not within limits                 
BT_FT_ERR-348                  BT DPA min and max power diff is not within threshold
BT_FT_ERR-349                  BT failed to set Mac and Chain                    
BT_FT_ERR-350                  Failed to read the power accuracy data to the NVM cache
BT_FT_ERR-351                  Failing to write DDC                              
BT_FT_ERR-352                  Failed to verify BT callback registration. Make sure BT is connected and enabled before this action
BT_FT_ERR-353                  Test should configure single chain only (Chain A or B)
     
"""

data = {'Pareto': [], 'ErrorDescription': []}

for line in error_code.split('\n'):
    errcode, desc = split_words_after_last_3_digits(line)
    if errcode is not None and desc is not None:
        data['Pareto'].append(errcode)
        data['ErrorDescription'].append(desc)

df = pd.DataFrame(data)

df.to_excel('output.xlsx', index=False)
