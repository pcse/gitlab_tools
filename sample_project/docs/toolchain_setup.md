# Tool Chain Setup for CPSC 250
****
Python
====

We need Python 3.6+ in addition to some modules including:
* matplotlib
* numpy
* scipy
* pandas

The easiest way to get all of these libraries in one step is to install the Anaconda system.
* https://www.anaconda.com/distribution/

Follow the installation directions there.

If you already have Python 3.6+ installed on your machine, you may manually install the required modules.

****
Git/GitBash
====

We will use Git for our Source Code Management, and use the Bash shell for the command line interface.

Git https://git-scm.org/downloads
* When it asks you whether or not you want to use VIM, select the "Use system file editor" option.
* For Windows, when it asks you about which command line interface to use, select the "Git Bash Command Line Interface".
* You should leave all other options as default when finishing the installation.



****
PyCharm
====

PyCharm is an *Integrated Development Environment* (IDE) for Python.  It is installed on the lab machines; we will provide setup directions for your personal machine later.

If you have not set up PyCharm for your machine, do the following:
1. Download Pycharm from the [JetBrains website](https://www.jetbrains.com/pycharm/).
    * Please select the **Community Edition**
    * Do *NOT* use the **Edu** edition, as the Edu edition changes the user interface.
2. Once you have downloaded PyCharm, install it on you system.
3. Once you launch PyCharm for the first time, it will ask you some customization options. Most of them are personal preference options (e.g. theme).
4. Once you have finished configuring PyCharm it will present a project selection menu, we will come back to this menu once we have cloned our project, for now you can leave it open.

Start the PyCharm IDE; the main page will start at the project selection menu.

Select `Open Project` and browse to the folder where you just cloned the repo.

> NOTE: Always use the cloned repo folder.  
> Do NOT copy files around because you are editing in a different folder than your git repo.
> Use the same folder always!


In order to consistently run our unit tests in PyCharm and on GitLab/WebCat, we need to make a change to the PyCharm configuration.

From the main PyCharm menu, select `Run` and then `Edit Configurations` as shown in
![Run menu](../img/config_menu.png).

Then edit the `Working Directory` at the bottom of the `Run/Debug Configurations` dialog to remove the `tests` folder so that the working directory points to the main repo as shown in  
![Run/Debug Configurations Dialog](../img/config_dialog.png), and select `OK`.

We are now ready to start coding.
