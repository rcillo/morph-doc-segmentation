#!/usr/bin/env ruby

require 'scanf'

trios_toolbox_path = "/Users/rcillo/tcc/trios/bin/bin/"

puts "window dimension 'w,h' format:"
w, h = gets.scanf("%d,%d")

puts "imgset:"
# example: /Users/rcillo/tcc/experiments/icdar_2009/imgsets/math_expressions.s
imgset = gets

base = "win#{w}x#{h}"
win_filename = "#{base}.w"
itv_filename = "#{base}.itv"
mtm_filename = "#{base}.mtm"
xpl_filename = "#{base}.xpl"

system("#{trios_toolbox_path}win_create -d #{w},#{h} > #{win_filename}")

system("#{trios_toolbox_path}win2itv -o #{itv_filename} < #{win_filename}")

system("#{trios_toolbox_path}collect -win #{win_filename} -xpl #{xpl_filename} -imgset #{imgset}")

system("#{trios_toolbox_path}decision -mtm #{mtm_filename} -xpl #{xpl_filename}")

system("#{trios_toolbox_path}mae -w #{win_filename} -mtm #{mtm_filename}")
