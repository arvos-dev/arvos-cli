Arvos Utility Tool
========

CLI tool for running arvos.

Requirements
--------------------------

1. Python 3.9 and pip  installed
2. Docker installed
3. Debugfs mounted ( sudo mount -t debugfs debugfs /sys/kernel/debug )


How to install
------------------

::

    $ pip install arvos


Usage
------

The following command will build an application image ( based on jdk 17 ) from the specified jar, run it, and run the tracer app for a period of 2 minutes.

::

    $ arvos --jar target/application.json --trace-period 2 --pom pom.xml --verbose


You can check the logs of the tracer application by running :

::

    $ docker logs -f tracer

Supported platforms
---------------------

Only Linux is supported.








