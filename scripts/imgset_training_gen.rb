#!/usr/bin/env ruby

require 'fileutils'

$pubs = {
#  "simple" => [158,171,190,194,195,201,205,232,235,249,263,674,677,680,683,685]
  # "ieee" => [701, 792, 801]
  "cacm" => [263, 674, 677, 680, 683, 685, 686, 689, 692, 695, 802, 803],
  # "time" => [232, 720, 721, 723, 782, 783, 784, 785, 786],
  # "fortune" => [158, 235, 246, 249, 734, 752, 776],
  # "mixed" => [701,263,801,683,232,723,158,249]
}

$training_sizes = {
  "one_third" => 0.33,
  "half" => 0.5,
  "two_thirds" => 0.66
}

$windows = [
  {type: :dense, size: [3,3]},
  {type: :dense, size: [4,4]}
  # {type: :dense, size: [5,5]},
  # {type: :dense, size: [6,6]},
  # {type: :dense, size: [7,7]},
  # {type: :sparse, size: [3,3]},
  # {type: :sparse, size: [5,5]},
  # {type: :sparse, size: [7,7]},
  # {type: :sparse, size: [9,9]},
  # {type: :sparse, size: [11,11]}
]

$regions = ["TextRegion_heading", "TextRegion_paragraph"]


$dataset_base_dir = "/mnt/training_set"
$imgsets_base_dir = $dataset_base_dir + "/imgsets"
$win_base_path = "/mnt/manual_tests/windows"
$test_results_dir = $dataset_base_dir + "/test_results"
$ops_base_dir = $dataset_base_dir + "/ops"
$trios_build = "/home/ubuntu/trioslib-code/bin/bin/trios_build"
$trios_test = "/home/ubuntu/trioslib-code/bin/bin/trios_test"
$op_type = "BB"

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
  imgsets = []
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
      imgset_filename = "test_imgset_#{region}_#{name}.s"
      imgset_absolute_path = pub_dir + "/#{imgset_filename}"
      files = pub_files[([pub_files.size * tsize, 1].max)..-1]
      imgset = {}
      imgset[:region] = region
      imgset[:pub_name] = pub_name
      imgset[:pub_size] = pub_files.size
      imgset[:size] = files.size
      imgset[:path] = imgset_absolute_path
      unless File.exists?(imgset_absolute_path)
        f = File.new(imgset_absolute_path, "w+")
        write_imgset(f, region, files, file_base)
        f.close
      end
      imgsets << imgset
    }
  }
  return imgsets
end

# training_imgsets = gen_training_imgsets(pub)
def gen_training_imgsets(pub)
  imgsets = []
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
      imgset_filename = "training_imgset_#{region}_#{name}.s"
      imgset_absolute_path = pub_dir + "/#{imgset_filename}"
      files = pub_files[0..([pub_files.size * tsize, 1].max)]
      imgset = {}
      imgset[:region] = region
      imgset[:pub_name] = pub_name
      imgset[:pub_size] = pub_files.size
      imgset[:size] = files.size
      imgset[:path] = imgset_absolute_path
      unless File.exists?(imgset_absolute_path)
        f = File.new(imgset_absolute_path, "w+")
        write_imgset(f, region, files, file_base)
        f.close
      end
      imgsets << imgset
    }
  }
  return imgsets
end

#  ops = build_ops(training_imgsets)
def build_ops(imgsets)
  ops = []
  $windows.each do |win|
    imgsets do |imgset|
      # /home/ubuntu/trioslib-code/bin/bin/trios_build BB windows/dense/4x4.w /mnt/training_set/imgsets/simple/imgset_TextRegion_paragraph_one_third.s ops/4x4_one_third_paragraph.op
      op = {}
      op[:dir] = "#{$ops_base_dir}/#{imgset[:pub_name]}/#{imgset[:region]}/#{win[:type]}"
      op[:path] = "#{op[:dir]}/#{win[:size]}.op"
      op[:imgset] = imgset
      op[:win] = win
      system("#{$trios_build} #{$op_type} #{win[:path]} #{imgset[:path]} #{op[:path]}")
      ops << op
    end
  end
  return ops
end

def complement_imgset(op, imgsets)
  imgsets.each do |imgset|
    return imgset if imgset[:size] + op[:imgset][:size] == imgset[:pub_size]
  end
end

# test_results = test_ops(ops, test_imgsets)
def test_ops(ops, test_imgsets, pub_size)
  test_results = []
  ops.each do |op|
    test_imgset = complement_imgset(op, test_imgsets)
    result_text = `#{$trios_test} #{op[:path]} #{test_imgset[:path]}`
    result = {}
    result[:op] = op
    result[:test_imgset] = test_imgset
    result[:text] = result_text
    result[:path] = $test_results_dir + "/#{result[:imgset][:pub_name]}_#{result[:imgset][:region]}_#{result[:op][:win][:type]}_#{result[:op][:win][:size]}.txt"
    test_results << result
  end
  return test_results
end

# write_test_results(test_results)
def write_test_results(results)
  results.each do |result|
    f = File.new(result[:path], "w+")
    f.write(result[:text])
    f.close
  end
end

FileUtils.mkdir($imgsets_base_dir) unless Dir.exists?($imgsets_base_dir)
FileUtils.mkdir($ops_base_dir) unless Dir.exists?($ops_base_dir)
FileUtils.mkdir($test_results_dir) unless Dir.exists?($test_results_dir)

$pubs.each { |pub| 
  training_imgsets = gen_training_imgsets(pub)
  test_imgsets = gen_test_imgsets(pub)
  ops = build_ops(training_imgsets)
  test_results = test_ops(ops, test_imgsets)
  write_test_results(test_results)
  # stats = fscore_stats(ops, test_imgsets)
  # write_fscore_stats(stats)
  # results = merge_segmentations(ops, test_imgsets)
  # fscore_stats(results)
}

