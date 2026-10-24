"""WSL transport only; business Core runs in the chosen Windows Python process."""
import argparse, os, pathlib, subprocess, sys
def main():
 p=argparse.ArgumentParser();p.add_argument('--windows-python',required=True);p.add_argument('--skill-area',required=True);p.add_argument('--current-project');a=p.parse_args()
 if os.name!='posix' or 'microsoft' not in pathlib.Path('/proc/sys/kernel/osrelease').read_text().lower():raise SystemExit('WSL required')
 def convert(x):return subprocess.check_output(['wslpath','-w',str(pathlib.Path(x).resolve())],text=True).strip()
 exe=subprocess.check_output(['wslpath','-u',a.windows_python],text=True).strip()
 cmd=[exe,'-B',convert(pathlib.Path(__file__).with_name('invoke.py')),'--skill-area',convert(a.skill_area)]
 if a.current_project:cmd+=['--current-project',a.current_project]
 try:return subprocess.run(cmd,env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'}).returncode
 except OSError:raise SystemExit('Windows adapter unavailable')
if __name__=='__main__':raise SystemExit(main())
