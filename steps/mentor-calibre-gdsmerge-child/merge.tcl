#=========================================================================
# merge.tcl
#=========================================================================
# Merge so that gds0 has gds1 as a child cell and instantiates that cell
# at the given coordinate.
#
# Author : Christopher Torng
# Date   : May 25, 2020

#-------------------------------------------------------------------------
# Variables
#-------------------------------------------------------------------------

set gds0    $env(design_gds)
set gds1    $env(child_gds)
set gdsout  design_merged.gds

set coord_x $env(coord_x)
set coord_y $env(coord_y)

#-------------------------------------------------------------------------
# Checks
#-------------------------------------------------------------------------
# Check for name conflicts that have to be resolved

puts "> Checking for conflicts between $gds0 and $gds1"
layout filemerge -mode reportconflictsonly -in $gds0 -in $gds1

#-------------------------------------------------------------------------
# Merge
#-------------------------------------------------------------------------
# See "Batch Commands for Layout Manipulation" in calbr_drv_ref.pdf
#

puts "> Reading $gds0"
set L0 [ layout create $gds0 \
                -dt_expand \
                -preservePaths \
                -preserveTextAttributes \
                -preserveProperties ]

puts "> Reading $gds1"
set L1 [ layout create $gds1 \
                -dt_expand \
                -preservePaths \
                -preserveTextAttributes \
                -preserveProperties ]

set L0_topcell [ $L0 topcell ]
set L1_topcell [ $L1 topcell ]

# Import gds1 into gds0 as a child cell

puts "> Importing $L1 ($gds1) into $L0 ($gds0) in memory"
$L0 import layout $L1 FALSE append

# Create a reference in gds0's topcell which points to the new child cell

puts "> Creating reference for $L1_topcell in $L0_topcell at xy ($coord_x, $coord_y)"
$L0 create ref $L0_topcell $L1_topcell $coord_x $coord_y 0 0 1.0

# Flatten the child cell

puts "Info: Flatten child = $::env(flatten_child)"

if { $::env(flatten_child) } {
  $L0 flatten ref $L0_topcell $L1_topcell $coord_x $coord_y 0 0 1.0
}

# Stream out gds0

puts "> Streaming out $gdsout"
$L0 gdsout $gdsout $L0_topcell


