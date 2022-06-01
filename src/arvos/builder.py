import docker 
import sys, os, shutil
from arvos.helpers import ok, error, title
from mako.template import Template

class Builder(object):
  def __init__(self):
    self.client = docker.from_env()
    self.imageTag = "arvos:app-test"
    self.prepareBuildContext()

  def prepareBuildContext(self):
    dockerfileTemplate = Template("""FROM ayoubensalem/jdk17-dtrace-test\nCOPY . .""")

    with open("Dockerfile", "w") as f:
      f.write(dockerfileTemplate.render())

  def buildTestImage(self):
    title(f"Building Test Image with tag %s" % self.imageTag)
    try :
      self.appImage = self.client.images.build(
        path=".",
        tag=self.imageTag,
        nocache=True
      )
      ok("Build Finished Successfully")
    except Exception as e:
      print(e)

  def runUnitTests(self):
    title(f"Running Unit Tests %s" % self.imageTag)
    try:
      self.client.containers.get('app').remove(force=True)
    except docker.errors.NotFound:
      pass

    try:
      self.appContainer = self.client.containers.run(
        image=self.imageTag,
        detach=True,
        name="app",
        stdout=True,
        network_mode="host"
      )
    except Exception as e:
      self.appContainer.remove(force=True, ignore_errors=True)
      print(e)

  def runArthasAgent(self):
    # print("Running arthas agent .. ")
    try :
      exit_code, output = self.appContainer.exec_run(
        cmd="bash -c 'while [ ! -f /tmp/pid ]; do sleep 1; done;  /jdk/bin/java -jar arthas-boot.jar --attach-only $(cat /tmp/pid)'"
      )
      if exit_code != 0 :
        error("Could not run arthas agent!!")
        sys.exit(1)
      # ok("You application is ready, Go hit your endpoints.")
    except Exception as e:
      self.appContainer.remove(force=True, ignore_errors=True)
      print(e)

  def getTestApplicationPID(self):
    try:
      exit_code, output = self.appContainer.exec_run(
        cmd="cat /tmp/pid"
      )
      if exit_code != 0 :
        error("Could not get test application PID")
        sys.exit(1)
      return output.decode("utf-8").strip()
    except Exception as e:
      print(e)
    
  def pauseUnitTests(self):
    try:
      self.appContainer.pause()
    except Exception as e:
      print(e)

    
  def resumeUnitTests(self):
    try:
      self.appContainer.unpause()
    except Exception as e:
      print(e)