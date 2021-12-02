# Speed Testing

An Internet of Thing (IoT) style package of code and config to run background tests on actual broadband speeds experienced by the consumer using a Raspberry Pi, some shell script, some python and some NodeJS/JavaScript.

The author's set up is as follows:

- a Raspberry Pi connected by ethernet cable to my Broadband router
  - runs the 'test' code as cron jobs
  - uses tconfiguration to decide whether t osave outputs locally or send to
    remote API (for Cloud back-end/analysis)
  - back-end is WIP

## Set Up and First Run

To get chromium working on pi, some specific steps are required

- [](https://stackoverflow.com/questions/53927815/oserror-errno-8-exec-format-error-using-chromedriver-with-selenium-and-linux)
- [Get Chrome 65 armhf security updates installer](https://launchpad.net/ubuntu/trusty/+package/chromium-chromedriver)
- To install _'direct'_ from url:

    ```bash
    TEMP_DEB="$(mktemp)" &&
    wget -O "$TEMP_DEB" 'http://launchpadlibrarian.net/361669488/chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb' &&
    sudo dpkg -i "$TEMP_DEB"
    rm -f "$TEMP_DEB"
      ```

First run will downloadand install Chromium for pypetter so probably best to invoke first run manually.

## Set up automatic information gathering

Edit your crontab to enable the tests to run on a schedule, whether or not you're logged in. (Won't run if the pi is turned off. Tests won't work if Pi not connected to a network!)

```(bash)
  crontab -e
```

Then add the following line(s):

```(bash)
SHELL=/bin/bash
*/5 * * * * /home/pi/bin/speedTestPing
*/60 * * * * /home/pi/bin/speedTestRates
0 */4 * * * /usr/bin/nohup /usr/local/bin/node /home/pi/bin/js/index.js &
```

Save and exit (or exit and save, whichever you prefer).

`SHELL=/bin/bash` tells crontab to run the jobs in a bash shell, without this command the jobs may run in a different shell type making behaviour unpredictable and hard(er) to debug.

The other lines indicate the jobs to start and the schedule they should be started on. Use the excellent [crontab.guru](https://crontab.guru/) to experiment with different crontab schedules.

*Note* I have not finished working up speedGrabWeb to where I want it to be yet.  At the moment it uses headless Chrome to grab an image of my router speed report page.  I want to extract the upload/download speed values and only save those.  Hence, at the tiem of writing, there's no other code here for that.

## AWS Components - Build an AWS AppSync Service using boto3

TODO

## Python Code Components - Send Results to AWS AppSync

Copy the `py` folder to `/home/pi/bin` (or wherever you're installing to).

The code has been written to work with Python version 3.5. Some parts are slightly more backwards compatible, but I make no guarantees.

So, you'll need to set your default version of Python to 3.5 or greater.  You can find some instructions which should work for pi on the [Linux Config](https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux) website.  I ran:

```(bash)
  sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 1
  python --version
```

The `<space>1` at the end of the command isn't a typo.  It means 'use this as the primary option'.  Please note the above instruction is fragile.  I did it and it did what I wanted.  I haven't checked for side effects.

To install python dependencies, run `sudo pip install -r py/requirements.txt`

## Reference Materials

- Crontab
  - [Linux Man Page for crontab](http://man7.org/linux/man-pages/man5/crontab.5.html)
  - A more accessible article on [How to use Cron in Linux](https://opensource.com/article/17/11/how-use-cron-linux)
- Python
  - Using [pip requirements files](https://pip.pypa.io/en/stable/user_guide/#id1) to install all dependencies in one go

## Python Insights Along the Way

I'm still learning python so here are some notes along the way:

- `python3 -m pip install - requiremetns.txt` to install python3 packages - `pip install...` may use python2
- `source mypython/bin/activate` to active virtual env
