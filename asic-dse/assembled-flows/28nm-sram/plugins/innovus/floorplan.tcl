#=========================================================================
# floorplan.tcl
#=========================================================================
# This script is called from the Innovus init flow step.

floorPlan -s $core_width $core_height \
             $core_margin_l $core_margin_b $core_margin_r $core_margin_t

setFlipping s

# Take all ports and split into halves

set all_ports       [dbGet top.terms.name]

set num_ports       [llength $all_ports]
set half_ports_idx  [expr $num_ports / 2]

set pins_left_half  [lrange $all_ports 0               [expr $half_ports_idx - 1]]
set pins_right_half [lrange $all_ports $half_ports_idx [expr $num_ports - 1]     ]

# Spread the pins evenly across the left and right sides of the block

set ports_layer M4

editPin -layer $ports_layer -pin $pins_left_half  -side LEFT  -spreadType SIDE
editPin -layer $ports_layer -pin $pins_right_half -side RIGHT -spreadType SIDE

#-------------------------------------------------------------------------
# SRAM
#-------------------------------------------------------------------------

# Place the SRAM an inset of four stdcell row heights into the core area

set sram_inset [expr $r_pitch * 4]

placeInstance sram/sram/mem_000_000 \
              [expr $core_margin_l + $sram_inset] \
              [expr $core_margin_b + $sram_inset] \
              My

# Cut the stdcell rows around the SRAM

selectInst sram/sram/mem_000_000
cutRow -selected -halo $sram_margin
deselectInst *

