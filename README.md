# sharkbait

These scripts are used to download recently discovered malware payloads that are reported to URLHaus.  It is designed to run constantly behind a network security platform and will attempt to download payloads on a randomized time interval.

## Requirements
- Python3


## Installation
Clone the repo onto a Linux or Mac host
```bash
$ git clone https://github.com/stealthllama/sharkbait.git
```

Install the required Python3 dependencies
```bash
$ cd sharkbait
$ sudo pip3 install -r requirements.txt
```

Copy the Python scripts into /usr/local/bin or another directory in your $PATH
```bash
$ sudo cp *.py /usr/local/bin/
```

Optionally, configure your host to automatically start sharkbait at boot time.  This can typically be done in /etc/rc.local, /etc/init.d or /etc/systemd, depending on your OS platform.

## Usage
*sharkbait.py*

The `sharkbait.py` script is designed to run as a background process and can be launched from system startup tools or simply with a nohup shell command.  It will log results to `/tmp/sharkbait.log` by default.
```bash
usage: sharkbait.py [-h] --mode {nibble,chum,frenzy} [--logfile LOGFILE]

Generate malware download activity.

optional arguments:
  -h, --help            show this help message and exit
  --mode {nibble,chum,frenzy}
                        Malware download timing
  --logfile LOGFILE     The log filename
  ```

  *sharkreport.py*

  The `sharkreport.py` script can be used at any time to report on the results of the malware download activity.  It parses the `/tmp/sharkbait.log` file by default.
  ```bash
  usage: sharkreport.py [-h] [--logfile LOGFILE]

Generate sharkbait reports.

optional arguments:
  -h, --help         show this help message and exit
  --logfile LOGFILE  The log filename
  ```