import re
import subprocess
import helpers
import platform
import asyncio


# Extract float from string using regular expression
def extractStats(string):
    """
      For each regex:
        $1 = The whole number
        $2 = Integer part
        $3 = Fractional part with leading period
        $4 = Fractional part
    """
    # rtt min/avg/max/mdev = 10.424/10.687/10.864/0.179 ms
    integerOrFloat = "(?=.)([+-]?([0-9]*)(\\.([0-9]+))?)"
    reStringWindows = ''.join([
        "Minimum = ", integerOrFloat, "ms, ",
        "Maximum = ", integerOrFloat, "ms, ",
        "Average = ", integerOrFloat, "ms"
    ])
    reStringNix = ''.join([
        "min/avg/max/mdev = ", integerOrFloat, "/",
        integerOrFloat, "/",
        integerOrFloat, "/",
        integerOrFloat, " ms"
    ])
    if platform.system().lower() == 'windows':
        reString = reStringWindows
    else:
        reString = reStringNix
    # Given pattern above, would return 3x 4 groups
    # we only want 1, 5 and 9 then
    return re.search(reString, string).group(1, 5, 9)


# Ping a host
def pingHost(host, noOfPings=1):
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    ping = subprocess.Popen(
        ["ping", param, str(noOfPings), host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, error = ping.communicate()
    # If ping is successful
    if error == b'':
        # Convert string to array of strings
        out = out.decode('utf-8').split('\n')
        # Iterate of each line in out
        for line in out:
            # If line contains "Average"
            if 'Average' in line:
                # Return RTT
                return extractStats(line)
    # If ping is unsuccessful
    else:
        # Return -1
        return -1

###############################################################################
# Main
###############################################################################


config = helpers.getConfig()
min, max, av = pingHost(config['host'], config['noOfPings'])
# Get guid
uuid = helpers.getGuid()

output = {}
output['uuid'] = uuid
output['min'] = str(float(min))
output['max'] = str(float(max))
output['av'] = str(float(av))
output['zip'] = config['zip']
output['countryCode'] = config['countryCode']
output['timestamp'] = helpers.getTimestamp()

if 'statusPage' in config:
    loop = asyncio.get_event_loop()
    coroutine = helpers.getStatus(config['statusPage'])
    output['status'] = loop.run_until_complete(coroutine)

# Send output to API over http
if not helpers.logOutput(output):
    helpers.saveToFile(output)
