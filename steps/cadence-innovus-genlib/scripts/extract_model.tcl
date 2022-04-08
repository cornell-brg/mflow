set lib_files {}

foreach view $vars(analysis_views) {
    set lib_name "${view}.lib"
    lappend lib_files $lib_name
    set_analysis_view -setup $view -hold $view
    do_extract_model $lib_name -view $view
}

merge_model_timing -library $lib_files -modes $vars(analysis_views) -mode_group combined -outfile design.lib

