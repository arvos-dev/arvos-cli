import subprocess
from sys import stderr
import sys
import docker 
import os, shutil
from arvos.helpers import ok, title, error
from pathlib import Path

class Tracer(object):
  def __init__(self, trace_period, pom, save_report):
    self.trace_period = trace_period
    self.pom = pom 
    self.client = docker.from_env()
    self.imageTag = "ayoubensalem/arvos-poc"
    self.save_report = save_report
    self.report_folder = "%s/arvos-reports" % Path.home()

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
      command += " --save-report "

    command += targetPID
    title("Running ARVOS Tracer Application for %s minutes" % self.trace_period)
    # print("You can check the tracer logs in another terminal by running : ", end="")
    # ok("docker logs -f tracer")

    if self.save_report:
      title("Arvos report will be saved under %s" % self.report_folder)

    try:
      self.client.containers.get('tracer').remove(force=True)
    except docker.errors.NotFound:
      pass

    try:
      self.appContainer = self.client.containers.run(
        image=self.imageTag,
        detach=True,
        stdout=True,
        stderr=True,
        network_mode="host",
        remove=False,
        name="tracer",
        mem_limit="1g",
        environment=[f'TRACE_TIME=%s' % self.trace_period],
        volumes=volumes,
        privileged=True,
        pid_mode="container:app",
        command=command
      )
    except docker.errors.ContainerError as c:
      error("Vulnerable symbols have been found!")
    except Exception as e:
      print(e)

  def waitUntilFinish(self):
    try:
      output = self.appContainer.wait()
      if output["StatusCode"] != 0 :
        error("Vulnerable symbols have been found!")
    except Exception as e :
      print(e)