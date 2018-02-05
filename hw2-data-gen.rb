#!/usr/bin/env ruby

require "csv"
require "erb"

csv = CSV.new(File.open('./DraftKingsdata.csv'), :headers => true)
player_data = csv.to_a.map {|row| row.to_hash}

template = ERB.new(DATA.read)
print template.result(binding)

__END__
<%= code = <<-CODE.chomp
PLAYER = 1..#{player_data.size};
player_names = #{player_data.map {|p| p["Name"]}};
player_salaries = #{player_data.map {|p| p["Salary"].to_i}};
player_avg_points = #{player_data.map {|p| p["AvgPointsPerGame"].to_f}};
position_eligible = array2d(PLAYER, POSITION,
    #{position_string = '['
      player_data.each do |p|
          positions = p["Position"].split('/')
          position_string << (positions.include?("PG") ? "1, " : "0, ") 
          position_string << (positions.include?("SG") ? "1, " : "0, ") 
          position_string << (positions.include?("PF") ? "1, " : "0, ") 
          position_string << (positions.include?("SF") ? "1, " : "0, ") 
          position_string << (positions.include?("C") ? "1, " : "0, ") 
      end
      position_string.gsub!(/0, $/, '0]')
      position_string}
);
salary_cap = 50000;
CODE
%>
