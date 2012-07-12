#!/usr/bin/env ruby

require "rubygems"
require "bundler/setup"
Bundler.require

require 'rexml/document'
include REXML

file = File.new("input.xml")
doc = Document.new(file)
root = doc.root

img = MiniMagick::Image.open("input.png") 

img.combine_options do |c| 

root.each_element('//text_region') { |text_region|
	polygon = ""
	text_region.each_element('coords/point') { |point|
		polygon = polygon + " #{point.attributes['x']},#{point.attributes['y']}"
	}
	
	c.draw "polygon #{polygon}" 
	c.fill("#0000FF") 
	
}

end

img.write  "output.png"

