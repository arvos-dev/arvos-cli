import subprocess
import docker 
import os
from arvos.helpers import ok

class Tracer(object):
  def __init__(self, trace_period, pom):
    self.trace_period = trace_period
    self.pom = pom 
    self.client = docker.from_env()
    self.imageTag = "ayoubensalem/arvos-poc"

  def traceApplication(self, targetPID):
    kernel_release = subprocess.run(["uname", "-r"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    volumes = [
      '/sys/kernel/debug:/sys/kernel/debug:rw',
      f"/lib/modules/%s:/lib/modules/%s" % (kernel_release, kernel_release),
      '/usr/src:/usr/src'
    ]
    command = ""
    if self.pom :
      pom_path = os.path.abspath(self.pom)
      volumes.append(
        f"%s:/pom.xml" % pom_path
      )
      command += "--pom pom.xml"

    command += targetPID

    try:
      self.appContainer = self.client.containers.run(
        image=self.imageTag,
        stdout=True,
        detach=False,
        stderr=True,
        network_mode="host",
        remove=True,
        name="tracer",
        # tty=True,
        environment=[f'TRACE_TIME=%s' % self.trace_period],
        volumes=[
          '/sys/kernel/debug:/sys/kernel/debug:rw',
          f"/lib/modules/%s:/lib/modules/%s" % (kernel_release, kernel_release),
          '/usr/src:/usr/src'
        ],
        privileged=True,
        pid_mode="container:app",
        command=command
      )
      ok("Tracer app has started and will run for %s minutes" % self.trace_period)
    except Exception as e:
      print(e)