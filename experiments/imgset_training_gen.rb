#!/usr/bin/env ruby

require 'fileUtils'

######## scripts
$min_itv_builder = "/Users/rcillo/tcc/automation/min_itv_builder.rb"

########


$pubs = {
  "ieee" => [701, 792, 801],
  "cacm" => [263, 674, 677, 680, 683, 685, 686, 689, 692, 695, 802, 803],
  "time" => [232, 720, 721, 723, 782, 783, 784, 785, 786],
  "fortune" => [158, 235, 246, 249, 734, 752, 776]
}

$training_sizes = {
  "one_third" => 0.33,
  "two_thirds" => 0.66,
  "full" => 1.0
}

$win_sizes = ARGV[0].split(",").map(&:to_i)

$regions = ["ImageRegion", "TextRegion_heading", "TextRegion_paragraph"]

$dataset_base_dir = "/Users/rcillo/tcc/experiments/icdar_2009"

$erased_images_base_dir = $dataset_base_dir + "/erased_regions"

$imgsets_base_dir = $dataset_base_dir + "/imgsets"

$win_base_path = "/Users/rcillo/tcc/experiments/icdar_2009/windows/#{ARGV[1]}/"
$maebb = "/Users/rcillo/tcc/trios/bin/bin/maebb"


def gen_training_imgsets(pub)
  pub_name = pub[0]
  pub_files = pub[1]
  pub_dir = $imgsets_base_dir+"/#{pub_name}"
  FileUtils.mkdir(pub_dir) unless Dir.exists?(pub_dir)
  pub_files.each { |file_base|  
    full_base_path = "00000#{file_base}"
    image_versions = $regions
    image_versions += ["black_and_white"]
    image_versions.each { |region|  
      src = $erased_images_base_dir + "/#{full_base_path}/#{region}/#{full_base_path}.pgm"
      dest = pub_dir + "/#{file_base}_#{region}.pgm"
      FileUtils.cp(src, dest) unless File.exists?(dest)
    }
  }
  $regions.each { |region| 
    $training_sizes.each { |training_size|
      name = training_size[0]
      tsize = training_size[1]
      imgset_filename = "imgset_#{region}_#{name}.s"
      imgset_absolute_path = pub_dir + "/#{imgset_filename}"
      files = pub_files[0..([pub_files.size * tsize, 1].max)]
      unless File.exists?(imgset_absolute_path)
        f = File.new(imgset_absolute_path, "w+")
        f.write("IMGSET  ########################################################\n")
        f.write(".n #{files.size}\n")
        f.write(".f 2\n")
        f.write(".d\n\n")
        f.write(pub_dir+"/\n")
        f.write(pub_dir+"/\n\n")
        files.each { |file_base|
          f.write("#{file_base}_black_and_white.pgm\n")
          f.write("#{file_base}_#{region}.pgm\n")
        }
        f.close
      end
    }
  }
end

def gen_ops(pub)
  pub_name = pub[0]
  pub_dir = $imgsets_base_dir+"/#{pub_name}"
  $win_sizes.each { |win_size|  
    $regions.each { |region| 
      $training_sizes.each { |training_size|
        name = training_size[0]
        imgset_filename = "imgset_#{region}_#{name}.s"
        imgset_absolute_path = pub_dir + "/#{imgset_filename}"
        dest_files_base = pub_dir + "/#{win_size}x#{win_size}_#{region}_#{name}"
        win = $win_base_path + "#{win_size}x#{win_size}.w"
        system("#{$min_itv_builder} #{win} #{imgset_absolute_path} #{dest_files_base}")
      }
    }
  }
end

def mae(pub)
  pub_name = pub[0]
  pub_dir = $imgsets_base_dir+"/#{pub_name}"
  $win_sizes.each { |win_size|  
    $regions.each { |region| 
      $training_sizes.each { |training_size|
        name = training_size[0]
        imgset_filename = "imgset_#{region}_full.s"
        imgset_absolute_path = pub_dir + "/#{imgset_filename}"
        dest_files_base = pub_dir + "/#{win_size}x#{win_size}_#{region}_#{name}"
        win = $win_base_path + "#{win_size}x#{win_size}.w"
        puts "#{win_size} training: #{name} region: #{region}"
        system("#{$maebb} -win #{win} -itv #{dest_files_base}_min.itv -imgset #{imgset_absolute_path}")
      }
    }
  }
end

FileUtils.mkdir($imgsets_base_dir) unless Dir.exists?($imgsets_base_dir)
$pubs.each { |pub| 
  gen_training_imgsets(pub)
  gen_ops(pub)
  puts "\n\n\n\n###MAES\n\n\n\n"
  mae(pub)
}

