#!/usr/bin/env ruby

require 'fileUtils'

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

variations = ["GraphicRegion", "MathsRegion", "ChartRegion", "ImageRegion", "NoiseRegion", "SeparatorRegion", "TextRegion_credit", "TextRegion_drop-capital", "TextRegion_footer", "TextRegion_heading", "TextRegion_page-number", "TextRegion_paragraph", "TextRegion_caption", "TextRegion_floating"]

FileUtils.mkdir(dest_dir) unless Dir.exists?(dest_dir)

Dir.foreach(root_dir) do |f|
  base = f.sub(/\.\w+/, '')
  base = base.sub(/[^0-9]+/, '')
  
  variations_root_dir = dest_dir + "/" + base
  unless Dir.exists?(variations_root_dir)
    FileUtils.mkdir(variations_root_dir)

    black_and_white_dir = variations_root_dir + "/black_and_white"
    pgm_filename = base + '.pgm'
    FileUtils.mkdir(black_and_white_dir)
    bin_cmd = "#{otsu_path} #{root_dir}#{f} #{black_and_white_dir}/#{pgm_filename}"
    puts bin_cmd
    system(bin_cmd)

    xml_path = root_dir + "pc-#{base}.xml"

    variations.each do |variation|
      variation_dir = variations_root_dir + "/" + variation
      FileUtils.mkdir(variation_dir)
      if variation.split('_').size == 2
        type = "-t #{variation.split('_')[1]}"
      end
      region = variation.split('_')[0]
      generate_cmd = "./generate_training_image_filling.rb -i #{black_and_white_dir}/#{pgm_filename} -o #{variation_dir}/#{pgm_filename} -r #{region} #{type} -xml #{xml_path}"
      puts generate_cmd
      system(generate_cmd)
    end

    FileUtils.mkdir(variations_root_dir + "/xml")
    FileUtils.cp(xml_path, variations_root_dir + "/xml")
  end
end