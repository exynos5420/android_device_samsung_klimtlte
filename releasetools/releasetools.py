def FullOTA_InstallEnd(info):
  info.script.Mount("/system")
  info.script.AppendExtra('run_program("/tmp/install/bin/variant_script.sh");')
  info.script.Unmount("/system")