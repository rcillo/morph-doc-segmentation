#!/usr/bin/env ruby

require "rubygems"
require "bundler/setup"
Bundler.require

require 'rexml/document'
include REXML

# params should be -xml -i -o -r
def load_params args
	params = {}
	args.each_slice(2) do | key_value |
		# puts "o #{key_value}"
		params[key_value[0][1..-1]] = key_value[1]
	end
	params
end

params = load_params(ARGV)

puts params

file = File.new(params["xml"])
doc = Document.new(file)
root = doc.root

img = MiniMagick::Image.open(params["i"]) 

img.combine_options do |c| 

root.each_element("//#{params['r']}") { |text_region|
	polygon = ""
	text_region.each_element('coords/point') { |point|
		polygon = polygon + " #{point.attributes['x']},#{point.attributes['y']}"
	}
	
	c.draw "polygon #{polygon}" 
	c.fill("#0000FF") 
	
}

end

img.write  params["o"]

