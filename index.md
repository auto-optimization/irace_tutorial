---
title: "Automatic Algorithm Configuration: Practical lab session"
subtitle: "Summer School on Automatic Algorithm Design 2023, Lille, France"
author: "Manuel López-Ibáñez, University of Manchester, UK (https://lopez-ibanez.eu)"
toc-title: "Contents"
toc: true
include-before: |
 <img style="float:right" src="./img/ssaad2023.png" height="100px" />
---

## Download ##

Download the materials from here: <https://lopez-ibanez.eu/exercises.zip>

## Setup ##

1.  Installing R: <https://mlopez-ibanez.github.io/irace/#installing-r>
 
1.  Install RStudio Desktop (optional but useful if you have never used R before):
    <https://posit.co/download/rstudio-desktop/>
    
1.  Open RStudio (or the R console) and type (this may take a while):
    
    ```R
    install.packages("irace", repos = "https://cloud.r-project.org")
    ```
 
1.  Find where **irace** is installed. Type in the R console:
    
    ```R
    library(irace)
    irace.cmdline("--help")
    cat(system.file(package="irace", "bin", mustWork=TRUE), "\n")
    ```
  
      The last command gives you the installation folder of **irace**, for example, `/home/user/R/irace/bin`. _Make a note of it!_
   
1.  You do not need to launch R or RStudio to run **irace**. If you visit the above folder, you will see that **irace** provides several executable files. You can call the executables directly like from the Bash shell, Terminal or Powershell:

    ```bash
    /home/user/R/irace/bin/irace --help
    ```
   
       If you add **irace**'s  `bin/` folder to the `PATH` environment variable of your operating system means, then you can simply type: `irace --help` (or `irace.exe --help` in Windows). How to do that is left as [homework](#homework). 
  
For simplicity, we will use the Rstudio console for the rest of the tutorial.
    
### Install iraceplot (optional) ###

1.  Install `rmarkdown` from the R console:

    ```R
    install.packages("rmarkdown", repos = "https://cloud.r-project.org")
    ```

1.  If you have installed RStudio, then you may have `pandoc` installed already. Otherwise, you have to follow the instructions from: <https://pandoc.org/installing.html> . You can verify that `pandoc` is correctly installed with:

    ```R
    rmarkdown::find_pandoc()
    ```

     and it should print the folder where `pandoc` is installed. Otherwise, you need to set the correct folder where `pandoc` (or `pandoc.exe` in Windows) is located with:
   
    ```R
    rmarkdown::find_pandoc(dir="C:/path/to/pandoc/bin/")
    ```

1.  Once the above is working, you can do:

    ```R
    install.packages("iraceplot", repos = "https://cloud.r-project.org")
    library(iraceplot)
    # If you need to change the broswer, use:
    # options(browser = "google-chrome")
    example("report", ask=FALSE)
    ```

## Part 1: A dummy scenario ##

### Exercise 1: Basic usage ###

1.  Open the folder `dummy` and look at the files `train-instances.txt`,  `parameters.txt` and `scenario.txt`.
 
1.  Open the Rstudio console and change the working directory to the location of the `dummy` folder (`Tools | Change Working Dir...` or `Session | Set Working Directory` depending on the version of RStudio). From the R console, if the location of `dummy` is `/path/to/dummy`, then you can type:

    ```R
    setwd("/path/to/dummy")
    list.files()
    ```
    
1.  Run **irace** and see what happens:

    ```R
    irace.cmdline("")
    ```

    If the above command says that it cannot find the function, you need load **irace** first using: 
    
    ```R
    library(irace)
    ```
    
1.  Open `parameters.txt` and change the value of `debug` to `1`. Run **irace** again. This example illustrates how you can communicate with the `targetRunner` via _fixed_ parameters. Remember to change `debug` back to `0`.
 
 
1.  You can also tell **irace** to report more details on what **irace** is doing:

    ```R
    irace.cmdline("--debug-level 2")
    ```
 
1.  Let's help **irace** a bit by providing an initial configuration:

    ```R
    irace.cmdline("--debug-level 2 --configurations-file=initial.txt")
    ```

    Can you see the initial configuration? Notice that 
 
1.  Now let's ask **irace** to run the best parameter configuration found on a set of test instances.

    a.  Edit `scenario.txt` and remove the `#` character before the line `testInstancesFile`.
    a.  Run **irace** again as you did above. What has happened now that did not happen before?
    
  
  
**:partying_face:** **Congratulations! You finished successfully your first automatic parameter configuration!** **:partying_face:**


### Exercise 2: Time as tuning budget ###

1.  Look at the file `scenario-time.txt`. What is different from the file `scenario.txt`?

