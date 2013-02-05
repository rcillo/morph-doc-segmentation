#!/usr/bin/env ruby

require 'fileutils'

$pubs = {
#  "simple" => [158,171,190,194,195,201,205,232,235,249,263,674,677,680,683,685]
  "ieee" => [701, 792, 801],
  "cacm" => [263, 674, 677, 680, 683, 685, 686, 689, 692, 695, 802, 803],
  "time" => [232, 720, 721, 723, 782, 783, 784, 785, 786],
  "fortune" => [158, 235, 246, 249, 734, 752, 776],
  "mixed" => [701,263,801,683,232,723,158,249]
}

$training_sizes = {
  "one_third" => 0.33,
  "two_thirds" => 0.66,
}

$win_sizes = {
  dense: [[3,3], [4,4], [5,5], [7,7]],
  sparse: [[5,5], [7,7], [9,9], [11,11]]
}

$regions = {titles: "TextRegion_heading", texts: "TextRegion_paragraph"}

$dataset_base_dir = "/mnt/training_set"

$imgsets_base_dir = $dataset_base_dir + "/imgsets"

$win_base_path = "/mnt/manual_tests/windows/"

def write_imgset(f, region, files, file_base)
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
end

def gen_test_imgsets(pub)
  imgsets = {}
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
      files = pub_files[([pub_files.size * tsize, 1].max)..-1]
      imgsets["#{pub_files.size-files.size}"] imgset_absolute_path
      unless File.exists?(imgset_absolute_path)
        f = File.new(imgset_absolute_path, "w+")
        write_imgset(f, region, files, file_base)
        f.close
      end
    }
  }
  return imgsets
end

# training_imgsets = gen_training_imgsets(pub)
def gen_training_imgsets(pub)
  imgsets = {}
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
      imgsets["#{files.size}"] imgset_absolute_path
      unless File.exists?(imgset_absolute_path)
        f = File.new(imgset_absolute_path, "w+")
        write_imgset(f, region, files, file_base)
        f.close
      end
    }
  }
  return imgsets
end

#  ops = build_ops(training_imgsets)
def build_ops(pub)
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

FileUtils.mkdir($imgsets_base_dir) unless Dir.exists?($imgsets_base_dir)
$pubs.each { |pub| 
  training_imgsets = gen_training_imgsets(pub)
  test_imgsets = gen_test_imgsets(pub)
  ops = build_ops(training_imgsets)
  test_results = test_ops(ops, test_imgsets) # test each op (region type X window shape X trainingset size)
  write_test_results(test_results)
  stats = fscore_stats(ops, test_imgsets)
  write_fscore_stats(stats)
  results = merge_segmentations(ops, test_imgsets)
  fscore_stats(results)
}

