#!/usr/bin/env ruby

require 'scanf'

trios_toolbox_path = "/Users/rcillo/tcc/trios/bin/bin/"

# puts "window location:"
win_filename = ARGV[0]

# puts "imgset:"
# example: /Users/rcillo/tcc/experiments/icdar_2009/imgsets/math_expressions.s
imgset = ARGV[1]

base = ARGV[2]

itv_filename = "#{base}.itv"
mtm_filename = "#{base}.mtm"
xpl_filename = "#{base}.xpl"
min_itv_filename = "#{base}_min.itv"

unless File.exists?(min_itv_filename)
  puts "gerando intervalos\n"
  puts "#{trios_toolbox_path}win2itv -o #{itv_filename} < #{win_filename}"
  system("#{trios_toolbox_path}win2itv -o #{itv_filename} < #{win_filename}")
end

unless File.exists?(min_itv_filename)
  puts "coletando\n"
  puts "#{trios_toolbox_path}collect -win #{win_filename} -xpl #{xpl_filename} -imgset #{imgset}"
  system("#{trios_toolbox_path}collect -win #{win_filename} -xpl #{xpl_filename} -imgset #{imgset}")
end

unless File.exists?(min_itv_filename)
  puts "decision\n"
  puts "#{trios_toolbox_path}decision -mtm #{mtm_filename} -xpl #{xpl_filename}"
  system("#{trios_toolbox_path}decision -mtm #{mtm_filename} -xpl #{xpl_filename}")
end

unless File.exists?(min_itv_filename)
  puts "mae\n"
  puts "#{trios_toolbox_path}mae -w #{win_filename} -mtm #{mtm_filename}"
  system("#{trios_toolbox_path}mae -w #{win_filename} -mtm #{mtm_filename}")
end

unless File.exists?(min_itv_filename)
  puts "isi\n"
  puts "#{trios_toolbox_path}isi -mtm #{mtm_filename} -itv_original #{itv_filename} -itv_min #{min_itv_filename}"
  system("#{trios_toolbox_path}isi -mtm #{mtm_filename} -itv_original #{itv_filename} -itv_min #{min_itv_filename}")  
end

