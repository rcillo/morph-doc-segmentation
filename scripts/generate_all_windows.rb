#!/usr/bin/env ruby

(13..21).each { |w|  
  (13..21).each { |h| 
    puts "/Users/rcillo/tcc/trios/bin/bin/win_create -d #{w},#{h} > #{w}x#{h}.w"
    system("/Users/rcillo/tcc/trios/bin/bin/win_create -d #{w},#{h} > #{w}x#{h}.w")
   }
}