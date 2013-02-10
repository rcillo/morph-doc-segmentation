#!/usr/bin/env ruby

require 'fileutils'

$test_imgsets = {
  "cacm" => [689, 692, 695, 802, 803],
  "time" => [783, 784, 785, 786]
}

$windows = [
  {type: :dense, size: [3,3]},
  {type: :dense, size: [4,4]},
  {type: :dense, size: [5,5]},
  {type: :dense, size: [6,6]},
  {type: :dense, size: [7,7]},
  # {type: :dense, size: [8,8]},
  {type: :sparse, size: [3,3]},
  {type: :sparse, size: [5,5]},
  {type: :sparse, size: [7,7]},
  {type: :sparse, size: [9,9]},
  {type: :sparse, size: [11,11]}
]

$regions = ["TextRegion_heading", "TextRegion_paragraph"]

$training_set_size = ["10", "20", "30", "40", "50"]

$dataset_base_dir = "/mnt/training_set"
$imgsets_base_dir = $dataset_base_dir + "/imgsets"
$ops_base_dir = $dataset_base_dir + "/ops"
$output_dir = $dataset_base_dir + "/output"
$trios_apply = "/home/ubuntu/trioslib-code/bin/bin/trios_apply"

pub_name = ARGV[0]
file_base = ARGV[1]
pub_dir = $imgsets_base_dir+"/#{pub_name}"
$regions.each do |region|
  input_image = pub_dir + "/#{file_base}_black_and_white.pgm"
  $training_set_size.each do |size|
    $windows.each do |window|
      op_description_path = "/#{pub_name}/#{region}/#{size}_percent/#{window[:type]}/#{window[:size][0]}x#{window[:size][1]}"
      operator = $ops_base_dir + "#{op_description_path}.op"
      output_image_dir = $output_dir + op_description_path
      FileUtils.mkdir_p(output_image_dir) unless Dir.exists?(output_image_dir)
      output_image = "#{output_image_dir}/#{file_base}.pgm"
      cmd = "#{$trios_apply} #{operator} #{input_image} #{output_image}"
      unless File.exists?(output_image)
        puts cmd
        puts `time #{cmd}`
      end
    end
  end
end
