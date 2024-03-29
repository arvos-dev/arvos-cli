import subprocess
from sys import stderr, maxsize
import docker 
import os, shutil
from arvos.helpers import ok, title, error
from pathlib import Path

class Tracer(object):
  def __init__(self, trace_period, pom, save_report, summary, detach):
    self.trace_period = trace_period
    self.pom = pom 
    self.client = docker.from_env()
    self.imageTag = "ayoubensalem/arvos-poc:3.0.12"
    self.save_report = save_report
    self.summary = summary
    self.report_folder = "%s/arvos-reports" % Path.home()
    self.detach = detach

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
      command += " --pom /pom.xml "


    shutil.rmtree(self.report_folder, ignore_errors=True)
    os.mkdir(self.report_folder)

    if self.save_report:
      volumes.append(
        f"%s:/stacks" % self.report_folder
      )
      command += " --save-report " + self.save_report

    if not self.summary :
      command += " --show-all "

    command += targetPID

    if self.trace_period ==  str(maxsize):
      title("Running the Tracer Application ...")
    else:
      title("Running the Tracer Application for %s minute(s) .." % self.trace_period)

    if self.save_report:
      title("Arvos report will be saved under %s" % self.report_folder)

    try:
      self.client.containers.get('tracer').remove(force=True)
    except docker.errors.NotFound:
      pass

    try:
      self.appContainer = self.client.containers.run(
        image=self.imageTag,
        detach=self.detach,
        stdout=False,
        stderr=True,
        network_mode="host",
        name="tracer",
        mem_limit="1g",
        shm_size="512000000",
        environment=[f'TRACE_TIME=%s' % self.trace_period],
        volumes=volumes,
        privileged=True,
        pid_mode="container:app",
        command=command
      )
      print("You can follow the tracer logs by running : ", end="")
      ok("docker logs -f tracer")
    except docker.errors.ContainerError as c:
      error("Vulnerable symbols have been found!")
      print("You can follow the tracer logs by running : ", end="")
      ok("docker logs -f tracer")
    except Exception as e:
      print(e)

  @staticmethod
  def stopTracer():
    try:
      client = docker.from_env()
      client.containers.get('tracer').kill(signal="SIGTERM")
    except docker.errors.NotFound:
      pass
    except docker.errors.APIError as e:
      print(e)
