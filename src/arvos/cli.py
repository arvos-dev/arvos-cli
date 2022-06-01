import argparse
import sys
from arvos.builder import Builder
from arvos.tracer import Tracer

def create_parser():
  parser = argparse.ArgumentParser(
    description="""
    Trace Java applications.
    Examples usage : 
      $ arvos --trace-period 3 --pom pom.xml --verbose
      $ arvos --save-report
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
  )

  parser.add_argument("--pom", "--only-versions-from-pom", help="Path to pom.xml file", type=str, required=False)
  parser.add_argument("--trace-period", help="Tracing period in minutes", type=str, default="2", required=False)
  parser.add_argument("--save-report", help="Save report as pdf", action="store_true")
  parser.add_argument("-v", "--verbose", action="store_true", help="verbose mode: print the BPF program (for debugging purposes)")

  return parser


if __name__== "__main__":
  parser = create_parser()
  args = vars(parser.parse_args())
  builder = Builder()
  builder.buildTestImage()
  builder.runUnitTests()
  builder.runArthasAgent()
  testApplicationPID = builder.getTestApplicationPID()
  builder.pauseUnitTests()
  tracer = Tracer(args['trace_period'], args['pom'])
  tracer.traceApplication(testApplicationPID)
  builder.resumeUnitTests()
  tracer.waitUntilFinish()

def main():
  parser = create_parser()
  args = vars(parser.parse_args())
  builder = Builder()
  builder.buildTestImage()
  builder.runUnitTests()
  builder.runArthasAgent()
  testApplicationPID = builder.getTestApplicationPID()
  builder.pauseUnitTests()
  tracer = Tracer(args['trace_period'], args['pom'], args['save_report'])
  tracer.traceApplication(testApplicationPID)
  builder.resumeUnitTests()
  tracer.waitUntilFinish()
