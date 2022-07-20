import argparse
import wget, os, shutil, sys
from arvos.builder import Builder
from arvos.tracer import Tracer
from arvos.helpers import title, error


DEMO_APP_JAR_LINK = "https://github.com/ayoubeddafali/spring-vulnerable-app/releases/download/0.0.1-snapshot/java-app-0.0.1-SNAPSHOT.jar"
DEMO_APP_POM_LINK = "https://raw.githubusercontent.com/ayoubeddafali/spring-vulnerable-app/main/pom.xml" 

def create_parser():
  parser = argparse.ArgumentParser(
    description="""
    Trace Java applications.
    Examples usage : 
      $ arvos --demo
      $ arvos scan --help
      $ arvos scan --jar target/jar  --pom pom.xml
      $ arvos scan --jar target/jar --save-report --trace-period 3 --detach
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
  )

  parser.add_argument("--demo", help="Run arvos against a demo application ( https://github.com/ayoubeddafali/spring-vulnerable-app ) ", action="store_true", default=False)

  sub_parsers = parser.add_subparsers(help="scan --help")
  # create the parser for the scan sub-command
  scan_parser = sub_parsers.add_parser('scan', help='Scan a custom java application')

  scan_parser.add_argument("--jar", help="Path to .jar file", type=str, required=True)
  scan_parser.add_argument("--pom", help="Path to pom.xml file", type=str, required=False)
  scan_parser.add_argument("--trace-period", help="Tracing period in minutes", type=str, default="2", required=False)
  scan_parser.add_argument("--save-report", help="Save report as a pdf file", action="store_true", default=False)
  scan_parser.add_argument("--summary", help="Show summary instead of full report", action="store_true", default=False)
  scan_parser.add_argument("--detach", "-d", help="Run tracer in the background", action="store_true", default=False)

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
  if not args['demo'] and 'jar' not in args:
    parser.print_help(sys.stderr)
    sys.exit(1)

  if args['demo']:
    download_demo_files()
    args['jar'] = '/tmp/arvos-demo/demo.jar'
    args['pom'] = '/tmp/arvos-demo/pom.xml'
    args['trace_period'] = 1
    args['save_report'] = True
    args['summary'] = False
    args['detach'] = False
    
  builder = Builder(args['jar'])
  builder.buildApplicationImage()
  builder.runApplicationImage()
  builder.runArthasAgent()
  tracer = Tracer(args['trace_period'], args['pom'], args['save_report'], args['summary'], args['detach'])
  tracer.traceApplication(builder.getApplicationPID())

def main():
  parser = create_parser()
  args = vars(parser.parse_args())

  if not args['demo'] and 'jar' not in args:
    parser.print_help(sys.stderr)
    sys.exit(1)

  if args['demo']:
    download_demo_files()
    args['jar'] = '/tmp/arvos-demo/demo.jar'
    args['pom'] = '/tmp/arvos-demo/pom.xml'
    args['trace_period'] = 1
    args['save_report'] = True
    args['summary'] = False
    args['detach'] = False

  builder = Builder(args['jar'])
  builder.buildApplicationImage()
  builder.runApplicationImage()
  builder.runArthasAgent()
  tracer = Tracer(args['trace_period'], args['pom'], args['save_report'], args['summary'], args['detach'])
  tracer.traceApplication(builder.getApplicationPID())
