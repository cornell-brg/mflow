#=========================================================================
# pre_postroute.tcl
#=========================================================================
# This plug-in script is called before the corresponding Innovus flow step

setOptMode -usefulSkewPostRoute true

# Help meet hold timing.. this target slack adjusts for inaccuracies in
# postroute extraction compared with signoff extraction

setOptMode -holdTargetSlack  0.020
setOptMode -setupTargetSlack 0.020

