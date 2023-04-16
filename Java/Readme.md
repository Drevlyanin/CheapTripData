# Instruction (counter_baseless)
## Before start
At first, you have to download the code with the executable file of the counter (folder 'counter').
To use that file you need Java version 8 (1.8.0 built) and Python version 3.10 (and higher) installed in your system.
Then you need to open file "counter-1.0-SNAPSHOT-jar-with-dependencies" in 'target' folder. You can open that file 
with extended output information using "cmd.exe" and command 'java -jar counter-1.0-SNAPSHOT-jar-with-dependencies' 
in 'target' folder.

## Source
You have two ways to input source files to counter:
1) Use scraping pipeline if you have not got ready files of locations and direct routes;
2) Use files of locations and direct routes, if you have already got them.

To use pipeline (the first way) you need to check checkbox 'Data extraction' and add the absolute path to the folder 
   with counter (should be finished with '/counter') into a field near the checkbox. 

To use files (the second way) you need to add absolute paths to files with locations and direct routes into the 
text fields. 

If you pointed checkbox of pipeline process initializing, the second way will not work, because during calculation 
   counter will use output of pipeline. After pipeline counter will use files 'cities.csv' (located in 
'src/main/java/pystarter/pypart/files/') and 'all_direct_valid_routes.csv' (located in 
'src/main/java/pystarter/pypart/output/csv/'). You can find more details about pipeline process [here](https://github.com/rmant7/CheapTripData/tree/main/Python). 

## Choice of routes
There are three types of routes can be the output information of the counter:
1) flying routes (transportation type - planes);
2) fixed routes (transportation type - all types except planes and ride share);
3) routes (transportation type - all types except ride share);

To choose types of routes you need - use checkboxes.

## Choice of output type
You can get output in three formats: CSV, JSON, SQL.
Use checkboxes to choose formats you need. 

If you need validation data - you can choose 'validation'. The 
output will be validation files of routes you have chosen on the previous step.

After you decided type of formats you need - fill text fields with absolute paths where you want to save output. 
Output in JSON format include 'partly' JSONs - files with routes grouped by 'from' location.

## Start
After installation of all necessary settings (paths and checkboxes) push the 'Start' button. 