1.  Run **irace** on this scenario using:

    ```R
    irace.cmdline("--scenario scenario-time.txt")
    ```

    Looking at the output, how many runs of the `targetRunner` was **irace** able to execute? 
    
    How many different configurations was **irace** able to execute?
    
    On how many instances was the best configuration evaluated?


### Exercise 3: Capping ###

1.  Look at the file `scenario-capping.txt`. What is different from the file `scenario-time.txt`?

1.  Run **irace** on this scenario using:

    ```R
    irace.cmdline("--scenario scenario-capping.txt")
    ```
1.  Change the fixed parameter `debug` from `0` to `1` to see what `targetRunner` is receiving from **irace**. Change it back to `0` afterwards.

1.  Change `maxTime` to a lower value, such as `1000` until you see the message:

    ```
    WARNING: with the current settings and estimated time per run ...
    ```

    You can do this with:
    ```R
    irace.cmdline("--scenario scenario-capping.txt --max-time 1000")
    ```

    Command-line options to **irace** override those in the `scenario.txt` file.

1.  Keep reducing `maxTime` until you see the message:

    ```
    Error: == irace == Insufficient budget
    ```

    What happened?

1.  Make sure to set again `maxTime=1200` and run again:

    ```R
    irace.cmdline("--scenario scenario-capping.txt")
    ```

    Looking at the output, how many runs of the `targetRunner` was **irace** able to execute? 
    How many different configurations was **irace** able to test?

1.  Now we will enable adaptive capping:

    ```R
    irace.cmdline("--scenario scenario-capping.txt --capping 1")
    ```

    Looking at the output, how many runs of the `targetRunner` was **irace** able to execute? 

    How many different configurations was **irace** able to test? 

    Notice also there is now a new column `Bound` in the output.

### Exercise 4: Rejection ###

1.  Look at the file `scenario-rejection.txt`, in particular, examine the `target Runner`.

1.  Run **irace** like:

    ```R
    irace.cmdline("--scenario scenario-reject.txt")
    ```
    
    Do you notice anything new in the output of **irace**? What is going on? Using `--debug-level 3` like we did before may give you a better idea.

### Exercise 5: Examining the log file ###

1.  **irace** creates a log file `irace.Rdata` that contains lots of data about the configuration process. You can load the file with:

    ```R
    results <- read_logfile("irace.Rdata")
    print(results$allConfigurations)
    print(results$experiments)
    ```
    
