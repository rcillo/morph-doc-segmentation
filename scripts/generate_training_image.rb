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

region_selector = "//#{params['r']}"
unless params["t"].nil?
	region_selector += "[@type=\'#{params['t']}\']"
end

puts "selector => #{region_selector}"

img.combine_options do |c| 

	root.each_element(region_selector) { |text_region|
		polygon = ""
		text_region.each_element('Coords/Point') { |point|
			polygon = polygon + " #{point.attributes['x']},#{point.attributes['y']}"
		}

		puts "draw polygon #{polygon}"
		
		c.draw "polygon #{polygon}"
		c.fill("#FFFFFF") 
		
	}

end

img.write  params["o"]

