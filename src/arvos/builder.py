import docker 
import sys, os, shutil
from arvos.helpers import ok, error
from mako.template import Template

class Builder(object):
  def __init__(self, artifact):
    self.artifact = artifact
    self.client = docker.from_env()
    self.buildContext = "/tmp/arvos-app/"
    self.imageTag = "arvos:app"
    self.prepareBuildContext()

  def prepareBuildContext(self):

    shutil.rmtree(self.buildContext, ignore_errors=True)
    os.mkdir(self.buildContext)

    jarFileAbsolutePath = os.path.abspath(self.artifact)
    jarFileName = os.path.basename(self.artifact)
    
    shutil.copyfile(jarFileAbsolutePath, self.buildContext  + jarFileName)

    dockerfileTemplate = Template("""FROM ayoubensalem/jdk-docker-jstack\nCOPY ${jarFileName} ./application.jar""")

    with open(f"%s/Dockerfile" % self.buildContext, "w") as f:
      f.write(dockerfileTemplate.render(jarFileName=jarFileName))

  def buildApplicationImage(self):
    ok(f"<h1>Building Application Image with tag : %s</h1>" % self.imageTag)
    try :
      self.appImage = self.client.images.build(
        path=self.buildContext,
        tag=self.imageTag,
        nocache=True
      )
      ok("<h1>Build Finished Successfully.</h1>")
    except Exception as e:
      print(e)

  def runApplicationImage(self):
    ok(f"<h1>Running Application Image : %s</h1>" % self.imageTag)
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
        cmd="bash -c './wait-for-it.sh -t 90 localhost:8080 && /jdk/bin/java -jar arthas-boot.jar --attach-only --select application.jar'"
      )
      if exit_code != 0 :
        error("Could not run arthas agent!!")
        sys.exit(1)
      ok("<green>You application is ready, Go hit your endpoints.</green>")
    except Exception as e:
      self.appContainer.remove(force=True, ignore_errors=True)
      print(e)

  def getApplicationPID(self):
    try:
      exit_code, output = self.appContainer.exec_run(
        cmd="pidof java"
      )
      if exit_code != 0 :
        error("Could not get application PID")
        sys.exit(1)
      return output.decode("utf-8").strip()
    except Exception as e:
      print(e)