1.  There is a lot more information in `results` if you know where to look.  A better way to analyze the logfile is to use the [iraceplot](https://auto-optimization.github.io/iraceplot/) package:

    ```R
    install.packages("iraceplot", repos = "https://cloud.r-project.org")
    report("irace.Rdata")
    ```


## Part 2: target-runner as a Python script ##

In this exercise, we will tune the parameters of the [`dual_annealing`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html) optimizer provided by SciPy. Usually, you would need to write your own `target-runner.py` script that communicates between **irace** and `dual_annealing`. In this case, I have written a possible `target-runner.py` that you can find in the folder `dual_annealing/`.

1.  Open the `target-runner.py`. What is it doing?

1.  Now open `instances.txt` and `parameters.txt` and try to understand how they relate to `target-runner.py`.

1.  Open `scenario.txt`. What is different from other scenario files we have used so far?

1.  If you are in Linux/MacOS, you can typically execute `target-runner.py` directly by doing in the terminal:

    ```bash
    chmod u+x ./target-runner.py
    ./target-runner.py
    ```

    In Windows, you need to find where `python3.exe` is installed, let's say: `C:/Python/bin/python3.exe`. Then, in `scenario.txt`, set the value of `targetRunnerLauncher` to that string and remove the character `'#'` at the start of the line.

1.  Now open the Rstudio console and change the working directory to the location of the `dual_annealing` folder (`Tools | Change Working Dir...` or `Session | Set Working Directory` depending on the version of RStudio). From the R console, if the location of `dual_annealing` is `/path/to/dual_annealing`, then you can type:

    ```R
    setwd("/path/to/dual_annealing")
    list.files()
    ```

1.  First, let's check that everything works. In the R console, run:

    ```R
    irace.cmdline("--check")
    ```
    
    If it says `Check unsuccesful`, then `target-runner.py` may not have executable permissions or **irace** cannot find `python3` or `python3.exe` or there is a Python package missing such as `scipy`.
    
1.  Now, let's launch **irace** and see what it is doing:

    ```R
    irace.cmdline("--debug-level 2")
    ```
 
     Usually we do not want so much detail, so let's cancel the execution with `Ctrl+C` (in Linux) `ESC` (in Windows) or click the ![STOP](./img/stop-icon.png){height=2em title=STOP} button in Rstudio.  You can also open the Task Manager and kill the python process and this will force **irace** to stop with an error.
     
     
1.  Let's launch **irace** again but this time using 2 CPUs to execute multiple calls to `target-runner.py` in parallel:

    ```R
    irace.cmdline("--parallel 2 ")
    ```

     (If you have 4 CPUs, you could use `--parallel 4`)
     
     What interesting things do you notice in the output?
     
1.  Let's wait until **irace** finishes to do an ablation analysis in the next part.


    
## Part 3: Ablation analysis ##

1. You should have a file `irace.Rdata` in the folder `dual_annealing`.

1. We are going to do an ablation analysis between the default configuration and the best found by **irace**. In the R console, type:

    ```R
    ablation("irace.Rdata", src = 1)
    ```
    
    (Usually, `target=` will provide the target configuration ID. The default is to choose the best found.)
    
    If **irace** was unlucky, it could happen that the best configuration found was the default (1) and ablation will give an error.
    

1.  Now you should have a file `log-ablation.Rdata` that contains the ablation results.  Let's visualize it:

    ```R
    plotAblation("log-ablation.Rdata", type="boxplot")
    ```
    
    What can you conclude from this plot?
 
## Part 4: ACOTSP scenario ##

For this exercise, we will use the  [ACOTSPQAP software](https://github.com/MLopez-Ibanez/ACOTSPQAP/).

1.  In the folder `acotsp`, you will find a file `scenario.txt`. What is different from other scenario files that we have examined?

1.  Examine also `parameters-acotsp.txt` and `target-runner-acotsp.py`.

1.  We need to compile the C code in `acotsp/src/`. In Linux and MacOS, you should be able to do it from the shell / terminal with:

    ```bash
    cd ./acotsp/src
    make acotsp
    ```
    
    In Windows, you may need to do something different to compile the code.
    
    If everything works, you should have an executable file `acotsp` in the folder `acotsp/src/` and the following should work:
    
    ```bash
    ./acotsp --help
    ```
    
1.  Now go back to the folder `acotsp`.  If you are in Linux/MacOS, you can typically execute `target-runner-acotsp.py` directly by doing in the terminal:

    ```bash
    chmod u+x ./target-runner-acotsp.py
    ./target-runner-acotsp.py
    ```

    In Windows, you need to find where `python3.exe` is installed, let's say: `C:/Python/bin/python3.exe`. Then, in `scenario.txt`, set the value of `targetRunnerLauncher` to that string and remove the character `'#'` at the start of the line.

    
1.  In RStudio, change the working directory to the location of the `acotsp` folder (`Tools | Change Working Dir...` or `Session | Set Working Directory` depending on the version of RStudio). From the R console, if the location is `/path/to/acotsp`, then you can type:

    ```R
    setwd("/path/to/acotsp")
    list.files()
    ```
1.  First, let's check that everything works:

    ```R
    irace.cmdline("--check")
    ```
    
    If it says `Check unsuccesful`, then `target-runner-acotsp.py` or `./acotsp/src/acotsp` (or `./acotsp/src/acotsp.exe`) may not have executable permissions or **irace** cannot find `python3` or `python3.exe`.
    
1.  Now, let's launch **irace** and see what it is doing:

    ```R
    irace.cmdline("--debug-level 2")
    ```
 
     Usually we do not want so much detail, so let's cancel the execution with `Ctrl+C` (in Linux) `ESC` (in Windows) or click the ![STOP](./img/stop-icon.png){height=2em title=STOP} button in Rstudio.  You can also open the Task Manager and kill the python process and this will force **irace** to stop with an error.
          
     
1.  Let's launch **irace** again but this time using 2 CPUs to execute multiple calls to `target-runner-acotsp.py` in parallel:

    ```R
    irace.cmdline("--parallel 2 ")
    ```

     (If you have 4 CPUs, you could use `--parallel 4`)
     
     What interesting things do you notice in the output?

1.  If you have enough time, let `irace` run to completion and then do an ablation analysis like we did earlier.



## Homework ##

1.  Add **irace**'s  `bin/` folder to the `PATH` environment variable of your operating system. Check that it works by opening a system terminal (bash shell, Terminal or Powershell) and type: `irace --help` (or `irace.exe --help` in Windows). Now you are repeat all the exercises by using `irace` from the terminal. For example, if using R, you evaluated `irace.cmdline("--check")`, you will type in the terminal `irace --check`.
 
1.  Use [iraceplot](https://auto-optimization.github.io/iraceplot/) to analyze the `irace.Rdata` file generated by each exercise.
 
1.  You can also tune multi-objective optimizers with **irace**. Check the example provided by the [**MOEADr**](https://fcampelo.github.io/MOEADr/) package: <https://fcampelo.github.io/MOEADr/articles/Comparison_Usage.html> 
