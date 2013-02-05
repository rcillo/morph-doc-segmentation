#!/usr/bin/env ruby

require 'fileutils'

def load_params args
  params = {}
  args.each_slice(2) do | key_value |
    # puts "o #{key_value}"
    params[key_value[0][1..-1]] = key_value[1]
  end
  params
end

params = load_params(ARGV)

root_dir = params["root_dir"]
dest_dir = params["dest_dir"]
otsu_path = params["otsu"]
generating_strategy = params["gen_strategy"]
debug = params["debug"] == "true"

variations = ["GraphicRegion", "MathsRegion", "ChartRegion", "ImageRegion", "NoiseRegion", "SeparatorRegion", "TextRegion_credit", "TextRegion_drop-capital", "TextRegion_footer", "TextRegion_heading", "TextRegion_page-number", "TextRegion_paragraph", "TextRegion_caption", "TextRegion_floating"]

FileUtils.mkdir(dest_dir) unless Dir.exists?(dest_dir)
i = 0
Dir.foreach(root_dir) do |f|
  i += 1
  puts "processing:\t #{f}\n"
  puts "progress:\t #{i} de #{Dir.entries(root_dir).size} -> #{i/Dir.entries(root_dir).size}\n"
  base = f.sub(/\.\w+/, '')
  base = base.sub(/[^0-9]+/, '')

  unless File.directory?(f)
  
    variations_root_dir = dest_dir + "/" + base
    unless Dir.exists?(variations_root_dir)
      FileUtils.mkdir(variations_root_dir)
    end

    black_and_white_dir = variations_root_dir + "/black_and_white"
    pgm_filename = base + '.pgm'
    unless Dir.exists?(black_and_white_dir)
      FileUtils.mkdir(black_and_white_dir)
    end
    bw_file =  "#{black_and_white_dir}/#{pgm_filename}"
    bin_cmd = "#{otsu_path} #{root_dir}#{base}.tif #{bw_file}"
    unless File.exists?(bw_file)
      puts bin_cmd if debug
      system(bin_cmd)
    end

    xml_path = root_dir + "pc-#{base}.xml"
    
    variations.each do |variation|
      variation_dir = variations_root_dir + "/" + variation
      unless Dir.exists?(variation_dir)
        FileUtils.mkdir(variation_dir)
      end
      if variation.split('_').size == 2
        type = "-t #{variation.split('_')[1]}"
      end
      region = variation.split('_')[0]
      variation_file = "#{variation_dir}/#{pgm_filename}"
      generate_cmd = "#{generating_strategy} -i #{black_and_white_dir}/#{pgm_filename} -o #{variation_file} -r #{region} #{type} -xml #{xml_path}"
      unless File.exists?(variation_file)
        puts generate_cmd if debug
        system(generate_cmd)
      end
      
      unless Dir.exists?(variations_root_dir + "/xml")
        FileUtils.mkdir(variations_root_dir + "/xml")
        FileUtils.cp(xml_path, variations_root_dir + "/xml")
      end
    end
  end
end
