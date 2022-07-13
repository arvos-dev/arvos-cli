import argparse
import wget, os, shutil
from arvos.builder import Builder
from arvos.tracer import Tracer
from arvos.helpers import title


DEMO_APP_JAR_LINK = "https://github.com/ayoubeddafali/spring-vulnerable-app/releases/download/0.0.1-snapshot/java-app-0.0.1-SNAPSHOT.jar"
DEMO_APP_POM_LINK = "https://raw.githubusercontent.com/ayoubeddafali/spring-vulnerable-app/main/pom.xml" 

def create_parser():
  parser = argparse.ArgumentParser(
    description="""
    Trace Java applications.
    Examples usage : 
      $ arvos --jar target/jar --trace-period 3 --pom pom.xml --verbose
      $ arvos --jar target/jar --save-report
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
  )

  parser.add_argument("--jar", help="Path to .jar file", type=str, required=False)
  parser.add_argument("--pom", "--only-versions-from-pom", help="Path to pom.xml file", type=str, required=False)
  parser.add_argument("--trace-period", help="Tracing period in minutes", type=str, default="2", required=False)
  parser.add_argument("--save-report", help="Save report as pdf", action="store_true")
  parser.add_argument("--summary", help="Show summary instead of full output", action="store_true")
  parser.add_argument("--demo", help="Run arvos against a demo application", action="store_true")
  parser.add_argument("-v", "--verbose", action="store_true", help="verbose mode: print the BPF program (for debugging purposes)")

  return parser


def download_demo_files():

  shutil.rmtree("/tmp/arvos-demo", ignore_errors=True)
  os.mkdir("/tmp/arvos-demo")

  title("Downloading demo application ..")
  wget.download(DEMO_APP_JAR_LINK, "/tmp/arvos-demo/demo.jar")
  wget.download(DEMO_APP_POM_LINK, "/tmp/arvos-demo/pom.xml")
  print("\n")

if __name__== "__main__":
  parser = create_parser()
  args = vars(parser.parse_args())
  if args['demo']:
    download_demo_files()
    args['jar'] = '/tmp/arvos-demo/demo.jar'
    args['pom'] = '/tmp/arvos-demo/pom.xml'
  builder = Builder(args['jar'])
  builder.buildApplicationImage()
  builder.runApplicationImage()
  builder.runArthasAgent()
  tracer = Tracer(args['trace_period'], args['pom'])
  tracer.traceApplication(builder.getApplicationPID())

def main():
  parser = create_parser()
  args = vars(parser.parse_args())
  if args['demo']:
    download_demo_files()
    args['jar'] = '/tmp/arvos-demo/demo.jar'
    args['pom'] = '/tmp/arvos-demo/pom.xml'
  builder = Builder(args['jar'])
  builder.buildApplicationImage()
  builder.runApplicationImage()
  builder.runArthasAgent()
  tracer = Tracer(args['trace_period'], args['pom'], args['save_report'], args['summary'])
  tracer.traceApplication(builder.getApplicationPID())
